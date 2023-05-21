[Return to README.md](../README.md)

## System Architecture
<br/>

### Description and technical implementation
<br/>

#### Design:
The project's system architecture is based on using Docker, Nginx, Python Frameworks, Celery as a concurrent background worker, and databases like Redis and PostgreSQL. All sensitive data, such as credentials or system-wide constants, are stored in a centralized environment variable file (.env). This file is not part of the public repository and must be requested from the authors or set up with your own credentials to ensure the application functions as expected.
<br/><br/>

#### Description and Implementation:
The application and all its services are designed to be started as individual Docker containers. There is an Nginx container, two containers for the main Python frameworks (Django together with DRF and FastAPI). Each framework requires its own background worker (Celery) and corresponding Redis database. Additionally, there is a main database that utilizes PostgreSQL, resulting in a total of 8 containers. To provide a convenient user experience, the project includes a docker-compose.yml file that simplifies the startup process. This YAML file configures dependencies between services, sets up data volumes for persistent databases, and manages the exposed ports.
To run the application, use the command: $ docker-compose up --build.
<br/><br/>
### Schema
![hotsox_architecture](pics/system_architecture/architecture-diagram.png)
<br/><br/>
#### Services and their purpose:
<br/>

##### NGINX:
Nginx is a high-performance, open-source web server and reverse proxy server. It efficiently handles HTTP, HTTPS, and other network protocols. Nginx's key strength lies in its ability to handle concurrent connections with low memory usage, making it suitable for serving large-scale websites and applications. In this project, Nginx is configured as a reverse proxy, receiving client requests and forwarding them to backend services. It acts as an intermediary between clients and application services within the Docker Compose structure.
<br/><br/>

##### PYTHON FRAMEWORKS:
The project is based on Python 3.11.x and embraces modern approaches in the Python ecosystem. The main full-stack framework chosen is Django (4.x), which is used for rendering HTML sites. In addition to Django, the project supports two different API services: FastAPI and Django Rest Framework (DRF). Both APIs serve the same purpose and act as the main resources for developers to interact with the application, particularly when writing their own frontend. The APIs e.g. support basic CRUD operations for users, socks, swiping, and matching.
<br/><br/>

##### BACKGROUND WORKERS AND BROKER:
Celery is a distributed task queue system for Python and serves as a concurrent background worker in this project. Each Python framework instance is accompanied by a Celery instance, which handles tasks such as sending emails. These tasks can be computationally intensive and may potentially block the framework from executing further user requests. By employing a concurrent background worker like Celery, the frameworks are freed up, resulting in a better user experience. Communication between the Python frameworks and their corresponding Celery instances is facilitated by a broker pipeline, which, in this case, is a Redis database. Tasks are stored in the Redis database and picked up by the background worker. The results of the computations can also be sent back to the frameworks through the broker, if needed.
<br/><br/>

##### SQL DATABASE:
This application uses PostgreSQL as its main database. PostgreSQL is a highly performant and open-source SQL database that fulfills all the technical requirements of the project. The database service, along with all other services, runs as a Docker container. To ensure data persistence, a storage folder (./data) is configured to store any transactions during execution on the systems harddrives.
<br/><br/>

##### DEPLOYMENT:
The current design allows users to deploy the entire architecture in a single location, whether it's on a virtual machine (VM) or a physical machine. If the need arises to distribute services across different resources, such as multiple VMs, it can be achieved by configuring a custom Docker structure. Since the application components are encapsulated within Docker containers, this process is relatively straightforward and should be easily achievable.
<br/><br/>



## Licenses/ Dependencies:
- Docker  (https://www.docker.com)
- Nginx (https://www.nginx.com)
- Django (https://www.djangoproject.com)
- FastAPI  (https://fastapi.tiangolo.com)
- Celery  (https://docs.celeryq.dev/en/stable/)
- Redis (https://redis.io)
- PostgreSQL (https://www.postgresql.org)
