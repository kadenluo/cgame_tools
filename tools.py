import sys
import os
import readline
from PIL import Image, ImageColor

Image.MAX_IMAGE_PIXELS = 2300000000 #修改最大限制

def fillColor(input_dir, output_dir, backColor="#ffffff"):
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

def createTxt(input_dir, output_dir):
    '''创建同名txt文件'''
    for filename in os.listdir(input_dir):
        basename, ext = os.path.splitext(filename)
        if ext != ".png":
            continue
        f = open(os.path.join(output_dir, f"{basename}.txt"), "w")
        f.close()

def addContent(input_dir, content):
    '''添加内容到文件末尾'''
    for filename in os.listdir(input_dir):
        basename, ext = os.path.splitext(filename)
        if ext != ".txt":
            continue
        with open(os.path.join(input_dir, filename), "a") as f:
            f.write(content)

def main():
    default_input_dir = "./input"
    default_output_dir = "./output"
    print("1 - 填充图片底色;")
    print("2 - 创建png同名的txt文件;")
    print("3 - 添加内容到txt文件;")
    print("q - 退出;")
    func = (input("请输入你要使用的功能>>")).strip()
    if func == "q":
        return
    elif func == "1":
        in_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        out_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        color = input("请输入底色RGB值(默认为'#ffffff'):") or "#ffffff"
        fillColor(in_dir, out_dir, color)
    elif func == "2":
        in_dir = input("请输入png目录(默认为'./input'):") or default_input_dir
        out_dir = input("请输入输出目录(默认为'./output'):") or default_output_dir
        createTxt(in_dir, out_dir)
    elif func == "3":
        in_dir = input("请输入txt目录(默认为'./input'):") or default_input_dir
        content = input("请输入要增加的文字内容:")
        if len(content) == 0 :
            print("文字内容不能为空")
            return
        addContent(in_dir, content)
    else:
        print("invalid input.")
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    os.system("pause")
