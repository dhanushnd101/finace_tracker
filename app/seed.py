from datetime import timedelta
from app import db
from app.models.user import User
from app.models.transaction import Transaction
from app.utils.datetime_utils import now_utc, parse_iso8601

def create_test_data():
    """Helper function to create test users and transactions."""
    users = [
        {
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_admin': True
        },
        {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': 'user1123',
            'first_name': 'Regular',
            'last_name': 'User One',
            'is_admin': False
        },
        {
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password': 'user2123',
            'first_name': 'Regular',
            'last_name': 'User Two',
            'is_admin': False
        }
    ]

    created_users = []
    
    # Create users
    for user_data in users:
        # Check if user already exists
        if db.session.execute(db.select(User).filter_by(username=user_data['username'])).scalar_one_or_none() is None:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_admin=user_data['is_admin']
            )
            user.password = user_data['password']
            
            try:
                db.session.add(user)
                db.session.commit()
                created_users.append(user)
                print(f"Created user: {user_data['username']}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating user {user_data['username']}: {str(e)}")
        else:
            user = db.session.execute(db.select(User).filter_by(username=user_data['username'])).scalar_one()
            created_users.append(user)
            print(f"User {user_data['username']} already exists")
    
    # Create sample transactions for each user
    categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Salary', 'Freelance']
    today = now_utc()
    
    for user in created_users:
        # Skip if user already has transactions
        if user.transactions:
            print(f"User {user.username} already has transactions")
            continue
            
        transactions = []
        
        # Create 10 sample transactions per user
        for i in range(10):
            is_income = i % 3 == 0  # Every 3rd transaction is an income
            amount = 10.50 * (i + 1)
            if is_income:
                amount = 100 * (i + 1)  # Higher amounts for income
                
            transaction = Transaction(
                user_id=user.id,
                amount=amount,
                description=f"Sample {'income' if is_income else 'expense'} {i+1}",
                category=categories[i % len(categories)],
                transaction_type='income' if is_income else 'expense',
                transaction_date=(today - timedelta(days=10-i)).replace(tzinfo=None)
            )
            transactions.append(transaction)
        
        try:
            db.session.add_all(transactions)
            db.session.commit()
            print(f"Created {len(transactions)} transactions for user {user.username}")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating transactions for user {user.username}: {str(e)}")
    
    return [user.username for user in created_users]

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        created = create_test_data()
        if created:
            print(f"Successfully created users: {', '.join(created)}")
        else:
            print("No new users were created")
