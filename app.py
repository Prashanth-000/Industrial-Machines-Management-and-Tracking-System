from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# MySQL Database connection settings
db = pymysql.connect(host='localhost', user='root', password='', database='dbms_database')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
            admin = cursor.fetchone()

            if admin:
                session['logged_in'] = True
                session['username'] = username
                #flash('Login successful!', 'success')
                return redirect(url_for('home'))  # Redirect to avoid form resubmission
            else:
                flash('Invalid username or password!', 'error')
                return redirect(url_for('login'))  # Redirect to avoid form resubmission
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('login'))  # Redirect to avoid form resubmission

    return render_template('login.html')


# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        try:
            cursor = db.cursor()
            # Check if username already exists
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('signup'))  # Redirect for PRG pattern
            
            # Hash the password before storing it
            hashed_password = password
            
            # Insert the new admin record
            cursor.execute(
                "INSERT INTO admins (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            db.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        
        except Exception as e:
            db.rollback()  # Rollback any changes in case of an error
            flash(f"An error occurred: {str(e)}", 'error')
        finally:
            cursor.close()  # Ensure the cursor is closed properly
    
    return render_template('signup.html')

# Home Route
@app.route('/')
def home():
    if 'logged_in' in session:
       # flash('Welcome to the homepage!', 'success')  # Flash message for logged-in users
        return render_template('home.html')
    else:
        flash('Please log in to access the home page.', 'info')  # Flash message for non-logged-in users
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Machines Route
@app.route('/machines', methods=['GET'])
def machines():
    if 'logged_in' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    # If logged in, fetch and display machines
    cursor = db.cursor()
    cursor.execute("SELECT * FROM machines")  # Get all machines from the database
    machines = cursor.fetchall()  # Fetch all the records
    
    return render_template('machines.html', machines=machines)
#adding new machine 
@app.route('/add_machine', methods=['GET', 'POST'])
def add_machine():
    if 'logged_in' not in session:
        flash('Please log in to add a machine.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':  # Handling the form submission
        name = request.form['name']
        type_ = request.form['type']
        installation_date = request.form['installation_date']
        manufacturer = request.form['manufacturer']
        model_number = request.form['model_number']
        warranty_period = request.form['warranty_period']
        
        # Status is always set to 'Available' for new machines
        status = 'Available'

        cursor = db.cursor()
        cursor.execute("INSERT INTO machines (name, type, installation_date, manufacturer, model_number, warranty_period, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        (name, type_, installation_date, manufacturer, model_number, warranty_period, status))  # Insert new machine
        db.commit()  # Commit the transaction
        
        flash("Machine added successfully!", 'success')  # Show success message
        return redirect('/machines')  # Redirect back to the machines page

    # If it's a GET request, display the form to add a new machine
    return render_template('add_machine.html')

# Edit machine (Only for logged in users)
@app.route('/edit_machine/<int:machine_id>', methods=['GET', 'POST'])
def edit_machine(machine_id):
    if 'logged_in' not in session:
        flash('Please log in to edit a machine.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':  # Handle form submission for editing machine
        name = request.form['name']
        type_ = request.form['type']
        installation_date = request.form['installation_date']
        manufacturer = request.form['manufacturer']
        model_number = request.form['model_number']
        warranty_period = request.form['warranty_period']
        # Keep the status as 'Available' to prevent user modification
        status = "Available"  # Status is not allowed to be modified by users
        
        cursor = db.cursor()
        cursor.execute("UPDATE machines SET name = %s, type = %s, installation_date = %s, manufacturer = %s, model_number = %s, warranty_period = %s, status = %s WHERE machine_id = %s", 
                        (name, type_, installation_date, manufacturer, model_number, warranty_period, status, machine_id))  # Update machine data
        db.commit()  # Commit the transaction
        
        flash("Machine updated successfully!", 'success')  # Show success message
        return redirect('/machines')  # Redirect back to the machines page
    
    # If GET method, pre-fill form with current machine data
    cursor = db.cursor()
    cursor.execute("SELECT * FROM machines WHERE machine_id = %s", (machine_id,))  # Get the machine data by ID
    machine = cursor.fetchone()  # Fetch the data for the specific machine

    return render_template('edit_machine.html', machine=machine)  # Render the edit machine form with data

# Delete machine (Only for logged in users)
@app.route('/delete_machine/<int:machine_id>', methods=['GET'])
def delete_machine(machine_id):
    if 'logged_in' not in session:
        flash('Please log in to delete a machine.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT status FROM machines WHERE machine_id = %s", (machine_id,))
    machine = cursor.fetchone()

    if machine is None:
        flash('Machine not found.', 'error')
        return redirect('/machines')

    # Only delete the machine if it is available
    if machine[0] == 'Available':
        cursor.execute("DELETE FROM machines WHERE machine_id = %s", (machine_id,))
        db.commit()  # Commit the transaction
        flash("Machine deleted successfully!", 'success')
    else:
        flash("Cannot delete machine. It is not available.", 'error')

    return redirect('/machines')


# Route to display all employees
@app.route('/employees', methods=['GET'])
def employees():
    if 'logged_in' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees")  # Ensure this query is correct
    employees = cursor.fetchall()

    print("Fetched employees:", employees)  # Add a debug statement

    if not employees:
        flash('No employees found in the database.', 'warning')  # If no employees found

    return render_template('employees.html', employees=employees)



# Adding new employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'logged_in' not in session:
        flash('Please log in to add an employee.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':  # Handle form submission
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        date_of_hire = request.form['date_of_hire']
        status = "Active"  # Default status is always Active

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO employees (name, phone_number, email, address, date_of_hire, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, phone_number, email, address, date_of_hire, status))

        db.commit()  # Commit the transaction
        flash('Employee added successfully!', 'success')
        return redirect('/employees')  # Redirect to the employee list page

    return render_template('add_employee.html')  # Render the Add Employee form

# Edit employee (Only for logged in users)
@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if 'logged_in' not in session:
        flash('Please log in to edit an employee.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()  # Fetch the employee data

    if not employee:
        flash('Employee not found.', 'error')
        return redirect('/employees')

    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        date_of_hire = request.form['date_of_hire']
        status = employee[6]  # Keep the existing status, don't allow modification

        cursor.execute("""
            UPDATE employees
            SET name = %s, phone_number = %s, email = %s, address = %s, date_of_hire = %s, status = %s
            WHERE employee_id = %s
        """, (name, phone_number, email, address, date_of_hire, status, employee_id))

        db.commit()  # Commit changes
        flash('Employee details updated successfully!', 'success')
        return redirect('/employees')  # Redirect to employee list page

    return render_template('edit_employee.html', employee=employee)  # Render the edit form

# Delete employee (Only for logged in users)
@app.route('/delete_employee/<int:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    if 'logged_in' not in session:
        flash('Please log in to delete an employee.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))  # Delete the employee by ID
    db.commit()  # Commit the transaction

    flash("Employee deleted successfully!", 'success')  # Show success message
    return redirect('/employees')  # Redirect back to the employees page


# Work Orders Route
@app.route('/workorders', methods=['GET'])
def workorders():
    if 'logged_in' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Fetch all work orders with machine and employee details
    cursor = db.cursor()
    cursor.execute("""
        SELECT wo.work_order_id, wo.work_order_date, wo.due_date, wo.task_description, 
               wo.status, m.name AS machine_name, e.name AS employee_name
        FROM work_orders wo
        JOIN machines m ON wo.machine_id = m.machine_id
        JOIN employees e ON wo.employee_id = e.employee_id
    """)
    work_orders = cursor.fetchall()
    
    return render_template('workorders.html', work_orders=work_orders)
@app.route('/add_workorder', methods=['GET', 'POST'])
def add_workorder():
    if 'logged_in' not in session:
        flash('Please log in to add a work order.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()

    if request.method == 'POST':
        # Get form data
        machine_id = request.form['machine_id']
        employee_id = request.form['employee_id']
        work_order_date = request.form['work_order_date']
        due_date = request.form['due_date']
        task_description = request.form['task_description']

        # Insert work order into the database
        cursor.execute("INSERT INTO work_orders (machine_id, employee_id, work_order_date, due_date, task_description, status) VALUES (%s, %s, %s, %s, %s, 'Pending')",
                       (machine_id, employee_id, work_order_date, due_date, task_description))
        db.commit()

        # Update machine status to 'Not Available' and employee status to 'Inactive'
        cursor.execute("UPDATE machines SET status = 'Not available' WHERE machine_id = %s", (machine_id,))
        cursor.execute("UPDATE employees SET status = 'Inactive' WHERE employee_id = %s", (employee_id,))
        db.commit()

        flash('Work order added successfully!', 'success')
        return redirect('/workorders')

    # Fetch available machines (status = 'Available') and active employees (status = 'Active')
    cursor.execute("SELECT machine_id, name FROM machines WHERE status = 'Available'")
    machines = cursor.fetchall()

    cursor.execute("SELECT employee_id, name FROM employees WHERE status = 'Active'")
    employees = cursor.fetchall()

    return render_template('add_workorder.html', machines=machines, employees=employees)

@app.route('/edit_workorder/<int:work_order_id>', methods=['GET', 'POST'])
def edit_workorder(work_order_id):
    if 'logged_in' not in session:
        flash('Please log in to edit a work order.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM work_orders WHERE work_order_id = %s", (work_order_id,))
    work_order = cursor.fetchone()

    # If the status is "Completed", prevent editing
    if work_order[6] == 'Completed' and request.method == 'POST':
        flash('This work order has already been completed and cannot be edited.', 'error')
        return redirect(url_for('workorders'))

    if request.method == 'POST':  # Handle the form submission for editing the work order
        work_order_date = request.form['work_order_date']
        due_date = request.form['due_date']
        task_description = request.form['task_description']
        status = request.form['status']
        machine_id = request.form['machine_id']
        employee_id = request.form['employee_id']

        cursor.execute("""
            UPDATE work_orders 
            SET work_order_date = %s, due_date = %s, task_description = %s, status = %s 
            WHERE work_order_id = %s
        """, (work_order_date, due_date, task_description, status, work_order_id))
        
        db.commit()

        # Update machine and employee status if the work order is completed
        if status == 'Completed':
            cursor.execute("UPDATE machines SET status = 'Available' WHERE machine_id = %s", (machine_id,))
            cursor.execute("UPDATE employees SET status = 'Active' WHERE employee_id = %s", (employee_id,))
            db.commit()

        flash("Work order updated successfully!", 'success')
        return redirect('/workorders')

    cursor.execute("SELECT * FROM machines WHERE status = 'Available'")
    machines = cursor.fetchall()

    cursor.execute("SELECT * FROM employees WHERE status = 'Active'")
    employees = cursor.fetchall()

    return render_template('edit_workorder.html', work_order=work_order, machines=machines, employees=employees)

@app.route('/delete_workorder/<int:work_order_id>', methods=['GET'])
def delete_workorder(work_order_id):
    if 'logged_in' not in session:
        flash('Please log in to delete a work order.', 'error')
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    
    # Fetch work order details before deletion to get the machine_id and employee_id
    cursor.execute("SELECT machine_id, employee_id, status FROM work_orders WHERE work_order_id = %s", (work_order_id,))
    work_order = cursor.fetchone()
    
    if work_order:
        machine_id = work_order[0]
        employee_id = work_order[1]
        status = work_order[2]
        
        if status == 'Completed':
            # Reset the machine and employee status back to available and active respectively
            cursor.execute("UPDATE machines SET status = 'Available' WHERE machine_id = %s", (machine_id,))
            cursor.execute("UPDATE employees SET status = 'Active' WHERE employee_id = %s", (employee_id,))
        
        # Delete the work order
        cursor.execute("DELETE FROM work_orders WHERE work_order_id = %s", (work_order_id,))
        db.commit()

        flash("Work order deleted successfully!", 'success')
    else:
        flash("Work order not found.", 'error')

    return redirect('/workorders')


if __name__ == '__main__':
    app.run(debug=True)
