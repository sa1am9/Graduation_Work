import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Department(Base):
    """Department class"""

    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    employees = relationship('Employee')

    def __init__(self, name): # init class by name
        self.name = name

class Employee(Base):
    """Employee class"""

    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String, default='User')
    date_of_birth = Column(Date, nullable=False)
    salary = Column(Integer, default=0)
    department_id = Column(Integer, ForeignKey('department.department_id'),
                           nullable=False)

    def __init__(self, name, date_of_birth, salary, department_id):
        self.name = name
        if isinstance(date_of_birth, datetime.date):
            self.date_of_birth = date_of_birth
        else:
            self.date_of_birth = Employee.date_from_str(date_of_birth)
        self.salary = salary
        self.department_id = department_id

    @staticmethod
    def date_from_str(str_object):
        """Convert string to date
        @param: format dd/mm/yyyy
        """
        return datetime.datetime.strftime(str_object, "%d/%m/%y")