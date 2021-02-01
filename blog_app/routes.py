from blog_app import app
from flask import render_template, flash, redirect, request, url_for, session
from blog_app.models import Entry, flash_msg, post_handling,db
from blog_app.forms import EntryForm, LoginForm
import functools


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route('/', methods=['GET'])
def index():
    all_post = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_post=all_post)


@app.route('/drafts/', methods=['GET'])
@login_required
def list_drafts():
    all_post = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("list_drafts.html", all_post=all_post)


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            post_handling(form=form)
            flash(flash_msg(form.is_published.data))
            return redirect(url_for("create_entry"))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/post/<int:entry_id>/", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            post_handling(form=form, entry=entry)
            flash("zmiany zostały zapisane")
            return redirect(url_for('index'))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route('/delete/<int:entry_id>/', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash("Post został usunęty")
    return redirect(url_for('list_drafts'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash("You are now logged in.", 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


