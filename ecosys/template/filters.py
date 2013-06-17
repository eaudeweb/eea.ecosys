import json


def filter_eu(countries):
    return filter(lambda c: 'eu' in c['categories'], countries)


def filter_eea(countries):
    return filter(lambda c: 'eea' in c['categories'], countries)


def filter_eionet(countries):
    return filter(lambda c: 'eionet' in c['categories'], countries)


def filter_eun22(countries):
    return filter(lambda c: 'eun22' in c['categories'], countries)


def to_json(value):
    try:
        return json.dumps(value)
    except ValueError:
        return ''