import cv2
import easyocr
from pylab import rcParams
import spacy
from spacy import displacy

rcParams['figure.figsize'] = 8, 16

reader = easyocr.Reader(['en'])
image_path="../collection_dataset/crop_image/check2.png"

img=cv2.imread(image_path)
image=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

output=reader.readtext(image)
print(f"Extracted text: {output}")

extracted_text=""

for i in range(len(output)):
  cord = output[i][0]
  x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
  x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
  cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,0,255),2)
  print(output[i][1])
  extracted_text=extracted_text+output[i][1]+" "
  print(f"Extracted text: {extracted_text}")

NER=spacy.load('en_core_web_sm')

text1=NER(extracted_text)
print(f"text1: {text1}")

for token in text1.ents:
    print(token.text,token.start_char, token.end_char,token.label_)
