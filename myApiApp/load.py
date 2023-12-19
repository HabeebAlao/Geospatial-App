from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import eds, counties

# Auto-generated `LayerMapping` dictionary for eds model

ElectoralDistricts_mapping = {

    'osm_id': 'OSM_ID',

    'name_tag': 'NAME_TAG',

    'name_ga': 'NAME_GA',

    'name_en': 'NAME_EN',

    'alt_name': 'ALT_NAME',

    'alt_name_g': 'ALT_NAME_G',

    'osm_user': 'OSM_USER',

    'osm_timest': 'OSM_TIMEST',

    'attributio': 'ATTRIBUTIO',

    'logainm_re': 'LOGAINM_RE',

    'co_name': 'CO_NAME',

    'co_osm_id': 'CO_OSM_ID',

    't_ie_url': 'T_IE_URL',

    'area': 'AREA',

    'latitude': 'LATITUDE',

    'longitude': 'LONGITUDE',

    'epoch_tstm': 'EPOCH_TSTM',

    'geom': 'MULTIPOLYGON',

}

# Auto-generated `LayerMapping` dictionary for counties model

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

eds_shp = Path(__file__).resolve().parent / 'data' / 'eds' / 'eds.shp'
counties_shp = Path(__file__).resolve().parent / 'data' / 'counties' / 'counties.shp'


def run(verbose=True):
    lm = LayerMapping(eds, eds_shp, ElectoralDistricts_mapping, transform=False)

    lm1 = LayerMapping(counties, counties_shp, counties_mapping, transform=False)

    lm.save(strict=True, verbose=verbose)

    lm1.save(strict=True, verbose=verbose)
