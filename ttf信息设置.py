# 需要用fontforge安装目录的bin\ffpython.exe运行
from ttf字体生成 import set_fontinfo
import sys,os,fontforge

if len(sys.argv)==2:
    output=sys.argv[1]
else:
    print("用法: python %s <ttf字体文件路径>"%sys.argv[0])
    sys.exit(1)

path=os.path.join(os.getcwd(),output)
font=fontforge.open(path)
print("Setting font info ...")
set_fontinfo(font)
print("Saving ...")
font.generate(path)