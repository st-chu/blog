from blog_app import app
from flask import render_template, flash, redirect, request, url_for
from blog_app.models import Entry, db
from blog_app.forms import EntryForm


@app.route('/')
def index():
    all_post = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_post=all_post)


@app.route('/new-post/', methods=['POST'])
def create_entry():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            title=form.title.data,
            body=form.body.data,
            is_published=form.is_published.data
        )
        db.session.add(entry)
        db.session.commit()
        if form.is_published.data is True:
            flash("Post został dodany i opublikowany")
            return redirect(url_for("index"))
        flash("Post został dodany i czeka na publikację")
        return redirect(url_for("index"))
    else:
        errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route('/new-post/', methods=['GET'])
def create_entry_form():
    form = EntryForm()
    errors = None
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/edit-post/<int:entry_id>/", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)
