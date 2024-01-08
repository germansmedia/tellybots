import yaml
import random
from PIL import Image
import numpy as np
import cv2

width = 1920
height = 1920
frames = 115
rootdir = "/run/media/desmond/Data/tellybots"

def normal(image,path):
    input = Image.open(path).convert('RGBA')
    operand = np.array(input,dtype=np.float32)
    rgb = operand[...,:3]
    a = operand[...,3] / 255.0
    return image * (1.0 - a[...,np.newaxis]) + rgb * a[...,np.newaxis]

def screen(image,path):
    input = Image.open(path).convert('RGBA')
    operand = np.array(input,dtype=np.float32)
    rgb = operand[...,:3]
    a = operand[...,3] / 255.0
    return image + rgb * a[...,np.newaxis] - image * rgb * a[...,np.newaxis] / 255.0

output = cv2.VideoWriter(f"{rootdir}/dst/test.mp4",cv2.VideoWriter_fourcc(*'mp4v'),30,(width,height))
for i in range(0,frames):
    print(f"frame {i:05}")
    image = np.zeros([width,height,3],np.float32)
    image = normal(image,f"{rootdir}/src/Backgrounds/DarkGrey.png")
    image = normal(image,f"{rootdir}/src/Skin/TB_Base_Black_{i:05}.png")
    image = normal(image,f"{rootdir}/src/Accents/Gold/Accents_Gold_{i:05}.png")
    image = screen(image,f"{rootdir}/src/Accents/Gold Glow/Accents_Gold_Glow_{i:05}.png")
    image = normal(image,f"{rootdir}/src/Attribute/Headphones/Attri_Headphones_{i:05}.png")
    image = screen(image,f"{rootdir}/src/Attribute/Headphones Glow/TB_Headphones_Glow_{i:05}.png")
    image = normal(image,f"{rootdir}/src/Telly_001/Telly_001_{i:05}.png")
    image = screen(image,f"{rootdir}/src/Telly_001_Glow/Telly_001_Glow_{i:05}.png")
    output.write(image.astype(np.uint8)[...,::-1])
output.release()

# follow this with: ffmpeg -i input.mp4 -b:v 10M output.mp4