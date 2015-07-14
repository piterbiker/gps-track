import os, csv
import android
import datetime

from katalogi import kat
from katalogi import podkat

from myspatial import kml_start
from myspatial import kml_trasa1
from myspatial import kml_trasa2
from myspatial import kml_trasa3
from myspatial import kml_wpt1
from myspatial import kml_wpt2
from myspatial import kml_wpt3
from myspatial import kml_koniec

droid = android.Android()

def show_dir(path):
    nodes = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            nodes.append(file)

    if path != path: nodes.insert(0, '..')

    droid.dialogCreateAlert(path)
    droid.dialogSetItems(nodes)
    droid.dialogShow()

    result = droid.dialogGetResponse().result
    droid.dialogDismiss()
    if 'item' not in result:
        return
    target = nodes[result['item']]
    target_path = os.path.join(path, target)
    return target_path

folder = (kat + podkat)
plikod = show_dir(folder)
print(plikod)
namef = plikod.replace(folder,'')
namef = namef.replace('.csv','')

teraz = str(datetime.date.today())
tytul1 = teraz.replace('201','1')

prop = (tytul1.replace('-','') + '_' + namef + '.kml')

pliktxt = open(plikod)
data = csv.reader(pliktxt, delimiter = ',')
data.__next__()

d = droid.dialogGetInput('Name of KML file', 'Enter filename', prop).result
e = folder + d
zapisny = open(e, 'w')

kml_start(zapisny, plikod)
kml_trasa1(zapisny)

for row in data:
    koo1 = str(row[2])
    koo2 = str(row[1])
    kml_trasa2(zapisny, koo1, koo2)

kml_trasa3(zapisny)
kml_wpt1(zapisny, teraz)

pliktxt.seek(0, 0)
data2 = csv.reader(pliktxt, delimiter = ',')
data2.__next__()

for row in data2:
    koo0 = str(row[0])
    koo1 = str(row[2])
    koo2 = str(row[1])
    kml_wpt2(zapisny, koo0, koo1, koo2)
pliktxt.close()

kml_wpt3(zapisny)
os.chdir(folder)
kml_koniec(zapisny, d)
droid.dialogCreateAlert('CSV => KML', 'KML file was ceated')
droid.dialogShow()



