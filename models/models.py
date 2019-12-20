from app.app import db


class Employee(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer, index=True)
    name = db.Column(db.String(60), index=True, unique=True)
    date_of_birth = db.Column(db.DateTime(60), index=True)


    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))


    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')
    def __repr__(self):
        return '<Department: {}>'.format(self.name)

