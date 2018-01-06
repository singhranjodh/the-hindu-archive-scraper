import requests
from bs4 import BeautifulSoup as bs

with open('links.txt', 'r') as f:
    content = f.readlines()

for c in range(len(content)):
    try:
        html = requests.get(content[c][:-1])
        soup = bs(html.__dict__['_content'], "html5lib")
        article = soup.select("[class~=article]")
        title = article[0].select("[class~=title]")
        title = title[0].get_text()
        body = article[0].select("[id*='content-body-']")
        with open(str(c) + ".txt", 'w') as f:
            f.write(title)
            f.write("\n")
            for p in body[0].find_all("p"):
                f.write(p.get_text())
            f.write("\n")
    except:
        print("No article in ", str(content[c][:-1]))