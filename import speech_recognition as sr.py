import speech_recognition as sr
import pyttsx3
import datetime as dt
import pywhatkit as pk
import wikipedia as wiki
import smtplib
import requests
import json
import os

listener = sr.Recognizer()

speaker = pyttsx3.init()

# RATE
rate = speaker.getProperty('rate')  # getting details of the current speaking rate
speaker.setProperty('rate', 150)  # setting up a new voice rate

def speak(text):
    speaker.say('yes Boss. ' + text)
    speaker.runAndWait()

def speak_ex(text):
    speaker.say(text)
    speaker.runAndWait()

va_name = 'jarvis'

speak_ex('I am your ' + va_name + '. Tell me boss.')

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if va_name in command:
                command = command.replace(va_name + ' ', '')
                print(command)
                speak(command)

    except sr.UnknownValueError:
        print('Sorry, I did not get that. Please repeat.')
        return take_command()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return take_command()

    return command

def send_email(to, subject, message):
    # Configure your email settings here
    email_address = 'your_email@gmail.com'
    email_password = 'your_email_password'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        email_message = f'Subject: {subject}\n\n{message}'
        server.sendmail(email_address, to, email_message)
        server.quit()
        print('Email sent successfully.')
        speak('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        speak('Sorry, there was an error sending the email.')

while True:
    user_command = take_command()
    if 'close' in user_command:
        print('See you again boss. I will be there whenever you call me.')
        speak('See you again boss. I will be there whenever you call me.')
        break
    elif 'time' in user_command:
        cur_time = dt.datetime.now().strftime("%I:%M %p")
        print(cur_time)
        speak(cur_time)
    elif 'play' in user_command:
        user_command = user_command.replace('play', '')
        print('Playing ' + user_command)
        speak('Playing ' + user_command + '. Enjoy boss.')
        pk.playonyt(user_command)
        break
    elif 'search for' in user_command or 'google' in user_command:
        user_command = user_command.replace('search for', '')
        user_command = user_command.replace('google', '')
        speak('Searching for ' + user_command)
        pk.search(user_command)
    elif 'who is' in user_command:
        user_command = user_command.replace('who is', '')
        info = wiki.summary(user_command, 2)
        print(info)
        speak(info)
    elif 'send email' in user_command:
        speak('Sure, please provide the recipient, subject, and the message.')
        try:
            to = input('Recipient: ')  # You can replace this with voice recognition as well
            subject = input('Subject: ')
            message = input('Message: ')
            send_email(to, subject, message)
        except Exception as e:
            print(f'Error in email input: {str(e)}')
            speak('Sorry, there was an error in the email input.')
    elif 'set reminder' in user_command:
        speak('Sure, please provide the reminder details.')
        try:
            reminder_time = input('Reminder time (format HH:MM AM/PM): ')
            reminder_message = input('Reminder message: ')
            # You can add logic to set reminders here
            print(f'Reminder set for {reminder_time}: {reminder_message}')
            speak(f'Reminder set for {reminder_time}: {reminder_message}')
        except Exception as e:
            print(f'Error in reminder input: {str(e)}')
            speak('Sorry, there was an error in the reminder input.')
    elif 'weather' in user_command:
        speak('Sure, please provide the city name for weather updates.')
        try:
            city = input('City: ')  # You can replace this with voice recognition as well
            weather_api_key = 'your_weather_api_key'
            weather_url = f'https://openweathermap.org/city/1264527'
            response = requests.get(weather_url)
            weather_data = json.loads(response.text)
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
            print(f'Temperature: {temperature}K, Description: {weather_description}')
            speak(f'Temperature: {temperature} Kelvin, Description: {weather_description}')
        except Exception as e:
            print(f'Error in weather input: {str(e)}')
            speak('Sorry, there was an error in the weather input.')
    elif 'who are you' in user_command:
        speak_ex('I am your ' + va_name + ', Tell me boss.')
    else:
        speak_ex('Please say it again')
