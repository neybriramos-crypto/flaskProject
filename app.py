from flask import Flask, render_template, redirect, url_for, flash, request, abort
from config import Config
from models import db, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTAS ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('Completa todos los campos.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('El correo ya está registrado.', 'danger')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw, role='user')
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Inicia sesión para continuar.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        users = User.query.order_by(User.username).all()
        return render_template('admin_dashboard.html', users=users)
    return render_template('user_dashboard.html')

@app.route('/toggle_role')
@login_required
def toggle_role():
    current_user.role = 'admin' if current_user.role == 'user' else 'user'
    db.session.commit()
    flash('Rol actualizado.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'warning')
        return redirect(url_for('dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)