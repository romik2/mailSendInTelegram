import flask_conn

class Messages(flask_conn.db.Model):
    id = flask_conn.db.Column(flask_conn.db.Integer, primary_key=True)
    text_message = flask_conn.db.Column(flask_conn.db.Text, nullable=False)
    from_message = flask_conn.db.Column(flask_conn.db.Text, nullable=False)
    subject_message = flask_conn.db.Column(flask_conn.db.Text, nullable=False)
    key = flask_conn.db.Column(flask_conn.db.Text, unique=True, nullable=False)

with flask_conn.app.app_context():
    flask_conn.db.create_all()
