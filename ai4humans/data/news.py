from ai4humans.data import rucos
from collections import Counter
import json
from json import JSONDecoder
import os

def read(path):
  dec = JSONDecoder()
  docs = rucos.read_documents(dec, os.path.join(path, "datasets", "RuCoS", "train.jsonl")) \
    + rucos.read_documents(dec, os.path.join(path, "datasets", "RuCoS", "val.jsonl")) \
    + rucos.read_documents(dec, os.path.join(path, "datasets", "RuCoS", "test.jsonl"))

  entity_mapping = json.load(open(os.path.join(path, "datasets", "RuCoS_meta", "top1000_entity_mapping.json")))
  entity_meta = json.load(open(os.path.join(path, "datasets", "RuCoS_meta", "entity_meta.json")))

  docs_meta, docs_dropped = rucos.build_documents_meta(docs, entity_mapping, entity_meta, {'-'})
  docs_text = [doc["passage"]["text"].split("\n@highlight\n")[0] for doc in docs]

  return docs_meta, docs_text, docs_dropped

def tags_summary(docs_meta):
  info = Counter()
  for _, meta in docs_meta.items():
    for tag in meta["tags"]:
      info[tag] += 1
  return info

def format_act(act):
  s = "News{inform("
  acc = []
  for tag, entity in act:
    acc.append("{}={}".format(tag, entity))
  s += ", ".join(acc)
  s += ")}"
  return s

def format_text(act, text):
  return "{}[BOS]{}[EOS]".format(format_act(act), text)

def format_texts(docs_meta, docs_text):
  docs_acts = rucos.build_acts(docs_meta)
  acc = []
  for doc_id, acts in docs_acts.items():
    for act in acts:
      acc.append(format_text(act, docs_text[doc_id]))
  return acc

def slot_values(label):
  return [
    label,
    label.lower(),
    label.upper(),
    label.capitalize(),
  ]
