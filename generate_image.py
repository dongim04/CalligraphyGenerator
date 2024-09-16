import vqgan_clip.generate
from vqgan_clip.engine import VQGAN_CLIP_Config
import os

config = VQGAN_CLIP_Config()
config.output_image_size = [128,128]
vqgan_clip.generate.image(eng_config = config,
        text_prompts = 'A pastoral landscape painting by Rembrandt',
        iterations = 100,
        output_filename = 'output.png')