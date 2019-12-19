from flask import render_template, Blueprint, url_for, redirect, request, flash
from models.models import Employee
from app.app import db
from forms.forrms import EmployeeForm, SearchForm


emp = Blueprint("emp", __name__)


@emp.route("/employees")
def show_employees():
    """Render a list of all employees"""
    employees = Employee.query.order_by(Employee.id).all()
    return render_template("employees.html", employees=employees,
                           title="All employees")


@emp.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    """Add a new employee using a form."""
    form = EmployeeForm()

    if form.validate_on_submit():
        # Create new Employee with values from the form.
        employee = Employee(
            name=form.name.data,
            date_of_birth=form.date_of_birth.data,
            salary=form.salary.data,
            department_id=form.department_id.data,
        )
        db.session.add(employee)
        db.session.commit()
        flash("Employee has been added!", "success")
        return redirect(url_for("emp.show_employees"))

    return render_template(
        "employee_add.html", title="Add new employee",
        form=form, legend="New Employee"
    )


@emp.route("/employee/<int:employee_id>")
def show_employee(employee_id):
    """Render page of an employee with a given id"""
    employee = Employee.query.get_or_404(employee_id)
    return render_template(
        "employee.html", title=employee.name, employee=employee
    )


@emp.route("/employee/<int:employee_id>/update", methods=["GET", "POST"])
def update_employee(employee_id):
    """Render page on which you can update information about an
    employee with a given id.
    """
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm()

    if form.validate_on_submit():
        # Set employee attributes to values from the form.
        employee.name = form.name.data
        employee.date_of_birth = form.date_of_birth.data
        employee.salary = form.salary.data
        employee.department_id = form.department_id.data
        db.session.commit()
        flash("Employee has been updated!", "success")
        return redirect(url_for("emp.show_employees"))
    if request.method == "GET":
        # Fill the form with current values.
        form.name.data = employee.name
        form.date_of_birth.data = employee.date_of_birth
        form.salary.data = employee.salary
        form.department_id.data = employee.department_id

    return render_template(
        "employee_add.html", title="Update employee",
        form=form, legend=f"Update {employee.name}"
    )


@emp.route("/employee/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    """Delete employee with a given id"""
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee has been deleted!", "success")
    return redirect(url_for("emp.show_employees"))


@emp.route("/search_employees", methods=["GET", "POST"])
def search_employees():
    """Search employees by date of birth."""
    form = SearchForm()
    if form.validate_on_submit():
        employees = Employee.query\
            .filter(form.from_date.data <= Employee.date_of_birth,
                    Employee.date_of_birth <= form.to_date.data).all()
        return render_template("employees.html", employees=employees,
                               title="Search results")
    return render_template(
        "search.html", title="Search employees", form=form,
        legend="Search employees by date of birth"
    )