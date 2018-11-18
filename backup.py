import requests
import re
from bs4 import BeautifulSoup

def getLink():
    linkArray = []
    # dari https://news.detik.com/indeks/all/20?date=11/15/2018 diketahui terdapat 20 halaman index
    for x in range(1,21):
        print('collecting link in page : '+str(x))
        r = requests.get('https://news.detik.com/indeks/all/'+str(x)+'?date=11/15/2018')
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('article')
        for x in results:
         regex = r"href=\"(https.*)\""
         match = re.search(regex, str(x))
         # print("Match at index %s, %s" % (match.start(), match.end()))
         linkArray.append(match.group(1))
    # print(len(results))
    # print(results[0])
    # print(linkArray)
    # for x in linkArray:
    #     print(x)
    #
    print(str(len(linkArray))+' link collected')
    return linkArray

def getWords(url):
    meaninglessWords = ['href','https','http','www','com','search','searchall','query','target','blank','br','strong','table','class','linksisip','tbody','tr','td','div','class','lihatjg','Baca','juga','data-action','data-category','Detil','Artikel','data-label','List','Berita','news','detik','com','read','ke','di','Rp','Pilihan','em','single','identity']
    wordsCollected =[]
    # link diambil dari kumpulan index detikcom
    r = requests.get(url)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    # dari metode inspect element, didapat berita selalu ada didalam tag <div class="detail_text" id="detikdetailtext">
    results = soup.find_all('div',attrs={'class':'detail_text', 'id':'detikdetailtext'})
    # print(results)

    # real data start after </b> end before <div class="clearfix
    regex = r"</b>(.*)<div class=\"clearfix"
    raws = re.findall(regex, str(results), re.S)
    # collect semua kata
    regex = r"[-a-zA-Z]+"
    rawsCollected = re.findall(regex, str(raws), re.DOTALL)
    for match in rawsCollected:
        # filter data
        if (str(match) not in meaninglessWords) and (len(str(match)) > 1) and ('--' not in str(match)):
            wordsCollected.append(match)
            print("appended: %s" % (match))
        else:
            print("kicked: %s" % (match))
        # print("match (%s): %s" % (len(match),match))
    return wordsCollected

# def main():
#     linkCollected = getLink()
#     for link in linkCollected:
#         getWords(link)
    # print(linkCollected)


main()
    # getWords('https://news.detik.com/berita/d-4302346/kemenag-kartu-nikah-minimalkan-pemalsuan-buku-nikah')
# def main():
    # getLink()
#
# # link diambil dari kumpulan index detikcom
# r = requests.get('https://news.detik.com/berita/d-4302346/kemenag-kartu-nikah-minimalkan-pemalsuan-buku-nikah')
# # print(r.text)
# soup = BeautifulSoup(r.text, 'html.parser')
#
# # dari metode inspect element, didapat berita selalu ada didalam tag <div class="detail_text" id="detikdetailtext">
# results = soup.find_all('div',attrs={'class':'detail_text', 'id':'detikdetailtext'})
# # print(results)
#
# # real data start after </b>
# # real data end before <div class="clearfix
# regex = r"</b>(.*)<div class=\"clearfix"
# raws = re.findall(regex, str(results), re.S)
# # collect semua kata
# regex = r"[-a-zA-Z]+"
# rawsCollected = re.findall(regex, str(raws), re.DOTALL)
# for match in rawsCollected:
#     print("match: %s" % (match))
#
#


# print(len(results[0].contents))
# x=0
# for contentsnyah in results[0].contents:
#     print('content ke '+str(x)+' : '+str(contentsnyah))
#     x=x+1
# #
# # # dari pola artikel selalu ada nama kota asal berita
# # regex = r"<b>(.*)</b>"
# # match = re.search(regex, str(results))
# # cityResults = match.group(1)
# # # print(cityResults)
# #
# # # kemudian isi berita
# # print(str(results))
# # # re.match(pattern, string)
# # regex = r"</b>.*\s<div class=\"clearfix"
# # # regex = r"</b>.*<div class=\"clearfix mb20\"> \s"
# # matches = re.findall(regex, str(results), re.DOTALL)
# # for match in matches:
# #     print("Full match: %s" % (match))
# #
# # # paragraphResults = match.group(1)
# # # print(paragraphResults)
# # # for
# # # paragraphResults = match.group(1)
# # # paragraphResults = soup.find_all('p')
# # # print(cityResults)
# # # # href="https://news.detik.com/berita/d-4302346/kemenag-kartu-nikah-minimalkan-pemalsuan-buku-nikah"
# # # # print(results)
