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
nameofile = droid.dialogGetInput('Filename', 'Enter txt filename:').result

plikzap = (kat + podkat + nameofile + '.csv')
plikpom = (kat + nameofile + '.txt')
	
wybor = drzwi('Write mode:', ["append", "overwrite"])
if wybor == 1:
    openzap = open(plikzap, 'w')
    openzap.write('')
    openzap.close()

    openpom = open(plikpom, 'w')
    openpom.write('')
    openpom.close()

wybor2 = drzwi('Record mode:', ["walk", "run", "bike", "measure"])
if wybor2 == 0:
    tryb = 8
elif wybor2 == 1:
    tryb = 6
elif wybor2 == 2:
    tryb = 4
elif wybor2 == 3:
    tryb = 2

wybor3 = drzwi('Full CSV data:', ["NO", "YES"])

droid.startLocating(2000, 3)

lastOld = 0
lostOld = 0

while True:
    locat = droid.readLocation()
    if 'gps' in droid.readLocation().result:
        try:
            lat = str(locat.result['gps']['latitude'])
            lon = str(locat.result['gps']['longitude'])
            wysoko = str(locat.result['gps']['altitude'])
        except Exception as p:
            print ('Failure: ', p)
            sygnal = 'NONE'
        else:
            last = str(lat)[:9]
            lost = str(lon)[:9]

            if (last != lastOld and lost != lostOld):
                wysokost = str(wysoko)[:4]
                znaczn = datetime.datetime.now()
                znacznik = str(znaczn.strftime('%Y-%m-%d %H:%M:%S'))
                sygnal = 'GPS'

                # writing text file with attributes:
                # time,latitude,longitude,height(HAGL),source of signal\n
                if wybor3 == 1:
                    openzap = open(plikzap, 'a')
                    openzap.write(znacznik + ',' + last + ',' + lost + ',' + sygnal + ',' + wysokost + ',\n')
                    openzap.close()

                openpom = open(plikpom, 'a')
                openpom.write(lost + ' ' + last + ',')
                openpom.close()

                lastOld = last
                lostOld = lost
                
        finally:
            szer = (last + ' N [' + sygnal + ']')
            dlug = (lost + ' E | ' + wysokost + '  [mnpm]')

            print(szer)
            print(dlug)
            print(40 * '-')
    else:
        print ("Waiting for turn on GPS module...") 
    
    time.sleep(tryb)
    
droid.stopLocating()

