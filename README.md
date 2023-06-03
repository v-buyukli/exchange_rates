# exchange_rates
____
**Get started**
- 
- Clone repository 
- Install requirements:

    `pip install -r requirements.txt`

- Migrate command:

    `python manage.py migrate`

- Run RabbitMQ on Docker:

    `docker run -d -p 5672:5672 rabbitmq` 

- Runserver command:

    `python manage.py runserver`

- Starting the worker process:

    `celery -A exchange_rates worker -l INFO` 

- Start the celery beat service:

   `celery -A exchange_rates beat`

The app receives daily exchange rates for UAH-USD and UAH-EUR.  
But for tests, you can change the time in the `/exchange_rates/celery.py` by changing the value of the variable `time_period`  
(for example, execute every minute: `time_period = crontab()`)