# Finance Tracker - Full Stack Application

A full-stack application for managing personal finances with a Flask backend API and React frontend.

## Project Structure

This project is organized as a monorepo with separate frontend and backend directories:

```
finance_tracker/
├── backend/           # Flask API
│   ├── app/           # Flask application code
│   ├── tests/         # Backend tests
│   └── ...
├── frontend/         # React frontend
│   ├── public/        # Static assets
│   ├── src/           # React source code
│   └── ...
└── ...
```

## Features

- User authentication (register, login, profile)
- User management (CRUD operations)
- Transaction management (income, expenses, savings)
- Admin functionality for user management
- JWT-based authentication
- MySQL database with SQLAlchemy ORM
- Transaction filtering and categorization
- React frontend with component-based architecture
- RESTful API design

## Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL Server
- pip (Python package manager)
- npm (Node.js package manager)

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env  # Then edit .env with your settings
   ```

5. Start the MySQL database:
   ```bash
   make startdb
   ```

6. Initialize the database:
   ```bash
   make initdb
   ```

7. Seed the database with sample data:
   ```bash
   make seed
   ```

8. Run the backend server:
   ```bash
   make run
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. The frontend will be available at http://localhost:3000

## Development

- Backend API runs on http://localhost:5000
- Frontend development server runs on http://localhost:3000
- API documentation is available in the backend README or via Postman collection

## Testing

### Backend Tests
```bash
cd backend
make test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

See the README files in the respective directories for deployment instructions.

## License

MIT
