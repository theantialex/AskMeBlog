# AskMeBlog

This project was created as a final work for "Web Technology" course in Technopark. It serves as an example of a simple Q&A website.

Running
-------
Creating database template

    python manage.py migrate
    
Seeding database with faker data

    python manage.py filldb [--filldb={small, large, medium}] 

Running the website

    python manage.py runserver

Address
-------
  http://127.0.0.1:8000/
