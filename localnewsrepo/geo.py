import json
import os
import sqlite3

from localnewsrepo.util import generic_error_info
from localnewsrepo.util import getDictFromJsonGZ
from localnewsrepo.util import haversine

def get_city_details(db_filepath, zipcode):
    
    try:
        #ZipCodes Table fields in zipcodes.db ['zip', 'city', 'state', 'longitude', 'latitude', 'timezone', 'dst']
        con = sqlite3.connect(db_filepath)

        cursor = con.execute('select distinct city, state, latitude, longitude from ZipCodes where zip="%s"' % zipcode)
        db_fields = cursor.fetchone()
        con.close()

        if( db_fields is not None ):
            city_details = {}
            city_details['city'] = db_fields[0]
            city_details['state'] = db_fields[1].strip().upper()
            #city_details['country'] = country
            city_details['city-latitude'] = db_fields[2]
            city_details['city-longitude'] = db_fields[3]

            return city_details
    except:
        generic_error_info()
    
    return {}

def get_k_media_near_zip(country, zipcode_or_city, k, media_types=['newspaper', 'tv', 'radio'], **kwargs):

    country = country.strip()
    zipcode_or_city = zipcode_or_city.strip()
    if( country == '' or zipcode_or_city == '' ):
        return {}
    
    us_city_details = {}
    data_path = '{}/sources/'.format( os.path.dirname(os.path.abspath(__file__)) )
    unfiltered_media = getDictFromJsonGZ(f'{data_path}countries_local_media.json.gz')

    if( country.lower() == 'usa' ):
        us_city_details = get_city_details( data_path + 'zipcodes.db', zipcode_or_city )
        unfiltered_media = unfiltered_media.get('USA', {}).get(us_city_details.get('state', ''), {})
    else:
        unfiltered_media = unfiltered_media.get(country, {}).get(zipcode_or_city, {})

    if( len(unfiltered_media) == 0 ):
        return {}
    
    merged_media = []
    for media in media_types:
        merged_media += unfiltered_media[media]


    for i in range(len(merged_media)):
        
        source = merged_media[i]
        source['country'] = country

        if( len(us_city_details) != 0 ):
            coordinates = ( source['city-county-lat'], source['city-county-long'] )
            distance_miles = haversine( (us_city_details['city-latitude'], us_city_details['city-longitude']), coordinates)

            #additional metadata - start
            source['state'] = us_city_details['state']
            source['miles'] = distance_miles
            #additional metadata - end


    if( len(us_city_details) != 0 ):
        merged_media = sorted(merged_media, key=lambda source: source['miles'])
    
    merged_media = merged_media if k == -1 else merged_media[:k]
    selfargs = {**kwargs, 'country': country, 'zipcode_or_city': zipcode_or_city, 'k': k, 'media_types': media_types}
    result = {'local_media': merged_media, 'self': selfargs}

    return result

