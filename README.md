# cord19 : merging and preparing linguistic annotation of the corpus
cord19 is covid-19 open-source corpus from  https://www.semanticscholar.org/cord19/download. Documentation available at https://github.com/allenai/cord19

## stage01: Download and merge json files into a single text file
Open in Google Colab - Jupyter notebook [https://colab.research.google.com/github/iued-uni-heidelberg/cord19/blob/main/cord19download2text.ipynb](https://colab.research.google.com/github/iued-uni-heidelberg/cord19/blob/main/cord19download2text.ipynb)

You can also split the file into several text files, each containing the necessary number of text and/or filter the corpus by a certain keyword, e.g., 'covid'

## stage02: extract lemmas after TreeTagger part-of-speech annotation
Open in Google Colab: [https://colab.research.google.com/github/iued-uni-heidelberg/cord19/blob/main/cord19treetagger2lemmas.ipynb](https://colab.research.google.com/github/iued-uni-heidelberg/cord19/blob/main/cord19treetagger2lemmas.ipynb)

This script will extract the third column from your \*vert file. You can modify the script to extract other types of annotation or combination of annotation columns and/or their sub-parts (e.g., lemmatized parts-of-speech + lemma, etc.


