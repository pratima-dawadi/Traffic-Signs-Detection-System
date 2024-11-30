import cv2
import easyocr
from pylab import rcParams
import spacy
from spacy import displacy


def billboard_text(image_path):
    rcParams['figure.figsize'] = 8, 16

    reader = easyocr.Reader(['en'])

    img=cv2.imread(image_path)
    image=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    output=reader.readtext(image)

    extracted_text=""

    for i in range(len(output)):
        cord = output[i][0]
        x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
        x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
        cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,0,255),2)
        extracted_text=extracted_text+output[i][1]+" "

    print(f"Extracted text: {extracted_text}")
    return extracted_text

def entity_recognition(extracted_text):
    nlp=spacy.load('billboard_detection/model-best')
    doc = nlp(extracted_text)    
    category = ""
    
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Start: {ent.start_char}, End: {ent.end_char}, Label: {ent.label_}\n")
        category = category + " " + ent.label_



# if __name__=='__main__':
#     extracted_text=[
#         "Lainchaur Pharmacy",
#         "Pacific Guest House and Apartment",
#         "National School of Sciences",
#         "Modern Nepal College",
#         "Daksha Travel and Tours Pvt. Ltd.",
#         "Nepal Bank Limited",
#         "Namaste Party Venue",
#         "Saraswati Books Store"

#     ]
#     entity_recognition(extracted_text)