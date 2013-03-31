web: newrelic-admin run-program python src/manage.py runserver 0.0.0.0:$PORT --noreload --settings=nhl_sim.settings_heroku
worker: newrelic-admin run-program python src/manage.py celery worker --settings=nhl_sim.settings_heroku
