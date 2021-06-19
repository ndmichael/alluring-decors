import secrets
import os
from flask import Flask, render_template, url_for, flash, redirect, request
from alluringdecors.forms import (
                                    RegistrationForm, LoginForm, 
                                    NewProjectForm, ProjectCategoryForm, 
                                    FAQForm, FeedbackForm, ContactForm
                                )
from alluringdecors.models import User, Category_project, Project, FAQ, Feedback, Contact
from alluringdecors import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


def save_image(form_img):
    rand_hex = secrets.token_hex(3)
    f_name, f_ext = os.path.splitext(form_img.filename)
    image_fn = f_name + rand_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images/project_images', image_fn)
    form_img.save(image_path)
    return image_fn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_active=True, is_staff=False)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully create for {form.username.data} you can now login', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():   
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You are login as {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'login unsuccessful check email or password', 'success')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout/")
def logout():   
    logout_user()
    flash(f'You have been logout, Please login again', 'danger')
    return redirect(url_for('login'))

@app.route("/account/")
@login_required
def account():  
    return render_template('account.html', title='account') 

@app.route("/project/")
def project():  
    return render_template('project.html', title='project') 

@app.route("/project/ongoing/")
def ongoing_project():  
    slug = request.args.get('slug')
    category = Category_project.query.filter_by(name=slug).first()
    projects = Project.query.filter_by(project=category).order_by(Project.date_added.desc())
    return render_template('ongoing_projects.html', projects=projects, title='on-going project', category=category) 

@app.route("/project/upcoming/")
def upcoming_project():  
    slug = request.args.get('slug')
    category = Category_project.query.filter_by(name=slug).first()
    projects = Project.query.filter_by(project=category).order_by(Project.date_added.desc())
    return render_template('upcoming_projects.html', title='up-coming project', category=category,projects=projects) 

@app.route("/project/accomplished/")
def accomplished_project():  
    slug = request.args.get('slug')
    category = Category_project.query.filter_by(name=slug).first()
    projects = Project.query.filter_by(project=category).order_by(Project.date_added.desc())
    return render_template('accomplished_projects.html', title='accomplised project', category=category, projects=projects) 

@app.route("/category/detail/<int:project_id>",)
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', title='project id', project=project) 

@app.route("/project/create/", methods=['GET', 'POST'])
# @login_required
def new_project():  
    form = NewProjectForm()
    form.category.choices = [(project.id, project.name )for project in Category_project.query.all()]
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_image(form.picture.data)
        project = Project(name=form.name.data, client=form.client.data, image_file=image_file,
         description=form.description.data, 
        category_id=form.category.data)
        db.session.add(project)
        db.session.commit()
        flash(f'New Project Created', 'success')
        return redirect(url_for('new_project'))
    return render_template('new_project.html', title='new project', form=form) 
 

@app.route("/category/create/", methods=['GET', 'POST'])
def project_category(): 
    form = ProjectCategoryForm()
    if form.validate_on_submit():
        category = Category_project(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'New category Created', 'success')
        return redirect(url_for('project_category'))
    return render_template('create_cat_project.html', title='create category Project', form=form) 


@app.route("/faq/", methods=['GET', 'POST'])
def faq(): 
    # faqs = FAQ.query.all().order_by(FAQ.date_added.desc()) 
    faqs = FAQ.query.all()
    form = FAQForm()
    if form.validate_on_submit():
        faq = FAQ(question=form.question.data, answer=form.answer.data)
        db.session.add(faq)
        db.session.commit()
        flash(f'New FAQ "{form.question.data}" Created', 'success')
        return redirect(url_for('faq'))
    return render_template('faq.html', title='create category Project', legend="Add Faq", form=form, faqs=faqs) 


@app.route("/faq/<int:faq_id>/update", methods=['GET', 'POST'])
def faq_update(faq_id):
    faqs = FAQ.query.all()
    faq = FAQ.query.get_or_404(faq_id)
    form = FAQForm()
    if form.validate_on_submit():
        faq.question= form.question.data
        faq.answer= form.answer.data
        db.session.commit()
        flash(f'FAQ"{faq.question}" Successfully Updated', 'success')
        return redirect(url_for('faq'))
    elif request.method == 'GET':
        form.question.data = faq.question
        form.answer.data = faq.answer
        
    return render_template('faq.html', title='update FAQ', legend="Update Faq", form=form, faqs=faqs) 

@app.route("/faq/<int:faq_id>/delete", methods=['GET','POST'])
def faq_delete(faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash(f'faq"{faq.question}" deleted', 'danger')
    return redirect(url_for('faq'))



@app.route("/feedback/", methods=['GET', 'POST'])
def feedback(): 
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(quality=form.quality.data, suggestion=form.suggestion.data, feedback=current_user)
        db.session.add(feedback)
        db.session.commit()
        flash(f'Feedback sent successfully', 'success')
        return redirect(url_for('index'))
    return render_template('feedbackform.html', title='send feedback', form=form)



@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    contacts = Contact.query.order_by(Contact.date_added.desc())
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(title=form.title.data, detail=form.detail.data)
        db.session.add(contact)
        db.session.commit()
        flash(f'New Contact Added', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Alluring Contact', legend="Add New Contact", form=form, contacts=contacts) 

@app.route("/contact/<int:contact_id>/update", methods=['GET', 'POST'])
def contact_update(contact_id):
    contacts = Contact.query.order_by(Contact.date_added.desc())
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm()
    if form.validate_on_submit():
        contact.title= form.title.data
        contact.detail= form.detail.data
        db.session.commit()
        flash(f'Contact "{contact.title}" Successfully Updated', 'success')
        return redirect(url_for('contact'))
    elif request.method == 'GET':
        form.title.data = contact.title
        form.detail.data = contact.detail
        
    return render_template('contact.html', title='Alluring Contact', legend="Update Contact", form=form, contacts=contacts) 

@app.route("/contact/<int:contact_id>/delete", methods=['GET','POST'])
def contact_delete(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash(f'Contact "{contact.title}" deleted', 'danger')
    return redirect(url_for('contact'))


@app.route("/admin/")
def admin():
    return render_template('admin.html', title='admin') 

@app.route("/users/")
def users():
    users = User.query.filter_by(is_active=True).order_by(User.id.desc())
    return render_template('users.html', title='users', users=users) 

@app.route("/users/<int:id>")
def deactivate_user(id):
    user = User.query.get_or_404(id)
    user.is_active = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users')) 