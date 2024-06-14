# Social-Networking-API

Overview
-
This project is a social networking API built with Django and Django Rest Framework (DRF). It includes custom user authentication using email instead of username, and provides functionality for friend requests between users.

Features
-
-Custom user model with email authentication
-Friend request functionality (send, receive, accept)
-User search functionality
-JWT authentication for secure API access

Installation
-
Prerequisites
-Docker
-Docker Compose

Clone the Repository

Docker Setup
-
Build and run the Docker containers: docker-compose up --build
Create a Superuser
Once the containers are running, open a new terminal and run: docker-compose exec web python manage.py createsuperuser
Access the Application
The application should now be running at http://localhost:8000.

API Endpoints
-
Login and Signup
-POST api/signup
-POST api/login

Authentication
Obtain JWT Token
-POST /api/token/

User Search
-GET /api/users/search/?keyword=search_term

Send Friend Request
-POST /api/friend-requests/send/

View Received Friend Requests
-GET /api/friend-requests/received/

Accept Friend Request
-POST /api/friend-requests/accept/

Reject Friend Request
-POST /api/friend-requests/reject/
