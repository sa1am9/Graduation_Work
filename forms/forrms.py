from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, FloatField,
                     DateTimeField, SelectField)
from wtforms.validators import DataRequired, Length, ValidationError
from models.models import Department


class EmployeeForm(FlaskForm):
    """Form for adding and updating employees."""
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    date_of_birth = DateTimeField("Date of Birth", format='%m/%d/%y',validators=[DataRequired()])
    salary = FloatField("Salary", validators=[DataRequired()])
    department_id = SelectField("Department", coerce=int, choices=[
        (department.id, department.name) for department in
        Department.query.order_by(Department.id).all()])

    submit = SubmitField("Submit")

    def __init__(self):
        super().__init__()
        EmployeeForm.department_id = SelectField("Department", coerce=int, choices=[
            (department.id, department.name) for department in
            Department.query.order_by(Department.id).all()])


class DepartmentForm(FlaskForm):
    """Form for adding and updating departments."""
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    def validate_name(self, name):
        """Check if department with provided name exists."""
        department = Department.query.filter_by(name=name.data).first()
        if department:
            raise ValidationError("Department with this name already exists.")

    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    """Form for searching employees by date of birth."""
    from_date = DateTimeField("From",  format='%m/%d/%y', validators=[DataRequired()] )
    to_date = DateTimeField("To", format='%m/%d/%y',  validators=[DataRequired()])

    def validate_to_date(self, to_date):
        """Check if from date is before to date in the form."""
        if self.to_date.data < self.from_date.data:
            raise ValidationError("To date must be after from date.")

    submit = SubmitField("Search")