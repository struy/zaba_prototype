import random as rand
from urllib import request
from faker import Factory
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from items.models import Item
from gifts.models import Gift, GiftType
from jobs.models import Job, JobType
from rents.models import Rental, PropertyType

AUTHOR_ID = 2
local = ['en_US', 'uk_UA', 'ru_RU', 'pl_PL']
for loc in local:
    fake = Factory.create(loc)
    # items
    for i in range(5):
        image_url = fake.image_url(800, 600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        item = Item(title=fake.catch_phrase(),
                    description=fake.text(),
                    author_id=AUTHOR_ID,
                    point=Point((float(local_lat[0]), float(local_lat[1]))),
                    expires=fake.date_this_year(),
                    city=local_lat[2],
                    address=fake.street_address(),
                    local=loc[:2],
                    # uniq
                    condition=rand.randint(0, 4),
                    price=rand.randint(1, 2000),
                    )
        item.image.save(image_name, ContentFile(response.read()))
    # jobs
    for i in range(5):
        image_url = fake.image_url(800, 600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        job = Job(title=fake.job(),
                  description=fake.text(),
                  author_id=AUTHOR_ID,
                  point=Point((float(local_lat[0]), float(local_lat[1]))),
                  local=loc[:2],
                  address=fake.street_address(),
                  city=local_lat[2],
                  expires=fake.date_this_year(),
                  # uniq
                  jobtype=JobType.objects.filter(pk=rand.randint(0, 4)),
                  duration=rand.randint(0, 3),
                  salary=rand.randint(1, 2000),
                  countries=rand.choice(['US', 'UA', 'RU', 'PL'])
                  )
        job.image.save(image_name, ContentFile(response.read()))
    # rents
    for i in range(5):
        image_url = fake.image_url(800, 600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        rent = Rental(title=fake.catch_phrase(),
                      description=fake.text(),
                      author_id=AUTHOR_ID,
                      point=Point((float(local_lat[0]), float(local_lat[1]))),
                      local=loc[:2],
                      address=fake.street_address(),
                      city=local_lat[2],
                      expires=fake.date_this_year(),
                      # uniq
                      property_type=PropertyType.objects.filter(pk=rand.randint(0, 4)),
                      bathrooms=rand.randint(1, 3),
                      bedrooms=rand.randint(1, 3),
                      pet_policy=rand.randint(0, 5),
                      furnished=bool(rand.getrandbits(1)),
                      prefer_sex=rand.choice(['a', 'w', 'm']),
                      price=rand.randint(1, 2000),
                      )
        rent.image.save(image_name, ContentFile(response.read()))
    # gifts
    for i in range(5):
        image_url = fake.image_url(800, 600)
        response = request.urlopen(image_url)
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        local_lat = fake.local_latlng()
        gift = Gift(title=fake.catch_phrase(),
                    description=fake.text(),
                    gift_type=GiftType.objects.filter(pk=rand.randint(0, 4)),
                    author_id=AUTHOR_ID,
                    point=Point((float(local_lat[0]), float(local_lat[1]))),
                    expires=fake.date_this_year(),
                    city=local_lat[2],
                    address=fake.street_address(),
                    local=loc[:2])
        gift.image.save(image_name, ContentFile(response.read()))
