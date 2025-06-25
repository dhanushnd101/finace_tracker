from app import create_app, db

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Only create tables when running directly, not when imported by tests
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True, use_reloader=False)  # Disable reloader to avoid conflicts
