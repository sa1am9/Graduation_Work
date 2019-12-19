from app.app import ma


class EmployeeSchema(ma.Schema):
    """Utility class for serializing employees data."""
    class Meta:
        """Fields for serializing."""
        fields = ("id", "name", "date_of_birth", "salary", "department_id")

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class DepartmentSchema(ma.Schema):
    """Utility class for serializing departments data."""
    class Meta:
        """Fields for serializing."""
        fields = ("id", "name")

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)