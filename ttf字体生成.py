# 需要用fontforge安装目录的bin\ffpython.exe运行
import fontforge,json

def contour_to_glyph(glyph, contour):
    pen = glyph.glyphPen()
    for points in contour:
        #points=points[::4] # 缩小字体大小
        size=700
        points=[(x,-y+size) for x,y in points]
        # 将找到的轮廓点转化为字形轮廓
        pen.moveTo(*points[0])
        for point in points[1:]:
            pen.lineTo(*point)
        pen.closePath()

def set_fontinfo(font):
    # 设置字体信息
    font.fontname = "ShuFaTi"
    font.fullname = "ShuFaTi Regular"
    font.familyname = "书法体"
    font.weight = "Regular"
    font.version = "1.0"

def create_font(chars, contours, output_path):
    font = fontforge.font()
    font.encoding = "UnicodeFull"

    for char, contour in zip(chars, contours):
        print("Processing:",char)
        glyph = font.createChar(ord(char))
        contour_to_glyph(glyph, contour)

    set_fontinfo(font)

    # 保存字体
    font.generate(output_path)

def main():
    with open("glyph_data.json",encoding="utf-8") as f:
        chars, contours=json.load(f)

    output_path = "书法.ttf"  # 替换为输出 TTF 文件路径
    create_font(chars, contours, output_path)
    print("TTF font file created successfully.")

if __name__=="__main__":main()