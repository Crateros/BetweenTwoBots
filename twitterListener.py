import tweepy
from env import keys


CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):

    def __init__(self):
        # self.tweetBot = TweetBot()
        #initialize Twitter authorization with tweepy
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def on_status(self, status):
        print(status.text)

    def on_erorr(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["beer"])


# toReply = "someonesTwitterName" #user to get most recent tweet
# api = tweepy.API(auth)
#
# #get the most recent tweet from the user
# tweets = api.user_timeline(screen_name = toReply, count=1)
#
# for tweet in tweets:
#     api.update_status("@" + toReply + " This is what I'm replying with", in_reply_to_status_id = tweet.id)
