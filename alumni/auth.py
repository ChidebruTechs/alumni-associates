from flask import Blueprint, request, redirect, render_template, url_for, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from alumni.models import User, Members, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import BlogForm, UserForm, LoginForm, ProfileForm
from .models import Blogs, db
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    form = UserForm()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        user = User().query.filter_by(email=email).first()
        if user:
            flash("Email Already exist",  "warning")
        elif len(password) < 7:
            flash("Password too weak, should be at least 8 character",  "warning")
        elif password != confirm:
            flash("Password Don't match, Check and try again", "warning")
        else: 
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
            flash('Account Created ', 'primary')
    return render_template('admin/register.html', form= form, user=current_user)
  

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User().query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True) 
                return redirect(url_for('auth.index', user=current_user))
            else:
                flash('Wrong Email/Password, Check and try again!', 'danger')
        else:
            flash('Email does\'t exist!', 'danger')
    return render_template('admin/login.html', form=form, user=current_user)
 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/')
@login_required
def index():
    profile =Profile.query.all()
    return render_template('index.html', profile=profile, user=current_user)

# Display members
@auth.route("/members", methods=['GET', 'POST'])
def members():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    members =Members.query.all()
    return render_template('admin/members.html', members=members, user=current_user)

#Add Member
@auth.route("/add_member", methods=['GET', 'POST'])
def add_member():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cohort = request.form['cohort']
        profession = request.form['profession']
        location = request.form['location']
        gender = request.form['gender']
        try:
            members = Members(firstname=firstname, lastname=lastname, cohort=cohort, profession=profession, location=location, gender=gender)
            db.session.add(members)
            db.session.commit()
            flash('Member has been Inserted Successfully', 'success')
            return redirect(url_for('auth.members'))
        except:
            flash("An Error Occurred")
    return render_template('members.html', user=current_user)


@auth.route("/update_member", methods=['GET', 'POST'])
def update_member():
    if request.method == 'POST':
        member = Members.query.get(request.form.get('id'))
        member.firstname = request.form['firstname']
        member.lastname = request.form['lastname']
        member.cohort = request.form['cohort']
        member.profession = request.form['profession']
        member.location = request.form['location']
        member.gender = request.form['gender']

        db.session.commit()
        flash('Member updated Successfully', 'warning')
        return redirect(url_for('auth.members'))

#  DELETE MEMBER
@auth.route("/delete_member/<id>", methods=['GET', 'POST'])
def delete_member(id):
        member = Members.query.get(id)
        db.session.delete(member)
        db.session.commit()
        flash('Member Deleted', 'danger')
        return redirect(url_for('auth.members'))


@auth.route("/add_blog", methods=['GET', 'POST'])
def add_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blogs(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = "" 
        form.content.data = "" 
        form.author.data = "" 
        form.slug.data = ""

        db.session.add(blog)
        db.session.commit()
        flash('Your Blog has been Posted Successfully', 'success')
    return render_template('blog/add-blog.html', form=form, user=current_user)


@auth.route("/blog/edit/<int:id>", methods=['GET', 'POST'])
def edit_blog(id):
    post  = Blogs.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data 
        post.author = form.author.data 
        post.slug = form.slug.data
        db.session.add(post)
        db.session.commit()
        flash('Blog has been Updated Successfully', 'success')
        return redirect(url_for('views.post', id=post.id))
    form.title.data = post.title 
    form.content.data = post.content 
    form.author.data = post.author 
    form.slug.data = post.slug 
    return render_template('blog/edit-blog.html', form=form, post=post, user=current_user)

    
@auth.route("/blog/delete/<int:id>", methods=['GET', 'POST'])
def delete_blog(id):
    post  = Blogs.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('The Blog Post has been deleted!', 'danger')
        blogs  = Blogs.query.order_by(Blogs.blog_date)
        return render_template('blog/blog-posts.html', user=current_user, blogs=blogs, post=post)
    except:
        flash('An error occerred while trying to delete the blog!')
        blogs  = Blogs.query.order_by(Blogs.blog_date)
        return render_template('blog-posts.html', user=current_user, blogs=blogs)




@auth.route("/create_profile", methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm()
    count = 0
    if form.validate_on_submit():
        if count <= 1:
            profile = Profile(profession=form.profession.data, location=form.location.data, phone=form.phone.data, linkedin=form.linkedin.data, facebook=form.facebook.data, twitter=form.twitter.data, instagram=form.instagram.data, tiktok=form.tiktok.data, status=form.status.data, youtube=form.youtube.data)
            form.profession.data = ''
            form.location.data  = ''
            form.phone.data  = '' 
            form.linkedin.data = '' 
            form.facebook.data  = '' 
            form.twitter.data  = '' 
            form.instagram.data = ''
            form.youtube.data  = '' 
            form.status.data  = '' 
            form.tiktok.data  = '' 
            db.session.add(profile)
            db.session.commit()
            flash('Your Profile has been Created Successfully', 'success')
            count += 1
        else:
            flash('You can\'t create more than one Profile', 'warning')
    return render_template('profile/create-profile.html', form=form, user=current_user)


@auth.route("/profile/edit/<int:id>", methods=['GET', 'POST'])
def edit_profile(id):
    prof  = Profile.query.get_or_404(id)
    form = ProfileForm()
    if form.validate_on_submit():
        prof.profession = form.profession.data
        prof.location = form.location.data
        prof.phone = form.phone.data
        prof.linkedin = form.linkedin.data
        prof.facebook = form.facebook.data
        prof.twitter = form.twitter.data
        prof.instagram = form.instagram.data
        prof.youtube = form.youtube.data
        prof.status = form.status.data
        prof.tiktok = form.tiktok.data
        db.session.add(prof)
        db.session.commit()
        flash('Your Profile has been Updated Successfully', 'success')
        return redirect(url_for('auth.proflie', id=post.id))
    form.profession.data = prof.profession
    form.location.data  = prof.location 
    form.phone.data  = prof.phone 
    form.linkedin.data = prof.linkedin 
    form.facebook.data  = prof.facebook 
    form.twitter.data  = prof.twitter 
    form.instagram.data = prof.instagram 
    form.youtube.data  = prof.youtube 
    form.status.data  = prof.status 
    form.tiktok.data  = prof.tiktok 
    return render_template('profile/edit-profile.html', form=form, prof=prof, user=current_user)


@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = BlogForm()
    return render_template('admin/dashboard.html',frorm=form, user=current_user)

