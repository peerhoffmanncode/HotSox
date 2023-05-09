[Return to README.md](../README.md)

### MAIN FEATURE: Server side sending of emails
Folder: [django/app_home/]
<br/><br/>
The "app_mail" of the HotSox Project contains the functions to notify a user via email on:

- user profile registration.
- user profile deletion.
- match between two users.
- unmatching of a user.
<br/><br/>

### Description

The app_mail is a Email Notification System, a feature that sends email notifications to users for certain events that occur in the system.
It is build by integrating the Django enbedded email module to the distributed system of a 3rd party application called Celery.
We can briefly describe it as Django "sending email content" to Celery, meanwhile Celery actually is in charge of sending the email notification to the user.

More specifically, an email notification is sent when a user has a new match, when a match is deleted, or when an account is deleted.
<br/><br/>

### Purpose

The purpose of the Email Notification System is to provide users with real-time updates and confirmations
**new_match**
**match_deleted**
**account_deleted**
By receiving email notifications, users can stay informed and engaged in the use of the app, contacting new matches and also get confirmation that a match or account was successfully deleted.
<br/><br/>

### Technical Implementation

The Email Notification System is implemented using **Celery**, and the Django **send_mail()** function.

Specifically, the feature is defined as a Celery task using the **@shared_task()** decorator, which allows the task to be executed asynchronously in the background.

The _celery_send_mail()_ function takes four parameters: email_subject, email_message, recipient_list, and notification - the same as the original Django send_mail function plus notification.
When notification is True, the function calls the send_mail() function with the provided parameters to send an email notification to the specified recipients.
The User attribute "notification" will be True if the user has selected that they would like to get emails when signing up or when changing their profile.
<br/><br/>

### UI/UX

This feature does not have a user interface as it is triggered automatically by events in the system.
<br/><br/>

### Dependencies

The Email Notification System depends on Celery for Task Queueing and Redis as the message broker for Celery itself.
<br/><br/>

#### Celery

Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system.
It’s a task queue with focus on real-time processing, exible, and reliable distributed system to process vast amounts of messages, while providing operations wwhile also supporting task scheduling. Additional informations for Celery are available at the following link: [https://docs.celeryq.dev/en/stable/]
<br/><br/>

#### Redis

Redis is a powerful and versatile in-memory data store that allows developers to handle and process data in real-time applications with exceptional speed and efficiency. As an open-source solution, Redis provides a robust and scalable caching and message broker system that enhances the performance and responsiveness of applications. With Redis, developers can store and manipulate various data types, including strings, hashes, lists, sets, and sorted sets. Its in-memory nature enables rapid data access and retrieval, making it ideal for use cases that require low-latency and high-throughput operations. Redis also offers advanced features such as pub/sub messaging, transactions, and Lua scripting, allowing developers to build complex and sophisticated data processing pipelines. Additionally, Redis supports persistence options to ensure data durability and fault tolerance. Its simplicity, speed, and versatility make Redis a popular choice for caching, real-time analytics, task queuing, and other demanding use cases in modern application development. [https://redis.io/]
<br/><br/>

### Licenses

The licenses for this feature depend on the licenses of the tools used to implement it, which are Django, Celery, and Django's email module.
Django and Celery are both licensed under the BSD 3-Clause License, while Django's email module is licensed under the Python Software Foundation License. https://docs.celeryq.dev/en/stable/copyright.html
Redis is open source software released under the terms of the three clause BSD license. https://redis.io/docs/about/license/
