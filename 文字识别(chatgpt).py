import requests,json,traceback,os,gzip,bz2,zlib,time
from warnings import warn
try:import brotli # 处理brotli压缩格式
except ImportError:brotli=None

ORIGIN="chrome-extension://dhoenijjpgpeimemopealfcbiecgceod"
TOKEN="" # Bearer的token，可自行添加

COOKIE='CloudFront-Key-Pair-Id=; lang=zh-CN; '
'_uetvid=; '
f'token=Bearer%20{TOKEN}; '
'refresh_token=discard; '
'userinfo-avatar=https://chitchat-avatar.s3.amazonaws.com/default-avatar-14.png; '
'userinfo-name=User; userinfo-type=phone; '
'_ga=; _gcl_au=; '
'_ga_0PRFKME4HP=; '
'CloudFront-Policy=; '
'CloudFront-Signature='
'_rdt_uuid=' # 可自行添加

HEADER={ # 从浏览器的开发工具复制获得
 'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate, br, zstd',
 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,ja;q=0.5',
 'authorization': f'Bearer {TOKEN}',
 'Cache-Control': 'no-cache',
 'Cookie': COOKIE,
 'Origin': ORIGIN,
 'Pragma': 'no-cache',
 'Sec-Fetch-Dest': 'empty',
 'Sec-Fetch-Mode': 'cors',
 'Sec-Fetch-Site': 'none',
 'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
 'sec-ch-ua-mobile': '?0',
 'sec-ch-ua-platform': '"Windows"',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 '
               'Edg/130.0.0.0'
}

MODELS=["sider", # Sider Fusion
    "gpt-4o-mini",
    "claude-3-haiku",
    "gemini-1.5-flash",
    "llama-3" # llama 3.1 70B
]
ADVANCED_MODELS=["gpt-4o",
"claude-3.5-sonnet",
"gemini-1.5-pro",
"llama-3.1-405b",
"o1-mini",
"o1" # o1-preview
]
def upload_image(filename):
    url="https://api1.sider.ai/api/v1/imagechat/upload"
    header = HEADER.copy()
    #header["content-type"] = "multipart/form-data"
    #header["accept-encoding"] = "gzip, deflate"
    with open(filename, 'rb') as img:
        files = {'file': ("ocr.jpg",img,'application/octet-stream')}  # file 应与API要求的字段名一致
        response = requests.post(url, headers=header, files=files)
        if response.status_code!=200:
            raise Exception({"error": response.status_code, "message": response.text[:1024]})
    coding=response.headers.get('Content-Encoding')
    if not response.content.startswith(b"{") and coding is not None:
        decompress=None
        if coding == 'deflate':
            decompress=zlib.decompress
        elif coding == 'gzip':decompress=gzip.decompress
        elif coding == 'bzip2':decompress=bz2.decompress
        elif brotli is not None and coding == 'br':
            decompress=brotli.decompress
        data=decompress(response.content)
    else:
        data=response.content
    return json.loads(data.decode("utf-8"))

def get_text(url,headers,payload):
    # 一个生成器，获取输出结果
    response = requests.post(url, headers=headers, json=payload, stream=True)
    if response.status_code == 200:
        for line_raw in response.iter_lines():
            if not line_raw.strip():continue
            try:
                # 解析每一行的数据
                line = line_raw.decode("utf-8")
                if not line.startswith("data:"):continue

                response = line[5:]  # 去掉前缀 "data:"
                if not response:continue # 确保数据非空
                if response=="[DONE]":break
                parsed_data = json.loads(response)

                if "data" in parsed_data and "text" in parsed_data["data"]:
                    # parsed_data["data"]["cid"]包含了对话上下文id
                    yield parsed_data["data"]["text"] # 输出消息
            except Exception as err:
                warn(f"Error processing stream: {err} Raw: {line_raw}")
    else:
        raise Exception({"error": response.status_code, "message": response.text})

def chat(prompt, model="gpt-4o-mini"):
    # 一个生成器，使用提示词调用AI，返回结果 (备用)
    url = "https://api2.sider.ai/api/v2/completion/text"
    header = HEADER.copy()
    header["content-type"] = 'application/json'
    payload = {
        "prompt": prompt,
        "stream": True,
        "app_name": "ChitChat_Edge_Ext",
        "app_version": "4.23.1",
        "tz_name": "Asia/Shanghai",
        "cid": "", # conversation id，用于对话上下文，如果为空则开始新对话
        "model": model,
        "search": False,
        "auto_search": False,
        "filter_search_history": False,
        "from": "chat",
        "group_id": "default",
        "chat_models": [],
        "files": [],
        "prompt_template": {
            "key": "artifacts", # 在artifact的新窗口中显示结果
            "attributes": {"lang": "original"}
        },
        "tools": {"auto": ["data_analysis"]}, # 还可以加入"search"或者"text_to_image"
        "extra_info": {
            "origin_url": ORIGIN+"/standalone.html",
            "origin_title": "Sider"
        }
    }
    return get_text(url,header,payload)

def ocr(filename,model="gemini-1.5-flash"):
    # 一个生成器，调用OCR并返回结果
    data = upload_image(filename)
    img_id = data["data"]["id"]
    url="https://api2.sider.ai/api/v2/completion/text"
    payload = {
        "prompt": "ocr",
        "stream": True,
        "app_name": "ChitChat_Edge_Ext",
        "app_version": "4.23.1",
        "tz_name": "Asia/Shanghai",
        "model": model,
        "from": "ocr",
        "image_id": img_id,
        "ocr_option": {
            "force_ocr": True,
            "use_azure": False
        },
        "tools": {},
        "extra_info": {
            "origin_url": ORIGIN+"/standalone.html",
            "origin_title": "Sider"
        }
    }
    return get_text(url,HEADER,payload)

def image_ocr():
    i=0
    while True:
        filename="%d.png"%i
        if not os.path.isfile(filename):
            print("%s 不存在，已终止处理"%filename)
            break
        print("处理:",filename)
        try:
            with open("%d.txt"%i,"w",encoding="utf-8") as f:
                for result in ocr(filename):
                    f.write(result)
        except Exception:
            traceback.print_exc()
        time.sleep(5)
        i+=1

if __name__=="__main__":
    image_ocr()