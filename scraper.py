from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

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
	cleanText = []
	for text in rawText:
		text = text.split(" | ")
		clean = {text[0],text[1]}
		cleanText.append()
	return cleanText



def main():
	print(glossary("https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/zz%3A_Back_Matter/20%3A_Glossary"))
	return 0

if __name__=="__main__":
	main()