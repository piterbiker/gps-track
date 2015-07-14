import android, time
import datetime

from katalogi import kat
from katalogi import podkat

droid = android.Android()

def drzwi(glowa, krotka):
    droid.dialogCreateAlert(glowa)
    droid.dialogSetItems(krotka)
    droid.dialogShow()
    nika=droid.dialogGetResponse().result["item"]
    return nika

teraz = str(datetime.date.today())
nameofile = droid.dialogGetInput('Nazwa pliku', 'podaj nazwe pliku txt:').result

plikzap = (kat + podkat + nameofile + '.csv')
plikpom = (kat + nameofile + '.txt')
	
wybor = drzwi('Zapis pliku:', ["dodawanie", "nadpisywanie"])
if wybor == 1:
    openzap = open(plikzap, 'w')
    openzap.write('')
    openzap.close()

    openpom = open(plikpom, 'w')
    openpom.write('')
    openpom.close()

wybor2 = drzwi('Tryb zapisu:', ["spacer", "bieg", "rower", "pomiary"])
if wybor2 == 0:
    tryb = 8
elif wybor2 == 1:
    tryb = 6
elif wybor2 == 2:
    tryb = 4
elif wybor2 == 3:
    tryb = 2

wybor3 = drzwi('Pelne dane CSV:', ["NIE", "TAK"])

droid.startLocating(2000, 3)

while True:
    locat = droid.readLocation()
    if 'gps' in droid.readLocation().result:
        try:
            lat = str(locat.result['gps']['latitude'])
            lon = str(locat.result['gps']['longitude'])
            wysoko = str(locat.result['gps']['altitude'])
        except Exception as p:
            print ('niepowodzenie: ', p)
            sygnal = 'BRAK'
        else:
            last = str(lat)[:9]
            lost = str(lon)[:9]
            wysokost = str(wysoko)[:4]
            znaczn = datetime.datetime.now()
            znacznik = str(znaczn.strftime('%Y-%m-%d %H:%M:%S'))
            sygnal = 'GPS'

# zapis pliku: czas,szerokosc,dlugosc,wysokosc,sygnal\n
            if wybor3 == 1:
                openzap = open(plikzap, 'a')
                openzap.write(znacznik + ',' + last + ',' + lost + ',' + sygnal + ',' + wysokost + ',\n')
                openzap.close()

            openpom = open(plikpom, 'a')
            openpom.write(lost + ' ' + last + ',')
            openpom.close()        
        finally:
            szer = (last + ' N [' + sygnal + ']')
            dlug = (lost + ' E | ' + wysokost + '  [mnpm]')

            print(szer)
            print(dlug)
            print(40 * '-')
    else:
        print ("Czekam na WL. modulu GPS...") 
    
    time.sleep(tryb)
    
droid.stopLocating()
