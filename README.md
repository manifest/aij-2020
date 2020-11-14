#  AI Journey 2020 competition

A solution for "AI 4 Humanities: ruGPT-3" track of the [AI Journey 2020 competition](https://ai-journey.ru/en/contest).


## How to use

```bash
tar xzf data.tar.gz
```
> Unzip data.


## Copyright notices

This repository includes third-party resources:
- `shell/pretrain_transformers.py`  
    A modified version of the scipt distributed with the [ruGPT-3](https://github.com/sberbank-ai/ru-gpts) model and mantained by the SberDevices team.
- `data/datasets/SentiRuEval_2016`  
    [The dataset](https://drive.google.com/drive/u/0/folders/0BxlA8wH3PTUfV1F1UTBwVTJPd3c) consists of user feedback regarding bank and telecom companies collected on Twitter. It was [presented](http://www.dialog-21.ru/media/3410/loukachevitchnvrubtsovayv.pdf) on the International Conference "Dialogue 2016" by Lukashevich and Rubtsova.
- `data/datasets/RuCoS`  
    The dataset automatically generated from CNN/Daily Mail news articles and distibuted within [Russian SuperGLUE benchmark](https://russiansuperglue.com).
