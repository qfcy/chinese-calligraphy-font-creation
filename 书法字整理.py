from collections import defaultdict
import json,os,shutil

charset=defaultdict(list)
total=9
for i in range(total):
    with open("%d.json"%i) as f:
        image_files=json.load(f)
    with open("%d.txt"%i,"r",encoding="utf-8") as f:
        chars="".join(f.read().splitlines())
    try:assert len(image_files)==len(chars)
    except AssertionError:
        print("Data doesn't match at %d"%i)
        continue
    for j in range(len(chars)):
        charset[chars[j]].append(image_files[j])

os.makedirs("整理",exist_ok=True)
os.chdir("整理")
path=os.getcwd()
for char in charset:
    os.makedirs(char,exist_ok=True)
    print("处理 %s: "%char,end="")
    for i in range(len(charset[char])):
        print("%d.png "%i,end="")
        shutil.copy2(charset[char][i],os.path.join(path,char,"%d.png"%i))
    print()