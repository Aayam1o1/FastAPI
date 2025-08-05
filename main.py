from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db
from pydantic import BaseModel
from typing import Annotated, List 
from fastapi import HTTPException

# Create tables
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
app = FastAPI()

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
    
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
@app.get("/")
def root():
    return {"message": "FastAPI with PostgreSQL connected!"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)

@app.get("/users/", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not foind")
    return result 

@app.get("/choices/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Choice not foind")
    return result 

@app.post("/questions/")
async def create_questions(question: QuestionBase, db:db_dependency):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    for choice in question.choices:
        db_choice= models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct,question_id=db_question.id)
        db.add(db_choice)
    db.commit()
        
        
