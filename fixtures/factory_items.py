import random as rand
from urllib import request
from faker import Factory
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from items.models import Item
from gifts.models import Gift
from jobs.models import Job
from rents.models import Rental


AUTHOR_ID = 2
local = ['en_US', 'uk_UA', 'ru_RU', 'pl_PL']
for loc in local:
    fake = Factory.create(loc)
    # items
    for i in range(5):
        image_url = fake.image_url(800,600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        item = Item(title=fake.catch_phrase(),
                    description=fake.text(),
                    author_id=AUTHOR_ID,
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
    for i in range(5):
        image_url = fake.image_url(800, 600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        gift = Gift(title=fake.catch_phrase(),
                    description=fake.text(),
                    gift_type=rand.randint(0, 4),
                    author_id=AUTHOR_ID,
                    point=Point((float(local_lat[0]), float(local_lat[1]))),
                    expires=fake.date_this_year(),
                    city=local_lat[2],
                    address=fake.street_address(),
                    local=loc[:2])
        gift.image.save(image_name, ContentFile(response.read()))

