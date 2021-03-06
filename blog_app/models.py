from . import db
import datetime


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow())
    is_published = db.Column(db.Boolean, default=False)


def flash_msg(is_published):
    if is_published is True:
        return "Post został dodany i opublikowany"
    return "Post został dodany i czeka na publikację"


def post_handling(form, entry=None):
    if entry is not None:
        form.populate_obj(entry)
        db.session.commit()
    else:
        entry = Entry(
            title=form.title.data,
            body=form.body.data,
            is_published=form.is_published.data
        )
        db.session.add(entry)
        db.session.commit()

