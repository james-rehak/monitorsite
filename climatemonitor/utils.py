# Helper Functions for Application


def convert_fahrenheit_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 1)

def convert_celcius_to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 1)