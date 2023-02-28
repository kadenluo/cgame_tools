
import os
import typing
from PIL import Image, ImageColor
from nubia import command, argument, Nubia, Options

Image.MAX_IMAGE_PIXELS = 2300000000 #修改最大限制

@command("filleColor")
@argument("input_dir", description="输入目录", positional=True)
@argument("output_dir", description="输出目录", positional=True)
@argument("backColor", description="底色的RGB值，比如白色为: #FFFFFF", positional=True)
def fillColor(input_dir, output_dir, backColor):
    '''填充图片底色'''
    color = ImageColor.getcolor(backColor, "RGBA")
    sample_method = Image.Resampling.NEAREST
    for filename in os.listdir(input_dir):
        basename = os.path.splitext(filename)[0]
        filepath = os.path.join(input_dir, filename)
        src_img = Image.open(filepath).convert("RGBA")
        # bgImg: Image.Image = Image.new("RGBA", (512, 512), (255, 255, 255,255))
        bgImg: Image.Image = Image.new("RGBA", (src_img.width, src_img.height), (255, 255, 255, 255))

        x = int((bgImg.width-src_img.width)/2)
        y = int((bgImg.height-src_img.height)/2)

        bgImg.paste(src_img, (x, y), mask=src_img)
        bgImg = bgImg.convert("RGB").convert("RGBA")

        outpath = os.path.join(output_dir,  f"{basename}.png")
        bgImg.save(outpath, format="png", dpi=(300,300))

@command("createTxt")
@argument("input_dir", description="输入目录", positional=True)
@argument("output_dir", description="输出目录", positional=True)
def createTxt(input_dir, output_dir):
    '''创建同名txt文件'''
    for filename in os.listdir(input_dir):
        basename, ext = os.path.splitext(filename)
        f = open(os.path.join(output_dir, f"{basename}.txt"), "w")
        f.close()

@command("addContent")
@argument("input_dir", description="输入目录", positional=True)
@argument("content", description="输出目录", positional=True)
def addContent(input_dir, content):
    '''添加内容到文件末尾'''
    for filename in os.listdir(input_dir):
        with open(os.path.join(input_dir, filename), "a") as f:
            f.write(content)
