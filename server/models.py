from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Research(db.Model, SerializerMixin):
    __tablename__ = 'research'
    serialize_rules = ('-research_authors.research_id','-research_authors.research')

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    research_authors = db.relationship('ResearchAuthors', back_populates='research')

    @validates('year')
    def validate_year(self, key, year):
        assert len(year) == 4, 'Year Must Have 4 Digits!'
        return year

class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'
    serialize_rules = ('-research.research_authors', '-authors.research_authors')

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('research.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    author = db.relationship('Author', back_populates='research_authors')
    research = db.relationship('Research', back_populates='research_authors')


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'
    serialize_rules = ('-research_authors.author_id', '-research_authors.author')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    research_authors = db.relationship('ResearchAuthors', back_populates='author')

    @validates('field_of_study')
    def validate_fos(self, key, field_of_study):
        possible = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']
        assert field_of_study in possible, f"Field of study must be one of {possible}"
        return field_of_study