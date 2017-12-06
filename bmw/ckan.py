import requests
import datetime
import time
import pytz

def get_tuple_from_record(x):
    timestamp = x['attrMd'][0]['value']
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+00:00')
    timestamp = pytz.utc.localize(timestamp)
    timestamp = time.mktime(timestamp.timetuple())
    timestamp = timestamp * 1000
    return (timestamp,float(x['attrValue']))

def ckan_to_series(resource_id, attr_name):
    url = 'http://fiware.acaciadata.com:8000/api/3/action/datastore_search?resource_id=' + resource_id + '&q=' + attr_name + '&limit=1000'
    r = requests.get(url)
    series = [get_tuple_from_record(x) for x in r.json()['result']['records']]
    return sorted(series,key=lambda x: x[0])

ckan_id = {'5g0e2929': '38e70012-7e00-479d-88de-b326ff29ee85',
    '5g118054': '022acadb-26b2-46f9-aad2-c7911002c19e',
    '5g118057': '5e2edbbd-33e4-49ac-af62-9fe2d13717c5',
    '5g118058': '9f424b23-6517-402a-8fd1-0199b0e2b163',
    'bw-pb01': 'bd5ec422-408c-46ff-b5e3-92ae7b83280f'}



#Example:
#series = ckan_to_series(ckan_id['5g118057'], 'batt')
#print(series)
