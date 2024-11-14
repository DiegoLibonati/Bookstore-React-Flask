# Bookstore React Flask

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Go to the folder where you cloned your repository
3. Run `docker-compose build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose up`
5. You have to be standing in the folder containing the: `docker-compose.yml`

## Description

This time I made a page about a Bookstore. It is made with the following technologies:

1. The API-REST with flask, python, mongodb
2. The FRONT-END with React JS - Typescript

In which you can add books in the main section of the page with title, author, genre, description and an image. In addition you can visualize the loaded books that are stored in Mongo DB with the above mentioned features.

## Endpoints

1. Create a book
2. Get all books
3. Get book by genre
4. Delete book by ID
5. Get all genres
6. Error endpoint

## Technologies used

1. REACT JS
2. TYPESCRIPT
3. FLASK
4. PYTHON
5. CSS
6. MONGO DB

## Libraries used

### Frontend
1. @testing-library/dom
2. @types/jest
3. @types/react
4. @types/react-dom
5. msw
6. @testing-library/jest-dom
7. @testing-library/react
8. @testing-library/user-event
9. react-icons

### Backend

1. pytest
2. pytest-env
3. flask_pymongo

## Testing

### Frontend

1. Join to the correct path of the clone and join to: `bookstore-app`
2. Execute: `yarn install`
3. Execute: `yarn test`

### Backend

1. Join to the correct path of the clone and join to: `bookstore-server`
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Bookstore-React-Flask`](https://www.diegolibonati.com.ar/#/project/Bookstore-React-Flask)

## Video

https://github.com/DiegoLibonati/Bookstore-Api-Rest-Page/assets/99032604/b9059c86-eecd-4e2f-a5c6-f891257cea32
