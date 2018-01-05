# Author: Ranjodh Singh

import requests
from bs4 import BeautifulSoup as bs
import os

url = "http://www.thehindu.com/archive/"
html = requests.get(url)
soup = bs(html.__dict__['_content'], "html5lib")
container = soup.select("#archiveTodayContainer")

for link in container[0].find_all("a"):
    resp = requests.get(link['href'])
    soup = bs(resp.__dict__['_content'], "html5lib")
    daily_links = soup.select("[class~=ui-state-default]")
    for l in daily_links:
        web_link = l['href']
        new_dir = "/".join(web_link.split("/")[-4:-1])
        os.makedirs(new_dir)
        s = bs(requests.get(web_link).__dict__['_content'], "html5lib")
        news_links = s.find_all('tr')[3].find_all('td')[-2].find_all("a")
        news_links = [i for i in news_links if "stories" in i['href']]
        print("Fetching news from ", web_link)
        for n in range(len(news_links)):
            news = bs(requests.get(web_link + news_links[n]['href']).__dict__['_content'], "html5lib")
            try:
                headline = news.find("h3").get_text()
            except:
                headline = ""
            with open(new_dir + "/" + str(n) + ".txt", "w") as f:
                f.write(headline)
                for x in news.find_all('p')[:-4]:
                    f.write(x.get_text())
