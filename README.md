# MAID

## Datasets

Our experiments are based on the open-source datasets [DiffusionForensics](https://github.com/ZhendongWang6/DIRE), [Artifact](https://github.com/awsaf49/artifact) and [GenImage](https://github.com/Andrew-Zhu/GenImage).

## Installation

1. Clone this repository and navigate to the MAID folder:

   ```bash
   git clone https://github.com/Zhu-Luyu/MAID.git
   cd MAID
   ```

2. Install the required packages:

   ```bash
   conda env create -f environment.yaml -n maid
   conda activate maid
   ```

3. Download pre-trained diffusion models:

   - [DDIM](https://heibox.uni-heidelberg.de/f/f179d4f21ebc4d43bbfe/?dl=1)
   - The repository for Stable Diffusion v1.5 has been removed, but you can use [Stable Diffusion v1.4](https://huggingface.co/CompVis/stable-diffusion-v1-4) as a substitute.
   - [DiT](https://huggingface.co/facebook/DiT-XL-2-256)
   - [DeepFloyd IF-I-M-v1.0](https://huggingface.co/DeepFloyd/IF-I-M-v1.0)
   - [LDM](https://huggingface.co/CompVis/ldm-celebahq-256)

## Training & Evaluation

Modify the script parameters as needed to run training and evaluation:

   ```bash
   sh train.sh
   sh eval.sh
   ```

To run DMA extraction before training or evaluation:

   ```bash
   cd dma
   # DDIM
   python compute_dma.py --diffusion_name "ddim" --diffusion_path path/to/your/ddim/checkpoint_file.ckpt --dataroot path/to/img_dataset --postfix "_ddim" --batch_size 100
   # IF. The usage of LDM, SD, and DiT is similar
   python compute_dma.py --diffusion_name "if" --diffusion_path path/to/your/if/model_folder --dataroot path/to/img_dataset --postfix "_if" --batch_size 100
   ```

## Model Classes

We selected the following model classes for the experiment:

1. DiffusionForensics (LSUN bedroom subset)

| Framework        | Classes               |
|------------------|-----------------------|
| GAN              | StyleGAN              |
| Diffusion Model  | ADM, IDDPM, PNDM      |
| -                | Real                  |

2. Artifact

| Framework        | Classes                                                                                                                                           |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| GAN              | BiqGAN, CIPS, CycleGAN, Denoising Diffusion GAN, Diffusion GAN, Gansformer, GauGAN, Lama, ProGAN, ProjectedGAN, StarGAN, StyleGAN, Taming Transformer, Generative Inpainting |
| Diffusion Model  | Latent Diffusion, Stable Diffusion, VQ Diffusion, Glide, Palette, Mat                                                                            |
| -                | Real                                                                                                                                               |

3. GenImage

| Framework        | Classes                           |
|------------------|-----------------------------------|
| GAN              | BigGAN                            |
| Diffusion Model  | ADM, Glide, Midjourney, SDv1.5, VQDM, wukong |
| -                | Real                              |

## Acknowledgments

Our code is based on the frameworks provided by [CNNDetection](https://github.com/PeterWang512/CNNDetection) and [DNF](https://github.com/YichiCS/DNF). We greatly appreciate their contributions and code.

## Citation

If you find this work useful for your research, please cite our paper:

```text
@INPROCEEDINGS{10888869,
  author={Zhu, Luyu and Ye, Kai and Yao, Jiayu and Li, Chenxi and Zhao, Luwen and Cao, Yuxin and Wang, Derui and Hao, Jie},
  booktitle={ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
  title={MAID: Model Attribution via Inverse Diffusion}, 
  year={2025},
  volume={},
  number={},
  pages={1-5},
  keywords={Limiting;Noise reduction;Autoencoders;Diffusion processes;Feature extraction;Diffusion models;Security;Surges;Speech processing;Glass box;Deepfake;Diffusion Model;Model Attribution},
  doi={10.1109/ICASSP49660.2025.10888869}
}
```
