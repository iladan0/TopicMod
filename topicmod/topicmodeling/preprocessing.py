#import spacy
from topicmod.config import myconfig


    
#nlp = spacy.load(myconfig.spacy_fr)

def stopwords_fr(filepath=myconfig.stopwords_fr):
    with open(filepath) as f:
        stop_fr = [w.strip('\n') for w in f.readlines()]
    return stop_fr

def preprocess(text_col):
    """This function will apply NLP preprocessing lambda functions over a pandas series such as df['text'].
       These functions include converting text to lowercase, removing emojis, expanding contractions, removing punctuation,
       removing numbers, removing stopwords, lemmatization, etc."""
    
    # convert to lowercase
    text_col = text_col.apply(lambda x: ' '.join([w.lower() for w in x.split()]))
    
    # remove emojis
    text_col = text_col.apply(lambda x: demoji.replace(x, ""))
    
    # remove punctuation
    text_col = text_col.apply(lambda x: ''.join([i for i in x if i not in string.punctuation]))
    
    # remove numbers
    text_col = text_col.apply(lambda x: ' '.join(re.sub("[0-9]+", " ", x).split()))

    # remove stopwords
    text_col = text_col.apply(lambda x: ' '.join([w for w in x.split() if w not in stop_fr]))

    # lemmatization
    #text_col = text_col.apply(lambda x: ' '.join([token.lemma_ for token in nlp(x)]))

    # remove short words
    text_col = text_col.apply(lambda x: ' '.join([w.strip() for w in x.split() if len(w.strip()) >= 3]))

    return text_col