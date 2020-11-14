from collections import Counter

def slot_error_rate(text, slot_values, n_slots=1):
  """
  Estimates slot error rate as:
  err = (p + q) / n_slots
  where
  - p, q is the number of missing and redundant slots in the document.
  - n_slots is the total numberof slots in the document.
  """
  n = 0
  words = text.split(" ")
  for word in words:
    is_subj = False
    for alt in slot_values:
      if alt in word:
        is_subj = True
    if is_subj:
      n += 1
  pq = abs(n - n_slots)
  err = pq / float(n_slots)
  return err

def rouge1_similarity(system, reference):
  sys_counter = Counter(system)
  ref_counter = Counter(reference)
  overlap = 0.

  for token in sys_counter:
    token_count_sys = sys_counter.get(token, 0)
    token_count_ref = ref_counter.get(token, 0)
    overlap += min(token_count_sys, token_count_ref)

  precision = overlap / len(system)
  recall = overlap / len(reference)

  if precision + recall != 0:
    rouge1_score = 2. * ((precision * recall) / (precision + recall))
  else:
    rouge1_score = 0.

  return rouge1_score

def average_overlap(similarity_fn, samples):
  assert len(samples) > 0, "At least two samples are required."
  if len(samples) == 1: return [1.]

  scores = [None] * len(samples)
  for candidate_index, candidate in enumerate(samples):    
    overlap = 0.
    for sample_index, sample in enumerate(samples): 
      if candidate_index == sample_index:
        continue

      sample_overlap = similarity_fn(samples[candidate_index], samples[sample_index])
      overlap += sample_overlap

    score = overlap / (len(samples) - 1)
    scores[candidate_index] = score

  return scores

def score(idsequences, tokenizer, slot_values=None, score_fn=average_overlap, similarity_fn=rouge1_similarity):
  scores = score_fn(similarity_fn, idsequences)

  acc = []
  for n, idseq in enumerate(idsequences):
    text = decode(idseq, tokenizer)
    err = 0.
    if slot_values != None:
      err = slot_error_rate(text, slot_values)
    item = {
      "score": scores[n],
      "err": err,
      "text": text,
    }
    acc.append(item)

  acc = sorted(acc, key=lambda a: a["score"] / (a["err"] + 1e-4), reverse=True)
  return acc

def decode(idseq, tokenizer):
  return tokenizer.decode(idseq).strip()

def unique(idsequences):
  acc = []
  for i in range(len(idsequences)):
    keep = True
    lt = idsequences[i]
    for j in range(i+1, len(idsequences)):
      rt = idsequences[j]
      if lt == rt:
        keep = False
    if keep:
      acc.append(lt)
  return acc

def process_outputs(idsequences, tokenizer, slot_values=None):
  return score(
    unique([process_output(idseq, tokenizer) for idseq in idsequences]),
    tokenizer,
    slot_values,
  )

def format_documents(docs):
  s = ""
  for doc in docs:
    s += "\n[score={:0.4f}, err={:1.0f}] {}".format(doc["score"], doc["err"], doc["text"])
  return s

def process_output(idseq, tokenizer):
  bos_index = idseq.index(tokenizer.bos_token_id) + 1
  eos_index = len(idseq)
  try:
    eos_index = idseq.index(tokenizer.eos_token_id)
  except:
    pass

  return idseq[bos_index:eos_index]
