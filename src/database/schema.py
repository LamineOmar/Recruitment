from pydantic import BaseModel
from typing import Optional

class JobDescription(BaseModel):
    job_description :str
    job_name  :str

    class Config:
        orm_mode = True


class Test(BaseModel):
    question : str
    option : str
    answer : str
    job_description_id : int

    class Config:
        orm_mode = True
        
        
class CandidatInfo(BaseModel):
    email : str 
    score : Optional[str]
    test_password : Optional[str]
    job_description_id : int

    class Config:
        orm_mode = True
        
        
class CandidatAnswer(BaseModel):
    id_candidat : int
    id_test : int
    candidat_answer : str

    class Config:
        orm_mode = True