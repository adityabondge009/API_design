# API_design
PROJECT README

This project is a FastAPI-based REST API that provides access to Gutenberg book data stored in a PostgreSQL database. It supports filtering by book ID, language, MIME type, author, title, and topic, along with pagination. The API returns structured JSON responses similar to Gutendex, including book details, authors, subjects, bookshelves, and download links.

OVERVIEW:
This project contains a Python script named "main.py".
It has been developed to run inside a Python virtual environment to avoid system-level package conflicts. The project is executed using Uvicorn, which runs the FastAPI application.

REQUIREMENTS:

Python 3.x installed on the system

Virtual Environment (venv)

Required Python packages:

fastapi

uvicorn

sqlalchemy

psycopg2

SETUP AND INSTALLATION STEPS:

Open terminal and go to project directory

Create a virtual environment using:
python3 -m venv venv

Activate the virtual environment:
source venv/bin/activate

Install required packages:
pip install fastapi uvicorn sqlalchemy psycopg2

RUNNING THE APPLICATION:

Make sure virtual environment is activated

Run the following command:
uvicorn main:app --reload

The server will start on:
http://127.0.0.1:8000

NOTE:
If you directly open the above link, you may get 404 if root path is not defined in the application.
Use correct API endpoints that are defined inside main.py.

PROJECT STRUCTURE:
main.py -> FastAPI application file
venv/ -> Virtual environment directory
README -> Project documentation file

ADDITIONAL NOTES:

Do not use pip globally in Ubuntu system environments because of PEP 668 restrictions.

Always use virtual environments for Python development.

Stop the server using CTRL + C.

AUTHOR:
Aditya Bondge
