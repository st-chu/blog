from blog_app import app
from flask import render_template, flash, redirect, request, url_for
from blog_app.models import Entry, db, post_handling
from blog_app.forms import EntryForm


@app.route('/')
def index():
    all_post = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_post=all_post)


@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            post_handling(form=form)
            if form.is_published.data is True:
                flash("Post został dodany i opublikowany")
                return redirect(url_for("create_entry"))
            flash("Post został dodany i czeka na publikację")
            return redirect(url_for("create_entry"))
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/post/<int:entry_id>/", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            post_handling(form=form, entry=entry)
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)
