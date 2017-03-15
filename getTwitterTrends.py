import tweepy


def setOAuthConnection():
    # credentials are confidential and should not be shared in the
    # public repository
    f = open('credentials.txt', 'r')
    content = f.readlines()
    consumer_token = content[0].strip()
    consumer_secret = content[1].strip()
    access_token = content[2].strip()
    access_secret = content[3].strip()

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    # if authentication was successful, account name will be printed
    print(api.me().name)

    return api


def getTrends(api):  # consider adding location as parameter
    return api.trends_place(1)  # 1 for worldwide


def main():
    api = setOAuthConnection()
    print(getTrends(api))

if __name__ == "__main__":
    main()
