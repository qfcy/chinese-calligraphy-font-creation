本项目实现了从原始CorelDraw CDR格式的书法字帖中，导出书法字的png图像，并调用OCR识别文字，自动生成字库和ttf字体，是制作字体、创造自己的字库的一个完整解决方案。

## 用法 & 实现步骤

#### 1.导出cdr文件中的位图为png格式

这里涉及了CorelDraw X4中老旧的VBA宏技术。除了这一步之外，其他的步骤全部用了Python 3。(实际上也是被迫用VBA的)
首先用coreldraw x4打开字帖文件，然后点击 "工具" -> "宏" -> "宏编辑器"，打开VBA界面
再在右侧的“工程”面板找到名字是当前打开的文件的工程，在工程的名字上右击，点击“导入文件”，导入"从cdr导出png"这个目录下的frm和bas文件。
然后在 "工具" -> "宏" -> "运行宏" 菜单中运行这个宏，即可。
png图片的导出目录可以在VBA代码中修改。另外，这个宏还能一次导出所有打开的cdr文件，所以在运行宏之前，可以一次打开多个cdr字帖，以便批量导出。

#### 2.图像合并.py

由于识别单个的书法字符不仅速度慢，而且容易将偏旁分开。正式调用OCR接口之前，需要首先拼合多个书法字的图像。
程序调用后，会在当前工作路径生成`0.png`,`1.png`,...的多张图像，以及标识每个字符所来自图像路径的json文件。便于后续的制作字库。

**用法**
假设前面CorelDraw导出图片的目录是`E:\导出`，执行：
```
cd work_dir
python 图像合并.py E:\导出
```
即可。

#### 3.文字识别

**文字识别(pytesseract).py**

这里调用了pytesseract库识别拼合后的图像。附带了中文模型的tesseract工具在`工具及资源`目录中。
调用`python "文字识别(pytesseract).py"`之后，会生成每张图对应的txt文件，作为识别结果。
注意由于识别结果有一些差错，需要在这一步**人工修改**和调整。
(个人发现pytesseract的识别准确率不高，后来改用了Sider提供的ChatGPT API)

**文字识别(chatgpt).py**

命令行参数和`文字识别(pytesseract).py`相同，不过需要自行注册Sider账号，并将token复制粘贴到程序中。
如果是Edge，cookie可以在[edge://settings/cookies/detail?site=sider.ai](edge://settings/cookies/detail?site=sider.ai)更快地找到。
由于国内不能用ChatGPT，自己用了[Sider](https://sider.ai)。不过Sider如果没有充会员，每天有30次ChatGPT调用。

#### 4.书法字整理.py 和 书法字整理_简体.py

这两个脚本实现了读取前面的txt和json文件，找到识别结果的一个字对应哪张图，再按字整理出字库。
注意需要**人工修改**txt文件的内容，使得txt文件中的文字个数和拼合书法字的实际个数一样，否则无法对应到正确的文字。
`书法字整理.py`整理出的书法字是繁体字，而`书法字整理_简体.py`整理的是简体字 (需要安装`opencc`库实现繁简转换)。
用法: `python 书法字整理.py`和`python 书法字整理_简体.py`，注意需要切换到`0.json`,`0.txt`,...所在的工作目录。

#### 5.ttf字体_转矢量图.py

这里调用`cv2`库，实现位图转换为矢量图。转换后的矢量图数据会保存在`glyph_data.json`中，便于后续使用。
需要注意的是，由于`cv2.imread`不支持中文路径，这里在转换开始前先将目录重命名为英文，并将重命名的对应关系保存在_backup.json中，便于在转换失败，或者转换完成之后恢复。

**用法**
```
python ttf字体_转矢量图.py <要转换的字库目录>
```
如果不提供字库目录，默认的目录是工作路径下的`chars`。仓库中示例的chars目录是将`整理_简体`这个目录重命名得到的。

#### 6.ttf字体生成.py

这里调用了fontforge库，读取前面生成的`glyph_data.json`，生成ttf字体文件。默认生成文件名为`书法.ttf`。
注意脚本需要用**fontforge安装目录的bin\ffpython.exe运行**，或者用安装的`fontforge`库。[FontForge下载链接](https://github.com/fontforge/fontforge/releases/latest)
用法: 
`"C:\Program Files\FontForgeBuilds\bin\ffpython.exe" ttf字体生成.py`，注意工作目录需要含有`glyph_data.json`，另外可以在python脚本中手动修改字体名称、输出路径等设置。

#### 7.利用FontCreator调整字体参数

直接用`ttf字体生成.py`生成的字体由于格式可能比较杂乱，是不能直接使用的。
启动`工具及资源`目录下的FontCreator软件，并打开ttf字体。
进入Tools -> Glyph Transformer这个菜单，再点击最右侧的小打开按钮，导入`FontCreator转换.xml`这个参数转换文件，即可批量转换生成字体的参数。
如果需要自定义参数，可以手动编写xml文件。`工具及资源\FontCreator转换向导参数`这个目录提供了一些参数模板，供参考。

#### 8.ttf信息设置.py

在用FontCreator保存字体之后，原有的字体元数据可能会丢失。这时需要调用`ttf信息设置.py`重新设置字体的元数据。
用法：`python ttf信息设置.py <ttf字体文件路径>`
注意本文件会导入`ttf字体生成.py`模块中的`set_fontinfo()`函数，依赖于`ttf字体生成.py`这个模块。

## 备注

项目的python以及CorelDraw宏代码的部分遵循GPL 3.0协议。
此外由于版权原因，这里仅仅提供一小部分原始的书法字，和中间处理过程的文件，作为示例参考。生成的完整ttf字体暂不提供。