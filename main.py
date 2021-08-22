import urllib.parse
import urllib.request
import argparse
from bs4 import BeautifulSoup

DOMAIN_NAME = "https://manga1000.com/"
TITLE_PAGE_SUFFIX = "-raw-free/"
CHAPTER_PAGE_SUFFIX = "-raw/"
METADATA_FILE_NAME = "./info.txt"

def parseTitlePage(titleUrl):
  beginTitleIndex = len(DOMAIN_NAME)
  if (beginTitleIndex == -1):
    raise ValueError('Invalid URL cant find proper domain prefix')

  endTitleIndex = titleUrl.find(TITLE_PAGE_SUFFIX)
  if (endTitleIndex == -1):
    raise ValueError('Invalid URL cant find proper title page suffix')

  substr = titleUrl[beginTitleIndex:endTitleIndex]
  titleInJP = urllib.parse.unquote(substr)
  return titleInJP

def handleManage(url):
  # Todo: need to ensure we don't make duplicat entries for the same title here.

  titleInJP = parseTitlePage(url)

  localdb = open(METADATA_FILE_NAME,"a+")
  localdb.write("%s:1\n" % titleInJP) # default chapter of 1.
  localdb.close()
  return

def handleLog(url):
  return

def handleList():
  # read info.txt, and print each line.
  try:
    with open(METADATA_FILE_NAME) as f:
        lines = [line.rstrip() for line in f]
        print(lines)
  except FileNotFoundError:
    print("File {} not found!".format(METADATA_FILE_NAME))
  return

def fetchUrl(url):
  user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
  headers={'User-Agent':user_agent,} 

  request=urllib.request.Request(url,None,headers) #The assembled request
  response = urllib.request.urlopen(request)
  parseData(response.read())

def parseData(data):
  soup = BeautifulSoup(data)
  chapterTds = soup.find_all("td")
  for td in chapterTds:
    beginIndex = td.string.find("第")
    endIndex = td.string.find("話")

    print(td.string[beginIndex+1:endIndex])
    # print(td.find("Raw")

"""
Q: What should the user be able to do?

- user should be able to "manage" a title into this manager.
==== python3 main.py manage <mainTitleUrl>
- user should be able to log for a given title, up to where they've read.
==== python3 main.py log <chapterUrl>
- user should be able to see all titles they've managed & up to where they've read
==== python3 main.py list
- user should be able to request if, for all titles there are any new chapters
==== python3 main.py new
- user should be able to open a chrome window from terminal to the main title page.
==== python3 main.py open <indexOfTitleReturnedBy list>
"""
def main():
  parser = argparse.ArgumentParser(description='Manga Manager')
  parser.add_argument('--manage', help='manage a given url')
  parser.add_argument('--log', help='log up to where youve read')
  parser.add_argument('--list', dest='list', action='store_const', const=True, default=False, help='list all titles')

  args = parser.parse_args()
  print(args)

  argCount = 0
  if args.manage != None: argCount += 1
  if args.log != None: argCount += 1
  if args.list: argCount += 1
  if argCount > 1:
    print("Cant have more than 1 param enabled. Returning")
    return

  if args.manage != None:
    handleManage(args.manage)
  # if args.log != None:
  #   handleLog(args.log) 
  if args.list:
    handleList()

main()