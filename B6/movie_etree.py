import xml.etree.ElementTree as ET
dom=ET.parse("movie.xml")
root=dom.getroot()
print u"===Kok element {}".format(root)
print u"===Kok element attrib {}".format(root.attrib.keys())
print u"===Kok element attribute metni {}".format(root.attrib["vitrin"])
for film in dom.findall("film"):
    filmAdi=film.attrib[film.attrib.keys()[0]]
    sfilmAdi=film.get("etiket")
    filmtipi=film.find("tip").text
    format=film.find("format").text
    sene=film.find("sene").text
    str="[+] Film Adi :%s veya film adi :%s tip :%s ,format: %s ,sene :%s"%(filmAdi,sfilmAdi,filmtipi,format,sene)
    print str

