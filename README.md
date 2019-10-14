# RSS READER

Users can register, login in and add multiple rss links.

### Quick explanation

Written in python 3.7, using tornado, postgres and redis.

## Libs used

- tornado, web framework
- momoko,  Psycopg2’s wraper for Tornado
- aiosmtplib, async smtp client
- aiosmtpd, async smtp server
- bcrypt, password hashing
- defusedxml, XML library
- xmlschema, xml schema validation
- aioredis, async redis library

## How to run

### Requirements

- Docker 
- Docker Compose

### Config file

- Copy/Rename ```/app/config/config.json.dist``` to ```/app/config/config.json```
- Remove settings comments.
- If you change port and host settings change them accordingly in docker and docker-compose files

### Running

- Run ```docker-compose up -d --build; docker-compose logs -f app``` to see the email sent from the debug email server.

## How to use

- Enter user name and password, click register
- If using default setup it should display debug email in the console.
- Refresh the page and you will be redirected back to login
- Enter user name and password, click login
- Add your rss xml links

## TODO

- Better error handling
- Logging
- Using transactions instead of multiple queries
- Feed Refresh functionality
- Better xml parsing
- Nicer front end
