# HotSox with no boundaries

## Installation notes

[+] pip install -r requirements.txt to install dependencies

[+] python manage.py collect static

[+] user docker-compose up --build

[+] connect to the Django application by [http://localhost]

[+] connect to the Djnago Restframework API by [http://api/v1/docs]

[+] connect to the FastAPI by [http://fastapi/v1/docs]

## Repository

https://github.com/Python-E03/hot-sox-teamrando

## Objective

Our objective is to connect people. We do this by letting people find their perfect match for one of their single socks.
Everybody needs a warm pair of socks, but what do you do if your pair of socks gets separated by losing one of the pair.
You need to find a new single socks for your lonely one - this is where HotSox comes to play.

## User Experience

Users can either use our prove of concept frontend application to create a user account, create a sock and start to find a new matching sock. The matching process is done via a swipe page where a user can decide if a shown sock might fit your own sock.
Once the user decides to like a sock, the user has to wait and hope, that the owner of the liked sock would also like the users sock too. If both owners of a socks decide to like each others sock you have a valid user match.
Once a match is set, the users are allowed to see each other's profile and can start a realtime chat.

Users can also use one of the provided API to build a customized frontend. As APIs we provide a FastAPI based api, or a Django Restframework based version.

## Features

The main features of the APP are,

- user creation with the option to edit and delete accounts.
- ability to have profile pictures (as much as you want)
- sock profile creation with the option to edit and delete your own socks.
- ability to have profile pictures for a sock (as much as you want)
- geo location detection and visualization via IP or city name
- realtime chat via websockets
- email notification about certain cations of a user or the system
- ability to swipe (like/dislike) socks, see a users matches and view match profiles

### Future Features

- AI base picture detection of socks to define sock attributes
- Pub/Sub logic to realize realtime notifications about matches, messages and so on.
- Forum for users to stay in touch

## Technologies Used

We are based on Django/ Django Restframework or FastApi, PostgreSQL, Docker and Nginx.
As CDN we use Cloudinary

## Testing

We rely on Unittesting in Django and FastAPI. Tests are done for methods of the ORM models and business logic (views)

## Deployment

Possible deployment platforms could be heroku, google cloud or aws.

## Credits

Python3:
https://www.python.org

Django:
https://www.djangoproject.com

Django Rest Framework:
https://www.django-rest-framework.org

FastAPI:
https://fastapi.tiangolo.com

Celery:
https://docs.celeryq.dev/en/stable/

CSS/bootstrap:
https://getbootstrap.com/docs/4.0/components/card/#card-columns

Redis:
https://redis.io

Postgres DB:
https://www.postgresql.org

Cloudinary:
https://cloudinary.com/documentation/image_upload_api_reference#destroy_method

Docker:
https://www.docker.com

Nginx:
https://www.nginx.com
