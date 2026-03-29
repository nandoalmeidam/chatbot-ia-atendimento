from sqlalchemy import Column, Integer, String
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MensagemDB(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    texto = Column(String)
    
Base.metadata.create_all(bind=engine)