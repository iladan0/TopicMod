import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from topicmod.topicmodeling.bertopmod import load_model
import bertopic
st.set_page_config(page_title="Topic modeling sur les Avis Google Maps ", page_icon="🔍")
st.title("Topic modeling sur les Avis Google Maps")

@st.cache(allow_output_mutation=True)
def make_wordcloud(top_words_dict):
    wordcloud = WordCloud(
        width=900,height=500, max_words=1628, background_color="white",
        relative_scaling=0).generate_from_frequencies(top_words_dict)
    fig = plt.figure(figsize=[15,10])
    # plot the wordcloud
    plt.imshow(wordcloud, interpolation="bilinear")
    # remove plot axes
    plt.axis("off")
    return fig

def get_top_words(topic_model,topic_nbr):
    return dict((t[0], t[1]) for t in topic_model.topic_representations_[topic_nbr])

@st.cache(hash_funcs={bertopic._bertopic.BERTopic: lambda _: None})
def get_intertopic_dist_map(topic_model):
    return topic_model.visualize_topics()

@st.cache(hash_funcs={bertopic._bertopic.BERTopic: lambda _: None})
def get_topic_representation(topic_model, topic_nbr=1):
    topic_repres = {
        'topic number':topic_nbr,
        'documents count': topic_model.topic_sizes_[topic_nbr],
        'top 10 words': get_top_words(topic_model, topic_nbr),
        'representative documents':topic_model.representative_docs_[topic_nbr][:3]
    }
    return topic_repres

@st.cache(hash_funcs={bertopic._bertopic.BERTopic: lambda _: None})
def get_topic_keyword_barcharts(topic_model):
    return topic_model.visualize_barchart(top_n_topics=8, n_words=5, height=300, width=230)

@st.cache(hash_funcs={bertopic._bertopic.BERTopic: lambda _: None})
def get_close_topics(topic_model, keyword):
    topics, similarity = topic_model.find_topics(keyword, top_n=5)
    top_words = [' '.join([i[0] for i in topic_model.get_topic(topic=t)]) for t in topics]
    df = pd.DataFrame({'topic': topics, 'similarity': similarity, 'top_words':top_words})
    return df

@st.cache(hash_funcs={bertopic._bertopic.BERTopic: lambda _: None})
def get_topics_over_time(topic_model, topics_over_time):
    return topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=10)



tm_state = st.text('Loading topics model...')
topic_model = load_model()
tm_state.text('Loading topics model... done!')

st.markdown("## 📋 Top 10 Topics avec leurs nombre de documents")
freq = topic_model.get_topic_info(); 
st.dataframe(freq.head(10))

fig1 = get_intertopic_dist_map(topic_model)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("## 📊 Mots représentatifs des top 10 topics")
fig3 = get_topic_keyword_barcharts(topic_model)
st.plotly_chart(fig3)

st.markdown("## 🔍 Explorer un topic")
topic_nbr = st.select_slider(
'Select a topic number :',
options=[i for i in range(0,len(freq)-2)])
st.header('Topic '+str(topic_nbr))
fig2 = make_wordcloud(get_top_words(topic_model,topic_nbr))
st.pyplot(fig2)
docs_rep= get_topic_representation(topic_model,topic_nbr=topic_nbr)
st.write(docs_rep)

st.markdown("## 🔍 Trouver les thématiques proches à un mot clé")
kw = st.text_input('Find topics most similar to :','conseiller')
st.dataframe(get_close_topics(topic_model, kw))

#fig2 = get_topics_over_time(text, topics, dates, topic_model)
#st.write(fig2)
