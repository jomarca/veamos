import tweepy

consumer_key = 'sOCtIn12MdBUekw7K8JW7Tm9p'
consumer_secret = '92ByN3XKpeqtINLRTLRAFfhfmUkOjRWDiSLzhZRmIcS5EdnNms'
access_token = '1107203070998573056-WtHzQdR5Y1ZCS9hxZxGXFLYyr1dYLF'
access_token_secret = '4r1FJQaxiq8OLoAZnrmUpcYBXXwQn4yyn7QCDE7yIH1Ul'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)

api.update_status('Updating using OAuth authentication via Tweepy!')