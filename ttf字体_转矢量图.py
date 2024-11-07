import sys
import cv2
import numpy as np
import os,json,random
from string import ascii_letters,digits

def process_image(images):
    contours=[]
    for i in range(len(images)):
        # 读取图像（请确保不是中文路径）
        img = cv2.imread(images[i], cv2.IMREAD_GRAYSCALE)
        size=700
        factor=size/max(img.shape[1],img.shape[0])
        img=cv2.resize(img,(int(img.shape[1]*factor),int(img.shape[0]*factor)),
                       interpolation=cv2.INTER_LINEAR)

        # 二值化处理
        _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

        # 找到轮廓
        contour, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.append([[tuple(int(num) for num in pos[0])
                          for pos in sub] for sub in contour])

        if (i+1) % 10 == 0:
            print("Processed %d/%d"%(i+1,len(images)))

    return contours

if __name__ == "__main__":
    path=sys.argv[1] if len(sys.argv)==2 else "chars"
    images=[];chars=[]
    # 由于cv2.imread不支持中文目录，需要重命名中文路径
    if os.path.isfile("_backup.json"):
        with open("_backup.json",encoding="utf-8") as f:
            chars,rename_map=json.load(f)
    else:
        rename_map={}
        for char in os.listdir(path):
            chars.append(char)
            if not char.isascii():
                rand="".join(random.choices(ascii_letters+digits, k=16))
                rename_map[char]=rand
        with open("_backup.json","w",encoding="utf-8") as f:
            json.dump([chars,rename_map],f) # 备份重命名前的目录名
        for char,rand in rename_map.items(): # 重命名
            os.rename(os.path.join(path,char),os.path.join(path,rand))
        print("Renamed Non-ASCII paths")

    for char in chars:
        images.append(os.path.join(path,rename_map.get(char,char),"0.png"))
    contours = process_image(images)
    with open("glyph_data.json","w",encoding="utf-8") as f:
        json.dump([chars,contours],f)
    print("Glyphs have been dumped successfully.")

    for char,rand in rename_map.items(): # 恢复重命名前的目录名
        os.rename(os.path.join(path,rand),os.path.join(path,char))
    print("Cleaned up")
    os.remove("_backup.json")