Children and Parent Adventure
=============================
<a href="http://adventuregame.herokuapp.com/adventure/"><img src="http://i.imgur.com/qsqU15x.png" /></a>
Requirements
============

| Name |  Version |
| :--: | :---: |
| [Python][ruby] | 2.7.X |
| [Django][rails] | 1.8.0 |

All Dependencies can be install through __requirements.txt__,
- navigate to app directory
- type command:
```
pip install -r requirements.txt
```

###Step 1###
  
**requirements.txt**: Dependencies which you need to install in your computer.
run following command in terminal
```
pip install -r requirements.txt
```


**PostgresSQL**: Go to http://www.postgresql.org/ to download postgresSQL


Initial data is saved in a folder named fixtures in each app(eg. coreapp/fixtures/coreapp.json)

run following command in terminal to import data to database
```
python manage.py loaddata coreapp.json map.json
```


Our site link is https://adventuregame.herokuapp.com
