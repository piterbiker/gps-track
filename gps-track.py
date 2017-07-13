import errno
import android
import os
import datetime, time
import pprint

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


def saveData2File(savingFile, tekst):
    try:
        openpom = open(savingFile, 'a')
    except (OSError, IOError) as e:
        print(e, e.errno, errno.EINTR, sep='\n')
    else:
        with openpom:
            openpom.write(tekst)


teraz = datetime.date.today()
terazProp = str(teraz.strftime('%y%m%d_'))
nameofile = droid.dialogGetInput('Filename', 'Enter txt filename:', terazProp).result

noYes = ["NO", "YES"]
plikpom = '{}{}.txt'.format(kat, nameofile)
plikzap = '{}{}{}.csv'.format(kat, podkat, nameofile)
	
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
    tryb = 6
elif wybor2 == 1:
    tryb = 4
elif wybor2 == 2:
    tryb = 2
elif wybor2 == 3:
    tryb = 1

# choose if you want saving data in CSV file 
wybor3 = mainMenu('Full CSV data:', noYes)

if wybor2 in [0, 1]:
    wybor4 = mainMenu('Geocoding:', noYes)
else:
    wybor4 = None

# start main program: Locating
droid.startLocating(1000, 2)

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
                # new waypoint's coordinates are different than old coordinates
                wysokost = str(wysoko)[:4]
                znaczn = datetime.datetime.now()
                znacznik = str(znaczn.strftime('%Y-%m-%d %H:%M:%S'))
                zapis = 'S'

                # writing text file (WKT)
                datapom = '{} {},'.format(lost, last)
                saveData2File(plikpom, datapom)

                if wybor3 == 1:
                    # write CSV file with attributes:
                    datazap = '{},{},{},{},{},\n'.format(znacznik, last, lost, sygnal, wysokost)
                    saveData2File(plikzap, datazap)

                lastOld = last
                lostOld = lost

            else:
                zapis = 'N'
                
            szer = '{} N [{}]'.format(last , sygnal)
            dlug = '{} E | {} [mnpm] ({})'.format(lost, wysokost, zapis)

            print(szer, dlug, 34 * '-', sep='\n')

            if wybor4:
                if wybor4 == 1:
                    # geocoding data
                    try:
                        adresy = droid.geocode(last, lost, 1).result
                    except Exception as g:
                        print('Geocoding error: {}'.format(g))
                    else:
                        pprint.pprint(adresy)
 
    else:
        print ("Waiting for turn on GPS module...") 
    
    time.sleep(tryb)
    
droid.stopLocating()

