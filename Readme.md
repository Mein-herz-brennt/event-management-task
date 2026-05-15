# Simple Calendar
### Event management task

### Setup
Before starting the project, please set up the .env file using the same structure as in .env.example .
```bash
git clone https://github.com/Mein-herz-brennt/event-management-task.git
cd event-management-task
docker compose up --build -d
```

### Access:

```copy
    http://localhost:8000/api/v1/docs/#/
```
### TODO
Develop a Django REST-Api for Event Management 
The primary goal of this task is to create a Django-based REST-Api 
that manages events (like conferences, meetups, etc.). The 
application will allow users to create, view, update, and delete events. 
It should also handle user registrations for these events. 
### Key Requirements:
- Design an Event model with fields such as title, description, 
date, location, and organizer. 
- Implement CRUD (Create, Read, Update, Delete) operations for 
the Event model. 
- Basic User Registration and Authentication. 
- Event Registration 
- API documentation 
- Docker 
- Readme file 
### Bonus Points: 
- Implement an advanced feature like event search or filtering. 
- Add a feature for sending email notifications to users upon event 
registration.

