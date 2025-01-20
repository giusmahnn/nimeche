# VoteSmart

VoteSmart is a student election system that allows students to vote for their preferred candidates in various positions. The system ensures secure and fair voting, providing a user-friendly interface for both voters and administrators.

## Table of Contents

- [VoteSmart](#votesmart)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Endpoints](#endpoints)
  - [Contributing](#contributing)
  - [Future Features](#future-features)

## Features

- Admin authentication and authorization
- Matric number validation for voters
- Secure voting process
- Admin dashboard to manage elections
- Real-time vote counting
- Responsive design

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/votesmart.git
    cd votesmart
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a [.env](http://_vscodecontentref_/2) file in the root directory and add the following:

    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DJANGO_SETTINGS_MODULE=nimeche.settings.local

    # Database settings
    Use default django db or configure external DB

5. Apply the migrations and create a superuser:

    ```sh
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

1. Access the application at `http://localhost:8000`.
2. Log in as an admin to manage elections and view the dashboard.
3. Voters can log in using their matric number and cast their votes.

## Endpoints

- `GET detail/<slug:slug>/`: Retrieve a list of candidates for a particular position.
- `POST matric-number/`: Matric Number Validation.
- `POST custom-login/`: Admin login.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Create a pull request with a detailed description of your changes.


## Future Features

- **Email Notifications**: Send email notifications to voters and candidates.
- **Two-Factor Authentication**: Enhance security with two-factor authentication for admin users.
- **Voting Analytics**: Provide detailed analytics and reports on voting patterns and results.
- **Mobile App**: Develop a mobile app for easier access to the voting system.
- **Live Results Dashboard**: Display live voting results on a public dashboard.
- **Automated Testing**: Add automated tests to ensure the reliability and stability of the application.
- **Accessibility Improvements**: Enhance the accessibility of the application to ensure it is usable by everyone, including those with disabilities.

---

Thank you for using VoteSmart! If you have any questions or need assistance, please feel free to contact us.