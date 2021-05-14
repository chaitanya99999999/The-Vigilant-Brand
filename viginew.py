import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'qTIVL4BRkIsP1u4K3CiG7viku'
        consumer_secret = 'lj4i87YmUerOeGZ0RVjWfQfduJ95bE58i2fdZAAHzddkzWfp0i'
        access_token = '725621133567905792-FzzWCsYANNpxgQkkwQpxtQg8pau2aqg'
        access_token_secret = 'jnRTAYRboQOT1V50r7tGojzP9uM0BuYiiY2WxPfgSaHAh'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            st.write("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        """
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # st.write error (if any)
            st.write("Error : " + str(e))


def notMain(ele):
    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets

    tweets = api.get_tweets(query=ele, count=200)
    # st.write(ele)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    # percentage of positive tweets
    
    pper = 100*(len(ptweets)/len(tweets))
    if (pper<10):
        st.markdown('<h2>Not a good brand name</h2>',unsafe_allow_html=True)
    elif(pper>10 and pper<20):
        st.markdown('<h2>Mehh,Can work for a normal brand</h2>',unsafe_allow_html=True)
    elif(pper>20 and pper<30):
        st.markdown('<h2>OMG It is gonna boom in the market</h2>',unsafe_allow_html=True)
    elif(pper>30 and pper<40):
        st.markdown('<h2>HUUUUGEEEEE Impact creator name</h2>',unsafe_allow_html=True)
    elif(pper>40 and pper<101):
        st.markdown('<h2>SUDER DUPER Brand booster name</h2>',unsafe_allow_html=True)
    # st.write(pper)
    st.write("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    nper = 100*(len(ntweets)/len(tweets))
    # percentage of negative tweets
    st.write("Negative tweets percentage: {} %".format(100 * (len(ntweets) / len(tweets))))
    # percentage of neutral tweets
    st.write(
        "Neutral tweets percentage: {} %  ".format(100 * ((len(tweets) - len(ntweets) - len(ptweets))) / len(tweets)))
    nnper=100*((len(tweets) - len(ntweets) - len(ptweets)))/len(tweets)
    df = pd.DataFrame({'Percentage': [pper, nper , nnper]},index=['Positive', 'Negative', 'Neutral'])
    labels = ['Positive%','Negative%','Neutral%']
    values = [pper, nper, nnper]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    st.plotly_chart(fig)
    # st.writeing first 5 positive tweets
    # st.write("Positive tweets:")
    new_ptweets = []
    new_ntweets = []
    for tweet in ptweets[:10]:
        new_ptweets.append(tweet['text'])
    # st.write(tweet['text'])
    # st.write(new_ptweets)
    st.markdown('<center><h2>Positive Tweets</h2></center>', unsafe_allow_html=True)
    for ele1 in new_ptweets:
        st.write(ele1)
    

    # st.writeing first 5 negative tweets
    # st.write("Negative tweets:")
    for tweet in ntweets[:10]:
        new_ntweets.append(tweet['text'])
    # st.write(tweet['text'])
    st.markdown('<center><h2>Negative Tweets</h2></center>', unsafe_allow_html=True)
    for ele1 in new_ntweets:
        st.write(ele1)
    


def main():
    st.title("Vigilant Brand")
    st.markdown('This dashboard is the ultimate solution for your brand image/ Influencer Image')
    # st.markdown('Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.')
    image = Image.open('color_bubbles.jpeg')
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.markdown('<center> <h1>Vigilant Brand</h1></center>',unsafe_allow_html=True)
    st.sidebar.markdown('<center> <h3>Enter the name of the Brand you want to get latest updates on.</h3></center>',unsafe_allow_html=True)
    st.sidebar.markdown('<center> <h3>Hit the Button to find its overall review taken from latest tweets by people.</h3></center>',unsafe_allow_html=True)
    st.sidebar.markdown('<center> <h3>HIT TO STAY UPDATED!!.</h3></center>',unsafe_allow_html=True)
    
    # st.sidebar.markdown("Select the Charts/Plots accordingly:")
    ele = st.text_input('Brand Name')
    if st.button('Find My Brand Value📈'):
        notMain(ele)


if __name__ == "__main__":
    # calling main function
    main()

