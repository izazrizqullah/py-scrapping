# #!/usr/bin/env python
# # coding:utf-8

# from importlib import reload
# import re
# import json
# import urllib
# import requests
# from self import self # type: ignore
# from freexici import freexici # type: ignore
# from autouseragents.autouseragents import AutoUserAgents # type: ignore
# from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


# class Alibabaa(object):
#     """
# This is a very simple python script to fetch API like search results data from https://s.1688.com.
# Can be really helpful if you just need some easy to use yet reliable interface level tool.
# You can use this tool under MIT license.
# Legal authority may be needed if you're going to use it in production environment.
#     """

#     def __init__(self, keywords=None, page=1, mode="view"):
#         self.KEYWORDS = []  # init KEYWORDS in constructor
#         if keywords:  # parse and add keywords
#             if isinstance(keywords, str):
#                 self.addKeyword(keywords, page)
#             elif isinstance(keywords, list):
#                 self.addKeywords(keywords, page)
#         self.PAGE = page  # init PAGE in constructor
#         #  target url to request data
#         self.URL = "https://s.1688.com/selloffer/rpc_async_render.jsonp?keywords={keyword}&button_click=top&n=y&uniqfield=pic_tag_id&templateConfigName=marketOfferresult&beginPage={page}&offset=9&pageSize=60&asyncCount=60&startIndex=0&async=true&enableAsync=true&rpcflag=new&_pageName_=market"
#         self.MUA = AutoUserAgents()  # init random agent object for convenient use afterwards
#         self.HEADERS = {  # init HEADERS param in constructor, useragent will be later set to a random one
#             "referer": "https://s.1688.com/",
#             "user-agent": "",
#             "x-requested-with": "XMLHttpRequest"
#         }
#         # init MODES pool param in constructor
#         self.MODES = ["view", "save", "api"]
#         if mode:
#             self.setMode(mode)
#         else:
#             self.setMode("view")
#         self.RESULTS = {}  # results to return
#         self.DATAFILE = r"data.txt"  # file name if set mode to save

#     # manually set up self.MODE param
#     @self
#     def setMode(self, mode):
#         if mode and isinstance(mode, str) and len(mode) > 0:
#             if mode in self.MODES:
#                 self.MODE = mode
#             else:
#                 raise NameError(
#                     "MODE param can only be view(default), save or api")
#         else:
#             raise TypeError("MODE param must be non-empty string")

#     # manually set up self.PAGE param
#     @self
#     def setPage(self, page):
#         if page and isinstance(page, int) and page > 0:
#             self.PAGE = page
#         else:
#             raise TypeError("PAGE param must be positive int")

#     # manually set up self.KEYWORDS param
#     @self
#     def addKeyword(self, keyword="", page=1):
#         if keyword:
#             if keyword not in self.KEYWORDS:
#                 self.KEYWORDS.append(keyword)
#         else:
#             raise KeyError("Keyword must be a string!")

#     # manually set up self.KEYWORDS in batch
#     @self
#     def addKeywords(self, keywords=[], page=1):
#         if keywords:
#             for keyword in keywords:
#                 self.addKeyword(keyword, page)
#         else:
#             raise KeyError("Keywords must be a non-empty list of strings!")

#     # method to extract useful data from every item of the returned results
#     def extract(self, item):
#         data = {}
#         mainBlock = item.find("div", class_="imgofferresult-mainBlock")
#         if mainBlock:
#             second = mainBlock.find(
#                 "div", class_=re.compile(r".*sm-offer-price.*"))
#             if second:
#                 tag = second.find("span", class_=re.compile(
#                     r".*sm-offer-priceNum.*"))
#                 if tag:
#                     priceStr = tag.getText().strip()
#                     priceList = re.findall(r"\d*\.\d*", priceStr)
#                     price = float(priceList[0])
#                     data["price"] = price if r"万" not in priceStr else price * 10000
#                 else:
#                     data["price"] = -1

#             third = mainBlock.find(
#                 "div", class_=re.compile(r".*sm-offer-title.*"))
#             if third:
#                 tag = third.find("a", attrs={"offer-stat": "title"})
#                 data["item"] = "" if not tag else tag[
#                     "title"].strip().encode("utf8")

#             fourth = mainBlock.find(
#                 "div", class_=re.compile(r".*sm-offer-company.*"))
#             if fourth:
#                 tag = fourth.find("a", attrs={"offer-stat": "com"})
#                 data["company"] = "unknown" if not tag else tag.getText(
#                 ).strip().encode("utf8")

#             fifth = mainBlock.find(
#                 "div", class_=re.compile(r".*sm-offer-sub.*"))
#             if fifth:
#                 tag = fifth.find("div", class_=re.compile(r".*location.*"))
#                 data["location"] = "unknown" if not tag else tag.getText(
#                 ).strip().encode("utf8")
#             return data
#         return None

#     def getResponse(self, url, headers, proxy=False, timeout=8):
#         if proxy:
#             proxies = freexici.randomProxy()
#             for p in proxies:
#                 proxies = p
#         else:
#             proxies = None
#         while True:
#             response = requests.get(
#                 url, headers=headers, proxies=proxies, timeout=timeout)
#             if response.status_code == 200:
#                 return response
#             else:
#                 return self.getResponse(url, headers, True)

#     def alimama(self, mode=None):
#         if not mode:
#             mode = self.MODE
#         else:
#             self.setMode(mode)
#         for keyword in self.KEYWORDS:
#             self.RESULTS[self.KEYWORDS.index(keyword)] = []
#             key = urllib.quote(keyword.decode("utf-8").encode("gbk"))
#             for i in range(self.PAGE):
#                 pdata = []
#                 url = self.URL.format(keyword=key, page=i + 1)
#                 self.HEADERS["user-agent"] = self.MUA.random_agent()
#                 response = self.getResponse(url, self.HEADERS)
#                 html = response.content.decode("gbk")
#                 # this is vital in this tool
#                 # some stupid way to mine out the data you want from a vast
#                 # ocean of formated yet not easy to deal with content
#                 m = re.search(r"\<li.*\>", html).group(0)
#                 m = re.sub(r"\\n", "", m)
#                 m = re.sub(r"\\r", "", m)
#                 m = re.sub(r"\\", "", m)
#                 p = re.sub(r"\<!--.*?--\>", "", m)
#                 # parse the formated data
#                 soup = BeautifulSoup(p, "lxml")
#                 items = soup.findAll(
#                     "li", class_="sm-offer-item sw-dpl-offer-item ")
#                 for item in items:
#                     data = self.extract(item)
#                     if data:
#                         pdata.append(data)
#                 if pdata:
#                     self.RESULTS[self.KEYWORDS.index(keyword)] = pdata
#                 if mode == "view":  # show data if mode is view
#                     for data in pdata:
#                         for k, v in data.items():
#                             print (k, v)
#         if mode == "save":  # save file if mode is save
#             with open(self.DATAFILE, "w") as f:
#                 try:
#                     f.write(json.dumps(self.RESULTS))
#                     return True
#                 except Exception as e:
#                     raise RuntimeError(
#                         "Unable to save scraped data to file {}".format(self.DATAFILE))
#         if mode == "api":  # return data if mode is api
#             return self.RESULTS


# if __name__ == '__main__':
#     print (Alibabaa().addKeyword("自行车").addKeywords(["拖把", "牙刷"]).setPage(10).setMode("view").alimama())


#!/usr/bin/env python
# coding:utf-8

#!/usr/bin/env python
# coding:utf-8

import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
import random

# List of user agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    # Add more user agents as needed
]

class Alibabaa(object):
    """
    This is a very simple python script to fetch API-like search results data from https://s.1688.com.
    Can be really helpful if you just need some easy-to-use yet reliable interface-level tool.
    You can use this tool under MIT license.
    Legal authority may be needed if you're going to use it in a production environment.
    """

    def __init__(self, keywords=None, page=1, mode="view"):
        self.KEYWORDS = []  # init KEYWORDS in constructor
        if keywords:  # parse and add keywords
            if isinstance(keywords, str):
                self.addKeyword(keywords, page)
            elif isinstance(keywords, list):
                self.addKeywords(keywords, page)
        self.PAGE = page  # init PAGE in constructor
        # target url to request data
        self.URL = "https://s.1688.com/selloffer/rpc_async_render.jsonp?keywords={keyword}&button_click=top&n=y&uniqfield=pic_tag_id&templateConfigName=marketOfferresult&beginPage={page}&offset=9&pageSize=60&asyncCount=60&startIndex=0&async=true&enableAsync=true&rpcflag=new&_pageName_=market"
        self.HEADERS = {  # init HEADERS param in constructor
            "referer": "https://s.1688.com/",
            "user-agent": random.choice(USER_AGENTS),
            "x-requested-with": "XMLHttpRequest"
        }
        # init MODES pool param in constructor
        self.MODES = ["view", "save", "api"]
        self.setMode(mode)
        self.RESULTS = {}  # results to return
        self.DATAFILE = r"data.txt"  # file name if set mode to save

    def setMode(self, mode):
        if mode and isinstance(mode, str) and len(mode) > 0:
            if mode in self.MODES:
                self.MODE = mode
            else:
                raise NameError("MODE param can only be view(default), save or api")
        else:
            raise TypeError("MODE param must be non-empty string")
        return self  # Return self for method chaining

    def setPage(self, page):
        if page and isinstance(page, int) and page > 0:
            self.PAGE = page
        else:
            raise TypeError("PAGE param must be positive int")
        return self  # Return self for method chaining

    def addKeyword(self, keyword="", page=1):
        if keyword:
            if keyword not in self.KEYWORDS:
                self.KEYWORDS.append(keyword)
        else:
            raise KeyError("Keyword must be a string!")
        return self  # Return self for method chaining

    def addKeywords(self, keywords=[], page=1):
        if keywords:
            for keyword in keywords:
                self.addKeyword(keyword, page)
        else:
            raise KeyError("Keywords must be a non-empty list of strings!")
        return self  # Return self for method chaining

    def extract(self, item):
        data = {}
        mainBlock = item.find("div", class_="imgofferresult-mainBlock")
        if mainBlock:
            second = mainBlock.find("div", class_=re.compile(r".*sm-offer-price.*"))
            if second:
                tag = second.find("span", class_=re.compile(r".*sm-offer-priceNum.*"))
                if tag:
                    priceStr = tag.getText().strip()
                    priceList = re.findall(r"\d*\.\d*", priceStr)
                    price = float(priceList[0])
                    data["price"] = price if r"万" not in priceStr else price * 10000
                else:
                    data["price"] = -1

            third = mainBlock.find("div", class_=re.compile(r".*sm-offer-title.*"))
            if third:
                tag = third.find("a", attrs={"offer-stat": "title"})
                data["item"] = "" if not tag else tag["title"].strip()

            fourth = mainBlock.find("div", class_=re.compile(r".*sm-offer-company.*"))
            if fourth:
                tag = fourth.find("a", attrs={"offer-stat": "com"})
                data["company"] = "unknown" if not tag else tag.getText().strip()

            fifth = mainBlock.find("div", class_=re.compile(r".*sm-offer-sub.*"))
            if fifth:
                tag = fifth.find("div", class_=re.compile(r".*location.*"))
                data["location"] = "unknown" if not tag else tag.getText().strip()
            return data
        return None

    def getResponse(self, url, headers, timeout=8):
        while True:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
            else:
                print(f"Error: {response.status_code}. Retrying...")

    def alimama(self, mode=None):
        if not mode:
            mode = self.MODE
        else:
            self.setMode(mode)
        for keyword in self.KEYWORDS:
            self.RESULTS[self.KEYWORDS.index(keyword)] = []
            key = urllib.parse.quote(keyword)
            for i in range(self.PAGE):
                pdata = []
                url = self.URL.format(keyword=key, page=i + 1)
                self.HEADERS["user-agent"] = random.choice(USER_AGENTS)
                response = self.getResponse(url, self.HEADERS)
                html = response.content.decode("utf-8", errors='ignore')  # Use utf-8 with error handling
                
                # Check if the expected content is present
                match = re.search(r"\<li.*\>", html)
                if match:
                    m = match.group(0)
                    m = re.sub(r"\\n", "", m)
                    m = re.sub(r"\\r", "", m)
                    m = re.sub(r"\\", "", m)
                    p = re.sub(r"\<!--.*?--\>", "", m)
                    soup = BeautifulSoup(p, "lxml")
                    items = soup.findAll("li", class_="sm-offer-item sw-dpl-offer-item ")
                    for item in items:
                        data = self.extract(item)
                        if data:
                            pdata.append(data)
                    if pdata:
                        self.RESULTS[self.KEYWORDS.index(keyword)] = pdata
                    if mode == "view":  # show data if mode is view
                        for data in pdata:
                            for k, v in data.items():
                                print(k, v)
                else:
                    print(f"No matching items found for keyword: {keyword} on page {i + 1}.")
        if mode == "save":  # save file if mode is save
            with open(self.DATAFILE, "w") as f:
                try:
                    f.write(json.dumps(self.RESULTS))
                    return True
                except Exception as e:
                    raise RuntimeError("Unable to save scraped data to file {}".format(self.DATAFILE))
        if mode == "api":  # return data if mode is api
            return self.RESULTS


if __name__ == '__main__':
    print(Alibabaa().addKeyword("鞋子").addKeywords(["饮料瓶", "充电器"]).setPage(10).setMode("view").alimama())
