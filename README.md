# zaba_prototype
**prototype ad site**


python manage.py compilemessages

create fixture:
./manage.py dumpdata auth.user --indent 2 > user.json
./manage.py loaddata user.json


`docker-compose -f "docker-compose.yml" up -d --build`

on Linux for start Elasticsearch > v.5
`sysctl -w vm.max_map_count=262144
`

check:
1. `manage.py check --deploy`
2. `pipdeptree`

Using django-extensions  for REST APIs or micro services 
`./manage.py runserver_plus --print-sql`
`./manage.py shell_plus --print-sql`