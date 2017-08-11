import os, csv
import csv

from katalogi import kat
from katalogi import podkat

from myspatial import gpx_start, gpx_koniec, gpx_trkpt

def show_dir(path):
    nodes = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            nodes.append(file)

    return nodes

folder = os.path.join(kat, podkat)
plikod = show_dir(folder)
print(plikod)

for input_file in plikod:

    namef = input_file.replace('.csv','')

    pliktxt = open(os.path.join(folder, input_file))
    data = csv.reader(pliktxt, delimiter = ',')
    data.__next__()

    output_file = (namef + '.gpx')
    e = os.path.join(folder, output_file)
    zapisny = open(e, 'w')

    gpx_start(zapisny, namef)

    for row in data:
        lat = str(row[1])
        lon = str(row[2])
        tme = row[0]
        ele = float(row[4])

        gpx_trkpt(zapisny, lat, lon, ele, tme)

    gpx_koniec(zapisny)
    pliktxt.close()

    print('GPX file was ceated')
