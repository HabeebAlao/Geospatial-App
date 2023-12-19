from pathlib import Path

from django.contrib.gis.utils import LayerMapping

from .models import Counties

counties_mapping = {

    'osm_id': 'OSM_ID',

    'name_tag': 'NAME_TAG',

    'name_ga': 'NAME_GA',

    'name_en': 'NAME_EN',

    'alt_name': 'ALT_NAME',

    'alt_name_g': 'ALT_NAME_G',

    'logainm_re': 'LOGAINM_RE',

    'osm_user': 'OSM_USER',

    'osm_timest': 'OSM_TIMEST',

    'attributio': 'ATTRIBUTIO',

    't_ie_url': 'T_IE_URL',

    'area': 'AREA',

    'latitude': 'LATITUDE',

    'longitude': 'LONGITUDE',

    'epoch_tstm': 'EPOCH_TSTM',

    'geom': 'MULTIPOLYGON',

}

counties_shp = Path(__file__).resolve().parent / 'data' / 'counties' / 'counties.shp'


def run(verbose=True):
    lm1 = LayerMapping(Counties, counties_shp, counties_mapping, transform=False)

    lm1.save(strict=True, verbose=verbose)
