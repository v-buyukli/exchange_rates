# exchange_rates
____
**Get started**

1. Clone repository
2. Install requirements:

    `pip install -r requirements.txt`

3. Migrate command:

    `python manage.py migrate`

4. Run RabbitMQ on Docker:

    `docker run -d -p 5672:5672 rabbitmq` 

5. Runserver command:

    `python manage.py runserver`,

6. Starting the worker process:

    `celery -A python_pro_task9 worker -l INFO` 

7. Start the celery beat service:

   `celery -A exchange_rates beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`