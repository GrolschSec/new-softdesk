# SoftDesk API

## Project Overview
The SoftDesk API is a robust and secure backend solution developed as part of the OpenClassrooms project curriculum. It is designed to facilitate issue tracking and project management, primarily catering to software development teams and businesses in a B2B context. The API serves as a centralized platform for managing technical issues, projects, and user collaborations.

This RESTful API, built using the Django REST Framework, provides a suite of functionalities to support the creation, tracking, and management of various entities like projects, issues, and comments. It is engineered to be platform-agnostic, ensuring seamless integration with web, Android, and iOS applications.

## Features

    User Authentication (using JWT)
    Project Management (CRUD operations on projects)
    Issue Tracking (creating, updating, and managing issues within projects)
    Commenting System (adding and managing comments on issues)

## Technologies
Django REST Framework, JWT for authentication.

## Installation
Clone the repository:  

    git clone https://github.com/GrolschSec/softdesk.git

Navigate to the project directory:

    cd softdesk/

Create a virtual environment:

    python3 -m venv env

Activate the virtual environment on Linux/macOS:

    source env/bin/activate

Activate the virtual environment on Windows:

    env\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

## Configuration
Before running the server you'll need to apply the migrations to the database:

    python3 manage.py migrate

## Running the Application

Run the development server:

    python3 manage.py runserver

## API Documentation
You can find the postman API documentation on the following link:
    https://documenter.getpostman.com/view/27960725/2s93zE3KeA
