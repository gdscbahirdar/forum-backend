# BiT-Forum Backend

Welcome to the BiT-Forum Backend repository! This project serves as the backend for an online forum dedicated to the Bahir Dar Institute of Technology (BiT), built using Django REST framework.

## Purpose

We built is as part of our final-year project but we wanted to open-source it to foster collaboration and learning among BiT students and teachers. By contributing to this project, students can gain hands-on experience with real-world software development and help enhance the forum with new features and improvements.

## Vision

We envision this forum to be a comprehensive platform for students and teachers to engage in discussions, share resources, and collaborate on projects. Your contributions can help make this vision a reality, whether by adding new features, improving existing functionality, or fixing bugs.

## Features

- Role-based access control for students, teachers, and faculty admins of the university.
- Question and answer platform with features to upvote, downvote, comment, etc.
- Resource sharing. You can share files, assignments, notes, links etc.
- Reward system through badges and reputation. Similar to StackOverflow.
- Notification updates.
- AI assistant and AI-driven profanity checks.

## Technologies Used

- Django
- Django REST framework
- PostgreSQL

## Quick Start

First Clone this repository to your local machine and create a `.env` file. Copy the contents of `.env.example` file found in the root directory of the project to `.env` and update the environment variables accordingly. Then you can start the project by following the commands below:

1. Create a Python virtual environment and activate it.
2. Open up your terminal and run the following command to install the packages used in this project.

```shell
$ pip install -r requirements.txt
```

3. Set up a Postgres database for the project.
4. Run the following commands to setup the database tables and create a superuser.

```shell
$ python manage.py migrate
$ python manage.py createsuperuser
```

5. Start the development server:

```shell
$ python manage.py runserver
```

## API Documentation

API documentation is provided using redoc. You can access the documentation at http://localhost:8000 once the server is running.

## Contributing

We welcome the BiT community to contribute to this project whether that is providing new features or bug fixes. Please see our CONTRIBUTING.md for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/gdscbahirdar/forum-backend/blob/master/LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue or contact the project maintainers.

Thank you for using BiT-Forum Backend! Happy coding!
