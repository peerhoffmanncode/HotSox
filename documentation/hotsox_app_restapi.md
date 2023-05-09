[Return to README.md](../README.md)

# HOTSOX "app_restapi"

The "app_restapi" of the HotSox Project contains all the API end-points for the entire project for possible future re-use of any 3rd party front-end applications.

## Django Rest Framework (DRF)

Django Rest Framework (DRF) is a powerful toolkit used to build APIs in Django. It provides a range of features, such as serialization, authentication, pagination, and much more. DRF is widely used in Django projects to create RESTful APIs quickly and easily.

## Implementation of DRF in the HotSox project

The HotSox project uses DRF to implement its user-related API endpoints. The file "serializers_users.py" contains the serializers for the User, UserMatch, and Sock models. Serializers in DRF are used to convert complex data types into native Python data types that can be easily rendered into JSON, XML, or other content types. Overall, DRF provides a powerful set of tools for building APIs in Django projects, and the serializers in serializers_users.py demonstrate the flexibility and ease of use of the toolkit.

## DRF Endpoints

The following URIs can be appended onto the root URL for both the Django Rest Framework (/api/v1/docs/ ) and FastAPI (/fastapi/v1/docs/) to access the desired endpoint.

| model             | endpoints                                                                           | create (POST) | retrieve<br>(GET) | update<br>(PUT) | delete<br>(DELETE) |
| ----------------- | ----------------------------------------------------------------------------------- | ------------- | ----------------- | --------------- | ------------------ |
| users             | users/<br>user/                                                                     | yes           | yes               | yes             | yes                |
| user profile pics | profilepic/<br>profilepic/{id}/                                                     | yes           | no                | no              | yes                |
| socks             | user/sock/<br>user/sock/{id}/                                                       | yes           | yes               | yes             | yes                |
| sock profile pic  | user/sock/{sock_id}/profilepic/<br>user/sock/{sock_id}/profilepic/{pic_id}/         | yes           | no                | no              | yes                |
| swipe             | user/swipe/{user_sock_id}/next/<br>user/swipe/(user_sock_id}/judge/{other_sock_id}/ | yes           | yes               | no              | no                 |
| matches           | user/matches/<br>user/match/{id}/                                                   | no            | yes               | no              | yes                |
| chats             | user/chats/<br>user/chats/{receiver}/                                               | yes           | yes               | no              | no                 |
| mail              | user/mail/<br>user/mail/{id}/                                                       | yes           | yes               | no              | yes                |

## Swagger

Swagger is a powerful framework that simplifies the process of documenting and exploring web APIs. It allows developers to describe API endpoints, request and response payloads, authentication mechanisms, and more in a structured and machine-readable format.
Swagger also provides tools and libraries to automatically generate client SDKs, server stubs, and API testing frameworks based on the API specification. By leveraging Swagger, you can streamline the API development process, improve collaboration between frontend and backend teams, and enhance the overall developer experience when working with your API.

With the use of Swagger, the HotSox project generated comprehensive API documentation that is both human-readable and interactive, making it easier for developers to understand and utilize our API.

> DRF HotSox Swagger endpoint is currently available while running the containerized application on your local host, at the following link [http://0.0.0.0/api/v1/docs/]

## Redoc

Redoc is a powerful tool designed to transform OpenAPI specifications into visually stunning and interactive API documentation. With Redoc, you can effortlessly create documentation that is not only informative but also aesthetically pleasing. It generates a clean and intuitive interface that allows developers to navigate through endpoints, view request and response examples, and understand the structure and functionality of the API.

Redoc focuses on providing a seamless user experience by offering features such as syntax highlighting, collapsible sections, interactive parameters, and response code snippets. It also supports various customization options, enabling you to tailor the documentation to match your brand or specific needs. By utilizing Redoc, you can present your API in a user-friendly manner, improving its adoption and making it easier for developers to integrate with our services.

> DRF HotSox Redoc endpoint is currently available while running the containerized application on your local host, at the following link [http://0.0.0.0/api/v1/redoc/]

## HotSox FastAPI module

For test purposes, HotSox CTO created also a FastAPI module:

[HotSox FastAPI documentation](hotsox_app_fastapi.md)
