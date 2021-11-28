import tweepy
import time


###################################################################################

""" Authorization information from Twitter account"""

"""

# Uncomment this section and insert credentials

CONSUMER_KEY =  'consumer key'

CONSUMER_SECRET = 'consumer secret'

ACCESS_KEY = 'access key '

ACCESS_SECRET =  'access secret'



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

"""
###################################################################################



keywords = ["rt to", "rt and win", "retweet and win", "rt for", "rt 4", "retweet to"]  #words we are looking for in potential contest tweets



bannedwords = ["vote", "bot", "b0t"]



bannedusers = ['bot', 'spot', 'lvbroadcasting', 'jflessauSpam', 'bryster125', 'MobileTekReview', 
                'ilove70315673', 'followandrt2win', 'traunte', 'ericsonabby', '_aekkaphon','furry_memes'] #list of potential and known users we wish to ignore



def isUserBot(username):
	""" Checks if the current user is in the list of banned users. Returns True if they are a banned user, False if not"""

	clean_username = username.replace("0", "o")

	clean_username = clean_username.lower()

	for i in bannedusers:

		if i in clean_username:

			return True

		else:

			return False



def search_tweets(twts):
	""" Searches for valid tweets (tweets with one more more of the keywords present) then, depending on the requirements to enter the contest, will favourite, follow, or retweet the tweet"""

	for t in twts:

		if not any(k in t.text.lower() for k in keywords) or any(k in t.text.lower() for k in bannedwords):

			continue

		if isUserBot(str(t.author.screen_name)) == False:      #if the user is not a bot

			if not t.retweeted:                                #and we have not previously retweeted the tweet

				try:

					api.retweet(t.id)                          #retweet the tweet

					print("rt " + (t.text))                  

					

					if "follow" in t.text or "Follow" in t.text or "FOLLOW" in t.text:    #if the word following is a requirement to enter
						user_id = t.retweeted_status.user.id                              #grab the username

						api.create_friendship(user_id)                                    #and send a friend request



				except Exception:

					pass



			if ("fav" in t.text or "Fav" in t.text or "FAV" in t.text or "Favorite" in t.text or "favorite" in t.text or "FAVORITE" in t.text or 
			     "favourite" in t.text or "Favourite" in t.text or "FAVOURITE" in t.text or "LIKE" in t.text or "Like" in t.text or "like" in t.text) and not t.favorited:   #if favouriting is a requirement to enter

				try:

					api.create_favorite(t.id)        #we favourite the tweet

					print("fav " + (t.text))

				except Exception:

					pass



def run():

	for key in ["RT to win", "retweet to win"]:

		print("\nSearching again\n")

		search_tweets(api.search_tweets(q=key))




if __name__ == '__main__':    #run every 25 seconds to avoid being banned for excessive botting

    while True:
            run()
            time.sleep(25)