# Finance Tracker Frontend

This is the frontend for the Finance Tracker application, built with React.

## Features

- User authentication (login, register)
- Dashboard for financial overview
- Transaction management (view, create, edit, delete)
- Responsive design

## Getting Started

### Prerequisites

- Node.js 14+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. The application will be available at http://localhost:3000

## Development Notes

### Handling Vulnerabilities

This project uses Create React App, which may show vulnerabilities in development dependencies. These don't affect production builds and can be safely ignored for development purposes.

### API Integration

The frontend communicates with the backend API using axios. The API base URL can be configured in `src/services/api.js`.

### Project Structure

- `src/components/` - Reusable UI components
- `src/pages/` - Page components
- `src/services/` - API and service functions
- `src/utils/` - Utility functions

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Testing

```bash
npm test
```

## License

MIT
