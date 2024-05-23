import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
#text="""Samsung first entered the electronics industry in 1969 with several electronics-focused divisions.Their first products were black-and-white televisions. During the 1970s the company began to export home electronics products overseas.At that time Samsung was already a major manufacturer in Korea, and it had acquired a 50 percent stake in Korea Semiconductor.The late 1970s and early ’80s witnessed the rapid expansion of Samsung’s technology businesses.Separate semiconductor and electronics branches were established, and in 1978 an aerospace division was created.Samsung Data Systems (now Samsung SDS) was established in 1985 to serve businesses’ growing need for systems development. That helped Samsung quickly become a leader in information technology services. Samsung also created two research and development institutes that broadened the company’s technology line into  electronics, semiconductors, high-polymer chemicals, genetic engineering tools, telecommunications, aerospace, and nanotechnology."""


def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    #print(doc)
    tokens=[token.text for token in doc]
    #print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    #print(word_freq)

    max_freq=max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq

    #print(word_freq)

    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
    #print(sent_scores)

    select_len=int(len(sent_tokens)*0.3)
    #print(select_len)

    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)

    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    #print("ORIGINAL TEXT",text)
    #print("SUMMARIZE TEXT",summary)
    #print("LENGTH OF ORIGINAL TEXT",len(text.split(' ')))
    #print("LENGTH OF SUMMARIZE TEXT",len(summary.split(' ')))

    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))