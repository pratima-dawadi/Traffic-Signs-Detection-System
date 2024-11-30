import spacy
import pandas as pd
from spacy.training import Example
from spacy.util import minibatch, compounding
import random


df=pd.read_csv('data.csv')

TRAIN_DATA = []
for _, row in df.iterrows():
    text = row['name']
    entities = [(0, len(text), row['entity'])]
    TRAIN_DATA.append((text, {"entities": entities}))

nlp = spacy.blank('en') 

if 'ner' not in nlp.pipe_names:
    ner = nlp.add_pipe('ner')
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

nlp.begin_training()

for i in range(20):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update(
                [example],
                drop=0.5,
                losses=losses,
            )
    print(losses)

nlp.to_disk('./spacy_model')