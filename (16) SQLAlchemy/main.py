from sqlalchemy.orm import sessionmaker
from models import Employee, engine

Session = sessionmaker(bind=engine)
with Session() as session:
    employee = Employee(
        first_name="Ivan",
        last_name="Ivanov",
        age=33
    )
    session.add(employee)
    session.commit()