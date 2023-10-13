from flask import Flask, render_template, request, redirect, session, url_for, g,flash
from flask_mail import Mail, Message
from modelv1 import auth, SignupForm, LoginForm, db 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import random,json

app = Flask(__name__)

with open('config.json', 'r') as f:
    params = json.load(f)

# For email functionality

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail']['gmail-username'],
    MAIL_PASSWORD=params['gmail']['gmail-password']
)

if params['FLASK']['ENVIORMENT'] == 'development':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = params['FLASK']['DATABASE']
    app.config['SECRET_KEY'] = 'secret'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = ""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db to work with app
db.init_app(app)  # Initialize the db instance with your Flask app

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(auth_id):
    if auth_id is not None:
        return auth.query.get(int(auth_id))
    return None

# Routes and other code...

@app.route('/',)
def home():
    return render_template('home.html')



@app.context_processor
def inject_auth_id():
    if current_user.is_authenticated:
        auth_id = current_user.auth_id
        return dict(auth_id=auth_id)
    else:
        return dict(auth_id=None)





@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = auth.query.filter_by(email=form.email.data).first()
        if user:
            stored_pass=user.password
            form_pass=form.password.data
            print(stored_pass)
            print(form_pass)
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',data='Wrong Password',form=form)
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data

        # Check if the email is already registered in the database
        existing_user = auth.query.filter_by(email=email).first()
        if existing_user:
            flash('User with this email already exists. Please log in.')
            return render_template('signup.html', form=form,data='Account Already Exist')

        # If the email is not found, proceed with user registration
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = auth(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    if params['FLASK']['CREATE_TABLES']:  # Check a configuration flag
        with app.app_context():
            db.create_all()
            params['FLASK']['CREATE_TABLES']="False"
            with open('config.json', 'w') as f:
                json.dump(params, f, indent=4)
    app.run()
