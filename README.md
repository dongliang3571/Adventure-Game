Children and Parent Adventures
=============================

Demo Link
=========

https://adventuregame.herokuapp.com

<a href="http://adventuregame.herokuapp.com/adventure/"><img src="http://i.imgur.com/qsqU15x.png" /></a>
Technoloies are developing fast, humans can't live without smartphone and computers. But somehow we got too attached to these devices that we even spend more time on them rather than our families. But it's hard to get rid of this type of attachment, we want to make an app that can let you play with families. Here comes Children and Parent Adventures, this is initially designed for parents and chidren, it could be developed more for friends and more.
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
- Navigate to app directory, eg. *Adventure-Game/adventute_game*
- Type command:`pip install -r requirements.txt`
- Initial data is saved in a folder named fixtures in each app(eg. Adventure-Game/adventure_game/coreapp/fixtures/coreapp.json), run following command in terminal to import data to database:
```
python manage.py loaddata coreapp.json map.json
```

How to Run
==========
- Navigate to app directory, eg. *Adventure-Game/adventute_game*
- Type command:`python manage.py runserver`, note:change hosting address and port by doing: `python manage.py runserver 0.0.0.0:8000`
- Open browser and type address http://127.0.0.1:8000/ (this is default address and port, if you have've change them please go to your address and port)

Some Screenshots
================

<img src="http://i.imgur.com/8Hfbrid.png" >

<img src="http://i.imgur.com/KdjYLeB.png" >

<img src="http://i.imgur.com/EMXpYWZ.png" >

<img src="http://i.imgur.com/6ASPPxq.png" >
[python]: https://www.python.org/
[django]: https://www.djangoproject.com/
[post]: https://www.postgresql.org/
