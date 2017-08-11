import os
import xlrd, datetime

from katalogi import kat 
from katalogi import podkat 

from myspatial import gpx_start, gpx_koniec, gpx_trkpt

def show_dir(path):
    nodes = []
    for file in os.listdir(path):
        if file.endswith(".xls"):
            nodes.append(file)

    return nodes

folder = os.path.join(kat, podkat)
plikod = show_dir(folder)
print(plikod)

for input_file in plikod:
    wb = xlrd.open_workbook(os.path.join(folder, input_file))
    namef = input_file.replace('.xlsx', '').replace('.xls', '')
    sh = wb.sheet_by_name(namef)

    output_file = (namef + '.gpx')
    e = os.path.join(folder, output_file)
    zapisny = open(e, 'w')

    gpx_start(zapisny, namef)

    for rownum in range(sh.nrows):
        row = sh.row_values(rownum)
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(float(row[4]), wb.datemode)
        tme = '{}-{}-{}T{}:{}:{}'.format(year, month, day, hour, minute, second)

        lat = str(row[0])
        lon = str(row[1])
        ele = float(row[3])*0.3048

        gpx_trkpt(zapisny, lat, lon, ele, tme) 

    gpx_koniec(zapisny) 
    
    print('GPX file was ceated') 
