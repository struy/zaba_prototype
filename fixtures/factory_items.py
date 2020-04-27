import random as rand
from urllib import request
from faker import Factory
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from items.models import Item


local = ['en_US', 'uk_UA', 'ru_RU', 'pl_PL']
for loc in local:
    fake = Factory.create(loc)
    for i in range(20):
        image_url = fake.image_url(width=800, height=600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower()+'.jpeg'
        local_lat = fake.local_latlng()
        item = Item(title=fake.catch_phrase(),
                    description=fake.text(),
                    owner_id=1,
                    point=Point((float(local_lat[1]), float(local_lat[0]))),
                    condition=rand.randint(0, 4),
                    price=rand.randint(1, 2000),
                    expires=fake.date(),
                    city=local_lat[2],
                    address=fake.street_address())
        item.image.save(image_name, ContentFile(response.read()))

        # Python3 save from folder
        # item.image.save('abc.png', File(open('/tmp/pic.png', 'rb')))



