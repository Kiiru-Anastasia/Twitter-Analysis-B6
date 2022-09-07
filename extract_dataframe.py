import json
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self):
        # list(map(lambda tweet: tweet['user']['statuses_count'], self.tweets_list))
        statuses_count = []
        for row in self.tweets_list:
            statuses_count.append(row['user']['statuses_count'])

        return statuses_count
        
    def find_full_text(self)->list:
        text = []
        for row in self.tweets_list:
            text.append(row['full_text'])

        return text
       
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []
        for row in text:
            polarity.append(seTextblob(tweet))
            blob = TextBlob(row)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_time = []
        for row in self.tweets_list:
            created_time.append(row['created_at'])
        return created_time

    def find_source(self)->list:
        source = []
        for row in self.tweets_list:
            source.append(row['source'])

        return source

    # def find_screen_name(self)->list:
    #     screen_name = self.tweets_list['screen_name']

    #     return screen_name

    # def find_followers_count(self)->list:
    #     followers_count = self.tweets_list['followers_count']

    #     return followers_count

    # def find_friends_count(self)->list:
    #     friends_count = 

    def is_sensitive(self)->list:
        is_sensitive = []
        for row in self.tweets_list:
            if 'possibly_sensitive' in row.keys():
                is_sensitive.append(row['possibly_sensitive'])
            else:
                is_sensitive.append('')

        df = pd.DataFrame(is_sensitive, columns = ['sensitivity'])
        df.to_json('data/sample_sensitivity.json', index=False)

        return is_sensitive

    # def find_favourite_count(self)->list:
        
    
    # def find_retweet_count(self)->list:
    #     retweet_count = 

    # def find_hashtags(self)->list:
    #     hashtags =

    # def find_mentions(self)->list:
    #     mentions = 


    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        # columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
        #     'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        columns = ['created_at', 'status_count', 'original_text', 'source', 'polarity', 'subjectivity', 'possibly_sensitive']
        scount = self.find_statuses_count()
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        #lang = self.find_lang()
        #fav_count = self.find_favourite_count()
        #retweet_count = self.find_retweet_count()
        # screen_name = self.find_screen_name()
        # follower_count = self.find_followers_count()
        # friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        # hashtags = self.find_hashtags()
        # mentions = self.find_mentions()
        # location = self.find_location()
       # data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        data = zip(created_at, scount, text, source, polarity, subjectivity, sensitivity)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('data/sample_processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/africa_twitter_data.json")

    # df = pd.DataFrame(tweet_list)
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()
    print(tweet_df.head(10)) 

    # use all defined functions to generate a dataframe with the specified columns above