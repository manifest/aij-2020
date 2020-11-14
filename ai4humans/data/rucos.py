from collections import defaultdict

TOPICS = [
  'спорт',
  'политика',
  'бизнес',
  'мир',
]

def read_documents(decoder, path):
  acc = []
  with open(path) as file:
    acc = file.readlines()
    acc = [decoder.decode(line[:-1]) for line in acc]
  return acc

def build_documents_meta(docs, entity_mapping, entity_meta, ignore_tags):
  acc = {}
  drop = []
  for doc_id, doc in enumerate(docs):
    keep = False
    meta = {
        "entities": defaultdict(set),
        "tags": set(),
    }
    text = doc["passage"]["text"]
    for entity in doc["passage"]["entities"]:
      original_entity = text[entity["start"]:entity["end"]]
      if original_entity in entity_mapping:
        entity = entity_mapping[original_entity]
        tag = entity_meta[entity]["tag"]
        if tag in ignore_tags:
          continue
        meta["entities"][tag].add(entity)
        meta["tags"].add(tag)
        keep = True
    if keep:
      acc[doc_id] = meta
    else:
      drop.append(doc_id)
  return acc, drop

def build_acts(docs_meta):
  acc = defaultdict(list)
  for doc_id, meta in docs_meta.items():
    tags = meta["tags"]
    act = ()
    if "агенство" in tags:
      act += (("agency", list(meta["entities"]["агенство"])[0]),)

    options = []
    for topic in TOPICS:
      if topic not in tags:
        continue

      option = ()
      if topic in tags:
        option += (("topic", topic),)

      if (len(act) > 0 and len(option) > 0):
        options.append(option + act)
        options.append(option)
        acc[doc_id] += options
      elif (len(option) > 0):
        options.append(option)
        acc[doc_id] += options

      ## Get first topic acording to the list of topics
      break

  return acc
