
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 2300000000 #修改最大限制


def main():
    input_dir = "./in"
    output_dir = "./out"
    #input_dir = input("请输入原始图片目录:")
    #output_dir = input("请输入导出图片目录(目录相同会覆盖，注意备份):")
    #fillBackGround(input_dir, output_dir, (255,255,255))
    addContentToFile(input_dir, "hello")

def fillBackGround(input_dir, output_dir, backColor):
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

def createTxtFile(input_dir, output_dir):
	for filename in os.listdir(input_dir):
		basename, ext = os.path.splitext(filename)
		f = open(os.path.join(output_dir, f"{basename}.txt"), "w")
		f.close()

def addContentToFile(input_dir, content):
	for filename in os.listdir(input_dir):
		with open(os.path.join(input_dir, filename), "a") as f:
			f.write(content)
		

if __name__ == "__main__":
    main()
    os.system("pause")

