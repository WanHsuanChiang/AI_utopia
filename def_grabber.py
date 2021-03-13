from bs4 import BeautifulSoup
import requests
from IPython.display import Markdown, display
from pathlib import Path

def find_closest_wiki(term):
    wiki_base = 'https://en.wikipedia.org/'

    term_with_plus = term.replace(" ", "+")
    url = f"https://en.wikipedia.org/w/index.php?search={term_with_plus}"

    r = requests.get(url)

    if r.url.split("/")[-1].lower().replace("_", " ") == term.lower():
        return r.url

    html_content = r.text

    soup = BeautifulSoup(html_content)

    return wiki_base + soup.find('a', {"data-serp-pos": "0"})['href']

def find_wiki_def(term):
    url = find_closest_wiki(term)

    r = requests.get(url)
    html_content = r.text

    soup = BeautifulSoup(html_content, features="html.parser")

    definition = soup.find('p', {"class": ""}).text.split(".")[0] + "."
    closest = url
    p = Path(closest)
    if p.name == term or (p.name).lower() == term.lower():
        defWiki = f"Well what I understand is that: {definition}"
    else:
        defWiki = f"Did you know that {term} which is kind of same as {p.name}: {definition}"
    return defWiki
