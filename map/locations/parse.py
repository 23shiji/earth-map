import csv
import os
import yaml
import re
from crypt import crypt

def item(name_zh, name_en, lng, lat, tags, description):
    name = name_en.replace(' ', '_').lower() or name_zh.encode("idna").decode('ascii')
    desc_fp = f'descriptions/{name}.md'
    open(desc_fp, 'w').write(description)
    return dict(
        name=f'{name_zh}<br/>{name_en}',
        pos = dict(
            lng=lng,
            lat=lat
        ),
        template='city',
        tags = tags,
        desc = f'map/locations/{desc_fp}'
    )

def parse_pos(s):
    print(s)
    lat, lng = re.split(r'[ ,，]+', s)
    return float(lng), -float(lat)


def parse_tags(s, desc):
    tags = [
        w
        for w in s.split('|')
        if w
    ]
    if any('首都' in w for w in desc):
        tags.append('首都')
    return tags

def parse_description(desc, old):
    if old != '√' and old != '' and old != '无':
        desc += f"旧称: {old}\n\n"
    return desc

reader = csv.reader(open("cities.csv"))
next(reader)

data = [
    item(name_zh, name_en, *parse_pos(position), parse_tags(tags, description), parse_description(", ".join(description), old_name))
    for name_zh, name_en, position, tags, old_name, *description in reader
]

print(data)

yaml.dump(data, open('index.yaml', 'w'), allow_unicode=True)