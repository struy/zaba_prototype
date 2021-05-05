import random as rand
from urllib.error import URLError
from urllib import request
from faker import Factory
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from apps.items.models import Item
from apps.gifts.models import Gift, GiftType
from apps.jobs.models import Job, JobType
from apps.rents.models import Rental, PropertyType


def create_img(fake, model):
    try:
        image_url = fake.image_url()
        image_name = image_url.rsplit('.', 1)[1].lower() + '.jpeg'
        agent = str(fake.user_agent())
        print(agent)
        req = request.Request(
            image_url,
            data=None,
            headers={
                'User-Agent': agent
            }
        )
        response = request.urlopen(req)
        model.image.save(image_name, ContentFile(response.read()))
    except URLError:
        pass
    except Exception as err:
        pass


def start(count):
    author_id = 2
    local = ['en_US', 'uk_UA', 'ru_RU', 'pl_PL']

    for loc in local:
        fake = Factory.create(loc)
        # items
        for i in range(count):
            local_lat = fake.local_latlng()
            item = Item(title=fake.catch_phrase(),
                        description=fake.text(),
                        author_id=author_id,
                        point=Point((float(local_lat[0]), float(local_lat[1]))),
                        expires=fake.date_this_year(),
                        city=local_lat[2],
                        address=fake.street_address(),
                        local=loc[:2],
                        # uniq
                        condition=rand.randint(0, 4),
                        price=rand.randint(1, 2000),
                        )
            create_img(fake, item)

            # jobs
        for i in range(count):
            local_lat = fake.local_latlng()
            job = Job(title=fake.job(),
                      description=fake.text(),
                      author_id=author_id,
                      point=Point((float(local_lat[0]), float(local_lat[1]))),
                      local=loc[:2],
                      address=fake.street_address(),
                      city=local_lat[2],
                      expires=fake.date_this_year(),
                      # uniq
                      jobtype=JobType.objects.get(pk=rand.randint(1, 4)),
                      duration=rand.randint(0, 3),
                      salary=rand.randint(1, 2000),
                      countries=rand.choice(['US', 'UA', 'RU', 'PL'])
                      )
            create_img(fake, job)
            # rents
        for i in range(count):
            local_lat = fake.local_latlng()
            rent = Rental(title=fake.catch_phrase(),
                          description=fake.text(),
                          author_id=author_id,
                          point=Point((float(local_lat[0]), float(local_lat[1]))),
                          local=loc[:2],
                          address=fake.street_address(),
                          city=local_lat[2],
                          expires=fake.date_this_year(),
                          # uniq
                          property_type=PropertyType.objects.get(pk=rand.randint(1, 4)),
                          bathrooms=rand.randint(1, 3),
                          bedrooms=rand.randint(1, 3),
                          pet_policy=rand.randint(0, 5),
                          furnished=bool(rand.getrandbits(1)),
                          prefer_sex=rand.choice(['a', 'w', 'm']),
                          price=rand.randint(1, 2000),
                          )
            create_img(fake, rent)
            # gifts
        for i in range(count):
            local_lat = fake.local_latlng()
            gift = Gift(title=fake.catch_phrase(),
                        description=fake.text(),
                        gift_type=GiftType.objects.get(pk=rand.randint(0, 4)),
                        author_id=author_id,
                        point=Point((float(local_lat[0]), float(local_lat[1]))),
                        expires=fake.date_this_year(),
                        city=local_lat[2],
                        address=fake.street_address(),
                        local=loc[:2])
            create_img(fake, gift)
