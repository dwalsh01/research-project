from flask_sqlalchemy import Model, SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


'''
Misc base functions/classes
'''
def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class DBFunctions():
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class FileStore:
    filename = db.Column(db.String(100), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)

'''
Users section:

- Admin
- Researcher
- Reviewer
- Host university
- RC Centre?
'''
class Role(db.Model, DBFunctions):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Users(UserMixin, db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.relationship('Role', secondary='user_roles')
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


class Education(db.Model, DBFunctions):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    degree = db.Column(db.String(25), nullable=False)
    field_of_study = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(25))
    location = db.Column(db.String(50))
    year_degree_award = db.Column(db.DateTime)

class EducationSchema(ma.ModelSchema):
    class Meta:
        model = Education


class Employment(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution = db.Column(db.String(50))
    location = db.Column(db.String(100))
    years = db.Column(db.Float)

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
    deadline_text: Open/Rolling/Expired
'''
class ProposalCall(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    deadline_text = db.Column(db.String(50))
    deadline_time = db.Column(db.Date)
    award_amount = db.Column(db.Float, nullable=False)
    amount_left = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    short_text = db.Column(db.String(500), nullable=False)
    text_description = db.Column(db.Text(),  nullable=False)
    target_audience = db.Column(db.Text(), nullable=False)
    eligibil_text = db.Column(db.Text(), nullable=False)
    duration = db.Column(db.String(50))
    report_guidelines = db.Column(db.Text(), nullable=False)
    files = db.relationship('ProposalCallFiles', backref='call', lazy=True)
    start_date = db.Column(db.Date())
    start_date_end = db.Column(db.Date())
    contact = db.Column(db.String(75), nullable=False)

class ProposalThemes(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    prop_id = db.Column(db.Integer, db.ForeignKey('proposal_call.id'), nullable=False)
    theme_name = db.Column(db.String(100), nullable=False, unique=True)

class ProposalCallFiles(FileStore, db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
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
Application:
'''
class NrpArea(db.Model, DBFunctions):
    nrp_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nrp_title = db.Column(db.String(200), nullable=False)

class NrpSchema(ma.ModelSchema):
    class Meta:
        model = NrpArea


class ProposalApplication(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal_call.id'), nullable=False)
    applicant = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(60), nullable=False)
    amount_required = db.Column(db.Float, nullable=False)
    nrp_area = db.Column(db.Integer, db.ForeignKey('nrp_area.nrp_id'), nullable=False)
    textbox = db.Column(db.Text, nullable=False)
    animal_statement = db.Column(db.Text, nullable=False)
    human_statement = db.Column(db.Text, nullable=False)
    applicant_country = db.Column(db.String(75), nullable=False)
    list_of_co_applicants = db.relationship('CoApplicants', backref='propapp', lazy=True)
    list_of_collaborators = db.relationship('ApplicationCollaborators', backref='propapp', lazy=True)
    abstract = db.Column(db.Text, nullable=False)
    lay_abstract = db.Column(db.Text, nullable=False)
    signed = db.Column(db.Boolean, nullable=False)
    files = db.relationship('ApplicationFiles', backref='propapp', lazy=True)


class ApplicationFiles(FileStore, db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)

class CoApplicants(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)
    co_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class ApplicationCollaborators(db.Model, DBFunctions):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    organization = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(70), nullable=False)

class ApplicationDraft(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    prop_id = db.Column(db.Integer, db.ForeignKey('proposal_call.id'), nullable=False)
    applicant = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    draft = db.Column(db.JSON, nullable=False)

class ApplicationDraftSchema(ma.ModelSchema):
    class Meta:
        model = ApplicationDraft

class Reviews(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)
    themes = db.relationship('Themes', backref='review', lazy=True)

class Themes(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    theme_critique = db.Column(db.Text, nullable=False)
    theme_name = db.Column(db.String(100), db.ForeignKey('proposal_themes.theme_name'), nullable=False)
    theme_rating = db.Column(db.Integer, nullable=False)

class PendingReviews(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('proposal_application.id'), nullable=False)
    deadline = db.Column(db.Date)

class PendingReviewsSchema(ma.ModelSchema):
    class Meta:
        model = PendingReviews

'''

GRANT:
primary attrib (15/SIRG/3293)
'''
class AwardGrant(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=True)
    amount = db.Column(db.Float, nullable=False)
    funding_body = db.Column(db.String(60), nullable=False)
    funding_programme = db.Column(db.String(90), nullable=False)
    primary_attrib = db.Column(db.String(60), nullable=False, unique=True)
    pi = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

class RCTeam(db.Model, DBFunctions):
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    team_desc = db.Column(db.Text)
    primary_attrib = db.Column(db.ForeignKey('award_grant.primary_attrib'), nullable=False)
    team_members = db.relationship('RCTeamMembers', backref='rcteam', lazy=True)

class RCTeamMembers(db.Model, DBFunctions):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.ForeignKey('rc_team.team_id'), nullable=False)
    team_member = db.Column(db.ForeignKey('users.id'), nullable=False)
    team_member_position = db.Column(db.String(70), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    co_pi = db.Column(db.Boolean, default=False, nullable=False)
    pi = db.Column(db.Boolean, default=False, nullable=False)


class RCTeamMembersSchema(ma.ModelSchema):
    class Meta:
        model = RCTeamMembers

class RCTeamSchema(ma.ModelSchema):
    class Meta:
        model = RCTeam

class AwardGrantSchema(ma.ModelSchema):
    class Meta:
        model = AwardGrant

class ThemesSchema(ma.ModelSchema):
    class Meta:
        model = Themes

class ReviewsSchema(ma.ModelSchema):
    class Meta:
        model = Reviews

class ApplicationCollaboratorsSchema(ma.ModelSchema):
    class Meta:
        model = ApplicationCollaborators

class CoApplicantsSchema(ma.ModelSchema):
    class Meta:
        model = CoApplicants

class ApplicationFilesSchema(ma.ModelSchema):
    class Meta:
        model = ApplicationFiles

class ProposalApplicationSchema(ma.ModelSchema):
    class Meta:
        model = ProposalApplication

class EducationSchema(ma.ModelSchema):
    class Meta:
        model = Education

class ProposalCallFilesSchema(ma.ModelSchema):
    class Meta:
        model = ProposalCallFiles

class ProposalThemesSchema(ma.ModelSchema):
    class Meta:
        model = ProposalThemes

class ProposalCallSchema(ma.ModelSchema):
    class Meta:
        model = ProposalCall

class TeamsSchema(ma.ModelSchema):
    class Meta:
        model = Teams

class FundingSchema(ma.ModelSchema):
    class Meta:
        model = Funding

class AwardsSchema(ma.ModelSchema):
    class Meta:
        model = Awards

class SocietiesSchema(ma.ModelSchema):
    class Meta:
        model = Societies

class EmploymentSchema(ma.ModelSchema):
    class Meta:
        model = Employment

class UserRolesSchema(ma.ModelSchema):
    class Meta:
        model = UserRoles

class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role