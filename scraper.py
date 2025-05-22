from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import json

wd = webdriver.Firefox()

def getHTML(url):
	wd.get(url)
	html = wd.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup

def glossary(url,subject):
	soup = getHTML(url)
	rawText = soup.find_all("p",{"class":"glossaryElement"})
	cleanText = {}
	for texts in rawText:
		texts = texts.text.split(" | ")
		cleanText[texts[0]]=texts[1]
	return cleanText
	

def getLinks(url):
	soup = getHTML(url)
	raw = soup.find_all("a", {"class":"mt-sortable-listing-link mt-edit-section internal"})
	links = []
	glossaryLink = ""
	for link in raw:
		link = link["href"]
		if  ("Front Matter" not in link) and  ("Back Matter" not in link) and  ("Appendices" not in link):
			links.append(link)
	return links
	




def getData(url, subject):
	diction = glossary(url+"/zz%3A_Back_Matter/20%3A_Glossary",subject)
	with open((subject+"dict.json"), "w") as saving:
		json.dump(diction, saving, indent = 4)

	# getLinks(url)


def main():
	# subject = input("Subject?: ")
	# url = input("Url?: ")

	print(getLinks("https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)"))

	wd.close()
	return 0

if __name__=="__main__":
	main()