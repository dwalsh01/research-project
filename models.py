from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    prefix = db.Column(db.String(20))
    suffix = db.Column(db.String(20))
    phone = db.Column(db.String(25))
    phone_ext = db.Column(db.Integer)
    email=db.Column(db.String(50), nullable=False, unique=True)
    orcid=db.Column(db.String(50), nullable=False)

    def __init__ (self, f_name, l_name, job_title, prefix, suffix, phone, phone_ext, email, orcid):
        self.f_name = f_name
        self.l_name = l_name
        self.job_title = job_title
        self.prefix = prefix
        self.suffix = suffix
        self.phone = phone
        self.phone_ext = phone_ext
        self.email = email
        self.orcid = orcid

    def __repr__(self):
        return "<User: {}>".format(self.f_name)

class Education(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    degree = db.Column(db.String(25), nullable=False)
    field_of_study = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(25))
    location = db.Column(db.String(50))
    year_degree_award = db.Column(db.Integer)