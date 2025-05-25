from bs4 import BeautifulSoup
from selenium import webdriver
import json

wd = webdriver.Firefox()

def getHTML(url):
	wd.get(url)
	html = wd.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup

def glossary(url):
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
		if  ("Front_Matter" not in link) and  ("Back_Matter" not in link) and  ("Appendices" not in link):
			links.append(link)
	return links
	
	#open link
	# get all textboxes
	# get title + Link
	# get Text
	#  f name {text, link}
	
def getInfo(url):
	links = getLinks(url)
	data = {}
	for link in links:
		soup = getHTML(link)
		titleHTML = []
		contentHTML =[]
		
		title = soup.find("h1",{"id":"title"}).text.replace("\n","").strip()
		data[title] = {}

		allInfo = soup.find_all("a", {"class":"internal"})
		for info in allInfo:
			if "Key Terms" not in info.text and "Key Equations" not in info.text and "Summary" not in info.text and "Exercises" not in info.text and "mt-self-link" not in info["class"]:
				data[title][info.text] ={"link":info["href"],"content":info.parent.parent.find_all("dd")[0].text}

	return data



def getData(url, subject):
	diction = glossary(url+"/zz%3A_Back_Matter/20%3A_Glossary",subject)
	with open((subject+"dict.json"), "w") as saving:
		json.dump(diction, saving, indent = 4)

	diction = getInfo(url)
	with open((subject+"content.json"), "w") as saving:
		json.dump(diction, saving, indent = 4)


def main():
	subject = input("Subject?: ")
	url = input("Url?: ")

	getData(url,subject)
	
	wd.close()
	return 0

if __name__=="__main__":
	main()