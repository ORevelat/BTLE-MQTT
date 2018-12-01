import time
from logger import Logger as logger

KNOWN_DEVICES = [

    {
        'mac': '4C:65:A8:D0:63:55',
        'name': 'sensor_sdb',
        'sensor': 'xiaomith',
        'timer': 300,
        'last_beat': 0,
        'last_update': 0,
        'last_publish': 0,
        'values': {}
    },
    {
        'mac': 'C4:7C:8D:64:43:F2',
        'name': 'sensor_miflora1',
        'sensor': 'miflora',
        'timer': 600,
        'last_beat': 0,
        'last_update': 0,
        'last_publish': 0,
        'values': {}
    },
    {
        'mac': '78:A5:04:43:B0:A6',
        'name': 'dotti',
        'sensor': 'dotti',
        'timer': 600,
        'last_beat': 0,
        'last_update': 0,
        'last_publish': 0,
        'values': {}
    }

]

def update_values(new):
    if new is None:
        return

    for d in KNOWN_DEVICES:
        if d['mac'] == new['id']:
            d['values'].update(new)
            d['last_update'] = int(time.time())
