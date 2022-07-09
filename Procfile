release: python manage.py migrate
web: daphne budget_django.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=budget_django.settings -v2
