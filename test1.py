import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'Nt7ynRIbnJHZ4YggIshkoo208'
        consumer_secret = 'TV1oZol5VHKNJprHgKDjoSUUN08KAF7b3PzqlmyPkwRRybCSWd'
        access_token = '706742912629903361-sLCNwv4WRlpJnLwhASItGqTeFMAeE5X'
        access_token_secret = 'G6AheJ02ul8ZXJI1CcVWURQXBXDGGr1YCDlJpnHe3CuQa'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, h,query,count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count)
            df=pd.DataFrame(fetched_tweets)
            df.to_csv('tweets{0}.csv'.format(h))
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
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets
    query1=input("Enter the input query1:")
    query2=input("Enter the input query2:")
    h=1
    tweets1 = api.get_tweets(h,query = query1,count = 200)
    h=2
    tweets2 = api.get_tweets(h,query = query2,count = 200)
    xg1=[]
    yg1=[]
    xg2=[]
    yg2=[]
    x1=0
    x2=0
    y1=40
    y2=40
    pos1=0
    neg1=0
    pos2=0
    neg2=0
    for tweet1 in tweets1:
        if tweet1['sentiment']=='positive':
            y1=y1+1
            x1=x1+1
            pos1=pos1+1
            yg1.append(y1)
            xg1.append(x1)
        elif tweet1['sentiment']=='negative':
            y1=y1-1
            x1=x1+1
            neg1=neg1+1
            yg1.append(y1)
            xg1.append(x1)
        else:
            y1=y1
            x1=x1+1
            yg1.append(y1)
            xg1.append(x1)
    for tweet2 in tweets2:
        if tweet2['sentiment']=='positive':
            y2=y2+1
            x2=x2+1
            pos2=pos2+1
            yg2.append(y2)
            xg2.append(x2)
        elif tweet2['sentiment']=='negative':
            y2=y2-1
            x2=x2+1
            neg2=neg2+1
            yg2.append(y2)
            xg2.append(x2)
        else:
            y2=y2
            x2=x2+1
            yg2.append(y2)
            xg2.append(x2)

    pper1=((pos1)/(pos1+neg1))*100
    nper1=((neg1)/(pos1+neg1))*100
    pper2=((pos2)/(pos2+neg2))*100
    nper2=((neg2)/(pos2+neg2))*100
    print("Percentage of Supportive tweets for {0}:".format(query1))
    print(pper1)
    print("Percentage of Hatred tweets {0}:".format(query1))
    print(nper1)
    print("Percentage of Supportive tweets for {0}:".format(query2))
    print(pper2)
    print("Percentage of Hatred tweets {0}:".format(query2))
    print(nper2)
    if(len(tweets1)>len(tweets2)):
        plt.plot(xg1[0:x2],yg1[0:x2],color='red')
        plt.plot(xg2,yg2)
    else:
        plt.plot(xg1,yg1,color='red')
        plt.plot(xg2[0:x1],yg2[0:x1])
    plt.legend(["{0}".format(query1),"{0}".format(query2)])
    plt.xlabel('Tweets')
    plt.ylabel('Diff in Sentiments')
    plt.title('Sentiment Analysis')
    if(len(tweets1)>len(tweets2)):
        plt.xticks(np.arange(1,len(tweets2)+4,1))
    else:
        plt.xticks(np.arange(1,len(tweets1)+4,1)) 
    plt.yticks(np.arange(0,100,5))
    plt.show()
            
    
  
if __name__ == "__main__": 
    # calling main function 
    main() 
