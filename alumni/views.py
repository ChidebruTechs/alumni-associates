from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .forms import BlogForm, ContactForm, SearchForm
from .models import Blogs
views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return render_template('index.html', user=current_user)


@views.route('/about')
# @login_required
def about():
    return render_template('about.html', user=current_user)

@views.route('/events')
# @login_required
def events():
    return render_template('events.html', user=current_user)

@views.route('/news')
# @login_required
def news():
    return render_template('news.html', user=current_user)

@views.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html', user=current_user)

@views.route('/blog_posts', methods=['GET', 'POST'])
@login_required
def blog_posts():
    blogs  = Blogs.query.order_by(Blogs.blog_date)
    return render_template('blog/blog-posts.html', user=current_user, blogs=blogs)


@views.route('/blog_posts/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post  = Blogs.query.get_or_404(id)
    return render_template('blog/blog.html', post=post, user=current_user)


@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form, user=current_user)


@views.route('search', methods=['POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        post.searched = form.searching.data
    return render_template('search.html', form=form, searched=post.searched)


@views.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)

