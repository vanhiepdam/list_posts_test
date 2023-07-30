## Problem
Build a website that will list all posts in the system. The website should have the following
features:
1. List all posts in the system
1. Have pagination for the list of posts
1. Allow users to select the number of posts per page
1. Each post must have the following information:
    - Title
    - Author nickname
    - Preview of the most recent comment: Should be the first 8 words of the comment. Empty if there is no comment

## Technical requirements

1. Using django for the website UI and django-rest-framework for the API
1. Using ajax to load data
1. No test data will be provided. Need to create your own test data
1. While loading data, the website should be run smoothly without flashing
1. No authentication required


## Solutions

**Backend**
- Create a Django project with 2 apps: post and user_profile
- post app will be used to manage posts and comments, user_profile app will be used to manage users. Override default user model of django by User model in user_profile app in order to be easy to extend in the future
- Author of post will be stored in `user_profile` app as User model instance
- Each post will have a list of comments
 
**Models (main fields)**

**Post model**

| Column        | Type                        |
|---------------|-----------------------------|
| id            | int. auto increment         |
| title         | varchar(255)                |
| author_id     | integer. foreign key (User) |
| created_at    | datetime                    |
| created_by_id | integer. foreign key (User) |

**Comment model**

| Column       | Type                        |
|--------------|-----------------------------|
| id           | int. auto increment         |
| post_id      | integer. foreign key (User) |
| content      | text                        |
| created_at   | datetime                    |
| posted_by_id | integer. foreign key (User) |

Biggest problem:
- To get the most recent comment for each post, it would be not efficient to get all comments of all posts and then get the most recent comment for each post due to the number of comments can be very large, and Django performance will be affected. 
- Therefore, I will use a subquery to get the most recent comment for each post. The subquery will be used in the main query to get all posts. The subquery will be executed for each post in the main query. Check it out in `PostManager` class in `post/models.py` file
- In case there are too many comments for a post, the subquery will be slow and if it affects the performance of the api, we can consider to use a cache the last comment in a Post as a column. If put in this way, we have to handle to remove cache when user update/delete/create comments and concurrent comments updated. Harder problem and we can use the subquery first and see how it goes. Performance should be monitoring and optimised later if needed

## What I completed

1. API list posts v1 (included swagger api doc). Supported client control page size and pagination already
1. Admin UI for managing data
1. Set of unit tests
1. Documentation on how to deploy the application
1. Documentation on how to use the application
1. CI/CD pipeline with Github action
1. Dockerize application in order to run in local machine and deploy to cloud
1. Deploy application to the cloud to be easy to verify the project

## Assumptions

- Max number of results per page is 100
- Default number of results per page is 10
- Default page is 1
- Default order by of posts is created_at desc
- Default order by of comments is created_at desc

## Documentation

### Live Usage

To see the result: [List post page](http://18.183.204.247:8386)

To test the API, you can checkout
this [API Swagger Documentation](http://18.183.204.247:8386/api-doc) and interact with the API
directly on the Swagger UI.

Also, you can go to the [Django admin site](http://18.183.204.247:8386/admin) to manage the data such as create, update, delete posts and comments.

Django admin credentials:

```
account/password: admin/admin
```

### Tech stack

- [python-3.10](https://www.python.org/) for building backend application
- [Django 4.2.3](https://www.djangoproject.com/) for building web application
- [django-rest-framework 3.14.0](https://www.django-rest-framework.org/) for building RESTful API
- [PostgreSQL 14.8]() for storing data
- [pytest]() for testing
- [Docker](https://www.docker.com/) for containerization and deployment
- [poetry](https://python-poetry.org/) for dependency management
- [Makefile](#) for automating tasks and centralizing commands
- [Flake8](#) for linting
- [Black](#) for formatting
- [isort](#) for sorting imports
- [mypy](#) for type checking
- [safety](#) for checking security vulnerabilities in dependencies
- [GitHub Action](#) for CI/CD

### Installation on local machine

#### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)
- This guidance has been tested on MacOS (Intel chip) only

#### Steps
Main branch: `main`

1. Clone the repository

```shell
git clone git@github.com:vanhiepdam/list_posts_test.git

cd list_posts_test
```
**Notes**: If it raises permission denied issue, please login to your github account and try again


2. Create a `.env` file in the root directory of the project and fill in the environment variables

```shell
cp .env.template .env
vim .env

SECRET_KEY=3a677a%h+t_*kwr)
DEBUG=true
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DATABASE_NAME=list_post_test
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
APP_PORT=8000
HOST_DB_PORT=5432
```

3. Build the docker image

```shell
make build
```

4. Run the docker container

```shell
make up
```

**Notes**: For the first run, it will be failed due to postgresdb unhealthy. Just retry the command

5. Checkout the website at [http://localhost:8000](http://localhost:8000/). Data will be seeded
   automatically

6. While spawning up the backend server, it already created a super admin for you by default. To
   login into the admin site, you can use the following credentials:

```
account/password: admin/admin
```

#### API Documentation

Once the backend server is up and running, you can checkout the API documentation
at [http://localhost:8000/api-doc](http://localhost:8000/api-doc)

### Deployment

This project was set up to be deployed on an AWS EC2 instance using Docker and Docker Compose.

The process of deployment is automated by GitHub Action

1. Create a new branch for new feature
2. Push the code to the new branch
3. Create a pull request to merge the new branch to the main branch. CI will be triggered
   automatically, merge will be blocked if CI failed or running
4. Once the CI was successfully, dev can merge it to the main branch. CD will be triggered
   automatically
5. To see the unit tests coverage report, you can check out at GitHub Action log of the project
