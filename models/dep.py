from flask import render_template, Blueprint, url_for, redirect, request, flash
from sqlalchemy.exc import IntegrityError
from models.models import Employee, Department
from app.app import db
from forms.forrms  import DepartmentForm


dep = Blueprint("dep", __name__)


@dep.route("/departments")
def show_departments():
    """Render a list of all departments"""
    departments = Department.query.order_by(Department.id).all()
    employees = Employee.query.all()

    # Get information about all employees' salaries
    # and departments they belong to.
    salaries_info = {}
    for employee in employees:
        if employee.department_id in salaries_info:
            salaries_info[employee.department_id]["total"] += employee.salary
            salaries_info[employee.department_id]["count"] += 1
        else:
            salaries_info.update(
                {
                    employee.department_id: {
                        "total": employee.salary,
                        "count": 1,
                    }
                }
            )

    # Calculate average salaries for all departments
    # and store them in a dictionary.
    avg_salaries = {}
    for department in departments:
        if department.id in salaries_info:
            # If department has employees.
            avg_salaries[department.id] = (
                round(salaries_info[department.id]["total"]
                      / salaries_info[department.id]["count"], 2)
            )
        else:
            # Department has no employees.
            avg_salaries[department.id] = 0

    return render_template(
        "html/departaments.html", departments=departments,
        avg_salaries=avg_salaries, title="All departments"
    )


@dep.route("/add_department", methods=["GET", "POST"])
def add_department():
    """Add a new department using a form."""
    form = DepartmentForm()

    if form.validate_on_submit():
        # Set department name to a value from the form.
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash("Department has been added!", "success")
        return redirect(url_for("dep.show_departments"))

    return render_template(
        "html/departament_add.html", title="Add new department",
        form=form, legend="New Department"
    )


@dep.route("/department/<int:department_id>")
def show_department(department_id):
    """Render page of a department with a given id"""
    department = Department.query.get_or_404(department_id)
    return render_template(
        "html/departament.html", title=department.name, department=department
    )


@dep.route("/department/<int:department_id>/update", methods=["GET", "POST"])
def update_department(department_id):
    """Delete department with a given id"""
    department = Department.query.get_or_404(department_id)
    form = DepartmentForm()

    if form.validate_on_submit():
        # Set department name to a value from the form.
        department.name = form.name.data
        db.session.commit()
        flash("Department has been updated!", "success")
        return redirect(url_for("dep.show_departments"))
    if request.method == "GET":
        # Fill the form with current value.
        form.name.data = department.name

    return render_template(
        "html/departament_add.html", title="Update department",
        form=form, legend=f"Update {department.name}"
    )


@dep.route("/department/<int:department_id>/delete", methods=["POST"])
def delete_department(department_id):
    """Delete department with a given id"""
    department = Department.query.get_or_404(department_id)
    try:
        db.session.delete(department)
        db.session.commit()
    except IntegrityError:
        # If department has employees handle an exception.
        flash("Department that has employees cannot be deleted!", "danger")
        return redirect(url_for("dep.show_departments"))
    else:
        # Redirect to departments page with success message.
        flash("Department has been deleted!", "success")
        return redirect(url_for("dep.show_departments"))