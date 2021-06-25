import secrets
import os
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from alluringdecors.forms import (
                                    RegistrationForm, LoginForm, 
                                    NewProjectForm, ProjectCategoryForm, 
                                    FAQForm, FeedbackForm, ContactForm,
                                    RequestForm, RequestStatusForm,
                                    RemarkForm
                                )
from alluringdecors.models import User, Category_project, Project, FAQ, Feedback, Contact, Service_request
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
            flash(f'login unsuccessful check email or password', 'danger')
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
        else:
            project = Project(name=form.name.data, client=form.client.data, description=form.description.data, 
        category_id=form.category.data)
            db.session.add(project)
            db.session.commit()
        flash(f'New Project Created', 'success')
        return redirect(url_for('new_project'))
    return render_template('new_project.html', title='new project', form=form) 

@app.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
def project_update(project_id):
    project = Project.query.get_or_404(project_id)
    form = NewProjectForm()
    form.category.choices = [(project.id, project.name )for project in Category_project.query.all()]
    
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_image(form.picture.data)
        project.category_id= form.category.data 
        project.name= form.name.data
        project.client= form.client.data
        project.description= form.description.data
        project.image_file= image_file
        form.picture.data = project.image_file
        db.session.commit()
        flash(f'Project"{project.name}" Successfully Updated', 'success')
        return redirect(url_for('project_detail', project_id=project.id))
    elif request.method == 'GET':
        form.name.data = project.name
        form.client.data = project.client
        form.description.data = project.description
        form.picture.data = project.image_file    
    return render_template('new_project.html', image_link=form.picture.data, title='update Project', legend="Update Project", form=form) 
 

@app.route("/project/<int:project_id>/delete", methods=['GET','POST'])
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(f'"{project.name}" deleted', 'danger')
    return redirect(url_for('new_project'))

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
    return render_template('faq.html', title='Add New FAQ', legend="Add Faq", form=form, faqs=faqs) 


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
    return render_template('feedbackform.html', title='send feedback', form=form, legend="Send Us a Feedback")

@app.route("/feedback/all/")
def all_feedback():
    feedbacks = Feedback.query.order_by(Feedback.date_sent.desc())
    return render_template('allfeedbacks.html', title='send feedback', feedbacks=feedbacks,)



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
@login_required
def admin():
    if not current_user.is_staff: 
        abort(403)
    return render_template('admin.html', title='admin') 

@app.route("/users/")
@login_required
def users():
    if (not current_user.is_staff):
        flash(f'Access Denied', 'danger')
        return redirect(url_for('ServiceRequest'))    
    users = User.query.filter_by(is_active=True).order_by(User.id.desc())
    return render_template('users.html', title='users', users=users) 

@app.route("/users/<int:user_id>/delete")
@login_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users')) 


@app.route("/service/", methods=['GET','POST'])
def ServiceRequest():
    form = RequestForm()
    if form.validate_on_submit():
        service_request = Service_request(type=form.type.data, domain=form.domain.data, location=form.location.data, 
        service_request=current_user)
        db.session.add(service_request)
        db.session.commit()
        flash(f'Service Request Sent', 'success')
        return redirect(url_for('index'))
    return render_template('service_form.html', title='Request Form', legend="Request Service Form", form=form) 


@app.route("/all_services/")
@login_required
def allServices():
    if not current_user.is_staff:
        abort(403)
    services = Service_request.query.all()
    return render_template('all_request.html', title='All requests', services=services,) 


@app.route("/service/status/<int:service_id>", methods=['GET','POST'])
def serviceStatus(service_id):
    service = Service_request.query.get_or_404(service_id)
    form = RequestStatusForm()
    if form.validate_on_submit():
        service.status = form.status.data
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('allServices')) 
    elif request.method == 'GET':
        form.status.data = service.status
    return render_template('service_status.html', title='update service status', service=service, legend="Update Status", form=form) 

@app.route("/service/add_remark/<int:service_id>", methods=['GET','POST'])
def serviceRemark(service_id):
    service = Service_request.query.get_or_404(service_id)
    form = RemarkForm()
    if form.validate_on_submit():
        service.remark = form.remark.data
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('allServices')) 
    elif request.method == 'GET':
        form.remark.data = service.remark
    return render_template('addremark.html', title='Add Remark', service=service, legend="Add Remark", form=form) 


@app.route("/service/home/")
def home_decor():
    return render_template('home_decor.html', title='Home Decoration') 


@app.route("/service/office/")
def office_decor():
    return render_template('office_decor.html', title='Office Decoration') 


@app.route("/service/restaurant/")
def restaurant_decor():
    return render_template('restaurant_decor.html', title='Restaurant Decoration') 


@app.route("/service/bonquet/")
def banquet_decor():
    return render_template('banquet_decor.html', title='Banquet Decoration') 