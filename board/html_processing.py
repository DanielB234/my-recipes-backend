from html.parser import HTMLParser
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from os.path import basename, normpath


def get_html(url):
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    page = urlopen(req)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def get_soup(html):
    return BeautifulSoup(html, "html.parser")
     
def get_path_base(url):
    url_no_params = url.split('?')[0]
    return basename(normpath(url_no_params))

def get_clean_text(html_element):
    element_text = html_element.get_text()
    newline_stripped_element  = element_text.replace("\n","")
    stripped_element = ' '.join(newline_stripped_element.split())
    return stripped_element

def get_lists(html,ordering):
    soup = get_soup(html)
    soups = soup.find_all(ordering)
    ordered_lists = []
    for ordered_list in soups:
        elements = []
        list_elements = ordered_list.find_all("li")
        for element in list_elements:
            elements.append(get_clean_text(element))   
        ordered_lists.append(elements)
    return ordered_lists


class MyHTMLParser(HTMLParser):
     def __init__(self, *args, **kwargs):
         self.data = []
         super(MyHTMLParser, self).__init__(*args, **kwargs)
     def handle_data(self, data):
         data = data.strip()
         if data:
             self.data.append(data)

def get_header(parser,list_opener):
    temp = ""
    for x in parser.data:
        if x == list_opener:
            return temp
        temp = x
    return ""