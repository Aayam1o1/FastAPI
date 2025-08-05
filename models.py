from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base 


class User(Base):
    __tablename__ = "users"  # Table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    
class Choices(Base):
    __tablename__ = 'choices'
    
    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))