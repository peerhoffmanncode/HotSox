# HotSox with no boundaries 

## Installation notes (!! for deployment only !!)

run:
[+] pip install -r requirements.txt to install dependencies
[+] python manage.py collectstatic
[+] uvicorn hotsox_project.asgi:application --reload --host=0.0.0.0 --port=8000

## Repository

https://github.com/Python-E03/hot-sox-teamrando

## Objective

## User Experience

## Features

### Future Features

## Technologies Used

We are based on Django (4.1.7), PostgreSQL, and Docker.
We use Cloudinary as CDN host

## Testing

We rely on Unittesting in Django. Tests are done for methods of the ORM models and business logic (views)

## Bugs

### Resolved Bugs

### Remaining Bugs

## Deployment

Possible deployment platforms could be heroku, google cloud or aws.

## Credits

Python3:
https://www.python.org

Django:
https://www.djangoproject.com

Cloudinary:
https://cloudinary.com/documentation/image_upload_api_reference#destroy_method

CSS/bootstrap:
https://getbootstrap.com/docs/4.0/components/card/#card-columns

Postgres DB:
https://www.postgresql.org

Docker:
https://www.docker.com
