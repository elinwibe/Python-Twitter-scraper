#This code searches for tweets with a particuar keyword and writes certain fields into a CSV file

import sys, csv
import twitter
import os
import tweepy

# Replace the API_KEY and API_SECRET with your application's key and secret.
#This code is using AppAuthHandler, not OAuthHandler to get higher limits, 2.5 times.
auth = tweepy.AppAuthHandler('YOUR_API_KEY', 'YOUR_SECRET_API_KEY')
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)


if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
def clean(val):
	clean = ""
	if val:
		clean = val.encode('utf-8')
	return clean

searchQuery = ''  #This is for your hasthag(s), separate by comma
maxTweets = 80000 # Large max nr
tweetsPerQry = 100  # the max the API permits
fName = 'myfile.csv' #The CSV file where your tweets will be stored
csvfile = open(fName, 'w');
csvwriter = csv.writer(csvfile)

count=0

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L
tweetCount = 0

#print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as csvfile:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
				#The detals you want to scrape. Add other/additional data by putting different references, see Twitter developers website;
					csvwriter.writerow([tweet.created_at,
					clean(tweet.user.screen_name),
					clean(tweet.text),
					tweet.user.created_at, #Might seem arbitrary, but good for idintifying bots
					tweet.user.followers_count,
					tweet.user.friends_count,
					tweet.user.statuses_count,
					clean(tweet.user.location), #The location set by the user themselves
					tweet.user.geo_enabled,
					tweet.user.lang,
					clean(tweet.user.time_zone),
					tweet.retweet_count
					]);

            tweetCount += len(new_tweets)
            #print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except Exception as e:
            # Just exit if any error
            print("some error : " + str(e))
            pass

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
