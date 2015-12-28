from HTMLParser import HTMLParser
import requests

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def main():
    url = "http://mybusnow.njtransit.com/bustime/wireless/html/eta.jsp?route=166&id=26229&showAllBusses=off"

    req = requests.get(url)
    req = strip_tags(req.text)
    req = req.replace("\r\n", "")
    req = req.replace("\t\t\t\t", " ")

    start = req.find("To 166T")
    end = start + req[start:].find("MIN") + 3
    output = req[start:end].replace("\t\t\t",  ' ')
    if output == '':
        print "No bus!"
    else:
        print output

if __name__ == "__main__":
    main()
