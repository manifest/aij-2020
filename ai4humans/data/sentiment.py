from ai4humans.data import sentirueval2016
import os

def read(path):
  docs = sentirueval2016.preprocess_documents(
    sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "bank_train_2016.xml")) \
      + sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "banks_test_2016.xml")) \
      + sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "banks_test_etalon.xml")) \
      + sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "tkk_train_2016.xml")) \
      + sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "tkk_test_2016.xml")) \
      + sentirueval2016.read_documents(os.path.join(path, "datasets", "SentiRuEval_2016", "tkk_test_etalon.xml"))
  )
  return docs

def format_act(domain, act):
  s = domain + "{inform("
  acc = []
  for tag, entity in act:
    acc.append("{}={}".format(tag, entity))
  s += ", ".join(acc)
  s += ")}"
  return s

def format_text(domain, act, text):
  return "{}[BOS]{}[EOS]".format(format_act(domain, act), text)

def format_texts(docs):
  acc = []
  for doc in docs:
    for act in doc["acts"]:
      acc.append(format_text(doc["domain"], act, doc["text"]))
  return acc

def slot_values(label):
  return sentirueval2016.subject_alternatives(label)
