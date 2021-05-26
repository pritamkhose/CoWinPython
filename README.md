# Cowin Python
Deploying a simple Flask app to the cloud via Heroku

# Install dependecies

```sh
python --version

pip install -r requirements.txt

or 
pip install flask

pip list
pip show flask
pip uninstall flask

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
| FLASK_ENV | Run flask enviorment-mode | development  |
| TZ | Time zone of server | Asia/Calcutta  |
| BASEURL | own server url  |  http://localhost:5000/  |
| CORSDOMAIN | mongo database name | ["http://localhost:3000", "https://..."]  |
| MONGOURL | mongo db server url | mongodb://usename:password@serverurl:27017/MONGODB?ssl=true&retryWrites=true  |
| MONGODB | mongo database name |   |


# References

* [Cowin WebApp](https://www.cowin.gov.in/home)

* [Cowin API](https://apisetu.gov.in/public/api/cowin)

