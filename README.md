# Minimal Twitter API

This is a minimal API that replicates Twitter's API in a minimal way. Main functionalities are:

- Viewing, createing, and deleting tweets
- Filtering tweets based on various fields such as user, date, hashtags
- Replying tweets
- Liking tweets
- Following public profiles or sending follow requests to private profiles

## Future features

These features neither are implemented or being implemented. Aftering finishing the main functionalities that are mentioned periviously, these features will be added, too.

- Sending and recieving direct messages
- Blocking users
- Mentioning other profiles
- Adding media to tweets
- Retweeting

## How to run this project?

First create a file named _.env_. In this file you need a to create a variable called `SECRET_KRY` and set it to a random secret key.
To generate a random key you have two options:

- If you have [Django](https://www.djangoproject.com/) installed, import `get_random_secret_key` function from `django.core.management.utils` and invoke the function to get a random secret key.
- You can also use [Djecrety](https://djecrety.ir/) website to get a random secret key.

Both approaches work and if you perfer a simple way, use the seccond approach.

This project is dockerized. So in order to run it, you have to have [Docker](https://www.docker.com/) installed.

Clone the repository and cd into it. Now build and run the project by this command:

```shell
docker compose up --build
```

Visit `localhost:8000`.
