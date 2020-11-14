import xml.etree.ElementTree as ET
import re

SUBJECTID = {
  "sberbank",
  "vtb",
  "gazprom",
  "alfabank",
  "bankmoskvy",
  "raiffeisen",
  "uralsib",
  "rshb",
  "beeline",
  "mts",
  "megafon",
  "tele2",
  "rostelecom",
  "komstar",
  "skylink",
}
SUBJECTID_TO_LABELS = {
  "sberbank": "Сбер",
  "vtb": "ВТБ",
  "gazprom": "Газпром",
  "alfabank": "Альфа",
  "bankmoskvy": "Банк Москвы",
  "raiffeisen": "Райффайзен",
  "uralsib": "Уралсиб",
  "rshb": "Россельхоз",
  "beeline": "Билайн",
  "mts": "МТС",
  "megafon": "Мегафон",
  "tele2": "ТЕЛЕ2",
  "rostelecom": "Ростелеком",
  "komstar": "Комстар",
  "skylink": "Скай Линк",
}
LABEL_TO_SUBJECTID = {v:k for k,v in SUBJECTID_TO_LABELS.items()}
SUBJECTID_TO_DOMAIN = {
  "sberbank": "Bank",
  "vtb": "Bank",
  "gazprom": "Bank",
  "alfabank": "Bank",
  "bankmoskvy": "Bank",
  "raiffeisen": "Bank",
  "uralsib": "Bank",
  "rshb": "Bank",
  "beeline": "Telecom",
  "mts": "Telecom",
  "megafon": "Telecom",
  "tele2": "Telecom",
  "rostelecom": "Telecom",
  "komstar": "Telecom",
  "skylink": "Telecom",
}
SENTIMENTID = {
  "-1": "негативный",
  "0": "нейтральный",
  "1": "позитивный",
}

def _subjectids_to_alternatives(subjs):
  acc = []
  for subj in subjs:
    acc += _subjectid_to_alternatives(subj) 
  return acc

def _subjectid_to_alternatives(subj):
  return [
    subj,
    subj.lower(),
    subj.upper(),
    subj.capitalize(),
  ]

SUBJECT_ALTERNATIVE_LABELS = {
  "sberbank": _subjectids_to_alternatives(["Сбер", "Сб", "sber"]),
  "vtb": _subjectids_to_alternatives(["Внеш", "ВТБ", "vtb"]),
  "gazprom": _subjectids_to_alternatives(["Газ", "gaz"]),
  "alfabank": _subjectids_to_alternatives(["Альфа", "alfa"]),
  "bankmoskvy": _subjectids_to_alternatives(["Москв", "moskv"]),
  "raiffeisen": _subjectids_to_alternatives(["Райф", "raif"]),
  "uralsib": _subjectids_to_alternatives(["Урал", "ural"]),
  "rshb": _subjectids_to_alternatives(["Сельхоз", "РСХБ", "rshb"]),
  "beeline": _subjectids_to_alternatives(["Билайн", "Вымпел", "beeline"]),
  "mts": _subjectids_to_alternatives(["МТС", "mts"]),
  "megafon": _subjectids_to_alternatives(["Мега", "mega"]),
  "tele2": _subjectids_to_alternatives(["ТЕЛЕ", "tele"]),
  "rostelecom": _subjectids_to_alternatives(["Ростел", "rostel"]),
  "komstar": _subjectids_to_alternatives(["Комстар", "komstar"]),
  "skylink": _subjectids_to_alternatives(["Скай", "sky"]),
}

def subject_domain(id):
  return SUBJECTID_TO_DOMAIN[id]

def subject_label(id):
  return SUBJECTID_TO_LABELS[id]

def subject_id(label):
  return LABEL_TO_SUBJECTID[label]

def sentiment_label(id):
  return SENTIMENTID[id]

def subject_id_alternatives(subj):
  return SUBJECT_ALTERNATIVE_LABELS[subj]

def subject_alternatives(label):
  return subject_id_alternatives(subject_id(label))

def filter_documents(docs):
  """Filter documents that do not include subject in the text."""
  acc = []
  for doc in docs:
    keep = False
    for subj in doc["subjects"]:
      for alt in subject_id_alternatives(subj):
        if alt in doc["text"]:
          keep = True
    if keep:
      acc.append(doc)
  return acc

def preprocess_documents(docs):
  """Clean documents of the dataset."""
  acc = []
  for doc in docs:
    ## Messages with hyperlinks in the dataset are meaningless.
    if ("://" in doc["text"]):
      continue
    if ("ru" in doc["text"]):
      continue

    doc["text"] = re.sub(r"@[\d\w]+[.:\s]*", "", doc["text"])
    doc["text"] = re.sub(r"RT[\s]*", "", doc["text"])
    doc["text"] = re.sub(r"PM[\s]*", "", doc["text"])
    doc["text"] = re.sub(r"&.*;", "", doc["text"])
    doc["text"] = re.sub(r"[\s]*!+[\s!]*", "! ", doc["text"])
    doc["text"] = re.sub(r"[\s]*\.+[\s\.]*", ". ", doc["text"])
    doc["text"] = re.sub(r"[\s]*\,+[\s,]*", ", ", doc["text"])
    doc["text"] = re.sub(r"\.{1,2}", "!", doc["text"])
    doc["text"] = re.sub(r"…", "...", doc["text"])
    doc["text"] = re.sub(r"\s+", " ", doc["text"])
    doc["text"] = re.sub(r"[»\"'#\n]*", "", doc["text"])
    doc["text"] = re.sub(r"\A\W+", "", doc["text"])
    doc["text"] = re.sub(r"\s+$", "", doc["text"])
    for sep in ".?!":
      sentences = doc["text"].split(sep)
      doc["text"] = "".join(sentences[:-1] if len(sentences) > 1 else sentences)

    ## Skip short documents
    if len(doc["text"]) < 25:
      continue
    acc.append(doc)

  acc = filter_documents(acc)
  return acc

def read_documents(path):
  """Load the dataset."""
  acc = []
  root = ET.parse(path).getroot()
  for table in root.findall("database/table"):
    doc = {"acts": set(), "subjects": set()}
    for col in table:
      attr_name = col.attrib["name"]
      if attr_name == "text":
        doc["text"] = col.text
      if attr_name in SUBJECTID and col.text != "NULL":
        ## Add act with/without subject
        doc["acts"].add((("subject", subject_label(attr_name)), ("sentiment", sentiment_label(col.text))))
        doc["domain"] = subject_domain(attr_name)
        doc["subjects"].add(attr_name)
    acc.append(doc)
  return acc
