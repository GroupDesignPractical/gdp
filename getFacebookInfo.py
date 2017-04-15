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
  return facebook.GraphAPI(access_token=accessToken)


def getPostId(graph, newspage, path, maxCount):
  allPosts = graph.get_object(id=newspage, fields='posts')['posts']
  maxPageCount = maxCount / 25
  if maxCount % 25 != 0:
    maxPageCount += 1
  pageCount = 0
  postId = None
  while postId is None and allPosts['data'] != [] and pageCount < maxPageCount:
    pageCount += 1
    allPostIds = [p['id'] for p in allPosts['data']]
    links = graph.get_objects(ids=allPostIds, fields='link')
    # compare url hierarchic paths of given link and post link
    postIds = [pId for pId in allPostIds
               if getUrlPath(unshortenUrl(links[pId]['link']), 0) ==
               path]
    print(postIds)
    if postIds != []:
      postId = postIds[0]
    else:
      allPosts = requests.get(allPosts['paging']['next']).json()
  return postId


def getUrlPath(url, flag):
  path = urllib.parse.urlparse(url)[2]
  if(flag == 0):
    print(path)
  return path


def unshortenUrl(url):
  return requests.head(url, allow_redirects=True).url


def getReactions(graph, newspage, link, maxCount):
    path = getUrlPath(unshortenUrl(link), 1)
    postId = getPostId(graph, newspage, path, maxCount)
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
#  argv[3] - (optional) number of posts to search through
#            (defaults to 25, i.e. one page)
def main():
  graph = initGraph()
  newspage = sys.argv[1]
  articleLink = sys.argv[2]
  if len(sys.argv) > 3:
    maxCount = int(sys.argv[3])
  else:
    maxCount = 25
  reactions = getReactions(graph, newspage, articleLink, maxCount)
  if reactions is not None:
    print(reactions)


if __name__ == '__main__':
  main()
