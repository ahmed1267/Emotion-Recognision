from flaskapp import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	filename = db.Column(db.String)
	emotion = db.Column(db.String)

	def __repr__(self):
		return f"{User} {self.name} are {self.emotion}"

