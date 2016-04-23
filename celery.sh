exec celery --app=experience.celery:app worker --loglevel=INFO 1>>/dev/null &
exec celery --app=experience.celery:app beat --loglevel=INFO 1>>/dev/null &
