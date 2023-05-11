[Return to README.md](../README.md)

# HotSox Project - System Architecture

## Schema

![hotsox_architecture](pics/system_architecture/architecture-diagram.png)

<br>

## Environment Variables (.env file)

<br/>

### Description

The purpose/aim of the feature is to provide a centralized location for all configurable parameters and settings for the project. This makes it easy to manage and change these settings without having to go through the codebase.

<br/>

### Technical implementation

The .env file is a plain text file that stores all the environment variables for the project. These variables are loaded into the project using the dotenv library, which reads the _.env_ file and sets the environment variables.
