import zipfile

def kml_start(f, nazwakml):
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("<name>" + nazwakml + "</name>\n")
    f.write("<visibility>1</visibility>\n")
    f.write("<Style id='lineStyle'>\n")
    f.write("<LineStyle>\n")
    f.write("<colorMode>random</colorMode>\n")
    f.write("<width>4</width>\n")
    f.write("</LineStyle>\n")
    f.write("</Style>\n")

def kml_trasa1(f):
    f.write("<Placemark>\n")
    f.write("<name>Trasa</name>\n")
    f.write("<styleUrl>#lineStyle</styleUrl>\n")
    f.write("<MultiGeometry><LineString><coordinates>\n")

def kml_trasa2(f, jeden, cztery):
    f.write(str(jeden) + "," + str(cztery) + ",0\n")

def kml_trasa3(f):
    f.write("</coordinates></LineString></MultiGeometry>\n")
    f.write("</Placemark>\n")

def kml_wpt1(f, folderkml):
    f.write("<Folder>\n")
    f.write("<name>" + folderkml + "</name>\n")

def kml_wpt2(f, nazwapunktu, jeden, cztery):
    f.write("<Placemark>\n")
    f.write("<name>" + nazwapunktu + "</name>\n")
    f.write("<description></description>\n")
    f.write("<Point>\n")
    f.write("<coordinates>" + str(jeden) + "," + str(cztery) + ",0</coordinates>\n")
    f.write("</Point>\n")
    f.write("</Placemark>\n")

def kml_wpt3(f):
    f.write("</Folder>\n") 

def kml_koniec(f, zap):
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()
    itemes = (zap + '.kmz')
    try:
        import zlib
        mode= zipfile.ZIP_DEFLATED
    except:
        mode= zipfile.ZIP_STORED
    zip = zipfile.ZipFile(itemes, 'w', mode)
    zip.write(zap)
    zip.close()

def plt_start(g):
    g.write("OziExplorer Track Point File Version 2.1\n")
    g.write("WGS 84\n")
    g.write("Altitude is in Feet\n")
    g.write("Reserved 3\n")
    g.write("0, 2, 65280, routes, 1, 0, 0, 65280\n")
    g.write(" 0\n")

def plt_body(g, jeden, cztery):
    g.write(cztery + "," + jeden + ",0,0.0,,,\n")

def plt_end(g):
    g.close()
