bertopic-app
==============================

# Project description:
bertopic-app is intended to scrap googlempas reviews and apply topic modeling techniques on them,

It contains 4 sous-packages : scraping, topicmodeling, EDA (exploratory data analysis) and webapp

# Configuration
install dependecies in requirements.txt
for hdbscan (download dependency as zipfile, unzip and then install it using python setup.py)

# Usage
The usage of different sous-packages is depicted in the guided notebooks
You can find the binary, that you should put in \bin folder, in the following link:
https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

#Webapp
To run the web application:
```
cd topicmod/webapp
streamlit run Homepage.py
```
