import sys
import json
import requests
import urllib
import time
import datetime

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def getToken():
  f = open('fbToken.txt', 'r')
  content = f.readlines()
  accessToken = content[0].strip()
  return accessToken

def getPostId(apiToken, newspage, path, date):
  twoDays = 48 * 60 * 60
  allLinks = requests.get('https://graph.facebook.com'
                          '/v2.8/' + newspage +
                          '/posts?' +
                          'fields=link' +
                          '&format=json' +
                          '&access_token=' + apiToken +
                          '&limit=100' +
                          '&since=' + str(date - twoDays) +
                          '&until=' + str(date + twoDays)).json()
  pageCount = 0
  postId = None
  while postId is None and allLinks != [] and pageCount < 15:
    pageCount += 1
    print("Page: " + str(pageCount) + "\n")
    index = 0
    # compare url hierarchic paths of given link and post link
    while index < len(allLinks['data']) and getUrlPath(
          unshortenUrl(allLinks['data'][index]['link']), 0) != path:
      index += 1
    if index < len(allLinks['data']):
      postId = allLinks['data'][index]['id']
    else:
      if 'paging' in allLinks:
        allLinks = requests.get(allLinks['paging']['next']).json()
      else:
         allLinks = []
  return postId

def getUrlPath(url, flag):
  path = urllib.parse.urlparse(url)[2]
  if(flag == 0):
    print(path)
  return path

def unshortenUrl(url):
  try:
    return requests.head(url, allow_redirects=True).url
  except:
    return url

def getReactions(apiToken, newspage, link, date):
    path = getUrlPath(unshortenUrl(link), 1)
    postId = getPostId(apiToken, newspage, path, date)
    if postId is None:
      print("No facebook post about this article has been found.")
      return None
    reactions = requests.get('https://graph.facebook.com'
                             '/v2.8/' +
                             str(postId) +
                             '''?fields=reactions.type(LIKE).summary(true).as(like),
                                       reactions.type(WOW).summary(true).as(wow),
                                       reactions.type(LOVE).summary(true).as(love),
                                       reactions.type(HAHA).summary(true).as(haha),
                                       reactions.type(ANGRY).summary(true).as(angry),
                                       reactions.type(SAD).summary(true).as(sad)''' +
                             '&format=json' +
                             '&access_token=' + apiToken).json()
    reactionSummary = {}
    reactionSummary['like'] = reactions['like']['summary']['total_count']
    reactionSummary['wow'] = reactions['wow']['summary']['total_count']
    reactionSummary['love'] = reactions['love']['summary']['total_count']
    reactionSummary['haha'] = reactions['haha']['summary']['total_count']
    reactionSummary['angry'] = reactions['angry']['summary']['total_count']
    reactionSummary['sad'] = reactions['sad']['summary']['total_count']
    # print(str(reactions).translate(non_bmp_map))
    return json.dumps(reactionSummary)

#  argv[1] - Name of Facebook news page (e. g. bbcnews)
#  argv[2] - Link to article
#  argv[3] - Date of article - yyyy-mm-dd
def main():
  accessToken = getToken()
  newspage = sys.argv[1]
  articleLink = sys.argv[2]
  date = time.mktime(datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d").timetuple())
  reactions = getReactions(accessToken, newspage, articleLink, date)
  if reactions is not None:
    print(reactions)

if __name__ == '__main__':
  main()
