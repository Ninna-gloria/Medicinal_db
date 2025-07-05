from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from .models import Plant, Use, User
from .forms import PlantForm,  RegistrationForm, LoginForm ,UseForm
from . import db, limiter
import os
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'app/static/img'

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page showing app purpose and navigation."""
    return render_template('index.html')

@main_bp.route('/plants', methods=['GET'])
@login_required
def plant_list():
    """List all plants, with optional search."""
    search = request.args.get('search', '')
    if search:
        plants = Plant.query.filter(Plant.name.ilike(f'%{search}%')).all()
    else:
        plants = Plant.query.all()
    return render_template('plant_list.html', plants=plants)

@main_bp.route('/plant/<int:plant_id>')
@login_required
def plant_detail(plant_id):
    """Show details and uses for a single plant."""
    plant = Plant.query.get_or_404(plant_id)
    uses = Use.query.filter_by(plant_id=plant_id).all()
    return render_template('plant_detail.html', plant=plant, uses=uses)

@main_bp.route('/uses/add/<int:plant_id>', methods=['GET', 'POST'])
@login_required
def add_use(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    form = UseForm()
    form.plant_id.data = plant_id  # Set the default plant

    if form.validate_on_submit():
        use = Use(
            plant_id=plant_id,
            use_description=form.use_description.data
        )
        db.session.add(use)
        db.session.commit()
        flash('Use added successfully!', 'success')
        return redirect(url_for('main.plant_detail', plant_id=plant.id))

    return render_template('add_use.html', form=form, plant=plant)

@main_bp.route('/plants/add', methods=['GET', 'POST'])
@login_required
@limiter.limit("5/minute")
def add_plant():
    form = PlantForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            try:
                img = Image.open(form.image.data.stream)
                img.verify()  # Validate image content
            except Exception:
                flash("Uploaded file is not a valid image.", "danger")
                return redirect(request.url)

            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(filepath)

        plant = Plant(
            name=form.name.data,
            common_name=form.common_name.data,
            description=form.description.data,
            location=form.location.data,
            image=filename,
            added_by=current_user.id
        )
        db.session.add(plant)
        db.session.commit()
        flash('Plant added successfully!', 'success')
        return redirect(url_for('main.plant_list'))
    return render_template('add_plant.html', form=form)

@main_bp.route('/plant/<int:plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plant(plant_id):
    """Allow admin to edit a plant."""
    if not current_user.is_admin:
        abort(403)
    plant = Plant.query.get_or_404(plant_id)
    form = PlantForm(obj=plant)
    if form.validate_on_submit():
        plant.name = form.name.data
        plant.description = form.description.data
        plant.location = form.location.data
        db.session.commit()
        flash('Plant updated.', 'success')
        return redirect(url_for('main.plant_detail', plant_id=plant.id))
    return render_template('add_plant.html', form=form, edit=True)

@main_bp.route('/plant/<int:plant_id>/delete', methods=['POST'])
@login_required
def delete_plant(plant_id):
    """Allow admin to delete a plant."""
    if not current_user.is_admin:
        abort(403)
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    flash('Plant deleted.', 'success')
    return redirect(url_for('main.plant_list'))
@main_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def register():
    """User registration with duplicate check and password hashing."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10/minute")
def login():
    """User login with rate limiting and session management."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/add_plant')
def add_plant_redirect():
    return redirect(url_for('main.add_plant'))
