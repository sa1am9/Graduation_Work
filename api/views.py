from flask import Blueprint, request, jsonify
from models.models import Employee, Department
from app.app import db
from api.layout import *


api = Blueprint("api", __name__)


@api.route("/api/employee", methods=["GET"])
def get_employees():
    """Return data of all employees."""
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


@api.route("/api/employee/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    """Return data of an employee with a given id."""
    employee = Employee.query.get_or_404(employee_id)
    return employee_schema.jsonify(employee)


@api.route("/api/employee", methods=["POST"])
def api_add_employee():
    """Add a new employee."""
    # Get attributes for an employee from json.
    name = request.json["name"]
    date_of_birth = request.json["date_of_birth"]
    salary = request.json["salary"]
    department_id = request.json["department_id"]
    # Create a new employee with received values.
    new_employee = Employee(
        name=name,
        date_of_birth=date_of_birth,
        salary=salary,
        department_id=department_id
    )
    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


@api.route("/api/employee/<int:employee_id>", methods=["PUT"])
def api_update_employee(employee_id):
    """Update an employee with a given id."""

    employee = Employee.query.get_or_404(employee_id)
    # Get attributes for an employee from json.
    name = request.json["name"]
    date_of_birth = request.json["date_of_birth"]
    salary = request.json["salary"]
    department_id = request.json["department_id"]
    # Set new values for attributes.
    employee.name = name
    employee.date_of_birth = date_of_birth
    employee.salary = salary
    employee.department_id = department_id

    db.session.commit()

    return employee_schema.jsonify(employee)


@api.route("/api/employee/<int:employee_id>", methods=["DELETE"])
def api_delete_employee(employee_id):
    """Delete an employee with a given id."""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# =========== Departments ==========

@api.route("/api/department", methods=["GET"])
def get_departments():
    """Return data of all departments."""
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    return jsonify(result)


@api.route("/api/department/<int:department_id>", methods=["GET"])
def get_department(department_id):
    """Return data of a department with a given id."""
    department = Department.query.get_or_404(department_id)
    return department_schema.jsonify(department)


@api.route("/api/department", methods=["POST"])
def api_add_department():
    """Add a new department."""
    # Get name from json.
    name = request.json["name"]
    # Create department with name from json.
    new_department = Department(name=name)
    db.session.add(new_department)
    db.session.commit()

    return department_schema.jsonify(new_department)


@api.route("/api/department/<int:department_id>", methods=["PUT"])
def api_update_department(department_id):
    """Update a department with a given id."""
    department = Department.query.get_or_404(department_id)
    # Get name from json.
    name = request.json["name"]
    # Set new department name.
    department.name = name
    db.session.commit()

    return department_schema.jsonify(department)


@api.route("/api/department/<int:department_id>", methods=["DELETE"])
def api_delete_department(department_id):
    """Delete a department with a given id."""
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()

    return department_schema.jsonify(department)