import PIL
from PIL import Image          #PIL主框架，包括载入图像文件、显示图像、存储图像等基本功能，以及图像类Image object。
from PIL import ImageEnhance   #图像参数调整模块。可调节Brightness（亮度）、Color（颜色对比度）、Contrast（对比度）、Sharpness（锐度）四个参数。
from PIL import ImageDraw      #绘制模块。
from PIL import ImageFont      #ImageDraw模块的辅助模块，读取字体文件并返回字体对象，以作为参数传递给ImageDraw的函数。



A2 = Image.open('C:/Users/zhang/Desktop/IELTS/趣图/__A2.png','r').convert('RGB')
#载入图像文件，并转换为RGB格式。

sheet = Image.new('RGB',(A2.width*3,(A2.height+100)*3))
# Image.new 函数生成初始化的Image对象，可理解为“画布”。需要三个参数：图像格式（一般是RGB或L）、大小（宽，高）、底色（可用3-tuple或英文字符串）。

Font = ImageFont.truetype('arial.ttf',80)
# 生成字体对象。字体对象的意义是作为参数传递给ImageDraw模块的函数，如果这些函数有需要。

for i in range(9):
    text = 'Channel {} Intensity {}'.format(i//3,(i%3)*0.4+0.1)
    #绘制流程
    text_img = Image.new('RGB',(A2.width,100))
    drawing = ImageDraw.Draw(text_img)
    drawing.text((0,0),text,font=Font)
    #ImageDraw对象的text方法三个参数：锚坐标（左上角点的坐标）、文本、字体。

    slic = Image.new('RGB',(A2.width,A2.height+100))
    slic.paste(A2,(0,0))
    slic.paste(text_img,(0,A2.height))

    #通道分离
    R,G,B = slic.split()
    enhancer_R = ImageEnhance.Brightness(R)
    enhancer_G = ImageEnhance.Brightness(G)
    enhancer_B = ImageEnhance.Brightness(B)


    if i//3 == 0:
        key_R,key_G,key_B = (i%3)*0.4+0.1,1,1
    elif i//3 == 1:
        key_R,key_G,key_B = 1,(i%3)*0.4+0.1,1
    else:
        key_R,key_G,key_B = 1,1,(i%3)*0.4+0.1
    #通道合并
    sheet.paste(Image.merge('RGB',(enhancer_R.enhance(key_R), enhancer_G.enhance(key_G), enhancer_B.enhance(key_B))),((i%3)*slic.width, (i//3)*slic.height))





sheet = sheet.resize((sheet.width//3,sheet.height//3))
sheet.show()