# Finance Tracker API

A Flask-based REST API for managing user finances with JWT authentication.

## Features

- User authentication (register, login, profile)
- User management (CRUD operations)
- Transaction management (income, expenses, savings)
- Admin functionality for user management
- JWT-based authentication
- MySQL database with SQLAlchemy ORM
- Transaction filtering and categorization
- Flask-Migrate for database migrations
- CORS support
- Environment-based configuration
- RESTful API design

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/finance_tracker
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Seed the database with test data:
   ```bash
   python -m app.seed
   ```
   This will create:
   - Admin user: admin/admin123
   - Regular users: user1/user1123, user2/user2123
   - Sample transactions for each user

7. Run the development server:
   ```bash
   flask run
   ```

## Testing

Run the test suite with:

```bash
pytest -v
```

## API Documentation

For more detailed API documentation, you can import the provided Postman collection.

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user profile

### Users (Admin only)

- `GET /api/users` - Get all users
- `GET /api/users/<user_id>` - Get user by ID
- `PUT /api/users/<user_id>` - Update user
- `DELETE /api/users/<user_id>` - Deactivate user
- `POST /api/users/<user_id>/promote` - Promote user to admin

### Transactions

- `GET /api/transactions` - Get all transactions for current user
  - Query params: `category`, `type` (income/expense), `start_date`, `end_date`
- `GET /api/transactions/<transaction_id>` - Get transaction by ID
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/<transaction_id>` - Update transaction
- `DELETE /api/transactions/<transaction_id>` - Delete transaction

## Transaction Types

- `income` - Money received (salary, gifts, etc.)
- `expense` - Money spent (bills, shopping, etc.)
- `saving` - Money set aside for savings

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/finance_tracker
```

## Running Tests

To run tests, use:

```bash
python -m pytest
```

## License

This project is licensed under the MIT License.
