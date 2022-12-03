import json
import gzip
import logging
import math
import os
import sys

logger = logging.getLogger('localnewsrepo.localnewsrepo')

def generic_error_info(slug=''):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    errMsg = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
    logger.error(errMsg + slug)

    return errMsg

#credit to: https://github.com/mapado/haversine/blob/master/haversine/__init__.py
def haversine(point1, point2, miles=True):
    
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    AVG_EARTH_RADIUS = 6371  # in km

    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(math.radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = math.sin(lat * 0.5) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * math.asin(math.sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers


#file - start

def readTextFromFile(infilename):

    text = ''

    try:
        with open(infilename, 'r') as infile:
            text = infile.read()
    except:
        print('\treadTextFromFile()error filename:', infilename)
        generic_error_info()
    

    return text

def dumpJsonToFile(outfilename, dictToWrite, indentFlag=True, extraParams=None):

    if( extraParams is None ):
        extraParams = {}

    extraParams.setdefault('verbose', True)

    try:
        outfile = open(outfilename, 'w')
        
        if( indentFlag ):
            json.dump(dictToWrite, outfile, ensure_ascii=False, indent=4)#by default, ensure_ascii=True, and this will cause  all non-ASCII characters in the output are escaped with \uXXXX sequences, and the result is a str instance consisting of ASCII characters only. Since in python 3 all strings are unicode by default, forcing ascii is unecessary
        else:
            json.dump(dictToWrite, outfile, ensure_ascii=False)

        outfile.close()

        if( extraParams['verbose'] ):
            logger.info('\tdumpJsonToFile(), wrote: ' + outfilename)
    except:
        generic_error_info('\n\terror: outfilename: ' + outfilename)
        return False

    return True

def getDictFromJsonGZ(path):

    json = getTextFromGZ(path)
    if( len(json) == 0 ):
        return {}
    return getDictFromJson(json)

def getTextFromGZ(path):
    
    try:
        with gzip.open(path, 'rb') as f:
            return f.read().decode('utf-8')
    except:
        generic_error_info()

    return ''

def getDictFromJson(jsonStr):

    try:
        return json.loads(jsonStr)
    except:
        generic_error_info('\tjsonStr prefix: ' + jsonStr[:100])

    return {}

def getDictFromFile(filename):

    try:

        if( os.path.exists(filename) == False ):
            return {}

        return getDictFromJson( readTextFromFile(filename) )
    except:
        print('\tgetDictFromFile(): error filename', filename)
        generic_error_info()

    return {}

def gzipTextFile(path, txt):
    
    try:
        with gzip.open(path, 'wb') as f:
            f.write(txt.encode())
    except:
        generic_error_info()

#file - end