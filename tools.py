import sys
import os
import re
import readline
import logging
from shutil import copyfile
from PIL import Image, ImageColor

Image.MAX_IMAGE_PIXELS = 2300000000 #修改最大限制

def fillColor(input_dir, output_dir, backColor="#ffffff"):
    '''填充图片底色'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    color = ImageColor.getcolor(backColor, "RGBA")
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            fillColor(filepath, os.path.join(output_dir, filename), backColor)
            continue
        basename = os.path.splitext(filename)[0]
        basename, ext = os.path.splitext(filename)
        if ext != ".png" and ext != ".jpg":
            continue
        src_img = Image.open(filepath).convert("RGBA")
        # bgImg: Image.Image = Image.new("RGBA", (512, 512), (255, 255, 255,255))
        bgImg: Image.Image = Image.new("RGBA", (src_img.width, src_img.height), (255, 255, 255, 255))

        x = int((bgImg.width-src_img.width)/2)
        y = int((bgImg.height-src_img.height)/2)

        bgImg.paste(src_img, (x, y), mask=src_img)
        bgImg = bgImg.convert("RGB").convert("RGBA")

        outpath = os.path.join(output_dir,  f"{basename}.png")
        bgImg.save(outpath, format="png", dpi=(300,300))

def scaleImage(input_dir, output_dir, size, boundary_size, backColor="#ffffff"):
    '''放大缩小图片'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    color = ImageColor.getcolor(backColor, "RGBA")
    sample_method = Image.Resampling.LANCZOS
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            scaleImage(filepath, os.path.join(output_dir, filename), size, boundary_size, backColor)
            continue
        basename = os.path.splitext(filename)[0]
        basename, ext = os.path.splitext(filename)
        if ext != ".png" and ext != ".jpg":
            continue
        src_img = Image.open(filepath).convert("RGBA")
        width = src_img.width
        height = src_img.height

        maxlen = size - 2*boundary_size
        if width > height:
            height = int(maxlen * height / width)
            width = maxlen 
        elif width < height:
            width = int(maxlen * width / height)
            height = maxlen 
        else:
            width = maxlen
            height = maxlen
        
        #bgImg: Image.Image = Image.new("RGBA", (width, height), color)
        bgImg: Image.Image = Image.new("RGBA", (size, size), color)
        src_img = src_img.resize((width, height), sample_method)

        x = int((bgImg.width-src_img.width)/2)
        y = int((bgImg.height-src_img.height)/2)

        bgImg.paste(src_img, (x, y), mask=src_img)
        bgImg = bgImg.convert("RGB").convert("RGBA")

        outpath = os.path.join(output_dir,  f"{basename}.png")
        bgImg.save(outpath, format="png", dpi=(300,300))

def scaleImageV2(input_dir, output_dir, size):
    '''放大缩小图片'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    sample_method = Image.Resampling.LANCZOS
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            scaleImageV2(filepath, os.path.join(output_dir, filename), size)
            continue
        basename = os.path.splitext(filename)[0]
        basename, ext = os.path.splitext(filename)
        if ext != ".png" and ext != ".jpg":
            continue
        src_img = Image.open(filepath).convert("RGBA")
        width = src_img.width
        height = src_img.height

        maxlen = size
        if width > height:
            height = int(maxlen * height / width)
            width = maxlen 
        elif width < height:
            width = int(maxlen * width / height)
            height = maxlen 
        else:
            width = maxlen
            height = maxlen
        
        src_img = src_img.resize((width, height), sample_method)
        outpath = os.path.join(output_dir,  f"{basename}.png")
        src_img.save(outpath, format="png", dpi=(300,300))

def createTxt(input_dir, output_dir):
    '''创建同名txt文件'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
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

def findChinese(input_dir):
    '''查找目录下的文件是否有中文或为空'''
    result = []
    for filename in os.listdir(input_dir):
        basename, ext = os.path.splitext(filename)
        if ext != ".txt":
            continue
        with open(os.path.join(input_dir, filename), 'rb') as f:
            content = f.read().decode('utf-8')
            if not re.search(r'[a-zA-Z]', content):
                result.append(filename)
                continue
            if re.search('[^a-zA-Z0-9,-_\n]', content):
                result.append(filename)
                continue
            #if re.search(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', content):
            #    result.append(filename)
    if len(result) == 0:
        print('success')
    else:
        print('：{}'.format(','.join(result)))

def mergeDir(input_dir1, input_dir2, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    input_files_1 = os.listdir(input_dir1)
    input_files_2 = os.listdir(input_dir2)
    for file in input_files_1:
        basename, ext = os.path.splitext(file)
        if ext != ".txt":
            continue

        if file not in input_files_2:
            copyfile(os.path.join(input_dir1, file), os.path.join(output_dir, file))
            continue

        content = ""
        with open(os.path.join(input_dir1, file), 'r') as f:
            content += f.read()
        content = content.strip(' ,\n')
        with open(os.path.join(input_dir2, file), 'r') as f:
            c = f.read().strip(' ,\n')
            if len(c) > 0:
                if len(content) > 0:
                    content += ","
                content += c
        with open(os.path.join(output_dir, file), 'w') as f:
            f.write(content)

    for file in input_files_2:
        basename, ext = os.path.splitext(file)
        if ext != ".txt":
            continue
        if file in input_files_1:
            continue
        copyfile(os.path.join(input_dir2, file), os.path.join(output_dir, file))

def mergeImages(input_dir, output_dir, max_col, max_row):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = _mergeImages(input_dir, max_col, max_row)
    if img:
        outpath = os.path.join(output_dir,  "{}.png".format(os.path.basename(input_dir)))
        img.save(outpath, format="png", dpi=(300,300))

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not os.path.isdir(filepath):
            continue
        img = _mergeImages(filepath, max_col, max_row)
        if img:
            outpath = os.path.join(output_dir,  f"{filename}.png")
            img.save(outpath, format="png", dpi=(300,300))

def _mergeImages(input_dir, max_col, max_row):
    # 获取文件夹下所有 png 图片的文件名
    files = [f for f in os.listdir(input_dir) if f.endswith(".png")]
    if len(files) == 0:
        return None
    # 计算总共有多少行和列
    #row = max(len(files) // max_col + (1 if len(files) % max_col else 0), max_row)
    #col = min(len(files), max_col)
    row = max_row
    col = max_col
    max_num = row*col
    # 获取第一张图片的宽度和高度
    image = Image.open(os.path.join(input_dir, files[0])).convert("RGBA")
    width, height = image.size
    print(width, height, row, col)
    # 创建一个空白的长图，大小为 (col * width, row * height)
    long_image: Image.Image = Image.new("RGBA", (col * width, row * height), (255, 255, 255, 255))
    # 遍历每一张图片，将其粘贴到长图上对应的位置
    for i, file in enumerate(files):
        image = Image.open(os.path.join(input_dir, file)).convert("RGBA")
        long_image.paste(image, ((i % col) * width, (i // col) * height), mask=image)
        if i >= max_num:
            break
    # 保存长图为指定的输出路径
    return long_image.convert("RGB").convert("RGBA")

def cropImages(input_dir, output_dir, top, bottom, left, right):
    '''裁剪图片'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            cropImages(filepath, os.path.join(output_dir, filename), top, bottom, left, right)
            continue
        basename = os.path.splitext(filename)[0]
        basename, ext = os.path.splitext(filename)
        if ext != ".png" and ext != ".jpg":
            continue
        src_img = Image.open(filepath).convert("RGBA")
        # bgImg: Image.Image = Image.new("RGBA", (512, 512), (255, 255, 255,255))
        width = src_img.width - left - right
        height = src_img.height - top - bottom

        #bgImg: Image.Image = Image.new("RGBA", (width, height), (255,255,255,255))

        print(left, top, width, height, src_img.width, src_img.height)

        #bgImg.paste(src_img, (left, top), mask=src_img)
        bgImg = src_img.crop((left, top, src_img.width-right, src_img.height-bottom))
        #bgImg = bgImg.convert("RGB").convert("RGBA")

        outpath = os.path.join(output_dir,  f"{basename}.png")
        bgImg.save(outpath, format="png", dpi=(300,300))

def trunImages(input_dir, output_dir):
    '''翻转图片'''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        #if os.path.isdir(filepath):
         #   trunImages(filepath, os.path.join(output_dir, filename))
          #  continue
        basename = os.path.splitext(filename)[0]
        basename, ext = os.path.splitext(filename)
        if ext != ".png" and ext != ".jpg":
            continue
        src_img = Image.open(filepath).convert("RGBA")
        bgImg = src_img.transpose(Image.FLIP_LEFT_RIGHT)
        outpath = os.path.join(output_dir,  f"{basename}.png")
        bgImg.save(outpath, format="png", dpi=(300,300))


def clearImageTags(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            clearImageTags(filepath, os.path.join(output_dir, filename))
            continue

        basename, ext = os.path.splitext(filename)
        if ext != ".png":
            continue

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        image = Image.open(filepath)
        image.save(os.path.join(output_dir, filename))

def _dealClassifyImages(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isdir(filepath):
            continue
        basename, ext = os.path.splitext(filename)
        dirname, classify, index = basename.split("_")
        targetdir = os.path.join(output_dir, classify)
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
        copyfile(filepath, os.path.join(targetdir, f"{index}{ext}"))

def classifyImages(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not os.path.isdir(filepath):
            continue
        print(f"deal dir({filepath})...")
        _dealClassifyImages(filepath, os.path.join(output_dir, filename))


def main():
    default_input_dir = "./input"
    default_output_dir = "./output"
    print("1 - 填充图片底色;")
    print("2 - 创建png同名的txt文件;")
    print("3 - 添加内容到txt文件;")
    print("4 - 查找目录下文件里是否有中文或为空;")
    print("5 - 合并目录文件;")
    print("6 - 调整图片到目标大小并留白：")
    print("7 - 合并图片;")
    print("8 - 裁剪图片;")
    print("9 - 翻转图片;")
    print("10 - 清楚图片tag;")
    print("11 - 等比缩放图片")
    print("12 - 图片分类")
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
    elif func == "4":
        in_dir = input("请输入txt目录(默认为'./input'):") or default_input_dir
        findChinese(in_dir)
    elif func == "5":
        in_dir_1 = input("请输入txt目录1:") 
        in_dir_2 = input("请输入txt目录2:") 
        out_dir = input("请输入输出目录:") 
        mergeDir(in_dir_1, in_dir_2, out_dir)
    elif func == "6":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        size = int(input("请输入目标尺寸大小(默认为512):") or 512)
        boundary_size = int(input("请输入留白大小(默认为0):") or 0)
        background_color = input("请输入背景颜色(默认为#ffffff):") or '#ffffff'
        scaleImage(input_dir, output_dir, size, boundary_size, background_color)
    elif func == "7":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(默认为'./output'):") or default_output_dir
        width = int(input("请输入横向最大数量:") or 10)
        height = int(input("请输入纵向最大数量:") or 10)
        mergeImages(input_dir, output_dir, width, height)
    elif func == "8":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        top = int(input("请输入top边裁剪像素:") or 0)
        bottom = int(input("请输入bottom边裁剪像素:") or 0)
        left = int(input("请输入left边裁剪像素:") or 0)
        right = int(input("请输入right边裁剪像素:") or 0)
        cropImages(input_dir, output_dir, top, bottom, left, right)
    elif func == "9":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        trunImages(input_dir, output_dir)
    elif func == "10":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        clearImageTags(input_dir, output_dir)
    elif func == "11":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        size = int(input("请输入目标尺寸大小(默认为512):") or 512)
        scaleImageV2(input_dir, output_dir, size)
    elif func == "12":
        input_dir = input("请输入原始图片目录(默认为'./input'):") or default_input_dir
        output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份, 默认为'./output'):") or default_output_dir
        classifyImages(input_dir, output_dir)
    else:
        print("invalid input.")
        return


if __name__ == "__main__":
    try:
        main()
        #scaleImage("./in", "./out", 1024, 0)
        #scaleImageV2("./in", "./out", 1024)
        #mergeImages("./in", "out", 3, 2)
        #cropImages("./in", "./out", 90, 0, 50, 50)
        #clearImageTags("./in", "./out")
        #classifyImages("测试序列帧", "./out")
    except Exception as e:
        logging.exception(e)
    os.system("pause")
