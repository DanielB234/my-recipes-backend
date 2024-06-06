from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv

req = Request(
    url = "https://www.recipetineats.com/chocolate-cake/",
    headers={'User-Agent': 'Mozilla/5.0'}
)

page = urlopen(req)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

soups = soup.find_all("ul")
# soups = soup.find_all("ol")
ordered_lists = []
csvreader = csv.writer
training_data = []
for ordered_list in soups:
    elements = []
    list_elements = ordered_list.find_all("li")
    for element in list_elements:
        element_text = element.get_text()
        newline_stripped_element  = element_text.replace("\n","")
        stripped_element = ' '.join(newline_stripped_element.split())
        normalized_element = stripped_element.encode('ascii','ignore').decode()
        elements.append(normalized_element)
    ordered_lists.append(elements)
    print(elements)
    is_instructions = input()
    for element in elements:
        training_data.append([element,is_instructions])
print(training_data)
    

with open('instructions-training/instructions_training.csv', 'a', newline="") as file:
    writer = csv.writer(file)
    writer.writerows(training_data)
