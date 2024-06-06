# Info
This package contains the backend processing for the my-recipes application, this is a flask program

This includes:
Scraping a web-page provided by the end user from the front-end
Isolating ingredients and instructions from web data filtering out lists
Interpreting the list sets into ingredients or instructions, 
by creating a likelyhood coefficient and comparing agains a threshhold
Creating a recipe in the database based on this information

Generating pdf files based on either recipes or the shopping list function 
and emailing these pdf's to a specified email

The files used to create  this includes a csv file containing a set of training data, the 

# Installation



Create a .env file with the following variables
DATABASE
USER
PASSWORD
HOST
SENDER_EMAIL
EMAIL_PASSWORD
RECEIVER_EMAIL

The first 4 of these are for the database, and will require a postgres database like the front end
the next 3 will be required to send pdf emails
To setup the sender email with a gmail account try this video: 
[https://www.youtube.com/watch?v=g_j6ILT-X0k]

# Run
```bash
flask --app board/__init__ run
```

make sure the server is running on on [http://127.0.0.1:5000]