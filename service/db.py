"""Module for work with database"""
import logging
from sqlalchemy import func
from rest.api import db
from models.models import *



# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
fh = logging.FileHandler('web-service.log')
ch.setLevel(logging.DEBUG)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


class Departments:
    """Works with departments."""
    @staticmethod
    def get_all():
        """
        Gets list of departments and average salaries
        :return: List of departments and average salaries
        :rtype: tuple (list<departments>, list<tuple(salary)>
        """
        departments = Department.query.all()
        salaries = db.session.query(func.avg(Employee.salary).label('average'),
                                    Employee.department_id).group_by(Employee.department_id).all()
        logger.debug('List of department was returned')
        return departments, salaries

    @staticmethod
    def get(dep_id):
        """
        Gets department
        :param int dep_id: department`s id that is used to find department
        :return: Department
        :rtype: Department
        """
        department = Department.query.filter_by(id=dep_id).first()
        if department is None:
            logger.debug(f'Department {dep_id} is not exist')
            raise AttributeError
        logger.debug(f'Department {dep_id} was returned')
        return department

    @staticmethod
    def add(dep_id):
        """
        Adds new department
        :param dep_id: The unique number of department
        :return: New department that has been added
        :rtype: Department
        """
        try:
            department = Department(id=dep_id)
        except:
            logger.debug(f'Department {dep_id} is exist, it can`t be added')
            raise AttributeError
        db.session.add(department)
        db.session.commit()
        logger.debug(f'Department {dep_id} was added')
        return department

    @staticmethod
    def update(dep_id, new_id):
        """
        Updates the department
        :param int dep_id: The number of department which is changed
        :param int new_id: A new number of department
        :return: modified department
        """
        department = Department.query.filter_by(id=dep_id).first()
        if department is None:
            logger.debug(f'Department {dep_id} is not exist, it can`t be updated')
            raise AttributeError
        try:
            department.id = new_id
        except:
            logger.debug(f'Incorrect data. Department {dep_id} can`t be updated')
            raise ValueError
        logger.debug(f'Department {dep_id} was updated')
        db.session.commit()
        return department

    @staticmethod
    def delete(dep_id):
        """
        Deletes the department
        :param int dep_id: The number of department which is deleted
        :return:
        """
        department = Department.query.filter_by(id=dep_id).first()
        if department is None:
            logger.debug(f'Department {dep_id} is not exist, it can`t be deleted')
            raise AttributeError
        for employee in department.employees:
            db.session.delete(employee)
        db.session.delete(department)
        db.session.commit()
        logger.debug(f'Department {dep_id} was deleted')


class Employees:
    """Works with employees."""
    @staticmethod
    def get_all():
        """
        Gets list of employees
        :return: List of employees
        :rtype: list
        """
        logger.debug('List of employees was returned')
        return Employee.query.all()

    @staticmethod
    def get_by_date(date_from, date_by):
        """
        Gets list of employees who were born on a certain date or in the period between dates
        :param date date_from: from date for filter
        :param date date_by: by date for filter
        :return: filtered list of employees
        :rtype: list
        """
        logger.debug('Filtered by dates list of employees was returned')
        return Employee.query.filter(date_from <= Employee.date_of_birthday, Employee.date_of_birthday <= date_by).all()

    @staticmethod
    def get(employee_id):
        """
        Gets employee
        :param int employee_id: employee`s id that is used to find employee
        :return: Employee
        :rtype: Employee
        """
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee is None:
            logger.debug(f'Employee {employee_id} is not exist')
            raise AttributeError
        logger.debug(f'Employee {employee_id} was returned')
        return employee

    @staticmethod
    def add(name, department_id, date_of_birthday, salary):
        """
        Adds new employee
        :param string name: Employee`s full name
        :param int department_id: Employee`s department number
        :param date date_of_birthday: Employee`s date of birthday
        :param float salary: Employee`s salary
        :return: new employee who has been added
        :rtype: Employee
        """
        if Department.query.filter_by(id=department_id).first() is None:
            logger.debug(f'Department isn`t exist. Employee can`t be added')
            raise AttributeError
        try:
            employee = Employee(name=name, department_id=department_id, date_of_birthday=date_of_birthday,
                                salary=salary)
        except:
            logger.debug(f'Incorrect data. Employee can`t be added')
            raise ValueError
        db.session.add(employee)
        db.session.commit()
        logger.debug(f'Employee was added')
        return employee

    @staticmethod
    def update(employee_id, name, department_id, date_of_birthday, salary):
        """
        Updates information about employee
        :param int employee_id: Employee`s id that is used to find employee
        :param string name: New employee`s full name
        :param int department_id: New employee`s department number
        :param date date_of_birthday: New employee`s date of birthday
        :param float salary: New employee`s salary
        :return: modified employee
        """
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee is None:
            logger.debug(f'Employee isn`t exist')
            raise AttributeError
        try:
            employee.name = name
            employee.department_id = department_id
            employee.date_of_birthday = date_of_birthday
            employee.salary = salary
            db.session.commit()
        except:
            logger.debug(f'Incorrect data. Employee can`t be updated')
            raise ValueError
        logger.debug(f'Employee was updated')
        return employee

    @staticmethod
    def delete(employee_id):
        """
        Deletes employee
        :param int employee_id: Employee`s id that is used to find employee
        :return:
        """
        employee = Employee.query.filter_by(id=employee_id).first()
        if employee is None:
            logger.debug(f'Employee isn`t exist. It can`t be deleted')
            raise AttributeError
        db.session.delete(employee)
        db.session.commit()
