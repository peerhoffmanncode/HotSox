# HotSox Web Application

## Welcome to HotSox! :P

The ultimate destination for sock enthusiasts and environmental crusaders.


### Introduction

Are you tired of constantly losing your favorite socks to the abyss known as the laundry machine? Are you sick of buying new socks only to have them disappear within a week? Well, my friend, you've come to the right place.
<br/><br/>

### Purpose

HotSox is a web application with a noble mission: to reunite lost socks with their rightful owners. We believe that every sock deserves a loving home and an equally loving match. Our state-of-the-art matching system utilizes advanced algorithms to connect sock owners with their missing mates. By keeping your socks together, you'll not only avoid the heartache of losing a sock but also contribute to saving the environment. Think about all the resources that go into making new socks. It's like a hug for the planet.
<br/><br/>

### Objective

Our objective is to connect people. We do this by letting people find their perfect match for one of their single socks.
Everybody needs a warm pair of socks, but what do you do if your pair of socks gets separated by losing one of the pair.
You need to find a new single socks for your lonely one - this is where HotSox comes to play.
<br/><br/>

### User Experience

Users can either use our prove of concept frontend application to create a user account, create a sock and start to find a new matching sock. The matching process is done via a swipe page where a user can decide if a shown sock might fit your own sock.
Once the user decides to like a sock, the user has to wait and hope, that the owner of the liked sock would also like the users sock too. If both owners of a socks decide to like each others sock you have a valid user match.
Once a match is set, the users are allowed to see each other's profile and can start a realtime chat.

Users can also use one of the provided API to build a customized frontend. As APIs we provide a FastAPI based api, or a Django Restframework based version.
<br/><br/>

### Feature overview of the App
Basic profile options
- option to create, edit and delete accounts user and depending sock accounts.
- ability to have many profile pictures for user and socks (stored on cloudinary CDN)

Matching System:
- Our cutting-edge algorithm ensures that no sock goes unpaired. Say goodbye to the days of mismatched socks and embrace a world of sock harmony.
- ability to swipe (like/dislike) socks
- see your current matches and view profiles of a matched user
- geo location detection and visualization via IP or specified city name
- realtime chat via websockets between matched users
- email notification about certain actions of a user or the system (e.g. new match detected)
<br/><br/>

### Future Development Features

- **AI base picture detection** of socks to define sock attributes.
- **Pub/Sub logic** to realize realtime notifications about matches, messages and so on.
- **Community Forum**: We're not just about socks; we're about community. Our website features a lively forum where sock enthusiasts can connect, share tips and tricks for keeping socks together, and even organize sock-themed meetups. Join the discussion and be a part of the sock revolution!
<br/><br/>

### Links to Feature's Documentation

- [homepage/swiping module](documentation/hotsox_app_home.md)
- [user/socks module](documentation/hotsox_app_user.md)
- [geolocalization module](documentation/hotsox_app_geo.md)
- [mail module](documentation/hotsox_app_mail.md)
- [chat module](documentation/hotsox_app_chat.md)
- [Django REST framework](documentation/hotsox_app_restapi.md)
- [FastAPI](documentation/hotsox_app_fastapi.md)
<br/><br/>

### Installation Notes

Pre-requisite: request the env file to our email address: hotsoxproject_at_gmail.com

To start using HotSox, simply follow these steps:

- clone the HotSox repository to your local machine.
- pip install -r requirements.txt to install dependencies
- python manage.py collect static
- user docker-compose up --build
- connect to the Django application by [http://localhost]
- connect to the Djnago Restframework API by [http://localhost/api/v1/docs]
- connect to the FastAPI by [http://localhost/fastapi/v1/docs]
<br/><br/>

### Testing

We rely on Unittesting in Django and FastAPI. Tests are done for methods of the ORM models and business logic (views)
<br/><br/>

### Deployment

Possible deployment platforms could be heroku, google cloud or aws.
<br/><br/>

### Technologies Used

- Python3:
  https://www.python.org

- Django:
  https://www.djangoproject.com

- Django Rest Framework:
  https://www.django-rest-framework.org

- FastAPI:
  https://fastapi.tiangolo.com

- Celery:
  https://docs.celeryq.dev/en/stable/

- CSS/bootstrap:
  https://getbootstrap.com/docs/4.0/components/card/#card-columns

- Redis:
  https://redis.io

- Postgres DB:
  https://www.postgresql.org

- Cloudinary:
  https://cloudinary.com/documentation/image_upload_api_reference#destroy_method

- Docker:
  https://www.docker.com

- Nginx:
  https://www.nginx.com
