import os
import yaml
import random
from PIL import Image
import numpy as np
import cv2

width = 1920
height = 1920
frames = 115
count = 50
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

backgrounds = os.listdir(f"{rootdir}/src/Backgrounds")
skins = os.listdir(f"{rootdir}/src/Skins")
accents = os.listdir(f"{rootdir}/src/Accents")
attributes = os.listdir(f"{rootdir}/src/Attributes")
tellies = os.listdir(f"{rootdir}/src/Telly")

for n in range(28,count):
    background = "Inferno_Screen"
    while background.endswith("Inferno_Screen"):
        background = backgrounds[random.randrange(len(backgrounds))]
    background_is_anim = not os.path.isfile(os.path.join(f"{rootdir}/src/Backgrounds",background))
    skin = skins[random.randrange(len(skins))]
    accent = "_Glow"
    while accent.endswith("_Glow"):
        accent = accents[random.randrange(len(accents))]
    accent_has_glow = True
    attribute = "_Glow"
    while attribute.endswith("_Glow"):
        attribute = attributes[random.randrange(len(attributes))]
    attribute_has_glow = f"{attribute}_Glow" in attributes
    telly = "_Glow"
    while telly.endswith("_Glow"):
        telly = tellies[random.randrange(len(tellies))]
    telly_has_glow = f"{telly}_Glow" in tellies

    print(f"{background} {background_is_anim} {skin} {accent} {accent_has_glow} {attribute} {attribute_has_glow} {telly} {telly_has_glow}")

    output = cv2.VideoWriter(f"{rootdir}/dst/{n:05}.mp4",cv2.VideoWriter_fourcc(*'mp4v'),30,(width,height))
    for i in range(0,frames):

        print(f"    frame {i:05}")

        image = np.zeros([width,height,3],np.float32)

        # background
        if background_is_anim:
            image = normal(image,f"{rootdir}/src/Backgrounds/{background}/{background}_{i:05}.png")
        else:
            image = normal(image,f"{rootdir}/src/Backgrounds/{background}")

        # skin
        image = normal(image,f"{rootdir}/src/Skins/{skin}/TB_Skin_{skin}_{i:05}.png")

        # accent
        image = normal(image,f"{rootdir}/src/Accents/{accent}/Accents_{accent}_{i:05}.png")
        if accent_has_glow:
            if accent == "Silver":
                image = screen(image,f"{rootdir}/src/Accents/{accent}_Glow/{accent}_Glow_{i:05}.png")
            else:
                image = screen(image,f"{rootdir}/src/Accents/{accent}_Glow/Accents_{accent}_Glow_{i:05}.png")

        # attribute
        image = normal(image,f"{rootdir}/src/Attributes/{attribute}/Attri_{attribute}_{i:05}.png")
        if attribute_has_glow:
            if attribute == "Crown":
                image = screen(image,f"{rootdir}/src/Attributes/{attribute}_Glow/{attribute}_Glow_{i:05}.png")
            else:
                image = screen(image,f"{rootdir}/src/Attributes/{attribute}_Glow/Attri_{attribute}_Glow_{i:05}.png")

        if telly == "Angry_eyes":
            image = normal(image,f"{rootdir}/src/Telly/{telly}/Telly_{telly}_00000_{i:05}.png")
        else:
            image = normal(image,f"{rootdir}/src/Telly/{telly}/Telly_{telly}_{i:05}.png")        
        if telly_has_glow:
            if telly == "Hypno":
                image = screen(image,f"{rootdir}/src/Telly/{telly}_Glow/Tely_{telly}_Glow_{i:05}.png")
            else:
                image = screen(image,f"{rootdir}/src/Telly/{telly}_Glow/Telly_{telly}_Glow_{i:05}.png")

        output.write(image.astype(np.uint8)[...,::-1])

    output.release()

# follow this with: ffmpeg -i input.mp4 -b:v 10M output.mp4