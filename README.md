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

    `python manage.py runserver`

6. Starting the worker process:

    `celery -A exchange_rates worker -l INFO` 

7. Start the celery beat service:

   `celery -A exchange_rates beat`

The app receives daily exchange rates for UAH-USD and UAH-EUR. 
But for tests, you can change the time in the `/exchange_rates/celery.py` by changing the value of the variable `time_period` 
(for example, execute every minute: `time_period = crontab()`).