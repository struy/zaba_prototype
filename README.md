# zaba_prototype
prototype ad site


python manage.py compilemessages


create fixture:
./manage.py dumpdata auth.user --indent 2 > user.json
./manage.py loaddata user.json
## docker
if you use docker please change "localhost" to "redis" (connection to Redis)
docker-compose -f "docker-compose.yml" up -d --build



