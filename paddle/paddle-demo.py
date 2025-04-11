from paddleocr import PaddleOCR, draw_ocr
import os

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = './paddle-demo.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]

# Use a system font that exists on macOS
font_path = '/System/Library/Fonts/Arial.ttf'  # Default system font on macOS
if not os.path.exists(font_path):
    font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'  # Alternative location

im_show = draw_ocr(image, boxes, txts, scores, font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('paddle-demo-result.jpg')
