from bs4 import BeautifulSoup
import requests 
import csv
import re

url = 'https://bolshayastrana.com/tury?utm_source=eLama-yandex&utm_medium=cpc&utm_campaign=Туры%20по%20России%20Регионы&utm_term=Походы%20по%20России&utm_content=cid%7C41397366%7Cgid%7C3763717881%7Caid%7C11180721978%7Cadp%7Cno%7Cdvc%7Cdesktop%7Cpid%7C16470247203%7Crid%7C%7Cdid%7C16470247203%7Cpos%7Cother1%7Cadn%7Csearch%7Ccrid%7C0%7C&roistat=direct3_search_11180721978_Походы%20по%20России&roistat_referrer=none&roistat_pos=other_1&yclid=6508863601408737279'
req = requests.get(url)
src = req.text
soup = BeautifulSoup(src, 'lxml')

with open('kod.html', 'w', encoding='utf-8') as file:
	file.write(src)
	
price = soup.find_all(itemprop="price")
for item in price:
	pr = item.text

location = soup.find_all(class_="tour-preview__location")
for item in location:
	locat = item.text.strip()

	
time_turs = soup.find_all(class_="tour-preview__details-value")
time_turs = str(time_turs)
q = re.findall(r'>.*?<', time_turs)
t = []
for item in q:
	if item[-2] == '.':
		t.append(item.replace('<', '').replace('>', ''))

a = soup.find_all(itemprop="url")

for item in a:
		item = str(item)
		i = re.findall(r'".*?"', item)
		i.pop()
		

with open('resultat.csv', 'w+', encoding='utf-8') as file:
	names = ['Location', 'Price', 'Data', 'Url']
	w = csv.DictWriter(file, delimiter = ",", lineterminator="\r", fieldnames=names)
	w.writeheader()
	for item in location:
		locat = item.text.strip()
		for item in price:
			pr = item.text
			for item in t:
				data = item
				for a in i:
					url_pages = 'https://bolshayastrana.com' + a.replace('"', '')
					w.writerow({"Location": locat, "Price": pr, "Data": data, "Url": url_pages})
