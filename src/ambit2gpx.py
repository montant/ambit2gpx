import os
import xml.dom.minidom
import math
import getopt
import sys

def radian2degree(radian):
    return radian * 180.0 / math.pi

def childElements(parent):   
    elements = []
    for child in parent.childNodes:
        if child.nodeType != child.ELEMENT_NODE:
            continue
        elements.append(child)
    return elements

class AmbitXMLParser(object):
    __root = None
    __outputfile = None
    def __init__(self, xml_node, altibaro, outputfile):
        assert isinstance(xml_node,xml.dom.Node)
        assert xml_node.nodeType == xml_node.ELEMENT_NODE
        self.__root = xml_node
        self.__outputfile = outputfile
        self.__altibaro = altibaro
        self.__altitude = None
        self.__hr = None
        
    def extension(self,hr):
        if (hr == None):
            return ""
        return """
<extensions> 
    <gpxtpx:TrackPointExtension> 
        <gpxtpx:hr>{hr}</gpxtpx:hr> 
    </gpxtpx:TrackPointExtension> 
</extensions>
""".format(hr=hr)           

    def __parse_sample(self, sample):
        latitude = None
        longitude = None
        time = None
        for node in childElements(sample):
            key = node.tagName
            if key == "Latitude":
                latitude = radian2degree(float(node.firstChild.nodeValue))
            if key == "Longitude":
                longitude = radian2degree(float(node.firstChild.nodeValue))
            if key == "UTC":
                time = node.firstChild.nodeValue
            if key == "HR":
                self.__hr = int((float(node.firstChild.nodeValue))*60+0.5)
            if key == "Altitude" and self.__altibaro:
                self.__altitude = node.firstChild.nodeValue
            if key == "GPSAltitude" and not self.__altibaro:
                self.__altitude = node.firstChild.nodeValue
        if latitude != None and longitude != None:
            print >>self.__outputfile, """
<trkpt lat="{latitude}" lon="{longitude}">
    <ele>{altitude}</ele>
    <time>{time}</time>
    {extension}  
</trkpt>
""".format(latitude=latitude, longitude=longitude, altitude=self.__altitude, time=time, extension=self.extension(self.__hr))
    def __parse_samples(self, samples):
        for node in childElements(samples):
            key = node.tagName
            if key == "sample":
                self.__parse_sample(node)
      
    def execute(self):   
        print >>self.__outputfile,'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
        print >>self.__outputfile,"""
<gpx 
xmlns="http://www.topografix.com/GPX/1/1"
xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" 
creator="ambit2gpx" version="1.1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
 <metadata>
    <link href="http://code.google.com/p/ambit2gpx/">
      <text>Ambit2GPX</text>
    </link>
   </metadata>
  <trk>
    <trkseg>  
"""              
        root = self.__root
        for node in childElements(root):
            key = node.tagName
            if key == "samples":
                self.__parse_samples(node)
                
        print >>self.__outputfile,"""
    </trkseg>        
  </trk>
</gpx>
"""

def usage():
    print """
ambit2gpx [--altibaro] filename
Creates a file filename.gpx in GPX format from filename in Suunto Ambit XML format.
If option --altibaro is given, elevation is retrieved from altibaro information. The default is to retrieve GPS elevation information.
"""

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha", ["help","altibaro"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(sys.argv[1:]) == 0:
        usage()
        sys.exit(2)
    output = None
    verbose = False
    altibaro = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--altibaro"):
            altibaro = True
        else:
            assert False, "unhandled option"
    # ...
    
    filename = args[0]
    (rootfilename, ext) = os.path.splitext(filename)
    if (ext == ""):
        filename += ".xml"
    if (not os.path.exists(filename)):
        print >>err, "File {0} doesn't exist".format(filename)
        sys.exit()
    file = open(filename)
    file.readline() # Skip first line
    filecontents = file.read()
    file.close()
    
    print "Parsing file {0}".format(filename)
    doc = xml.dom.minidom.parseString('<?xml version="1.0" encoding="utf-8"?><top>'+filecontents+'</top>')
    assert doc != None
    top = doc.getElementsByTagName('top')
    assert len(top) == 1    
    print "Done."
    
    outputfilename = rootfilename+ '.gpx'
    outputfile = open(outputfilename, 'w')
    print "Creating file {0}".format(outputfilename)
    AmbitXMLParser(top[0], altibaro, outputfile).execute()
    outputfile.close()
    print "Done."
        
if __name__ == "__main__":
    main()
