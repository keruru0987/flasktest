# coding=utf-8
# @Author : Eric

nlp_api = ['allennlp', 'gensim', 'nltk', 'spaCy', 'stanford-nlp', 'TextBlob', 'Transformers']
nlp_choose = 5  # 指定当前研究的API

api_label_prelink = {'allennlp':'https://github.com/allenai/allennlp/labels/', 'gensim':'https://github.com/RaRe-Technologies/gensim/labels/',
               'nltk':'https://github.com/nltk/nltk/labels/', 'spaCy': 'https://github.com/explosion/spaCy/labels/',
               'stanford-nlp':'https://github.com/stanfordnlp/CoreNLP/labels/', 'TextBlob':'https://github.com/sloria/TextBlob/labels/',
               'Transformers':'https://github.com/huggingface/transformers/labels/'}

api_prelink = {'allennlp':'https://github.com/allenai/allennlp/issues/', 'gensim':'https://github.com/RaRe-Technologies/gensim/issues/',
               'nltk':'https://github.com/nltk/nltk/issues/', 'spaCy': 'https://github.com/explosion/spaCy/issues/',
               'stanford-nlp':'https://github.com/stanfordnlp/CoreNLP/issues/', 'TextBlob':'https://github.com/sloria/TextBlob/issues/',
               'Transformers':'https://github.com/huggingface/transformers/issues/'}

github_filepath = {'gensim': 'data/issue/gensim.json', 'allennlp': 'data/issue/allennlp.json',
                   'nltk': 'data/issue/nltk.json', 'spaCy': 'data/issue/spaCy.json',
                   'stanford-nlp': 'data/issue/CoreNLP.json', 'TextBlob': 'data/issue/TextBlob.json',
                   'Transformers': 'data/issue/transformers.json'}

new_github_filepath = {'gensim': 'data/new_issue/gensim.csv', 'allennlp': 'data/new_issue/allennlp.csv',
                       'nltk': 'data/new_issue/nltk.csv', 'spaCy': 'data/new_issue/spaCy.csv',
                       'stanford-nlp': 'data/new_issue/stanford-nlp.csv', 'TextBlob': 'data/new_issue/TextBlob.csv',
                       'Transformers': 'data/new_issue/Transformers.csv'}

tagged_github_filepath = {'gensim': 'data/tagged_data/gensim.csv', 'allennlp': 'data/tagged_data/allennlp.csv',
                          'nltk': 'data/tagged_data/nltk.csv', 'spaCy': 'data/tagged_data/spaCy.csv',
                          'stanford-nlp': 'data/tagged_data/stanford-nlp.csv', 'TextBlob': 'data/tagged_data/TextBlob.csv',
                          'Transformers': 'data/tagged_data/Transformers.csv'}

stackoverflow_filepath = {'gensim': 'data/stackoverflow/gensim.csv', 'allennlp': 'data/stackoverflow/allennlp.csv',
                          'nltk': 'data/stackoverflow/nltk.csv', 'spaCy': 'data/stackoverflow/spacy.csv',
                          'stanford-nlp': 'data/stackoverflow/stanford-nlp.csv', 'TextBlob': 'data/stackoverflow/textblob.csv',
                          'Transformers': 'data/stackoverflow/transformers.csv'}

word2vec_modelpath = 'D:/model/GoogleNews-vectors-negative300.bin'

select_num = 20  # 选取的分数最高的issue数目

