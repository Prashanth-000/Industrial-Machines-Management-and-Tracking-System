from flask import Flask, request, redirect, url_for, flash, session
import pymysql
from flask import make_response, render_template
from datetime import datetime


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
        mpass=request.form['mpass']

        if mpass !='9880':
            flash('Incorrect Master Key.Please try again', 'error')
            return redirect(url_for('signup'))  # Redirect for PRG pattern
        
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
    if 'logged_in' not in session:
        flash('Please log in to access the home page.', 'info')
        return redirect(url_for('login'))
    
    cursor = db.cursor()

    # Fetch total machines and machines under maintenance
    cursor.execute("SELECT COUNT(*) FROM machines")
    total_machines = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) 
        FROM maintenance_schedules 
        WHERE status = 'Scheduled'
    """)
    machines_under_maintenance = cursor.fetchone()[0]

    # Fetch total employees and active employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
    active_employees = cursor.fetchone()[0]

    # Fetch total work orders and their status breakdown
    cursor.execute("SELECT COUNT(*) FROM work_orders")
    work_orders_total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE status = 'Pending'")
    pending_work_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE status = 'Completed'")
    completed_work_orders = cursor.fetchone()[0]

    # Fetch maintenance breakdown for the chart
    cursor.execute("""
        SELECT maintenance_type, COUNT(*) 
        FROM maintenance_schedules 
        WHERE status = 'Scheduled' 
        GROUP BY maintenance_type
    """)
    maintenance_data = cursor.fetchall()
    maintenance_types = [row[0] for row in maintenance_data]
    maintenance_counts = [row[1] for row in maintenance_data]

    # Close the cursor
    cursor.close()

    # Render the home page with data
    return render_template(
        'home.html',
        total_machines=total_machines,
        machines_under_maintenance=machines_under_maintenance,
        total_employees=total_employees,
        active_employees=active_employees,
        work_orders_total=work_orders_total,
        pending_work_orders=pending_work_orders,
        completed_work_orders=completed_work_orders,
        maintenance_types=maintenance_types,
        maintenance_counts=maintenance_counts
    )

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
        status = request.form['status'] # Status is not allowed to be modified by users
        
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
        status = request.form['status']  # Keep the existing status, don't allow modification

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
    
    # Check if the employee has any pending work orders
    cursor.execute("""
    SELECT COUNT(*) 
    FROM work_orders 
    WHERE employee_id = %s AND status = 'Pending'
    """, (employee_id,))
    pending_work_orders = cursor.fetchone()[0]

    if pending_work_orders > 0:
        # If there are pending work orders, show a flash message and prevent deletion
        flash('Employee has pending work orders, cannot delete.', 'error')
        return redirect('/employees')

    # If no pending work orders, proceed with deletion
    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    db.commit()

    flash("Employee deleted successfully!", 'success')
    return redirect('/employees')

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

        try:
            # Insert work order into the database
            cursor.execute(
                """
                INSERT INTO work_orders 
                (machine_id, employee_id, work_order_date, due_date, task_description, status) 
                VALUES (%s, %s, %s, %s, %s, 'Pending')
                """,
                (machine_id, employee_id, work_order_date, due_date, task_description)
            )
            db.commit()

            # Update machine and employee status
            cursor.execute("UPDATE machines SET status = 'Not available' WHERE machine_id = %s", (machine_id,))
            # cursor.execute("UPDATE employees SET status = 'Inactive' WHERE employee_id = %s", (employee_id,))
            db.commit()

            flash('Work order added successfully!', 'success')  # Success message
            return redirect(url_for('workorders'))  # Redirect to workorders page after submission

        except pymysql.Error as e:
            # Rollback the transaction and flash the error
            db.rollback()
            error_message = str(e.args[1])  # Extract the error message
            flash(f'Error: {error_message}', 'error')  # Flash error message
            return redirect(url_for('add_workorder'))  # Redirect to avoid form resubmission

    # Fetch available machines and employees
    cursor.execute("SELECT machine_id, name FROM machines WHERE status = 'Available'")
    machines = cursor.fetchall()

    cursor.execute("""
    SELECT e.employee_id, e.name
    FROM employees e
    LEFT JOIN work_orders w ON e.employee_id = w.employee_id AND w.status = 'Pending'
    WHERE e.status = 'Active'
    GROUP BY e.employee_id
    HAVING COUNT(w.work_order_id) < 2
    """)
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

    # Fetch the machine name for the current work order
    cursor.execute("SELECT name FROM machines WHERE machine_id = %s", (work_order[1],))
    work_order_machine_name = cursor.fetchone()[0]

    if request.method == 'POST':
        work_order_date = request.form['work_order_date']
        due_date = request.form['due_date']
        task_description = request.form['task_description']
        status = request.form['status']
        machine_id = request.form['machine_id']
        employee_id = request.form['employee_id']

        try:
            cursor.execute(
                """
                UPDATE work_orders 
                SET work_order_date = %s, due_date = %s, task_description = %s, status = %s, employee_id = %s
                WHERE work_order_id = %s
                """,
                (work_order_date, due_date, task_description, status, employee_id, work_order_id)
            )
            db.commit()

            # Update machine and employee statuses if completed
            if status == 'Completed':
                cursor.execute("UPDATE machines SET status = 'Available' WHERE machine_id = %s", (machine_id,))
                db.commit()

            flash('Work order updated successfully!', 'success')
            return redirect('/workorders')

        except pymysql.Error as e:
            # Rollback the transaction and flash the error
            db.rollback()
            error_message = str(e.args[1])  # Extract the error message
            flash(f'Error: {error_message}', 'error')  # Flash error message
            return redirect(url_for('edit_workorder', work_order_id=work_order_id))  # Redirect to avoid form resubmission

    # Fetch available machines and employees
    cursor.execute("SELECT * FROM machines WHERE status = 'Available'")
    machines = cursor.fetchall()

    cursor.execute("""
    -- Fetch the current employee for the work order
    SELECT e.employee_id, e.name
    FROM employees e
    WHERE e.employee_id = (SELECT employee_id FROM work_orders WHERE work_order_id = %s)

    UNION

    -- Fetch employees with fewer than 2 pending work orders
    SELECT e.employee_id, e.name
    FROM employees e
    LEFT JOIN work_orders w ON e.employee_id = w.employee_id AND w.status = 'Pending'
    WHERE e.status = 'Active'
    GROUP BY e.employee_id
    HAVING COUNT(w.work_order_id) < 2
""", (work_order_id,))
    employees = cursor.fetchall()


    return render_template('edit_workorder.html', 
                           work_order=work_order, 
                           work_order_machine_name=work_order_machine_name, 
                           machines=machines, 
                           employees=employees)

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
        
        # if status == 'Completed':
        #     # Reset the machine and employee status back to available and active respectively
        #     cursor.execute("UPDATE machines SET status = 'Available' WHERE machine_id = %s", (machine_id,))
        #     cursor.execute("UPDATE employees SET status = 'Active' WHERE employee_id = %s", (employee_id,))
        
        # Delete the work order
        cursor.execute("DELETE FROM work_orders WHERE work_order_id = %s", (work_order_id,))
        db.commit()

        flash("Work order deleted successfully!", 'success')
    else:
        flash("Work order not found.", 'error')

    return redirect('/workorders')
# Viewing maintenance schedules
@app.route('/maintenance', methods=['GET'])
def maintenance():
    if 'logged_in' not in session:
        flash('Please log in to view maintenance schedules.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("""
        SELECT ms.schedule_id, m.name AS machine_name, ms.scheduled_date, ms.maintenance_type,
               ms.cost, ms.status
        FROM maintenance_schedules ms
        JOIN machines m ON ms.machine_id = m.machine_id
        ORDER BY ms.status ASC, ms.scheduled_date
    """)
    maintenances = cursor.fetchall()

    return render_template('maintenance.html', maintenances=maintenances)

# Adding new maintenance schedule
@app.route('/add_maintenance', methods=['GET', 'POST'])
def add_maintenance():
    if 'logged_in' not in session:
        flash('Please log in to add maintenance schedules.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()

    if request.method == 'GET':
        # Fetch machine list for the dropdown
        cursor.execute("""
    SELECT m.machine_id, m.name
    FROM machines m
    WHERE m.status = 'Available'
    AND m.machine_id NOT IN (
        SELECT ms.machine_id
        FROM maintenance_schedules ms
        WHERE ms.status = 'Scheduled'
        GROUP BY ms.machine_id
        HAVING COUNT(ms.schedule_id) > 1
    )
    """)
        machines = cursor.fetchall()

        return render_template('add_maintenance.html', machines=machines)

    if request.method == 'POST':
        machine_id = request.form['machine_id']
        scheduled_date = request.form['scheduled_date']
        maintenance_type = request.form['maintenance_type']
        expenses = zip(request.form.getlist('expense_name[]'), request.form.getlist('expense_cost[]'),
                       request.form.getlist('expense_notes[]'))

        # Insert maintenance schedule
        cursor.execute("""
            INSERT INTO maintenance_schedules (machine_id, scheduled_date, maintenance_type, cost, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (machine_id, scheduled_date, maintenance_type, 0, 'Scheduled'))
        schedule_id = cursor.lastrowid

        # Insert expenses into the temporary table
        for expense_name, expense_cost, expense_notes in expenses:
            cursor.execute("""
                INSERT INTO expenses (maintenance_schedule_id, expense_name, cost, notes)
                VALUES (%s, %s, %s, %s)
            """, (schedule_id, expense_name, expense_cost, expense_notes))

        # Update the cost in the maintenance_schedules table
        cursor.execute("""
            UPDATE maintenance_schedules
            SET cost = (SELECT SUM(cost) FROM expenses WHERE maintenance_schedule_id = %s)
            WHERE schedule_id = %s
        """, (schedule_id, schedule_id))

        db.commit()
        flash('Maintenance schedule added successfully!', 'success')
        return redirect(url_for('maintenance'))
    
    #editing maintanace schedules
@app.route('/edit_maintenance/<int:maintenance_id>', methods=['GET', 'POST'])
def edit_maintenance(maintenance_id):
    if 'logged_in' not in session:
        flash('Please log in to edit maintenance schedules.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()

    cursor.execute("""
        SELECT schedule_id, m.name AS machine_name, ms.scheduled_date, ms.maintenance_type,
               ms.cost, ms.status
        FROM maintenance_schedules ms
        JOIN machines m ON ms.machine_id = m.machine_id
    """)
    maintenance = cursor.fetchall()

    if request.method == 'GET':
        # Fetch machine list for the dropdown
        # Fetch machine list for the dropdown, including the currently assigned machine
        cursor.execute("""
    SELECT m.machine_id, m.name
    FROM machines m
    WHERE m.status = 'Available'
    AND m.machine_id NOT IN (
        SELECT ms.machine_id
        FROM maintenance_schedules ms
        WHERE ms.status = 'Scheduled'
        GROUP BY ms.machine_id
        HAVING COUNT(ms.schedule_id) > 1
    )
""")
        machines = cursor.fetchall()



        # Fetch the selected maintenance schedule
        cursor.execute("SELECT * FROM maintenance_schedules WHERE schedule_id = %s", (maintenance_id,))
        maintenance = cursor.fetchone()

        # Fetch expenses associated with the maintenance schedule
        cursor.execute("SELECT temp_expense_id, expense_name, cost, notes FROM expenses WHERE maintenance_schedule_id = %s", (maintenance_id,))
        expenses = cursor.fetchall()

        return render_template('edit_maintenance.html', machines=machines, maintenance=maintenance, expenses=expenses)

    if request.method == 'POST':
        machine_id = request.form['machine_id']
        scheduled_date = request.form['scheduled_date']
        maintenance_type = request.form['maintenance_type']

        # "Status" remains frozen at "Scheduled"
        status = 'Scheduled'

        # Update the maintenance schedule
        cursor.execute("""
            UPDATE maintenance_schedules
            SET machine_id = %s, scheduled_date = %s, maintenance_type = %s, status = %s
            WHERE schedule_id = %s
        """, (machine_id, scheduled_date, maintenance_type, status, maintenance_id))

        # Handle deletions for marked expenses
        delete_expense_ids = request.form.getlist('delete_expense[]')
        if delete_expense_ids:
            cursor.execute("""
                DELETE FROM expenses
                WHERE temp_expense_id IN (%s)
            """ % ','.join(['%s'] * len(delete_expense_ids)), tuple(delete_expense_ids))

        # Get the updated data for the expenses
        expense_ids = request.form.getlist('expense_id[]')
        expense_names = request.form.getlist('expense_name[]')
        expense_costs = request.form.getlist('expense_cost[]')
        expense_notes = request.form.getlist('expense_notes[]')

        # Update the existing expenses
        for i in range(len(expense_ids)):
            cursor.execute("""
                UPDATE expenses
                SET expense_name = %s, cost = %s, notes = %s
                WHERE temp_expense_id = %s
            """, (expense_names[i], expense_costs[i], expense_notes[i], expense_ids[i]))

        # Add any new expenses that were submitted
        new_expense_names = request.form.getlist('new_expense_name[]')
        new_expense_costs = request.form.getlist('new_expense_cost[]')
        new_expense_notes = request.form.getlist('new_expense_notes[]')

        for i in range(len(new_expense_names)):
            if new_expense_names[i].strip() and new_expense_costs[i]:  # Ignore empty rows
                cursor.execute("""
                    INSERT INTO expenses (maintenance_schedule_id, expense_name, cost, notes)
                    VALUES (%s, %s, %s, %s)
                """, (maintenance_id, new_expense_names[i], new_expense_costs[i], new_expense_notes[i]))

        # Recalculate the total cost for the maintenance schedule
        cursor.execute("""
            UPDATE maintenance_schedules
            SET cost = (SELECT SUM(cost) FROM expenses WHERE maintenance_schedule_id = %s)
            WHERE schedule_id = %s
        """, (maintenance_id, maintenance_id))

        db.commit()
        flash('Maintenance schedule updated successfully!', 'success')
        return redirect(url_for('maintenance'))

# Deleting maintenance schedule
@app.route('/delete_maintenance/<int:schedule_id>', methods=['GET'])
def delete_maintenance(schedule_id):
    if 'logged_in' not in session:
        flash('Please log in to delete a maintenance schedule.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM maintenance_schedules WHERE schedule_id = %s", (schedule_id,))
    db.commit()

    flash('Maintenance schedule deleted successfully!', 'success')
    return redirect('/maintenance')

#marking maintenance schedule as completed
@app.route('/mark_done/<int:schedule_id>', methods=['POST'])
def mark_done(schedule_id):
    if 'logged_in' not in session:
        flash('Please log in to mark the maintenance as done.', 'error')
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    cursor.execute("""
        UPDATE maintenance_schedules
        SET status = 'Completed'
        WHERE schedule_id = %s;
    """, (schedule_id,))
    db.commit()
    
    flash('Maintenance marked as done successfully!', 'success')
    return redirect(url_for('maintenance'))  # Redirect back to the maintenance page


#View maintenance report
@app.route('/report/<int:schedule_id>', methods=['GET'])
def show_report(schedule_id):
    # Check if user is logged in
    if 'logged_in' not in session:
        flash('Please log in to view the report.', 'error')
        return redirect(url_for('login'))

    # Fetch the maintenance data from the database
    cursor = db.cursor()
    cursor.execute("""
        SELECT ms.schedule_id, m.name AS machine_name, ms.scheduled_date, ms.maintenance_type, ms.cost, ms.status
        FROM maintenance_schedules ms
        JOIN machines m ON ms.machine_id = m.machine_id
        WHERE ms.schedule_id = %s;
    """, (schedule_id,))
    maintenances = cursor.fetchall()
    
    # Current date for the report
    current_date = datetime.now().strftime("%B %d, %Y")

    # Render the report HTML page
    return render_template('report.html', current_date=current_date, maintenances=maintenances, schedule_id=schedule_id)

# #download report
# @app.route('/download_report/<int:schedule_id>', methods=['GET'])
# def download_report(schedule_id):
#     # Check if user is logged in
#     if 'logged_in' not in session:
#         flash('Please log in to download the report.', 'error')
#         return redirect(url_for('login'))

#     # Fetch the maintenance data from the database
#     cursor = db.cursor()
#     cursor.execute("""
#         SELECT ms.schedule_id, m.name AS machine_name, ms.scheduled_date, ms.maintenance_type, ms.cost, ms.status
#         FROM maintenance_schedules ms
#         JOIN machines m ON ms.machine_id = m.machine_id
#         WHERE ms.schedule_id = %s;
#     """, (schedule_id,))
#     maintenances = cursor.fetchall()
    
#     # Current date for the report
#     current_date = datetime.now().strftime("%B %d, %Y")

#     # Render the report HTML (this will render the same template you used for the report)
#     html_content = render_template('report.html', current_date=current_date, maintenances=maintenances, schedule_id=schedule_id)

#     # Set the path to wkhtmltopdf executable
#     path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Adjust path if needed

#     # Configure pdfkit to use this path
#     config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

#     # Generate the PDF from the HTML string using pdfkit
#     pdf = pdfkit.from_string(html_content, False, configuration=config)

#     # Prepare the response with the PDF file
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename=maintenance_report_{schedule_id}.pdf'

#     return response


if __name__ == '__main__':
    app.run(debug=True)
