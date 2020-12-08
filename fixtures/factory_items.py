import random as rand
from urllib import request
from faker import Factory
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from items.models import Item

local = ['en_US', 'uk_UA', 'ru_RU', 'pl_PL']
for loc in local:
    fake = Factory.create(loc)
    # items
    for i in range(100):
        image_url = fake.image_url()
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        item = Item(title=fake.catch_phrase(),
                    description=fake.text(),
                    author_id=1,
                    point=Point((float(local_lat[0]), float(local_lat[1]))),
                    condition=rand.randint(0, 4),
                    price=rand.randint(1, 2000),
                    expires=fake.date_this_year(),
                    city=local_lat[2],
                    address=fake.street_address(),
                    local=loc[:2])
        item.image.save(image_name, ContentFile(response.read()))
    # jobs  fake.job()
    # rents
    # gifts

