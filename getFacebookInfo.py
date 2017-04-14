import facebook
import sys
import json
import requests
import urllib


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


def initGraph():
  f = open('fbToken.txt', 'r')
  content = f.readlines()
  accessToken = content[0].strip()
  return facebook.GraphAPI(access_token=accessToken, version='2.7')


def getPostId(graph, newspage, link):
  allPosts = graph.get_object(id=newspage, fields='posts', limit=100)
  allPostIds = [p['id'] for p in allPosts['posts']['data']]
  links = graph.get_objects(ids=allPostIds, fields='link')
  # compare url hierarchic paths of given link and post link
  postIds = [pId for pId in allPostIds
             if getUrlPath(unshortenUrl(links[pId]['link']), 0) ==
             getUrlPath(link, 1)]
  print(postIds)
  if postIds != []:
    return postIds[0]
  return None


def getUrlPath(url, flag):
  path = urllib.parse.urlparse(url)[2]
  if(flag == 0):
    print(path)
  return path


def unshortenUrl(url):
  return requests.head(url, allow_redirects=True).url


def getReactions(graph, newspage, link):
    link = unshortenUrl(link)
    postId = getPostId(graph, newspage, link)
    if postId is None:
      print("No facebook post about this article has been found.")
      return None
    reactions = graph.get_object(id=postId,
                                 fields='''reactions.type(LIKE).summary(true).as(like),
                                         reactions.type(WOW).summary(true).as(wow),
                                         reactions.type(LOVE).summary(true).as(love),
                                         reactions.type(HAHA).summary(true).as(haha),
                                         reactions.type(ANGRY).summary(true).as(angry),
                                         reactions.type(SAD).summary(true).as(sad)''')
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
def main():
  graph = initGraph()
  newspage = sys.argv[1]
  articleLink = sys.argv[2]
  reactions = getReactions(graph, newspage, articleLink)
  if reactions is not None:
    print(reactions)


if __name__ == '__main__':
  main()
