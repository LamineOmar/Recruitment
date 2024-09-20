from sqlalchemy.orm import Session
from . import schema, models
from sqlalchemy import desc

class crud:
    def save_job_description(db: Session, info: schema.JobDescription):
        job_description_info_model = models.JobDescription(**info.dict())
        db.add(job_description_info_model)
        db.commit()
        db.refresh(job_description_info_model)
        return job_description_info_model


    def save_Test_info(db: Session, info: schema.Test):
        Test_model = models.Test(**info.dict())
        db.add(Test_model)
        db.commit()
        db.refresh(Test_model)
        return Test_model

    def save_CandidatInfo(db: Session, info: schema.CandidatInfo):
        CandidatInfo_model = models.CandidatInfo(**info.dict())
        db.add(CandidatInfo_model)
        db.commit()
        db.refresh(CandidatInfo_model)
        return CandidatInfo_model

    def save_CandidatAnswer(db: Session, info: schema.CandidatAnswer):
        CandidatAnswer_model = models.CandidatAnswer(**info.dict())
        db.add(CandidatAnswer_model)
        db.commit()
        db.refresh(CandidatAnswer_model)
        return CandidatAnswer_model
    
    
    def get_job_description_info(db: Session):
        return db.query(models.JobDescription).all()
    
    def get_Tests_info(db:Session):
        return db.query(models.Test).all()
    
    def get_last_job_description(db: Session):
        result = db.query(models.JobDescription).order_by(desc(models.JobDescription.job_description_id)).first()
        return result.job_description, result.job_description_id
    
        
    # def get_device_info(db: Session, token: str = None):
    #     if token is None:
    #         return db.query(models.DeviceInfo).all()
    #     else:
    #         return db.query(models.DeviceInfo).filter(models.DeviceInfo.token == token).first()
    
    # def get_nudges_configuration(db: Session):
    #     return db.query(models.Configuration).first()

    # def delete_nudges_configuration(db: Session):
    #     db.query(models.Configuration).delete()

    # def error_message(message):
    #     return {
    #         'error': message
    #     }