import tweepy, time, sys
import threading
import markovify
import nltk
import re
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import Stream

oldtext = []
back = []
backtext = []

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        print("THIS IS INPUT: ", sentence)
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class TweetBot:

    def __init__(self, botfood):
        #load text & build model
        self.load_botfood(botfood)

        #initialize Twitter authorization with tweepy
        auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
        auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))
        self.api = tweepy.API(auth)

    def load_botfood(self, botfood):
        #open botfood text and run it through Markofivy
        with open(botfood) as botfood:
            botfood_text = botfood.read()
        self.model = markovify.Text(botfood_text)

    def backlog(self):
        public_tweets = self.api.home_timeline()
        for tweet in public_tweets:
            if tweet.user.screen_name != "sven_dellstrom":
                backtext.insert(0, tweet.text)
                if tweet.user.screen_name not in back:
                    toReply = tweet.user.screen_name
                    self.tweet(toReply)
                    back.insert(0, tweet.user.screen_name)

    def timeline(self):
        public_tweets = self.api.home_timeline()
        with open("botfood.txt", 'r') as botfood_file:
            botfood = botfood_file.read()
            model = markovify.Text(botfood)
        with open ("botfood.txt", "a") as botfood_file:
            for tweet in public_tweets:
                # print(tweet.user.screen_name, tweet.text)
                if tweet.user.screen_name != "sven_dellstrom":
                    if tweet.text not in oldtext:
                        if tweet.text not in backtext:
                            if "sven_dellstrom" in tweet.text.lower() or "sven dellstrom" in tweet.text.lower():
                                toReply = tweet.user.screen_name
                                self.tweet(toReply)
                                oldtext.insert(0, tweet.text)
                                tobeinserted = tweet.text
                                tobeinserted = tobeinserted.split(' ', 1)[1]
                                botfood_file.write(tobeinserted + "\n")
                                if len(oldtext) > 15:
                                    oldtext.pop()

    def tweet(self, toReply):
        #generate Markov tweet & send it
        message = self.model.make_short_sentence(120)
        messageTwo = self.model.make_short_sentence(140)
        try:
            self.api.update_status('@' + toReply + " " + message)
            self.api.update_status(messageTwo)

        except tweepy.TweepError as error:
            print(error.reason)

    def follow(self):
        for follower in tweepy.Cursor(self.api.followers).items():
            follower.follow()
            print (follower.screen_name)

    def search(self):
        message = self.model.make_short_sentence(120)
        toReply = "tmrdrr"
        # self.api.update_status('@' + toReply + " " + message)
        twts = self.api.search(q="Hello World!")
        tweetMatch = ['Hello world!',
                    'Hello World!',
                    'Hello World!!',
                    'Hello World!!!',
                    'Hello, world!',
                    'Hello, World!']
        for s in twts:
            print(s.text)
            for match in tweetMatch:
                if match == s.text:
                    print("-------------------FOUND A MATCH!--------------------")
                    sn = s.user.screen_name
                    m = "@%s Python robot responding!" % (sn)
                    print("THIS IS M: ", m)
                    s = self.api.update_status(m, s.id)

    def automate(self, delay):
        #automaticlaly tweet on interval (delay)
        while True:
            # self.search()
            self.timeline()
            sleep(delay)

def main():
    bot = TweetBot("botfood.txt")
    bot.backlog()
    bot.follow()
    bot.automate(180)

if __name__ == "__main__":
    main()
