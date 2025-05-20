from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import json

def getHTML(url):
	wd = webdriver.Firefox()
	wd.get(url)
	html = wd.page_source
	soup = BeautifulSoup(html, "html.parser")
	wd.close()
	return soup

def glossary(url):
	soup = getHTML(url)
	rawText = soup.find_all("p",{"class":"glossaryElement"})
	cleanText = {}
	for texts in rawText:
		texts = texts.text.split(" | ")
		cleanText[texts[0]]=texts[1]
	# print(re.search('<p class="glossaryElement"><span class="glossaryTerm">(.+)</span>',rawText[0]))
		# text = text.split(" | ")
		# cleanText.append({text[0],text[1]})
	return cleanText



def main():
	diction = (glossary("https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/zz%3A_Back_Matter/20%3A_Glossary"))
	with open("dict.json", "w") as saving:
		json.dump(diction, saving, indent = 4)
	return 0

if __name__=="__main__":
	main()