# API Marketplace Agro

A RESTful API built with FastAPI for managing an agricultural marketplace where producers can list their products and users can browse available agricultural products.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## Features

- 🔐 **Secure Authentication**: JWT-based authentication system
- 👤 **User Management**: Support for different user types (producers and regular users)
- 📦 **Product Management**: CRUD operations for agricultural products
- 🔍 **Product Discovery**: Public endpoints for browsing available products
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📊 **MariaDB Database**: Reliable data storage with MariaDB
- 📚 **API Documentation**: Auto-generated interactive API documentation with Swagger UI

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.6 or higher (for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MarcosKNB/API-Restful.git
   cd API-Restful
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```env
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=your_db_name
   MARIADB_ROOT_PASSWORD=your_root_password
   ```

3. Build and start the containers:
   ```bash
   docker compose up -d
   ```

The API will be available at `http://localhost:8000`

### Local Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Admin de teste
- Arquivo teste.py, so rodar

## API Documentation

Once the server is running, you can access:

- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Main Endpoints

### Authentication
- `POST /token` - Get access token
- `POST /usuarios/` - Register new user

### Products
- `GET /produtos/` - List all products (public)
- `POST /produtos/` - Create new product (producers only)
- `GET /produtos/me` - List producer's products
- `GET /produtos/{id}` - Get product details
- `PUT /produtos/{id}` - Update product (owner only)
- `DELETE /produtos/{id}` - Delete product (owner only)

### Users
- `GET /usuarios/me` - Get current user info
- `PUT /usuarios/me` - Update current user info

## Project Structure

```
.
├── app/
│   ├── rotas/           # API routes
│   ├── crud.py         # Database operations
│   ├── database.py     # Database configuration
│   ├── deps.py         # Dependencies and utilities
│   ├── main.py         # Application entry point
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic schemas
│   └── security.py     # Authentication logic
├── compose.yaml        # Docker Compose configuration
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Problemas

Ao rodar no docker verifique se o seu proprio banco de dados esta rodando, se sim, desligue.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions or run into issues, please [open an issue](https://github.com/MarcosKNB/API-Restful/issues) in the GitHub repository.

## License

This project is open-source and available under the MIT License.
