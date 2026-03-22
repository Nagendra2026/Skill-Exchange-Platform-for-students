# SkillExchange Project

A Flask-based web application that connects learners and educators through skill sharing and matching. The platform uses machine learning to match users based on their skills and learning goals.

## Features

- **User Authentication** - Secure registration and login system with role-based access
- **Skill Matching** - ML-powered algorithm to match users with complementary skills
- **Discussion Forum** - Real-time discussion and chat for skill exchanges
- **Video Integration** - Zoom meeting integration for live sessions
- **Analytics Dashboard** - Track progress and skill development
- **Practice Lab** - Code editor for hands-on learning
- **Leaderboard** - Gamified learning with user rankings
- **Session Management** - Schedule and manage learning sessions

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Machine Learning**: Python (scikit-learn, joblib)
- **Frontend**: HTML, CSS, JavaScript
- **Video**: Zoom API Integration
- **File Management**: Werkzeug

## Project Structure

```
SkillExchangeProject/
├── app.py                    # Main Flask application
├── learning_dataset.csv     # ML training dataset
├── database/                # Database setup and management
│   ├── db_setup.py
│   ├── create_discussions.py
│   ├── update_db.py
│   └── update_submissions_db.py
├── ml_engine/              # Machine learning models
│   ├── matching.py         # Skill matching algorithm
│   ├── train_model.py      # Model training
│   ├── dataset_generator.py
│   └── feature_importance.csv
├── services/               # External service integrations
│   └── zoom.py            # Zoom API wrapper
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, images
└── uploads/              # User-uploaded files
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SkillExchangeProject.git
   cd SkillExchangeProject
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the database**
   ```bash
   python database/db_setup.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Configuration

- **Secret Key**: Update `app.secret_key` in `app.py` for production
- **Database**: SQLite is configured by default; change in `get_db()` function for other databases
- **Upload Folder**: File uploads are stored in the `uploads/` directory
- **Zoom API**: Configure Zoom credentials in `services/zoom.py`

## Usage

1. **Register** - Create a new account with a unique username and email
2. **Complete Profile** - Add your skills and learning interests
3. **Find Matches** - Browse matched skill partners in the platform
4. **Schedule Sessions** - Create video meetings or practice sessions
5. **Participate** - Join discussions and share knowledge

## Development

- **Database Migrations**: Use scripts in `database/` folder
- **Model Training**: Run `ml_engine/train_model.py` to retrain the matching model
- **Feature Analysis**: Check `ml_engine/feature_importance.csv` for model insights

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please follow the standard Git workflow:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues, questions, or suggestions, please create an issue on GitHub.
