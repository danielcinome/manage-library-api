# MANAGE LIBRARY API

Manage Library API is an application that provides services to manage an online library, allowing the search of books in various sources. The application integrates external APIs, such as Google Books and New York Times Book, to enrich the internal database and offer a wide range of books to users.

## Contenido

1. [Main Features](#main-features)
2. [External Integrations](#external-integrations)
2. [Installation](#installation)
3. [How to Use](#how-to-use)
4. [Project Structure](#project-structure)
5. [Authors and Contact](#authors-and-contact)

## Main Features
- Search for books by different attributes (title, author, etc.).
- Integration with Google Books and New York Times Book to enrich the database.
- Creation and deletion of book records in the internal database.
- Interactive API documentation through Swagger.

## External Integrations
- Google Books API: [Documentation](https://developers.google.com/books/docs/v1/getting_started?hl=es-419)
- New York Times Book API: [Documentation](https://developer.nytimes.com/docs/books-product/1/overview)

## Instalación

Follow the instructions in the README.md file to install and run the project locally. API documentation will be available at http://localhost:8000/docs after execution.

1. **Clone the Repository:**

```bash
git clone https://github.com/danielcinome/manage-library-api.git
cd manage-library-api
```

2. **Virtual Environment Configuration (Optional, but recommended):**

```bash
python -m venv venv
source venv/bin/activate   # For Unix-based systems (Linux/Mac)
```

3. **Installs Units:**

```bash
pip install -r requirements.txt
```

4. **Environment Variables Configuration:**

```
SECRET_KEY
ALGORITHM                       # Use case -> HS256
ACCESS_TOKEN_EXPIRE_MINUTES
SQLALCHEMY_DATABASE_URL
GOOGLE_BOOKS_API_URL            # Google Book API
NY_TIMES_API_URL                # New York Times Book API
NY_TIMES_API_KEY                # New York Times Book API
```

* To obtain the Google Book API and New York Times Books API variables, please access the documentation. [External Integrations](#external-integrations)
* To generate the SECRET_KEY you can use:
    ```bash
    openssl rand -hex 32
    ```

5. **Initialize the Database:**


```bash
alembic revision --autogenerate -m "create tables" # To generate the first migration
alembic upgrade head
```

## How to Use

To execute the project use the command:

```bash
# Example of command or code
python runner.py
```

![F1-1](https://i.ibb.co/bJFzKJz/Captura-de-pantalla-2023-12-14-a-la-s-12-07-33-p-m.png)

To use the book creation and deletion services, authentication is required:

- `/books/create`
- `/books/delete/{uuid}`

To do this, if you do not have your own user, you must generate a registration from `/register`.

- Then click on Authorize:

    ![F2-1](https://i.ibb.co/VVjwHgd/Captura-de-pantalla-2023-12-14-a-la-s-12-07-33-p-m.png)

- Enter your authentication credentials, once authenticated you will be able to use the mentioned services.

    ![F2-2](https://i.ibb.co/5nNpVXh/Captura-de-pantalla-2023-12-14-a-la-s-12-34-58-p-m.png)


## Project Structure

The current structure of the project is organized as follows:

```plaintext
│── alembic/
│── app/
    │── api/
    │   │── books/
    │   │── users/
    │   │── common/
    │   │── integration/
    │       │── google_api.py
    │       │── ny_times.py
    │── db/
    │   │── postgres/
    │       │── connector.py
    │── models/
    │   │── models.py
    │── main.py
│── requirements.txt
│── README.md
│── runner.py
```

- **alembic/**: Contains files related to Alembic, a database migration tool for SQLAlchemy. It is used to manage changes in the database schema.
- **app/**: Main directory of the application source code.

  - **api/**: Contains modules that define the API paths.
    - **books/**: Paths and logic related to books management.
    - **users/**: Paths and logic related to user management.
    - **integration/**: Contains modules for external integrations.
      - `google_api.py`: Functionalities to interact with Google Books API.
      - `ny_times.py`: Functionalities to interact with the New York Times Books API.

  - **db/**: Contains modules related to database management.
    - **postgres/**: Contains `connector.py`, which implements the connection to a PostgreSQL database.

  - **models/**: Contains `models.py`, where the data models used in the application are defined.

  - `main.py`: Main entry point of the application.

- **requirements.txt**: File that lists the project dependencies.
- **README.md**: Main documentation of the project.
- `runner.py`: File to run or start the application.


## Authors and Contact
- Daniel Chinome
- Contact: danielchinomedev@gmail.com
- [LinkedIn](https://www.linkedin.com/in/danielchinome/)