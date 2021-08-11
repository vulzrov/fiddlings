import PIL
from PIL import Image
from PIL import ImageDraw  #虽然Image模块有像素操作方法getpixel和putpixel，但复杂度较高所以一般用.load()方法和ImageDraw模块的point函数。

import pytesseract         #图像识别模块
#使用该模块要先进行四步预配置： 
 #1. 下载tesseract-ocr图像识别软件。
 #2. pip install pytesseract
 #3. 用.__file__方法返回模块pytesseract的安装路径。打开源代码（.py）。
 #4. 将源代码中的tesseract_cmd变量的值设置为tesseract-ocr软件的储存位置（Tesseract-OCR文件下tesseract.exe应用的完整路径）。
 #特别注意：\t是python转义字符，要用\\t解转义，否则报错。

#二值化函数。输入图像（优化：输入灰度图/RGB图/图像文件路径都可以）和阈值，返回二值化处理后的图像。
def binarization(img, threshold):
    try:
        image = img.convert('L')
    except:
        image = Image.open(img,'r').convert('L')

    pim = image.load()
    drawing = ImageDraw.Draw(image)

    for x in range(image.width):
        for y in range(image.height):

            if pim[x,y] > threshold:
                drawing.point((x,y),255)
            else:
                drawing.point((x,y),0)

    return image

#自动化识别流程。
#实际应用中我们不可能一个个阈值试，我们指定一个增量，遍历0-255，挑出较为合理的识别结果。
def auto_recognition(img, increment):

    for threshold in range(0,255,increment):

        image = binarization(img, threshold)

        text = pytesseract.image_to_string(image, lang='chi_sim')
        #默认只识别英文，如要识别中文需将lang参数设为chi_sim。有些资料显示chi_sim包需要额外安装，但我这里是自带了。

        print('Threshold {}: {}'.format(threshold, text))
        #本例打印了所有识别结果。实际应用中一般会设置一个“答案集”，用识别结果和答案集元素匹配，只显示匹配的结果。

image = Image.open('source/2.png','r')

auto_recognition(image, 10)


#额外补充：OCR不能识别角落的文字。只有文字占图像主体时才能识别，所以经常要切片、放大图像。（crop、resize）

#位图放大必然产生失真问题。resize的resample参数用于处理该问题。

#resample参数有六个可能值：Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS.

#这些是函数对象，表示实现resize方法的不同算法。不同情况下，这些算法的返回结果失真情况各异，具体情况具体分析。

#一般不分析，生成六个结果比较谁的识别效果好就行了。

#另外，向resample传参时要传字符串而非函数对象。
