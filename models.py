from app import db
from passlib.hash import sha256_crypt
from flask_login import UserMixin

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    prefix = db.Column(db.String(20), nullable=False)
    suffix = db.Column(db.String(20))
    phone = db.Column(db.String(25))
    phone_ext = db.Column(db.Integer)
    email=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(256))
    orcid=db.Column(db.String(50))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           "f_name": self.f_name,
           "l_name": self.l_name,
           "job_title": self.job_title,
           "prefix": self.prefix,
           "suffix": self.suffix,
           "phone": self.phone,
           "phone_ext": self.phone_ext,
           "email": self.email,
           "orcid": self.orcid,
       }

    def __init__ (self, f_name, l_name, job_title, prefix, suffix, phone, phone_ext, email, password, orcid):
        self.f_name = f_name
        self.l_name = l_name
        self.job_title = job_title
        self.prefix = prefix
        self.suffix = suffix
        self.phone = phone
        self.phone_ext = phone_ext
        self.email = email
        self.password = sha256_crypt.encrypt(str(password))
        self.orcid = orcid


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    degree = db.Column(db.String(25), nullable=False)
    field_of_study = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(25))
    location = db.Column(db.String(50))
    year_degree_award = db.Column(db.DateTime)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution = db.Column(db.String(50))
    location = db.Column(db.String(100))
    years = db.Column(db.Float)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Societies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    society_name = db.Column(db.String(50))
    membership_type = db.Column(db.Boolean)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    year = db.Column(db.Integer)
    awarding_body = db.Column(db.String(50))
    award_details = db.Column(db.String(100))

    def saveToDB(self):
            db.session.add(self)
            db.session.commit()

class Funding(db.Model):
    id = db.Column(db.Integer, primary_key= True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    funding_amt = db.Column(db.Float)
    funding_body = db.Column(db.String(50))
    programme = db.Column(db.String(50))
    status = db.Column(db.Boolean)


class Teams(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    primary_attribution = db.Column(db.Integer, db.ForeignKey('funding.id'), nullable=False)
