# Personal Finance Portal - Setup Guide

This guide will help you set up and run the Personal Finance Portal application in VS Code.

## Prerequisites

- Python 3.7 or higher
- VS Code
- Git (optional)

## Setup Instructions

Follow these steps to set up and run the application:

### 1. Extract the Project

Extract the `personal_finance_portal.zip` file to a location of your choice.

### 2. Open in VS Code

Open VS Code and select "Open Folder" to open the extracted `personal_finance_portal` directory.

### 3. Create a Virtual Environment

Open a terminal in VS Code (Terminal > New Terminal) and run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 5. Initialize the Database

The project includes a pre-initialized database, but if you want to start fresh:

```bash
# Set the Flask application
export FLASK_APP=run.py  # On Windows: set FLASK_APP=run.py

# Initialize the database (only if starting fresh)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application

Start the Flask development server:

```bash
python run.py
```

### 7. Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

You should see the login page. Register a new account to start using the application.

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
├── instance/                       # Instance-specific data (database)
├── tests/                          # Test suite
├── requirements.txt                # Project dependencies
├── run.py                          # Application entry point
└── README.md                       # Project documentation
```

## Features

- User authentication (register, login, logout)
- Expense tracking
- Budget management
- Investment tracking
- Bill reminders
- Dashboard with visualizations

## Troubleshooting

If you encounter any issues:

1. **Database errors**: Make sure the database file exists in the `instance` folder. If not, run the migration commands.

2. **Import errors**: Ensure you're running commands with the virtual environment activated.

3. **Module not found errors**: Verify all dependencies are installed with `pip install -r requirements.txt`.

4. **Port already in use**: If port 5000 is already in use, modify `run.py` to use a different port:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Change port number
   ```

## Next Steps

Refer to the `implementation_plan.md` file for details on future development and feature enhancements.
