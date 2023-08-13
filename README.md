## Exchange Rates

### Daily Foreign Exchange Rates Fetching and Saving Service

- The app receives daily exchange rates for *UAH-USD* and *UAH-EUR*. 
- For tests, you can change the time in the `/exchange_rates/celery.py` by changing the value of the variable `time_period`
(for example, execute every minute: `time_period = crontab()`)
- Additionally, a view with a currency exchange calculator has been added.
Currencies from the database are used, with the best rate for the user.

### Getting Started

- Clone repository 
- Build and run your app with Compose:  
  `docker compose up`
- Enter in a browser to see the application running:  
  *http://localhost:8000/*

**Built With**: Python3, Django, Celery, Postgres, Docker Compose, and GitHub Actions.

**Note**: This repository is used for demonstration and testing purposes only.
