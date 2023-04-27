import tweepy
import datetime

# Set up the authentication
auth = tweepy.OAuthHandler("API key", "API secret key")
auth.set_access_token("Access token", "Access token secret")

# Create a Tweepy API object
api = tweepy.API(auth)


#Test functionality - Works
api.update_status("Testing!")
