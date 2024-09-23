import os
import sys
import time
import torch
import torch.nn
import argparse
from PIL import Image
from tensorboardX import SummaryWriter

from time import time
from validate import validate
from data import create_dataloader

from earlystop import EarlyStopping
from networks.trainer import Trainer
from options.train_options import TrainOptions


"""Currently assumes jpg_prob, blur_prob 0 or 1"""
def get_val_opt():
    val_opt = TrainOptions().parse(print_options=False)
    val_opt.dataroot = '{}/{}/'.format(val_opt.dataroot, val_opt.val_split)
    val_opt.isTrain = False 
    val_opt.no_resize = False
    val_opt.no_crop = False
    val_opt.serial_batches = True 
    val_opt.jpg_method = ['pil'] 
    if len(val_opt.blur_sig) == 2:
        b_sig = val_opt.blur_sig
        val_opt.blur_sig = [(b_sig[0] + b_sig[1]) / 2]
    if len(val_opt.jpg_qual) != 1:
        j_qual = val_opt.jpg_qual
        val_opt.jpg_qual = [int((j_qual[0] + j_qual[-1]) / 2)]

    return val_opt


if __name__ == '__main__':
    import torch.multiprocessing as mp
    mp.set_start_method(method='forkserver', force=True)
    
    
    opt = TrainOptions().parse() 
    opt.dataroot = '{}/{}/'.format(opt.dataroot, opt.train_split)
    val_opt = get_val_opt()

    data_loader = create_dataloader(opt)
    dataset_size = len(data_loader)
    print('#training images batches = %d' % dataset_size)

    train_writer = SummaryWriter(os.path.join(opt.checkpoints_dir, opt.name, "tensorboard", "train"))
    val_writer = SummaryWriter(os.path.join(opt.checkpoints_dir, opt.name, "tensorboard", "val"))

    model = Trainer(opt)
    early_stopping = EarlyStopping(patience=opt.earlystop_epoch, delta=-0.001, verbose=True)
    
    from tqdm import tqdm
    for epoch in range(opt.niter):
        epoch_iter = 0

        # t1 = time()
        for i, data in enumerate(tqdm(data_loader)):     
            # t0 = time()
            model.total_steps += 1
            epoch_iter += opt.batch_size

            model.set_input(data)
            model.optimize_parameters()

            if model.total_steps % opt.loss_freq == 0:
                print("Train loss: {} at step: {}".format(model.loss, model.total_steps))
                train_writer.add_scalar('loss', model.loss, model.total_steps)

            if model.total_steps % opt.save_latest_freq == 0:
                print('saving the latest model %s (epoch %d, model.total_steps %d)' %
                      (opt.name, epoch, model.total_steps))
                model.save_networks('latest')
            
            # print(time()-t0, time()-t1)
            # t1 = time()

        if epoch % opt.save_epoch_freq == 0:
            print('saving the model at the end of epoch %d, iters %d' %
                  (epoch, model.total_steps))
            model.save_networks('latest')
            model.save_networks(epoch)

        # Validation
        model.eval()
        acc, purity, NMI, val_loss, class_report=validate(model.model, val_opt)
        val_writer.add_scalar('accuracy', acc, model.total_steps)
        val_writer.add_scalar('val loss', val_loss, model.total_steps)  # 记录验证损失
        val_writer.add_scalar('val loss per epoch', val_loss, epoch)
        val_writer.add_scalar('avg purity', purity, epoch)
        val_writer.add_scalar('NMI', NMI, epoch)
        print("(Val @ epoch {}) acc: {}; purity: {}; NMI: {}; val-loss: {}".format(epoch, acc, purity, NMI, val_loss))

        early_stopping(acc, model)
        if early_stopping.early_stop:
            cont_train = model.adjust_learning_rate()
            if cont_train:
                print("Learning rate dropped by 10, continue training...")
                early_stopping.adjust_delta(-0.002)
                model.load_networks('best')  
                print(f"Current learning rate after loading best model: {model.current_lr}")
            else:
                print("Early stopping.")
                break
        model.train()

