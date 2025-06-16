from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
# creates a webdriver
wd = webdriver.Firefox()
# gets html as soup object
def getHTML(url):
	wd.get(url)
	time.sleep(3)
	html = wd.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup
# extracts glossary stuff into a dictionary
def glossary(url):
	soup = getHTML(url)
	rawText = soup.find_all("p",{"class":"glossaryElement"})
	cleanText = {}
	for texts in rawText:
		texts = texts.text.split(" | ")
		cleanText[texts[0]]=texts[1]
	return cleanText
	
# gets chapter link from the main page
def getLinks(url):
	soup = getHTML(url)
	raw = soup.find_all("a", {"class":"mt-sortable-listing-link mt-edit-section internal"})
	links = []
	glossaryLink = ""
	for link in raw:
		link = link["href"]
		if  ("Front_Matter" not in link) and  ("Back_Matter" not in link) and  ("Appendices" not in link) and ("Appendix" not in link):
			links.append(link)
	return links
# gets both the content in the chapters and the links to the lessons, adds it to a dictionary under the chapter
def getInfo(url):
	links = getLinks(url)
	data = {}
	for link in links:
		soup = getHTML(link)
		
		title = soup.find("h1",{"id":"title"}).text.replace("\n","").strip()
		data[title] = {}

		allInfo = soup.find_all("a", {"class":"internal"})
		for info in allInfo:
			if "Key Terms" not in info.text and "Key Equations" not in info.text and "Summary" not in info.text and "Exercises" not in info.text and "mt-self-link" not in info["class"]:
				content = info.parent.parent.find_all("dd")[0].text
				if content != "":
					data[title][info.text] ={"link":info["href"],"content":content}

	return data


# runs the function for the scraping and saves the data
def getData(url, subject):
	diction = glossary(url+"/zz%3A_Back_Matter/20%3A_Glossary")
	with open((subject+"dict.json"), "w") as saving:
		json.dump(diction, saving, indent = 4)

	diction = getInfo(url)
	with open((subject+"content.json"), "w") as saving:
		json.dump(diction, saving, indent = 4)

# asks for necessary info, gets the data, closes the webdriver
def main():
	subject = input("Subject?: ")
	url = input("Url?: ")

	getData(url,subject)
	
	wd.close()
	return 0

if __name__=="__main__":
	main()