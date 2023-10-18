## Hotel Management Contains Two App first for Customer Interaction second one for Management


## [Customer](customer/)


## [Management](management/)


## Installation
`pip install -r requirements/base.txt`


## DataBase Design (DB is Postgresql)

User Model has flag to differentiate between management user and customer called is_staff.
we have to model one for room and one for room_reservation.

## to run the tests

`python manage.py test`
