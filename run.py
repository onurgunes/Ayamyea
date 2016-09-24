from bs4 import BeautifulSoup
import urllib.request
import Ad
import os
import webbrowser


def generate_url(city, towns, max_price, a20, page_offset):
    link = 'https://www.sahibinden.com/kiralik-daire?'
    link += "&pagingOffset=" + str(page_offset)
    link += "&pagingSize=50"
    for town in towns:
        link += "&address_town=" + town
    for a in a20:
        link += "&a20=" + a
    link += "&price_max=" + max_price
    link += "&address_city=" + city
    return link


def get_urls(link):
    urls = []
    request = urllib.request.Request(link)
    request.add_header('User-Agent', "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")

    response = urllib.request.urlopen(request)

    content = BeautifulSoup(response.read(), 'html.parser')
    response.close()

    titles = content.findAll("a", {"class": "classifiedTitle"})

    for title in titles:
        urls.append("http://www.sahibinden.com" + title["href"])

    is_last_page = False if len(content.findAll("a", {"class": "prevNextBut"})) > 1 else True

    return urls, is_last_page


def parse(content, url):
    flat = Ad.Ad()

    flat.url = url
    flat.title = content.find("div", {"class": "classifiedDetailTitle"}).findAll("h1")[0].text.strip().replace("\"", "").replace("'", "")
    flat.latitude = content.find("div", {"id": "gmap"})['data-lat']
    flat.longitude = content.find("div", {"id": "gmap"})['data-lon']
    flat.price = content.find("div", {"class": "classifiedInfo"}).findAll("h3")[0].text.strip()
    flat.town = content.find("div", {"class": "classifiedInfo"}).findAll("h2")[0].findAll("a")[1].text.strip()
    flat.district = content.find("div", {"class": "classifiedInfo"}).findAll("h2")[0].findAll("a")[2].text.strip()

    detailedInfo = content.find("ul", {"class": "classifiedInfoList"}).findAll("li")

    flat.id = detailedInfo[0].findAll("span")[0].text.strip()  # ilan numarası
    flat.flatSize = detailedInfo[3].findAll("span")[0].text.strip()  # m2
    flat.roomCount = detailedInfo[4].findAll("span")[0].text.strip()
    flat.floor = detailedInfo[6].findAll("span")[0].text.strip()  # 4. kat
    flat.heating = detailedInfo[8].findAll("span")[0].text.strip()
    flat.isFull = detailedInfo[10].findAll("span")[0].text.strip()  # Eşyalı
    flat.subscription = detailedInfo[13].findAll("span")[0].text.strip()  # aidat

    print(flat.to_json())
    return flat


def write_json(flats):
    data = ""
    for idx, flat in enumerate(flats):
        if idx != 0:
            data += ","
        data += flat

    data = "_data = \'[" + data
    data += "]\';"

    with open("data.json", "w") as file:
    	file.write(data)


def open_the_map():
    path = "file://" + os.path.abspath('map.html')
    webbrowser.open(path)


flats = []
urls = []

city = "6" # İl ; "6": Ankara
towns = ["64"] # İlçeler ; "59": Çankaya, "61": Keçiören, "64": Yenimahalle
max_price = "1000"
a20 = ["38473"]  # Oda sayısı ;  1+1: 38473, 2+1: 38470, 3+1: 38474
page_offset = 0
is_last_page = False

while not is_last_page:
    link = generate_url(city, towns, max_price, a20, page_offset)
    new_urls, is_last_page = get_urls(link)
    print(link)
    urls += new_urls
    page_offset += 50

for url in urls:
    try:
        request = urllib.request.Request(url)
        request.add_header('User-Agent', "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")

        response = urllib.request.urlopen(request)

        soup = BeautifulSoup(response.read(), 'html.parser')
        response.close()

        flat = parse(soup, url)

        flats.append(flat.to_json())

    except Exception as e:
        print(str(e))

write_json(flats)
open_the_map()