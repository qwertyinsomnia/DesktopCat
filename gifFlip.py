from PIL import Image, ImageSequence
import os

with Image.open('Src/CatSpriteWalk.gif') as im:
    frames = [f.copy().transpose(Image.FLIP_LEFT_RIGHT) for f in ImageSequence.Iterator(im)]
frames[0].save('Src/CatSpriteWalkR.gif', save_all=True, append_images=frames[1:], loop = 1, duration = 0.1, comment=b"aaabb")

# 翻转出来的gif实际使用过程中会有白色边框 有问题