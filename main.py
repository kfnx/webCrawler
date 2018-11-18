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
    meaninglessWords = ['href','https','http','www','com','search','searchall','query','target','blank','br','strong','table','class','linksisip','tbody','tr','td','div','class','lihatjg','Baca','juga','data-action','data-category','Detil','Artikel','data-label','List','Berita','news','detik','com','read','ke','di','Rp','Pilihan','em','single','identity','yang','dari','untuk','dan','ini','itu','ada','dia','saya','tag','dalam','akan','kita','kami','dengan','karena','saat','tidak','sudah','sebuah','Kami','kata','jadi','Dia','tak','kalau','Jadi','tersebut','adalah','pada','atau','mengatakan','di','telah','namun','kemudian','sebagai','melakukan','tapi','kepada','ujar','Saya','Selain','masih','menjadi','lagi','Kami','agar','align-center','hingga','mereka','Ini','nanti','jika']
    wordsCollected = []
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
    wordsKicked = 0
    for match in rawsCollected:
        # filter data
        if (str(match) not in meaninglessWords) and (len(str(match)) > 1) and ('--' not in str(match)):
            wordsCollected.append(match)
            # print("appended: %s" % (match))
        else:
            wordsKicked = wordsKicked+1
            # print("kicked: %s" % (match))
            # print("match (%s): %s" % (len(match),match))

    print(str(len(wordsCollected))+' words collected and '+str(wordsKicked)+' words kicked')
    return wordsCollected

def insertText(words):
    text_file = open("textCollected.txt", "w")
    for items in words:
        text_file.write(str(items)+' ')
    text_file.close()

def main():
    wordBank = []
    # collect all links
    linkCollected = getLink()
    # collect all words from every link
    for link in linkCollected:
        print('collecting from url : '+str(link))
        updateWords = getWords(link)
        wordBank = wordBank + updateWords
    # print(wordBank)
    # join all words collected to a text file
    insertText(wordBank)

main()
