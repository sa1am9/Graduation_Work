"""Realisation web server with REST API"""
import logging
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ApiConfiguration
from flask_restful import Api, Resource, reqparse
from service import db as crud

app = Flask(__name__)
app.config.from_object(ApiConfiguration)
# Data base
db = SQLAlchemy(app)
# REST Api
api = Api(app)
parser_for_department = reqparse.RequestParser()
parser_for_department.add_argument('dep_id')
parser_for_employee = reqparse.RequestParser()
parser_for_employee.add_argument('name')
parser_for_employee.add_argument('department_id')
parser_for_employee.add_argument('date_of_birthday')
parser_for_employee.add_argument('salary')
parser_for_employees = reqparse.RequestParser()
parser_for_employees.add_argument('date_from')
parser_for_employees.add_argument('date_by')
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
logger.info('Web-service started')


class Departments(Resource):
    """Class for GET method that is used to get list of department (/api/departments)"""
    def get(self):
        """
        GET method which returns list of departments
        :return: department`s ids` list and employees` list
        :rtype: JSON
        """

        data = crud.Departments.get_all()
        departments = data[0]
        avg_salaries = data[1]
        ids = []
        employees = []
        salaries = []
        for i in range(0, len(departments)):
            ids.append(departments[i].id)
            employees_list = []
            for employee in departments[i].employees:
                employees_list.append(employee.name)
            employees.append(employees_list)
            for salary in avg_salaries:
                # salary relates department
                if departments[i].id == salary[1]:
                    salaries.append(str(salary[0])[:-2])
                    avg_salaries.remove(salary)
                    break
            else:
                salaries.append('...')
        logger.debug('GET method (/api/departments) was successful')
        return {'ids': ids, 'employees': employees, 'salaries': salaries}


class DepartmentsIds(Resource):
    """Class for GET method that is used to get list of departments` ids (/api/departments-ids)"""
    def get(self):
        """
        GET method which returns list of departments` ids
        :return: department`s ids` list
        :rtype: JSON
        """

        departments = crud.Departments.get_all()[0]
        ids = []
        for department in departments:
            ids.append(department.id)
        logger.debug('GET method (/api/departments-ids) was successful')
        return {'ids': ids}


class Department(Resource):
    """
    Class for GET, PUT, DELETE method which is used for one department (/api/department/<dep_id>)
    """
    def get(self, dep_id):
        """
        GET method that returns the department that is found with department`s id
        :param int dep_id: department`s id which is used to return department
        :return: department`s id and list of employees who work in this department
        :rtype: JSON
        """

        try:
            department = crud.Departments.get(dep_id)
        except AttributeError:
            logger.debug(f'GET method (/api/department/{dep_id}) was not successful (404)')
            return {'error': 'department not found'}, 404
        employees = []
        for employee in department.employees:
            employees.append(employee.name)
        logger.debug(f'GET method (/api/department/{dep_id}) was successful')
        return {'id': department.id, 'employees': employees}

    def put(self, dep_id):
        """
        PUT method that receives new department`s id and updates it
        :param int dep_id: department`s id which is used to find department
        :return: new department`s id
        :rtype: JSON
        """

        data = parser_for_department.parse_args()
        try:
            crud.Departments.update(dep_id, data['dep_id'])
        except AttributeError:
            logger.debug(f'PUT method (/api/department/{dep_id}) was not successful (404)')
            return {'error': 'department not found'}, 404
        except ValueError:
            logger.debug(f'PUT method (/api/department/{dep_id}) was not successful (400)')
            return {'error': 'data incorrect'}, 400
        logger.debug(f'PUT method (/api/department/{dep_id}) was successful')
        return {'id': data['dep_id']}, 201

    def delete(self, dep_id):
        """
        DELETE method that deletes the department
        :param int dep_id: department`s id which is used to find department
        :return: id of department which has been deleted
        :rtype: JSON
        """

        try:
            crud.Departments.delete(dep_id)
        except:
            logger.debug(f'DELETE method (/api/department/{dep_id}) was not successful (404)')
            return {'error': 'employee not found'}, 404
        logger.debug(f'DELETE method (/api/department/{dep_id}) was successful')
        return {'id': dep_id}, 200


class AddDepartment(Resource):
    """Class for POST method that adds new department (/api/department)"""
    def post(self):
        """
        POST method that receives data and adds new department
        :return: department`s id which has been added
        :rtype: JSON
        """

        data = parser_for_department.parse_args()
        try:
            crud.Departments.add(data['dep_id'])
        except:
            logger.debug(f'POST method (/api/department) was not successful (400)')
            return {'error': 'incorrect data'}, 400
        logger.debug(f'POST method (/api/department) was successful')
        return {'id': data['dep_id']}, 201


class Employees(Resource):
    """Class for GET method that is used to get list of all employees (/api/employees)"""
    def get(self):
        """
        GET method that returns list of all employees
        :return: list of information about all employees (names, departments, dates of birthday,
        salaries)
        :rtype: JSON
        """

        employees = crud.Employees.get_all()
        ids = []
        names = []
        departments = []
        dates_of_birthday = []
        salaries = []
        for employee in employees:
            ids.append(employee.id)
            names.append(employee.name)
            departments.append(employee.department_id)
            dates_of_birthday.append(str(employee.date_of_birthday))
            salaries.append(str(employee.salary))
        logger.debug(f'GET method (/api/employees) was successful')
        return {'ids': ids, 'names': names, 'departments': departments,
                'dates_of_birthday': dates_of_birthday, 'salaries': salaries}

    def post(self):
        """
        POST method that returns filtered list of all employees by dates of birthday
        :return: list of information about all employees (names, departments, dates of birthday,
        salaries)
        :rtype: JSON
        """

        data = parser_for_employees.parse_args()
        if data['date_by'] is None or data['date_by'] == '':
            data['date_by'] = date.today()
        if data['date_from'] is None or data['date_by'] == '':
            data['date_from'] = ''
        employees = crud.Employees.get_by_date(data['date_from'], data['date_by'])
        ids = []
        names = []
        departments = []
        dates_of_birthday = []
        salaries = []
        for employee in employees:
            ids.append(employee.id)
            names.append(employee.name)
            departments.append(employee.department_id)
            dates_of_birthday.append(str(employee.date_of_birthday))
            salaries.append(str(employee.salary))
        logger.debug(f'POST method (/api/employees) was successful')
        return {'ids': ids, 'names': names, 'departments': departments,
                'dates_of_birthday': dates_of_birthday, 'salaries': salaries}


class Employee(Resource):
    """
    Class for GET, PUT, DELETE method which is used for one employee (/api/employee/<employee_id>)
    """
    def get(self, employee_id):
        """
        GET method that finds and returns employee
        :param int employee_id: employee`s id which is used to find employee
        :return: information about employee (name, department, date of birthday, salary)
        :rtype: JSON
        """

        try:
            employee = crud.Employees.get(employee_id)
        except AttributeError:
            logger.debug(f'GET method (/api/employee/{employee_id}) was not successful (404)')
            return {'error': 'employee not found'}, 404
        logger.debug(f'GET method (/api/employee/{employee_id}) was successful')
        return {'id': employee.id, 'name': employee.name, 'department_id': employee.department_id,
                'date_of_birthday': str(employee.date_of_birthday), 'salary': str(employee.salary)}

    def put(self, employee_id):
        """
        PUT method that receives new information about employee and updates it
        :param int employee_id: employee`s id which is used to find employee
        :return: employee`s id
        :rtype: JSON
        """

        data = parser_for_employee.parse_args()
        try:
            crud.Employees.update(employee_id, **data)
        except AttributeError:
            logger.debug(f'PUT method (/api/employee/{employee_id}) was not successful (404)')
            return {'error': 'employee not found'}, 404
        except ValueError:
            logger.debug(f'PUT method (/api/employee/{employee_id}) was not successful (400)')
            return {'error': 'incorrect data'}, 400
        logger.debug(f'PUT method (/api/employee/{employee_id}) was successful')
        return {'id': employee_id}, 201

    def delete(self, employee_id):
        """
        DELETE method that deletes employee
        :param int employee_id: employee`s id which is used to find employee
        :return: id of employee that has been deleted
        :rtype: JSON
        """

        try:
            crud.Employees.delete(employee_id)
        except:
            logger.debug(f'DELETE method (/api/employee/{employee_id}) was not successful (404)')
            return {'error': 'employee not found'}, 404
        logger.debug(f'DELETE method (/api/employee/{employee_id}) was successful')
        return {'id': employee_id}, 200


class AddEmployee(Resource):
    """Class for POST method that adds new employee (api/employee)"""
    def post(self):
        """
        POST method that receives data and adds new employee
        :return: employee`s id who has been added
        :rtype: JSON
        """

        data = parser_for_employee.parse_args()
        try:
            employee_id = crud.Employees.add(**data).id
        except AttributeError:
            logger.debug(f'POST method (/api/employee) was not successful (400)')
            return {'error': 'department not found'}, 400
        except ValueError:
            logger.debug(f'POST method (/api/employee) was not successful (400)')
            return {'error': 'incorrect data'}, 400
        logger.debug(f'POST method (/api/employee) was successful')
        return {'id': employee_id}, 201


api.add_resource(Departments, '/api/departments')
api.add_resource(DepartmentsIds, '/api/departments-ids')
api.add_resource(Department, '/api/department/<dep_id>')
api.add_resource(AddDepartment, '/api/department')
api.add_resource(Employees, '/api/employees')
api.add_resource(Employee, '/api/employee/<employee_id>')
api.add_resource(AddEmployee, '/api/employee')