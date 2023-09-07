# DRF Auth  

In this project I've implemented a regular authentiaction system using DRF. Current features:

- Sign up using email validation
- Requesting email validation email with timeoouts
- Login using JWT token
- Reset password

__Note__: This project is not maintained any further.

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
