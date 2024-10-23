import json
import warnings

import spacy
from spacy.tokens import DocBin

def read_jsonl(fpath):
    with open(fpath, "r") as f:
        for line in f:
            yield json.loads(line)

nlp = spacy.blank("en")
doc_bin = DocBin()
docs = []

for data in read_jsonl("admin.jsonl"):
    doc = nlp.make_doc(data["text"])
    ents = []
    for entity in data["label"]:
        start = entity[0]
        end = entity[1]
        label = entity[2]
        span = doc.char_span(
            start_idx=start,
            end_idx=end,
            label=label,
            alignment_mode="strict",
        )
        if span is None:
            msg = (
                f"Skipping entity [{start}, {end}, {label}] in the "
                "following text because the character span "
                "'{doc.text[start:end]}' does not align with token "
                "boundaries:\n\n{repr(text)}\n"
            )
            warnings.warn(msg)
        else:
            ents.append(span)
    doc.set_ents(entities=ents)
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")