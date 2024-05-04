import pytest
import api
import sys


def test_bad_arguments(monkeypatch):
    monkeypatch.setattr(sys,'argv', ['api.py'])
    with pytest.raises(SystemExit):
        api.user_arguments()

    monkeypatch.setattr(sys,'argv', ['api.py', 'agmail.com', 'weatherstack'])
    with pytest.raises(SystemExit):
        api.user_arguments()
        
    monkeypatch.setattr(sys,'argv', ['api.py', '', 'weatherstack'])
    with pytest.raises(SystemExit):
        api.user_arguments()

    monkeypatch.setattr(sys,'argv', ['api.py', 'agmail.com', ''])
    with pytest.raises(SystemExit):
        api.user_arguments()
        
    monkeypatch.setattr(sys,'argv', ['api.py', 'agmail.com', 'weather'])
    with pytest.raises(SystemExit):
        api.user_arguments()
    

def test_good_arguments(monkeypatch):
    monkeypatch.setattr(sys,'argv', ['api.py', 'a@gmail.com', 'weatherstack'])
    mail, API_name = api.user_arguments()
    assert mail == "a@gmail.com"
    assert API_name == "weatherstack"
    
    
def test_incorrect_weather_message():
    incorrect_type_argument = "weather : 10"
    with pytest.raises(TypeError):
        api.create_weather_message(incorrect_type_argument)
    
def test_correct_weather_message():
    correct_type_argument = {
        "city" : "Vilnius",
        "country" : "Lithuania",
        "observation_time" : "11:00",
        "temperature" : "3",
        "feelslike" : "1"
    }
    message = api.create_weather_message(correct_type_argument)
    assert message == 'Hello, and thank you for using our services!\nToday in Vilnius, Lithuania we have 3°C. The temperature feels like 1°C. The observation time is 11:00.\nHave a lovely day!'
        
    
    
    
def test_missing_key_weather_message():
    missing_key_argument = {
        "city" : "Vilnius",
        "country" : "Lithuania",
        "observation_time" : "11:00",
        "temperature" : "3",
    }
    message = api.create_weather_message(missing_key_argument)
    assert message == "Key error, not enough information"
    