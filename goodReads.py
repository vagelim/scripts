import requests

API_KEY = 'YOUR API KEY HERE'

url = 'https://www.goodreads.com/review/list.html'
r = []
UserID = 14583385
#As seen on your profile page URL
#TODO: Automatically populate UserID using auth.user from GoodReads API 
#https://www.goodreads.com/api/index#auth.user


for x in range (1,5):
    params = {'v' : 2, 'id' : UserID , 'key' : API_KEY, 'shelf' : 'to-read', 'page' : x}
    r.append(requests.get(url, params).text)
#In the case of the test account, the number of books was > 80, so 4 pages would suffice at 20 books per page



import xml.etree.ElementTree as ET


for x in range(0, len(r)):
    r[x] = r[x].encode('ascii', 'ignore')



titles = []


pages = []


for x in range(0, len(r)):
    root = ET.fromstring(r[x])
    for child in root.find('reviews'):
        for book in child.find('book'):
            #print book.tag, book.text
            if book.tag == 'title':
                try:
                    titles.append(book.text)
                except TypeError:
                    pass
                
            elif book.tag == 'num_pages':
                try:
                    pages.append(int(book.text))    
                except TypeError:
                    pages.append(-1)



pages, titles = (list(t) for t in zip(*sorted(zip(pages, titles))))

for x in range (0, len(titles)):
    if pages[x] == -1: #Book page info not found
        pages[x] = 'No info available'
    try:
        print titles[x] + ': ' + str(pages[x])
    except TypeError: #Some books do not have page numbers available on Goodreads
        #TODO: Add alternative search for number of pages
        if titles[x] == None:
            titles[x] = 'Not a book' #If this happens you broke something
    
        print titles[x] + ': ' + str(pages[x])


