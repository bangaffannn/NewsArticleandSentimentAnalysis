#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 00:29:34 2023

@author: macbook
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

#READING EXCEL OR XLSX FILES
data = pd.read_excel('articles.xlsx')

#DATA SUMMARY
data.describe()

#COLUMN SUMMARY
data.info()

#COUNTING NUMBER OF ARTICLE PER SOURCE
data.groupby(['source_id'])['article_id'].count()
#NUMBER REACTIONS BY PUBLISHER
data.groupby(['source_id'])['engagement_reaction_count'].sum()
#DROPPING COLUMN
data = data.drop('engagement_comment_plugin_count', axis=1)

#CREATING A KEYWORD FLAG
keyword = 'crash'
#ISOLATING EACH TITLE ROW

#CREATING FUNCTION
def keywordFlag(keyword):
    length = len(data)
    keyword_flag = []
    for word in range(0, length):
        heading = data['title'][word]
        try:
            if keyword in heading:
                 flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)  
    return keyword_flag

keywordFlag = keywordFlag('murder')

#CREATING NEW COLUMN IN DATA FRAME
data['keyword_flag'] = pd.Series(keywordFlag)

#SentimentIntensityAnalyzer
sent_int = SentimentIntensityAnalyzer()
text = data['title'][15]
sent = sent_int.polarity_scores(text)

neg = sent['neg']
pos = sent['pos']
neu = sent['neu']

#ADDING FOR LOOP TO EXTRACT SENTIMENT PER TITLE
title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

for analysis in range (0, len(data)):
    try:
        text = data['title'][analysis]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)
    
title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)

data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment

#VISUALIZING DATA
ypoint = data['title_neg_sentiment']
xpoint = data['title_pos_sentiment']
plt.scatter(xpoint, ypoint, color = 'red')
plt.show()

#WRITING THE DATA
data.to_excel('blogme_clean.xlsx', sheet_name = 'blogmedata', index = False)



