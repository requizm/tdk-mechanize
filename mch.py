#-*- coding: utf-8 -*- 
# encoding=utf8
import mechanize,lxml,urllib2,sys
from bs4 import BeautifulSoup


class TdkBot:

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        br = mechanize.Browser()
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        response = br.open("http://tdk.org.tr/index.php?option=com_yazimkilavuzu&view=yazimkilavuzu")

    def begin(self):
        self.main()

    def main(self):
        harfler = ['a','b','c','ç','d','e','f','g','h','ı','i','j','k','l','m','n','o','ö','p','r','s','ş','t','u','ü','v','y','z']
        f = open("output.txt","w")
        for harf in harfler:
            br.select_form(name='isimAra')
            textbox = br.form.find_control(id="kelime")
            textbox.value = harf
            br.submit(name='gonder', label='ARA')
            soup = BeautifulSoup(br.response().read(), "lxml")
            select = soup.select('select')[1]
            optionlar = select.findAll('option')
            sayfa_sayisi = len(optionlar) - 1
            mevcutsayfa = 1

            while mevcutsayfa <= sayfa_sayisi:
                kelimeler = soup.findAll('p', {"class": "thomicb"})

                for kelime in kelimeler:
                    element = kelime.select('a')[1]
                    element_href = element.get('href')
                    element_adi = element.text
                    print(element_href)
                    page_anlam = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                    page_anlam = page_anlam.open('http://tdk.org.tr'+element_href)
                    anlamsoup = BeautifulSoup(page_anlam.read(),"lxml")
                    #tablo = anlamsoup.select("table")[2]
                    tablo = anlamsoup.find("table", {"id": "hor-minimalist-a"})
                    tr = tablo.findAll("tr")
                    mevcut_tr = 1
                    print("işte kelime: "+element_adi)
                    f.write( element_adi + "/")

                    while mevcut_tr<len(tr):
                        f.write(tr[mevcut_tr].text)
                        mevcut_tr += 1
                    f.write(" - \n")
                    

                sonrakisayfa = soup.findAll("span", {"class": "comicm"})
                sonrakisayfa = sonrakisayfa[1].select('a')[0]
                srksyf = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                srksyf = srksyf.open('http://tdk.org.tr'+sonrakisayfa.get('href'))
                soup = BeautifulSoup(srksyf.read(),"lxml")
                yenikelimeler = soup.findAll('p', {"class": "thomicb"})
                print(kelimeler[0].text + " " + yenikelimeler[0].text)

                if kelimeler[0].text == yenikelimeler[0].text:
                    break
                else:
                    print(str(mevcutsayfa)+". Sayfa Bitti")
                    mevcutsayfa += 1
               
        f.close()
        br.close()

if __name__='__main__':
    bot = TdkBot()
    bot.begin()