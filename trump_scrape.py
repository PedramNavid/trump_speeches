import numpy as np
import pandas as pd
import requests
import bs4
import os

base_url = "http://www.presidency.ucsb.edu/"
speech_list = "http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=45&campaign=2016TRUMP&doctype=5000"
if not os.path.isdir('data'):
   os.mkdir('data')

# Grab page
res = requests.get(speech_list)
scrape = bs4.BeautifulSoup(res.text, 'lxml')

# Get list of speeches
elems = scrape.select('td.listdate a')
links = []

for e in elems:
    links.append((e.text, e.attrs['href']))

# Grab individual speeches
speeches = []
for idx, link in enumerate(links):
    print "Grabbing speech: ", idx + 1
    url = base_url + link[1][3:]
    res = requests.get(url)
    scrape = bs4.BeautifulSoup(res.text, 'lxml')
    speech = scrape.select('span.displaytext')[0].text.encode('utf-8')
    speeches.append(speech)
    with open(os.path.join("data", 
                           "speech_" + str(idx) + ".txt"), "w") as text_file:
        text_file.write(link[0])
        text_file.write('\n')
        text_file.write(speech)

# Create dataframe
d = {'title' : pd.Series([l[0] for l in links]),
     'link' : pd.Series([base_url + l[1][3:] for l in links]),
     'speech': pd.Series(speeches)}
df = pd.DataFrame(d)

with open(os.path.join("data", "full_speech.txt"), "w") as txt:
          for s in speeches:
            txt.write("%s\n" % s)
if __name__ == '__main__':
    df
