import sys
import re
import requests
import os
from dotenv import load_dotenv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


def main():
    email, API_name = user_arguments()
    password = os.environ.get("EMAIL_PASS")

    weather_params = {
        "access_key": os.environ.get("WEATHERSTACK_API_KEY"),
        "query": "Vilnius",
    }
    ip_params = {"access_key": os.environ.get("IPSTACK_API_KEY")}


    if API_name == "weatherstack":
        weather_response = weatherstack_response(weather_params)
        weather_message = create_weather_message(weather_response)
        send_email(weather_message, email, password)
    else:
        api_response = apistack_response(ip_params)
        ip_message = create_ip_message(api_response)
        send_email(ip_message, email, password)
        
    


def user_arguments():
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    APIs = ["weatherstack", "ipstack"]
    try:
        if len(sys.argv) == 3:
            mail = (sys.argv[1]).strip()
            API_name = sys.argv[2]
            if re.fullmatch(regex, mail) and API_name in APIs:
                return mail, API_name
            else:
                raise ValueError("Invalid email or API name. Please try again.")
        else:
            raise ValueError(
                "Incorrect number of arguments. Expecting exactly 2 additional command line arguments."
            )
    except ValueError as e:
        print("Error: ", e)
        sys.exit(1)


def weatherstack_response(params):
    response = requests.get("http://api.weatherstack.com/current", params)
    api_response = response.json()
    weather_info = {
        "city": api_response["location"]["name"],
        "country": api_response["location"]["country"],
        "observation_time": api_response["current"]["observation_time"],
        "temperature": api_response["current"]["temperature"],
        "feelslike": api_response["current"]["feelslike"],
    }
    return weather_info


def create_weather_message(info):
    if not isinstance(info, dict):
        raise TypeError("Expected 'info' to be a dictionary.")
    try:
        message = (
            f"Hello, and thank you for using our services!\n"
            f"Today in {info['city']}, {info['country']} we have {info['temperature']}°C. "
            f"The temperature feels like {info['feelslike']}°C. "
            f"The observation time is {info['observation_time']}.\n"
            "Have a lovely day!"
        )
    except KeyError:
        message = "Key error, not enough information"
    return message


def apistack_response(params):
    response = requests.get("http://api.ipstack.com/check", params)
    if response.status_code != 200:
        raise ValueError("Could not fetch weather data.")
    api_response = response.json()
    ip_info = {
        "ip": api_response["ip"],
        "continent": api_response["continent_name"],
        "country": api_response["country_name"],
        "city": api_response["city"],
    }
    return ip_info


def create_ip_message(info):
    message = (
        f"Hello and thank you for using our services!\n"
        f"Your IP address is {info['ip']}. Your current location: {info['continent']}, {info['country']}, {info['city']}"
    )
    return message


def send_email(message, receiver_email, email_pass):
    port = 465
    context = ssl.create_default_context()

    sender_email = "zskai83@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Hi there!'
    msg.attach(MIMEText(message, 'plain', 'utf-8')) 

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, email_pass)        
        server.send_message(msg)
        print("Email sent successfully!")


if __name__ == "__main__":
    main()
    
    
    
    
# Shift+tab
#ctrl+del
#ctrl+arrow up, down
#ctrl+f
#ctrl+d