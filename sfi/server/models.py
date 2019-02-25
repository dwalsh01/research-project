from flask_sqlalchemy import Model, SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class DBFunctions:
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class FileStore:
    filename = db.Column(db.String(100), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)


class Users(UserMixin, db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    #user_type = db.Column(db.Integer, db.ForeignKey('user_types.user_id'), nullable=False)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    prefix = db.Column(db.String(20), nullable=False)
    suffix = db.Column(db.String(20))
    phone = db.Column(db.String(25))
    phone_ext = db.Column(db.Integer)
    email=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(256))
    orcid=db.Column(db.String(50), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    @staticmethod
    def convertToSchema(request_data):
        mapping = {
            'first_name': 'f_name',
            'second_name': 'l_name',
            'job_title': 'job_title',
            'prefix': 'prefix',
            'suffix': 'suffix',
            'phone': 'phone',
            'phone_extension': 'phone_ext',
            'email': 'email',
            'password': 'password',
            'orcid': 'orcid'
        }
        out = dict()
        for key in request_data:
            out[mapping[key]] = request_data[key]
        return out


    def __init__ (self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.password = pbkdf2_sha256.hash(str(self.password))


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

class UsersSchema(ma.ModelSchema):
    class Meta:
        fields = ('id',
                  'f_name',
                  'l_name',
                  'job_title',
                  'prefix',
                  'suffix',
                  'phone',
                  'phone_ext',
                  'email',
                  'orcid'
                )

class EducationSchema(ma.ModelSchema):
    class Meta:
        fields = ('person_id',
                  'degree',
                  'field_of_study',
                  'institution',
                  'location',
                  'year_degree_award',

                )
class Education(db.Model, DBFunctions):
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    degree = db.Column(db.String(25), nullable=False)
    field_of_study = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(25))
    location = db.Column(db.String(50))
    year_degree_award = db.Column(db.DateTime)

    def __init__(self, person_id, degree, field_of_study, institution, location, year_degree_award):
       self.person_id = person_id
       self.degree = degree
       self.field_of_study = field_of_study
       self.institution = institution
       self.location = location
       self.year_degree_award = year_degree_award

class EducationSchema(ma.ModelSchema):
    class Meta:
        model = Education

class Employment(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution = db.Column(db.String(50))
    location = db.Column(db.String(100))
    years = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        return super(Employment).__init__(*args, **kwargs)


class Societies(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    society_name = db.Column(db.String(50))
    membership_type = db.Column(db.Boolean)


class Awards(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    year = db.Column(db.Integer)
    awarding_body = db.Column(db.String(50))
    award_details = db.Column(db.String(100))


class Funding(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key= True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    funding_amt = db.Column(db.Float)
    funding_body = db.Column(db.String(50))
    programme = db.Column(db.String(50))
    status = db.Column(db.Boolean)


class Teams(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    primary_attribution = db.Column(db.Integer, db.ForeignKey('funding.id'), nullable=False)

'''
Proposal:
    Deadline TEXT STRING
    Deadline int months
    Text - TEXT
    Target audience (text)
    Eligiblity criteria (text)
    Duration of the award (24/48 months etc) int MONTHS NULLABLE
    report guidelines TEXT
    report guidelines FILE
    Reporting Guidelines of the award (text/pdf)
    Start date DATE
    Start date end DATE
    contact EMAIL

    Closed/Rolling/Open
'''
class ProposalCall(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    deadline_text = db.Column(db.String(50))
    deadline_time = db.Column(db.Interval(native=True))
    award_amount = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    short_text = db.Column(db.String(500), nullable=False)
    text_description = db.Column(db.Text(),  nullable=False)
    target_audience = db.Column(db.Text(), nullable=False)
    eligibil_text = db.Column(db.Text(), nullable=False)
    duration = db.Column(db.Interval(native=True))
    report_guidelines = db.Column(db.Text(), nullable=False)
    files = db.relationship('ProposalCallFiles', backref='call', lazy=True)
    start_date = db.Column(db.Date())
    start_date_end = db.Column(db.Date())
    contact = db.Column(db.String(75), nullable=False)

class ProposalCallFiles(FileStore, db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    prop_id = db.Column(db.Integer, db.ForeignKey('proposal_call.id'), nullable=False)

class ShortProposalSchema(ma.ModelSchema):
    class Meta:
        fields = ('id',
                  'deadline_text',
                  'deadline_time',
                  'award_amount',
                  'title',
                  'short_text'
                 )

class LongProposalSchema(ma.ModelSchema):
    class Meta:
        model = ProposalCall

'''
Users:
    id
    USER_ID (indicates type)
    USER_NAME (friendly name)



primary attrib ID generation/matching

- RC Centre
- Host uni
- Reviewer
'''
class UserTypes(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)


'''

Application:
    Title (max 30 words)
    Duration (months)
    NRP Area: big list
    Textbox (250 words)
    Ethical issues:
        2 statements:
            animals?
            human bio material?
    applicants location (country)
    co-applicant-list
    list of collaborators:
        name
        organisation
        email
    abstract (max 200w)
    lay ab (max 100w)
    PDF/File doc(s)
    Declaration ("I agree with ...")

Should be able to have a draft (completed bool?)/seperate table
'''
class ProposalApplication(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal_call.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Interval(native=True))
    nrp_area = db.Column(db.Integer, db.ForeignKey('nrp_area.nrp_id'), nullable=False)
    textbox = db.Column(db.Text, nullable=False)
    animal_statement = db.Column(db.Text, nullable=False)
    human_statement = db.Column(db.Text, nullable=False)
    applicant_country = db.Column(db.String(75), nullable=False)
    #list_of_co_applicants = "??"
    #list_of_collabs = "??"
    abstract = db.Column(db.Text, nullable=False)
    lay_abstract = db.Column(db.Text, nullable=False)
    signed = db.Column(db.Boolean, nullable=False)
    # Relationship (1-many)
    files = db.relationship('ApplicationFiles', backref='proposal', lazy=True)


class ApplicationFiles(FileStore, db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    prop_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)

class NrpArea(db.Model, DBFunctions):
    nrp_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nrp_title = db.Column(db.String(200), nullable=False)

class NrpSchema(ma.ModelSchema):
    class Meta:
        model = NrpArea

'''

GRANT:
start
end
amt
funding body
funding programme
status
primary attrib (15/SIRG/3293)
'''
class AwardGrant(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
