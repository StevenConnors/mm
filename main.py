#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

url2 = "https://manga1000.com/%e4%b9%9d%e6%9d%a1%e3%81%ae%e5%a4%a7%e7%bd%aa-raw-free/"

headers={'User-Agent':user_agent,} 

request=urllib.request.Request(url2,None,headers) #The assembled request
response = urllib.request.urlopen(request)
data = response.read() # The data u need

print(data)

from bs4 import BeautifulSoup
soup = BeautifulSoup(data)
print(soup.prettify())

tds = soup.find_all("td")
for td in tds:
  # print(td.prettify())
  # print(type(td))
  # print(type(td.string))
  # print(td.string.find("第"))
  # print(td.string.find("】"))

  beginIndex = td.string.find("第")
  endIndex = td.string.find("話")

  print(td.string[beginIndex+1:endIndex])



  # print(td.find("Raw"))
  