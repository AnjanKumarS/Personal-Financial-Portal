# Personal Finance Portal

A Flask-based web application for tracking personal finances, including expenses, budgets, investments, and bill reminders.

## Features

- **Expense Tracking**: Record and categorize expenses
- **Budget Management**: Create and monitor budgets by category
- **Investment Tracking**: Track investment performance
- **Bill Reminders**: Manage upcoming bills and payment status
- **Dashboard**: Visualize financial data with charts and graphs

## Project Structure

```
personal_finance_portal/
│
├── app/                            # Main application package
│   ├── __init__.py                 # Flask application factory
│   ├── config.py                   # Configuration settings
│   ├── models/                     # Database models
│   ├── routes/                     # Route handlers
│   ├── static/                     # Static files
│   ├── templates/                  # Jinja2 templates
│   └── utils/                      # Utility functions
│
├── migrations/                     # Database migrations
├── tests/                          # Test suite
├── venv/                           # Virtual environment (not in version control)
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
├── requirements.txt                # Project dependencies
└── run.py                          # Application entry point
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- VS Code

### Installation

1. Clone or download the project to your local machine

2. Open the project folder in VS Code

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. Run the application:
   ```
   python run.py
   ```

8. Access the application in your web browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Next Steps

Refer to the `implementation_plan.md` file for a detailed roadmap of the remaining implementation tasks.

## Future AWS Deployment

The application is designed to be easily deployable to AWS:
- Database: AWS RDS (PostgreSQL)
- Application: AWS Elastic Beanstalk or EC2
- Static files: AWS S3
- Monitoring: AWS CloudWatch
