from main import app
import requests
from flask import render_template, request, redirect

@app.route('/')
def index():
    """
    Start page that redirect user to page with departments (/departments)
    :return: redirect to departments page
    """
    return redirect('/departments')


@app.route('/departments')
def departments():
    """
    Sends get request to server (api/departments); receives list of departments from server and
    displays it
    :return: HTML page ('departments.html') with departments list
    """
    departments_list = requests.get('http://127.0.0.1:5000/api/departments').json()
    logger.debug('Departments page was displayed with list of departments')
    return render_template('departments.html', departments_list=departments_list)


@app.route('/department/<dep_id>', methods=['GET', 'POST'])
def department(dep_id):
    """
    GET method: receives department`s id and displays HTML page for changing department`s id
    POST method: takes new department`s id, sends post request to server that updates department`s
    id in database
    :param str dep_id: department`s id which is used to find department
    :return: GET: HTML page with department`s id that for changing | POST: redirect to departments
    page after updating
    """
    if request.method == 'POST':
        new_id = request.form.get('department_id', '')
        url = 'http://127.0.0.1:5000/api/department/' + dep_id
        requests.put(url, data={'dep_id': new_id})
        logger.debug('Information about department was sent to server (update)')
        return redirect('/departments')
    logger.debug('Department page was displayed')
    return render_template('department.html', dep_id=dep_id)


@app.route('/department', methods=['GET', 'POST'])
def add_department():
    """
    GET method: displays page to add new department
    POST method: sends data about department into server (api/department) that adds new department
    in database
    :return: HTML page with form to add new department
    :return: POST: redirect to departments page after adding
    """
    if request.method == 'POST':
        dep_id = request.form.get('department_id', '')
        requests.post('http://127.0.0.1:5000/api/department', data={'dep_id': dep_id})
        logger.debug('Information about new department was sent to server (add)')
        return redirect('/departments')
    logger.debug('Department page was displayed')
    return render_template('add_department.html')


@app.route('/del-department/<dep_id>')
def del_department(dep_id):
    """
    Sends delete request to server (api/department) that deletes department from database
    :param str dep_id: department`s id which is used to find department
    :return: redirect to departments page (/departments)
    """
    url = 'http://127.0.0.1:5000/api/department/' + dep_id
    requests.delete(url)
    logger.debug('Department`s id was sent to server (delete)')
    return redirect('/departments')


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    """
    GET method: sends get request to server (api/employees); receives list of employees from server
    and displays it
    POST method: sends post request to server (api/employees) with dates from form; receives list of
    employees that has been filtered with dates - employees who were born on a certain date or in
    the period between dates
    :return: HTML page ('employees.html') with employees list
    """
    if request.method == 'POST':
        date_from = request.form.get('date_from', '')
        date_by = request.form.get('date_by', '')
        logger.debug('Dates was received and sent to server')
        employees_list = requests.post('http://127.0.0.1:5000/api/employees',
                                       data={'date_from': date_from, 'date_by': date_by}).json()
        dates = [date_from, date_by]
    else:
        employees_list = requests.get('http://127.0.0.1:5000/api/employees').json()
        dates = None
    logger.debug('Employees page was displayed')
    return render_template('employees.html', employees_list=employees_list, dates=dates)


@app.route('/employee/<employee_id>', methods=['GET', 'POST'])
def employee(employee_id):
    """
    GET method: sends get request to server (/api/employee<employee_id>) and get request to server
    (/api/departments-ids) that returns list of departments` ids; receives information about
    employee and displays it in form for changing employee`s data; departments` ids put into HTML
    tag selection for choice
    POST method: gets information about employee from form and sends it into server that updates
    info in database
    :param str employee_id: employee`s id which is used to find employee
    :return: GET: HTML page with information about employees that can be changed
    :return: POST: redirect to employees page after updating
    """
    url = 'http://127.0.0.1:5000/api/employee/' + employee_id
    if request.method == 'POST':
        name = request.form.get('name', '')
        department_id = request.form.get('department_id', 'None')
        date_of_birthday = request.form.get('date_of_birthday', '')
        salary = request.form.get('salary', '')
        requests.put(url, data={'name': name, 'department_id': int(department_id),
                                'date_of_birthday': date_of_birthday, 'salary': salary})
        logger.debug('Employee`s data was sent to server (update)')
        return redirect('/employees')
    employee_data = requests.get(url).json()
    ids = requests.get('http://127.0.0.1:5000/api/departments-ids').json()['ids']
    logger.debug(employee_data)
    logger.debug('Employee page was displayed')
    return render_template('employee.html', employee_data=employee_data, ids=ids)


@app.route('/employee', methods=['GET', 'POST'])
def add_employee():
    """
    GET method: sends get request to server (/api/departments-ids) that returns list of departments`
    ids; displays form
    to write information about new employee; departments` ids put into HTML tag selection for choice
    POST method: gets information about new employee from form and sends it into server that adds
    new employee in database
    :return: GET: HTML page with form to write information about new employee
    :return: POST: redirect to employees page after adding new employee
    """
    if request.method == 'POST':
        name = request.form.get('name', '')
        department_id = request.form.get('department_id', 'None')
        date_of_birthday = request.form.get('date_of_birthday', '')
        salary = request.form.get('salary', '')
        requests.post('http://127.0.0.1:5000/api/employee',
                      data={'name': name, 'department_id': department_id,
                            'date_of_birthday': date_of_birthday, 'salary': salary})
        logger.debug('Employee`s data was sent to server (add)')
        return redirect('/employees')
    ids = requests.get('http://127.0.0.1:5000/api/departments-ids').json()['ids']
    logger.debug('Employee page was displayed')
    return render_template('add_employee.html', ids=ids)


@app.route('/del-employee/<employee_id>')
def del_employee(employee_id):
    """
    Sends delete request to server (api/employee/<employee_id> that deletes employee in database
    :param str employee_id: employee`s id which is used to find employee
    :return: redirect to employees page
    """
    url = 'http://127.0.0.1:5000/api/employee/' + employee_id
    requests.delete(url)
    logger.debug('Employee`s id was sent to server (delete)')
    return redirect('/employees')



