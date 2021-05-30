# Cowin Python
Deploying a simple Flask app to the cloud via Heroku

# Install dependecies

```sh
python --version

pip install -r requirements.txt
```

# Run server

```sh
python app.py
```

You should be able to run this app on your own system via the familiar invocation and visiting [http://localhost:5000](http://localhost:5000).

## Set env config variable  

| name | Description | e.g. |
| --- | --- | --- |
| DEBUG | Run flask development-mode | True or False  |
| JOBRUN | Run Scheduler jobs function | True or False  |
| FLASK_ENV | Run flask enviorment-mode | development  |
| TZ | Time zone of server | Asia/Calcutta  |
| BASEURL | own server url  |  http://localhost:5000/  |
| CORSDOMAIN | mongo database name | ["http://localhost:3000", "https://..."]  |
| MONGOURL | mongo db server url | mongodb://usename:password@serverurl:27017/MONGODB?ssl=true&retryWrites=true  |
| MONGODB | mongo database name |   |


# References

* [Cowin WebApp](https://www.cowin.gov.in/home)

* [Cowin API](https://apisetu.gov.in/public/api/cowin)

* [stackoverflow 403](https://stackoverflow.com/questions/67498285/403-response-code-request-blocked-when-using-cowin-setu-apis)

* [APScheduler Example](https://github.com/r3ap3rpy/python/blob/master/flasksched/scheduled.py)
