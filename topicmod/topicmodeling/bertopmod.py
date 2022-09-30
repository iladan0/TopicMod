import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from topicmod.config import myconfig
from topicmod.topicmodeling.preprocessing import stopwords_fr
import streamlit as st

embedding_model = SentenceTransformer(myconfig.bert_multi)
vectorizer_model = CountVectorizer(stop_words=stopwords_fr())



def init_topic_model(df, topic_model=None):
    text = df['text'].to_list()
    dates = df['review_date'].apply(lambda x: pd.Timestamp(x))
    if not topic_model:
        topic_model = BERTopic(embedding_model=embedding_model,
                            vectorizer_model=vectorizer_model,
                            n_gram_range=(1,3),
                            diversity=0.6, 
                            verbose=False)

    return text, dates, topic_model


def init_topics_over_time(text, dates, topic_model):
    topics_over_time = topic_model.topics_over_time(docs=text, 
                                                    timestamps=dates, 
                                                    global_tuning=True, 
                                                    evolution_tuning=True, 
                                                    nr_bins=len(set(dates)) // 7)
    return topics_over_time

def load_model(filepath=myconfig.default_bertopic):
    return BERTopic.load(filepath)