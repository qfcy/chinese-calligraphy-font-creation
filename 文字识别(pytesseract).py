import os,shutil
from PIL import Image
import pytesseract.pytesseract as pytesseract

def traverse(path):
    # 一个生成器, 列出path下的所有png文件的文件名。(备用)
    for root,_dirs,_files in os.walk(os.path.realpath(path)):
        for name in _files:
            if not name.lower().endswith(".png"):continue
            yield os.path.join(root, name)

# 指定 Tesseract 可执行文件的路径（如果不是在 PATH 中）
home=os.path.split(__file__)[0]
pytesseract.tesseract_cmd = os.path.join(home,"tesseract","tesseract.exe")

i=0
while True:
    file="%d.png"%i
    if not os.path.isfile(file):
        print("%s 不存在，已终止处理"%file)
        break
    print("处理:",file)
    # 打开图像文件
    image = Image.open(file).convert("1")

    # 进行文字识别
    custom_config = r'--oem 3 -l chi_tra'
    text = pytesseract.image_to_string(image,
                config=custom_config)

    with open("%d.txt"%i,"w",encoding="utf-8") as f:
        f.write(text)

    i+=1