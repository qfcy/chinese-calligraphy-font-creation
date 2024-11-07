import sys,os,multiprocessing,json
from PIL import Image

Image.MAX_IMAGE_PIXELS=None
def traverse(path):
    for root,_dirs,_files in os.walk(os.path.realpath(path)):
        for name in _files:
            if not name.lower().endswith(".png"):continue
            yield os.path.join(root, name)

def merge_image(images,size,rows,cols,id=0):
    image=Image.new("RGB",(size*cols,size*rows),(255,255,255))
    extra_zoom=0.8 # 用于字符间隙
    for i in range(len(images)):
        img=Image.open(images[i])
        factor=size/max(img.size)*extra_zoom
        thumb=img.resize((int(img.size[0]*factor),int(img.size[1]*factor)),
                         Image.Resampling.BILINEAR)
        row=i//rows;col=i%cols
        centerx,centery=(col+0.5)*size,(row+0.5)*size
        image.paste(thumb,(int(centerx-thumb.size[0]/2),int(centery-thumb.size[1]/2)))
        if col==0:
            print("%d: Processed %d images"%(id,i))
    return image

def _task(args):
    id,pics,size,rows,cols=args
    pic=merge_image(pics,size,rows,cols,id)
    pic.save("%d.png"%id)
    print("Saved to %d.png"%id)
    with open("%d.json"%id,"w",encoding="utf-8") as f:
        json.dump(pics,f)

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("用法: python %s <待处理的目录>"%sys.argv[0])
        sys.exit(2)
    path=sys.argv[1]
    pics=list(traverse(path))
    size=50
    rows=20;cols=20
    steps=rows*cols
    tasks=[]
    for i in range(0,len(pics),steps):
        tasks.append((i//steps,pics[i:i+steps],size,rows,cols))
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.map(_task,tasks)