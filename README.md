# !!!README!!! #

**requirements.txt**: Dependencies which you need to install in your computer.
run following command in terminal
```
pip install -r requirements.txt
```


**PostgresSQL**: Go to http://www.postgresql.org/ to download postgresSQL


Initial data(for example, math questions) is saved in adventure_game/map/migrations/0002_auto_2...0618.py, run
```
python manage.py migrate
```
will automatically import the data to database.