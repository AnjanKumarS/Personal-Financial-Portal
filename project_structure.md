# Personal Finance Portal - Project Structure

## Overview
This document outlines the structure and components of the Flask-based Personal Finance Portal application. The application is designed to be run locally in VS Code first, with the potential for AWS deployment later.

## Project Structure

```
personal_finance_portal/
│
├── app/                            # Main application package
│   ├── __init__.py                 # Flask application factory
│   ├── config.py                   # Configuration settings
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── expense.py              # Expense model
│   │   ├── budget.py               # Budget model
│   │   ├── investment.py           # Investment model
│   │   └── bill.py                 # Bill reminder model
│   │
│   ├── routes/                     # Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── dashboard.py            # Dashboard routes
│   │   ├── expenses.py             # Expense management routes
│   │   ├── budgets.py              # Budget management routes
│   │   ├── investments.py          # Investment tracking routes
│   │   └── bills.py                # Bill reminder routes
│   │
│   ├── static/                     # Static files
│   │   ├── css/                    # CSS files
│   │   ├── js/                     # JavaScript files
│   │   └── img/                    # Image files
│   │
│   ├── templates/                  # Jinja2 templates
│   │   ├── base.html               # Base template
│   │   ├── auth/                   # Authentication templates
│   │   ├── dashboard/              # Dashboard templates
│   │   ├── expenses/               # Expense management templates
│   │   ├── budgets/                # Budget management templates
│   │   ├── investments/            # Investment tracking templates
│   │   └── bills/                  # Bill reminder templates
│   │
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       ├── auth_utils.py           # Authentication utilities
│       ├── date_utils.py           # Date handling utilities
│       └── chart_utils.py          # Chart generation utilities
│
├── migrations/                     # Database migrations (using Flask-Migrate)
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_expenses.py
│   ├── test_budgets.py
│   ├── test_investments.py
│   └── test_bills.py
│
├── venv/                           # Virtual environment (not in version control)
│
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
├── requirements.txt                # Project dependencies
└── run.py                          # Application entry point
```

## Key Components

### 1. Database Models

#### User Model
- User authentication information
- Profile details
- Preferences

#### Expense Model
- Expense amount, date, category
- Description and notes
- Receipt attachment (optional)
- Relationship to user

#### Budget Model
- Budget category
- Allocated amount
- Time period (monthly, yearly)
- Relationship to user

#### Investment Model
- Investment type (stocks, bonds, etc.)
- Purchase details (date, amount, price)
- Current value
- Relationship to user

#### Bill Model
- Bill name and amount
- Due date
- Recurring flag
- Payment status
- Relationship to user

### 2. Routes and Views

#### Authentication
- User registration
- Login/logout
- Password reset

#### Dashboard
- Overview of financial status
- Summary widgets
- Charts and graphs

#### Expense Management
- Add/edit/delete expenses
- View expense history
- Filter and search expenses
- Categorize expenses

#### Budget Management
- Create and manage budgets
- Track budget progress
- Budget vs. actual spending

#### Investment Tracking
- Add/edit/delete investments
- Track investment performance
- Portfolio overview

#### Bill Reminders
- Add/edit/delete bill reminders
- View upcoming bills
- Mark bills as paid

### 3. Features

#### User Authentication
- Secure user registration and login
- Password hashing
- Session management

#### Expense Tracking
- Manual expense entry
- Categorization
- Search and filtering
- Data visualization

#### Budget Management
- Budget creation by category
- Progress tracking
- Visual indicators

#### Investment Portfolio
- Manual investment entry
- Performance tracking
- Portfolio visualization

#### Bill Reminders
- Due date tracking
- Payment status
- Notification system (future enhancement)

#### Dashboard
- Financial overview
- Expense breakdown charts
- Budget progress
- Recent transactions
- Upcoming bills

### 4. Technologies

#### Backend
- Flask (Web framework)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF (Forms)
- Flask-Migrate (Database migrations)

#### Frontend
- HTML/CSS/JavaScript
- Bootstrap (Responsive design)
- Chart.js (Data visualization)
- jQuery (DOM manipulation)

#### Database
- SQLite (Development)
- PostgreSQL (Production - future)

#### Testing
- pytest (Testing framework)
- Coverage (Test coverage)

## Development Workflow

1. Set up virtual environment
2. Install dependencies
3. Configure development database
4. Run database migrations
5. Start development server
6. Access application via browser

## Future AWS Deployment Considerations

- Database: RDS (PostgreSQL)
- Static files: S3
- Application hosting: Elastic Beanstalk or EC2
- Email notifications: SES
- Monitoring: CloudWatch
