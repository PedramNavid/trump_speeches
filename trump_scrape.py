from lxml import html
import requests
page = requests.get("http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=45&campaign=2016TRUMP&doctype=5000")
tree = html.fromstring(page.content)
