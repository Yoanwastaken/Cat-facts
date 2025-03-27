from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if user is not authenticated

# Google OAuth Configuration
app.config['GOOGLE_CLIENT_ID'] = "YOUR_GOOGLE_CLIENT_ID"
app.config['GOOGLE_CLIENT_SECRET'] = "YOUR_GOOGLE_CLIENT_SECRET"

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_token_url="https://oauth2.googleapis.com/token",
    authorize_redirect_uri="http://127.0.0.1:5000/login/google/callback",
    client_kwargs={"scope": "openid email profile"},
)
# end

# Cat Facts API base URL for GET
CAT_FACTS_URL = "https://catfact.ninja/fact"

# Mock API base URL for POST, PUT, DELETE
MOCK_API_URL = "https://httpbin.org/anything"

# User Model for Authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # google
    #google_id = db.Column(db.String(200), unique=True, nullable=True)  # Google ID for OAuth users
    #google_id = db.Column(db.String(200), unique=True, nullable=True)  # Nullable for email users

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Page
@app.route('/')
def home():
    return render_template('index.html', fact=None, facts=[], response=None)

# Google Login Route
@app.route('/login/google')
def google_login():
    return google.authorize_redirect(url_for('google_callback', _external=True))

@app.route('/login/google/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()
    
    google_id = user_info["id"]
    email = user_info["email"]
    username = user_info.get("name", email)  # Use name or email as username

    #Check if the user already exists
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(username=username, email=email, google_id=google_id)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash("Google Login successful!", "success")
    return redirect(url_for("dashboard"))

# end

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(email=email).first():
            flash("Email already exists! Please log in.", "danger")
            return redirect(url_for('login'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials! Try again.", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

# Protected Dashboard Route (Only logged-in users can access)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

# Fetch Single Cat Fact (Protected)
@app.route('/get_single_fact', methods=['POST'])
@login_required
def get_single_fact():
    try:
        response = requests.get(CAT_FACTS_URL)
        response.raise_for_status()
        fact = response.json().get("fact", "No fact found.")
        return render_template('dashboard.html', name=current_user.username, fact=fact, facts=[], response=None)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching single cat fact: {str(e)}")
        return redirect(url_for('dashboard'))

# Fetch Multiple Cat Facts (Protected)
@app.route('/get_multiple_facts', methods=['POST'])
@login_required
def get_multiple_facts():
    try:
        count = int(request.form.get('count', 1))
        facts = []
        for _ in range(count):
            response = requests.get(CAT_FACTS_URL)
            response.raise_for_status()
            facts.append(response.json().get("fact", "No fact found."))
        return render_template('dashboard.html', name=current_user.username, fact=None, facts=facts, response=None)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching multiple cat facts: {str(e)}")
        return redirect(url_for('dashboard'))

# Create Mock Fact (Protected)
@app.route('/create_fact', methods=['POST'])
@login_required
def create_mock_fact():
    fact = request.form.get('new_fact')
    if not fact:
        flash("Please enter a fact to create.")
        return redirect(url_for('dashboard'))
    try:
        response = requests.post(MOCK_API_URL, json={"fact": fact, "type": "cat_fact"})
        response.raise_for_status()
        return render_template('dashboard.html', name=current_user.username, fact=None, facts=[], response=response.json())
    except requests.exceptions.RequestException as e:
        flash(f"Error creating mock fact: {str(e)}")
        return redirect(url_for('dashboard'))

# Update Mock Fact (Protected)
@app.route('/update_fact', methods=['POST'])
@login_required
def update_mock_fact():
    resource_id = request.form.get('update_id')
    updated_fact = request.form.get('updated_fact')
    if not resource_id or not updated_fact:
        flash("Please provide both Resource ID and Updated Fact.")
        return redirect(url_for('dashboard'))
    try:
        response = requests.put(f"{MOCK_API_URL}/{resource_id}", json={"fact": updated_fact, "type": "cat_fact"})
        response.raise_for_status()
        return render_template('dashboard.html', name=current_user.username, fact=None, facts=[], response=response.json())
    except requests.exceptions.RequestException as e:
        flash(f"Error updating mock fact: {str(e)}")
        return redirect(url_for('dashboard'))

# Delete Mock Fact (Protected)
@app.route('/delete_fact', methods=['POST'])
@login_required
def delete_mock_fact():
    resource_id = request.form.get('delete_id')
    if not resource_id:
        flash("Please enter the Resource ID to delete.")
        return redirect(url_for('dashboard'))
    try:
        response = requests.delete(f"{MOCK_API_URL}/{resource_id}")
        response.raise_for_status()
        return render_template('dashboard.html', name=current_user.username, fact=None, facts=[], response={"status": response.status_code})
    except requests.exceptions.RequestException as e:
        flash(f"Error deleting mock fact: {str(e)}")
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(debug=True)