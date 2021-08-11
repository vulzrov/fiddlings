import PIL
from PIL import Image
from PIL import ImageDraw  #��ȻImageģ�������ز�������getpixel��putpixel�������ӶȽϸ�����һ����.load()������ImageDrawģ���point������

import pytesseract         #ͼ��ʶ��ģ��
#ʹ�ø�ģ��Ҫ�Ƚ����Ĳ�Ԥ���ã� 
 #1. ����tesseract-ocrͼ��ʶ�������
 #2. pip install pytesseract
 #3. ��.__file__��������ģ��pytesseract�İ�װ·������Դ���루.py����
 #4. ��Դ�����е�tesseract_cmd������ֵ����Ϊtesseract-ocr����Ĵ���λ�ã�Tesseract-OCR�ļ���tesseract.exeӦ�õ�����·������
 #�ر�ע�⣺\t��pythonת���ַ���Ҫ��\\t��ת�壬���򱨴�

#��ֵ������������ͼ���Ż�������Ҷ�ͼ/RGBͼ/ͼ���ļ�·�������ԣ�����ֵ�����ض�ֵ��������ͼ��
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

#�Զ���ʶ�����̡�
#ʵ��Ӧ�������ǲ�����һ������ֵ�ԣ�����ָ��һ������������0-255��������Ϊ�����ʶ������
def auto_recognition(img, increment):

    for threshold in range(0,255,increment):

        image = binarization(img, threshold)

        text = pytesseract.image_to_string(image, lang='chi_sim')
        #Ĭ��ֻʶ��Ӣ�ģ���Ҫʶ�������轫lang������Ϊchi_sim����Щ������ʾchi_sim����Ҫ���ⰲװ�������������Դ��ˡ�

        print('Threshold {}: {}'.format(threshold, text))
        #������ӡ������ʶ������ʵ��Ӧ����һ�������һ�����𰸼�������ʶ�����ʹ𰸼�Ԫ��ƥ�䣬ֻ��ʾƥ��Ľ����

image = Image.open('source/2.png','r')

auto_recognition(image, 10)


#���ⲹ�䣺OCR����ʶ���������֡�ֻ������ռͼ������ʱ����ʶ�����Ծ���Ҫ��Ƭ���Ŵ�ͼ�񡣣�crop��resize��

#λͼ�Ŵ��Ȼ����ʧ�����⡣resize��resample�������ڴ�������⡣

#resample��������������ֵ��Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS.

#��Щ�Ǻ������󣬱�ʾʵ��resize�����Ĳ�ͬ�㷨����ͬ����£���Щ�㷨�ķ��ؽ��ʧ��������죬����������������

#һ�㲻������������������Ƚ�˭��ʶ��Ч���þ����ˡ�

#���⣬��resample����ʱҪ���ַ������Ǻ�������
