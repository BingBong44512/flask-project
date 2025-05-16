from bs4 import BeautifulSoup
import requests
import re

def createSoup(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	return soup

def glossary(url):
	soup=createSoup(url)
	txt = soup.find("tr")
	print(soup)


def text(url):
	soup=createSoup(url)

if __name__=="__main__":
	glossary("https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/zz%3A_Back_Matter/20%3A_Glossary")