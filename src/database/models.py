from .database import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

class JobDescription(Base):
    __tablename__ = 'job_description'
    job_description_id = Column(Integer, primary_key=True, autoincrement=True)
    job_description = Column(String)

class Test(Base):
    __tablename__ = 'test'
    id_test = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    option = Column(String)
    answer = Column(String)
    job_description_id = Column(Integer, ForeignKey('job_description.job_description_id'))

class CandidatInfo(Base):
    __tablename__ = 'candidat_info'
    id_candidatInfo = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    nom = Column(String)
    tel = Column(String)
    accepte = Column(Boolean, default=False) 
    test_password = Column(String)
    job_description_id = Column(Integer, ForeignKey('job_description.job_description_id'))

class CandidatAnswer(Base):
    __tablename__ = 'candidat_answer'
    id_candidatAnswer = Column(Integer, primary_key=True, autoincrement=True)
    id_candidatInfo = Column(Integer, ForeignKey('candidat_info.id_candidatInfo'))
    id_test = Column(Integer, ForeignKey('test.id_test'))
    candidat_answer = Column(String)
