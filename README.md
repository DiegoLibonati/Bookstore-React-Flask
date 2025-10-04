# Bookstore React Flask

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Join to `bookstore-app` folder and execute: `npm install` or `yarn install` in the terminal
3. Go to the previous folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development (Python)

NOTE: Install **pre-commit** inside: `bookstore-server` folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

This time I made a page about a Bookstore. It is made with the following technologies:

1. The API-REST with flask, python, mongodb
2. The FRONT-END with React JS - Typescript

In which you can add books in the main section of the page with title, author, genre, description and an image. In addition you can visualize the loaded books that are stored in Mongo DB with the above mentioned features.

## Technologies used

FrontEnd:

1. React
2. Typescript
3. CSS3
4. HTML5
5. Vite

BackEnd:

1. Python -> Flask

Deploy:

1. Docker
2. Nginx
3. Gunicorn

Database:

1. MongoDB -> PyMongo

## Libraries used

### Frontend

#### Dependencies

```
"react": "^18.2.0"
"react-dom": "^18.2.0"
"react-icons": "^4.4.0"
"web-vitals": "^2.1.4"
```

#### devDependencies

```
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.2"
"@testing-library/react": "^16.0.1"
"@testing-library/user-event": "^14.5.2"
"@types/jest": "^29.5.13"
"@types/node": "^20.10.6"
"@types/react": "^18.3.11"
"@types/react-dom": "^18.3.1"
"@vitejs/plugin-react": "^5.0.2"
"jest": "^29.7.0"
"jest-environment-jsdom": "^29.7.0"
"jest-fixed-jsdom": "^0.0.9"
"msw": "^2.4.11"
"ts-jest": "^29.2.5"
"ts-node": "^10.9.2"
"typescript": "^4.9.5"
"vite": "^7.1.7"
```

### Backend

#### Requirements.txt

```
Flask==3.1.2
Flask-PyMongo==3.0.1
pydantic==2.11.9
gunicorn==23.0.0
pre-commit==4.3.0
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
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

### **Version**

```ts
APP VERSION: 0.0.1
README UPDATED: 28/09/2025
AUTHOR: Diego Libonati
```

### **Env Keys**

1. `TZ`: Refers to the timezone setting for the container.
2. `VITE_API_URL`: Refers to the base URL of the backend API the frontend consumes.
3. `MONGO_URI`: Refers to the connection URI for the MongoDB database, including user, password, host, port, database name, and auth source.
4. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
5. `PORT`: Refers to the port on which the backend API is exposed.

```ts
# Frontend Envs
TZ=America/Argentina/Buenos_Aires

VITE_API_URL=http://host.docker.internal:5050

# Backend Envs
TZ=America/Argentina/Buenos_Aires

MONGO_URI=mongodb://admin:secret123@bookstore-db:27017/bookstore?authSource=admin

HOST=0.0.0.0
PORT=5050
```

### **Bookstore Endpoints API**

---

- **Endpoint Name**: Get Books
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/books/
- **Endpoint Fn**: This endpoint obtains all the Books
- **Endpoint Params**: None

---

- **Endpoint Name**: Get Books by Genre
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/books/:genre
- **Endpoint Fn**: This endpoint obtains all the Books
- **Endpoint Params**: 

```ts
{
  genre: string;
}
```

---

- **Endpoint Name**: Get Books All Genres
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/books/genres
- **Endpoint Fn**: This endpoint obtains all the Genres
- **Endpoint Params**:  None

---

- **Endpoint Name**: Create Book
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/books/
- **Endpoint Fn**: This endpoint create a new Book
- **Endpoint Body**:

```ts
{
    title: string;
    description: string;
    author: string;
    image: string;
    genre: string;
}
```

---

- **Endpoint Name**: Delete Book
- **Endpoint Method**: DELETE
- **Endpoint Prefix**: /api/v1/books/:id
- **Endpoint Fn**: This endpoint deletes a Book by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

## Known Issues