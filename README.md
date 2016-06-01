Children and Parent Adventure
=============================
<a href="http://adventuregame.herokuapp.com/adventure/"><img src="http://i.imgur.com/qsqU15x.png" /></a>
Requirements
============

| Name |  Version |
| :--: | :---: |
| [Python][python] | 2.7.X |
| [Django][django] | 1.8.0 |
| [PostgreSQL][post] | 9.X |

Setup
=====
All Dependencies can be install through __requirements.txt__,
- navigate to app directory
- type command:`pip install -r requirements.txt`
- Initial data is saved in a folder named fixtures in each app(eg. Adventure-Game/coreapp/fixtures/coreapp.json), run following command in terminal to import data to database

###Step 1###
  
**requirements.txt**: Dependencies which you need to install in your computer.
run following command in terminal
```
python manage.py loaddata coreapp.json map.json
```


[python]: https://www.python.org/
[django]: https://www.djangoproject.com/
[post]: https://www.postgresql.org/
