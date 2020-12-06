#  AI Journey 2020 competition

A winning (1st place) solution for "AI 4 Humanities: ruGPT-3" track of the [AI Journey 2020 competition](https://ai-journey.ru/en/contest).

In the work, I use pre-trained ruGPT-3 model for the task of semantically controlled response generation in context of goal-oriented dialog systems. The work is highly influenced by [Peng et. al 2020](https://arxiv.org/abs/2002.12328) and details may be found in the [presentation](docs/ai4humans.nesterov.pdf) (ru).

A model trained on RuCoS dataset:
- [Text generation](https://colab.research.google.com/drive/1lxNUY-gzeSDVXnZegteBCakET90Rj4Gf?usp=sharing) (colab)
- [Training of the model](https://colab.research.google.com/drive/18r0v7zaWrNtv565iEOa7BONYqG5vg88I?usp=sharing) (colab)

A model trained on SentiRuEval_2016 dataset:
- [Text generation](https://colab.research.google.com/drive/1Y_gy9CvPPaCvfCcp1dcYSi-tXlQjUPV6?usp=sharing) (colab)
- [Training of the model](https://colab.research.google.com/drive/1mW_hEaYlQbBvqWgQjpXzU88_IlE-1f9V?usp=sharing) (colab)



## Copyright notices

This repository includes third-party resources:
- `shell/pretrain_transformers.py`  
    A modified version of the scipt distributed with the [ruGPT-3](https://github.com/sberbank-ai/ru-gpts) model and mantained by the SberDevices team.
- `data/datasets/SentiRuEval_2016`  
    [The dataset](https://drive.google.com/drive/u/0/folders/0BxlA8wH3PTUfV1F1UTBwVTJPd3c) consists of user feedback regarding bank and telecom companies collected on Twitter. It was [presented](http://www.dialog-21.ru/media/3410/loukachevitchnvrubtsovayv.pdf) on the International Conference "Dialogue 2016" by Lukashevich and Rubtsova.
- `data/datasets/RuCoS`  
    The dataset automatically generated from CNN/Daily Mail news articles and distibuted within [Russian SuperGLUE benchmark](https://russiansuperglue.com).
