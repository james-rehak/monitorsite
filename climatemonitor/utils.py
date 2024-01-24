# Helper Functions for Application

import re

def convert_fahrenheit_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 1)

def convert_celcius_to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 1)

def is_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    return email is not None and re.fullmatch(regex,email)
