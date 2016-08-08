import android
import os, datetime, time

from katalogi import kat
from katalogi import podkat

droid = android.Android()

def mainMenu(topic, methodList):
    """
    print Android menu for choose options
    """
    droid.dialogCreateAlert(topic)
    droid.dialogSetItems(methodList)
    droid.dialogShow()
    nika=droid.dialogGetResponse().result["item"]
    return nika

teraz = datetime.date.today()
terazProp = str(teraz.strftime('%y%m%d_'))
nameofile = droid.dialogGetInput('Filename', 'Enter txt filename:', terazProp).result

plikzap = '{}{}{}.csv'.format(kat, podkat, nameofile)
plikpom = '{}{}.txt'.format(kat, nameofile)
	
# choose saving file method
wybor = mainMenu('Write mode:', ["append", "overwrite"])

if wybor == 1:
    # overwrite files
    openzap = open(plikzap, 'w')
    openzap.write('')
    openzap.close()

    openpom = open(plikpom, 'w')
    openpom.write('')
    openpom.close()

# choose type of activity (and time in sec. between saving waypoint: tryb)
wybor2 = mainMenu('Record mode:', ["walk", "run", "bike", "measure"])
if wybor2 == 0:
    tryb = 8
elif wybor2 == 1:
    tryb = 6
elif wybor2 == 2:
    tryb = 4
elif wybor2 == 3:
    tryb = 2

# choose if you want saving data in CSV file 
wybor3 = mainMenu('Full CSV data:', ["NO", "YES"])

# start main program: Locating
droid.startLocating(2000, 3)

lastOld = 0
lostOld = 0
zapis = None

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
            sygnal = 'GPS'

            if (last != lastOld and lost != lostOld):
                # new waypoint's coordinates are other than old coordinates
                wysokost = str(wysoko)[:4]
                znaczn = datetime.datetime.now()
                znacznik = str(znaczn.strftime('%Y-%m-%d %H:%M:%S'))
                zapis = 'S'

                # writing text file (WKT)
                openpom = open(plikpom, 'a')
                openpom.write(lost + ' ' + last + ',')
                openpom.close()

                if wybor3 == 1:
                    # write CSV file with attributes:
                    openzap = open(plikzap, 'a')
                    openzap.write('{}, {}, {}, {}, {},\n'.format(znacznik, last, lost, sygnal, wysokost))
                    openzap.close()

                lastOld = last
                lostOld = lost

            else:
                zapis = 'N'
                
            szer = '{} N [{}]'.format(last , sygnal)
            dlug = '{} E | {} [mnpm] ({})'.format(lost, wysokost, zapis)

            print(szer)
            print(dlug)
            print(40 * '-')
    else:
        print ("Waiting for turn on GPS module...") 
    
    time.sleep(tryb)
    
droid.stopLocating()
