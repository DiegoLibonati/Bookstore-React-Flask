# Bookstore React Flask

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Join to `bookstore-app` folder and execute: `npm install` or `yarn install` in the terminal
3. Go to the previous folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

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

#### Dependencies

```
"react": "^18.2.0"
"react-dom": "^18.2.0"
"react-icons": "^4.4.0"
"react-scripts": "5.0.1"
"web-vitals": "^2.1.4"
```

#### devDependencies

```
"@types/jest": "^29.5.13"
"@types/react": "^18.3.11"
"@types/react-dom": "^18.3.1"
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.2"
"@testing-library/react": "^16.0.1"
"@testing-library/user-event": "^14.5.2"
"jest": "^29.7.0"
"jest-environment-jsdom": "^29.7.0"
"jest-fixed-jsdom": "^0.0.9"
"msw": "^2.4.11"
"ts-jest": "^29.2.5"
"typescript": "^4.9.5"
```

### Backend

#### Requirements.txt

```
Flask
flask_pymongo
```

#### Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/Bookstore-React-Flask`](https://www.diegolibonati.com.ar/#/project/Bookstore-React-Flask)

## Video

https://github.com/DiegoLibonati/Bookstore-Api-Rest-Page/assets/99032604/b9059c86-eecd-4e2f-a5c6-f891257cea32

## Testing

### Frontend

1. Join to `bookstore-app` folder
2. Execute: `yarn test` or `npm test`

### Backend

1. Join to the correct path of the clone and join to: `bookstore-server`
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`
