import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

from texttable import Texttable
t = Texttable()

#Connection  with base URL
url = 'https://summerofcode.withgoogle.com/archive/2018/organizations/'
http = urllib3.PoolManager()
response = http.request('GET',url)
if(response.status != 200):
    print('Base URL Request Failed')
    quit()
baseSoup = BeautifulSoup(response.data,'html.parser')
listOfAllBaseLink =  baseSoup.find_all('a',{'class':'organization-card__link'})
myNewLinkList = []

# myNewLinkList will contain all organsitaions specific link
for a in listOfAllBaseLink:
    myNewLinkList.append(a['href'])

t.add_row(['Organisations','Technologies'])
print('Collecting data from website, it may take few minutes')
#Loop to execute over all organisations
#len(myNewLinkList)
for i in range(0,len(myNewLinkList)):
    article = http.request('GET',url + myNewLinkList[i][28:])
    if(article.status !=200):
        print('Article Request Failed')
        quit()
    article = article.data
    soupInside = BeautifulSoup(article,'html.parser')

    temp = soupInside.find_all('li',{'class':'organization__tag--technology'})
    techTag = [];
    for tag in temp:
        techTag.append(tag.string)
    title = soupInside.find('h3',{'class':'banner__title'})
    title = title.string
    techTag = ' ,'.join(techTag)
    t.add_row([title,techTag])

#loop ends here
print(t.draw())
