import tweepy

# Set up the authentication by reading the credentials from file
with open('creds.txt', 'r') as f:
    apiKey = f.readline().strip()
    apiSecretKey = f.readline().strip()
    accessToken = f.readline().strip()
    accessTokenSecret = f.readline().strip()

auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)


# Create a Tweepy API object
api = tweepy.API(auth)


MENTIONS_LOG_FILE = "mentions-log.txt"


def load_replied_tweet_ids():
    try:
        with open(MENTIONS_LOG_FILE, "r") as f:
            return set(int(line.strip()) for line in f)
    except FileNotFoundError:
        return set()

def save_replied_tweet_ids(ids):
    with open(MENTIONS_LOG_FILE, "w") as f:
        for tweet_id in ids:
            f.write(str(tweet_id) + "\n")


def reply_to_mentions():
    replied_tweet_ids = load_replied_tweet_ids()
    last_reply_id = max(replied_tweet_ids) if replied_tweet_ids else None
    mentions = api.mentions_timeline(since_id=last_reply_id)

    # For each mention, reply with "Hello World!" if the bot hasn't replied to it already
    for mention in mentions:
        query = mention.text
        query = query.lower().replace("@ahwaknow","")
         
        if mention.id not in replied_tweet_ids:
            api.update_status(
                status="'" + query +"'",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True
            )
            replied_tweet_ids.add(mention.id)

    # Save the updated set of replied tweet IDs to the file
    save_replied_tweet_ids(replied_tweet_ids)

# Call the function to reply to mentions
reply_to_mentions()