import os

class Config:
    
    # Files
    dirpath_package = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)
    inpdirpath = os.path.join(
        dirpath_package,
        r"data\input"
    )

    proxy ={
        "http":"http://BENREKIA:Iladis_2016@100.121.67.103:8080",
        "https":"https://BENREKIA:Iladis_2016@100.121.67.103:8080"}

    google_apikey = "AIzaSyDlsHtpTKpnSBEMSU4ehEZIyEPLsMyHtFk"

    stopwords_fr = os.path.join(dirpath_package, r"bin\stopwords_fr.txt")

    # language models
    #spacy_fr =  os.path.join(dirpath_package, r"bin\fr_core_news_lg-3.3.0\fr_core_news_lg\fr_core_news_lg-3.3.0")
    bert_multi = os.path.join(dirpath_package, r"bin\paraphrase-MiniLM-L12-v2")

    #trained bertopic model
    default_bertopic = os.path.join(dirpath_package, r"models\default_bertopic")

    df_ids = os.path.join(dirpath_package, r"data\interim\scraping\agences_ids.csv")
myconfig = Config()