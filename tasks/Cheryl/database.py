from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from teams_and_flags import team_data

Base = declarative_base()
engine = create_engine('sqlite:///main.db', echo=True)
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    flag = Column(String)
 
    def __init__(self, id, username, password, flag):
        self.id = id
        self.username = username
        self.password = password
        self.flag = flag

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    answer = Column(String)
    stage = Column(Integer)

    def __init__(self, user_id):
        self.user_id = user_id
        self.stage = 1

def init_db():
    Session = sessionmaker(bind=engine)
    s = Session()

    Base.metadata.create_all(engine)
    for id, (username, password, flag) in enumerate(team_data):
        user = User(id, username, password, flag)
        s.add(user)
        task = Task(id)
        s.add(task)
    s.commit()
    s.close()

def check_user(username, password):
    Session = sessionmaker(bind=engine)
    s = Session()

    return s.query(User).filter_by(username=username, password=password).first()

def get_user(id):
    Session = sessionmaker(bind=engine)
    s = Session()

    return s.query(User).filter_by(id=id).first()

def get_task(user_id):
    Session = sessionmaker(bind=engine)
    s = Session()

    return s.query(Task).filter_by(user_id=user_id).first()

def update_answer(user_id, answer):
    Session = sessionmaker(bind=engine)
    s = Session()

    task = s.query(Task).filter_by(user_id=user_id).first()
    task.answer = answer
    s.commit()
    s.close()

def update_stage(user_id, stage):
    Session = sessionmaker(bind=engine)
    s = Session()

    task = s.query(Task).filter_by(user_id=user_id).first()
    task.stage = stage
    s.commit()
    s.close()