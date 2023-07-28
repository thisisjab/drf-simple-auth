from django.core import validators


class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w](?!.*?\.{2})[\w.]{1,28}[\w]$'
    flags = 0
    message = 'Enter a valid username. Only a-z, 0-9, _, and . is allowd.'
