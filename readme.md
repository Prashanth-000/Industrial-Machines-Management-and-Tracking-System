pip install weasyprint
pip install pdfkit
Go to the wkhtmltopdf downloads page.
Download the Windows installer (choose the latest stable version).
Install the downloaded .exe file.
then change path as below---line 645(inside download_report route) for
path_to_wkhtmltopdf = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

Now Run app.py

 <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class="flashes">
                {% for category, message in messages %}
                    <li class="alert alert-{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
        {% endwith %}

    
 <script>
        // Automatically hide flash messages after 3 seconds
        window.onload = function() {
            setTimeout(function() {
                const flashMessages = document.querySelectorAll('.flashes li');
                flashMessages.forEach(message => {
                    message.style.transition = "opacity 0.5s ease-out";
                    message.style.opacity = 0;
                    setTimeout(() => message.remove(), 500);
                });
            }, 3000);
        };
    </script>

        .flashes {
            list-style-type: none;
            padding: 0;
            margin-bottom: 20px;
        }
        .flashes li {
            
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .alert-success {
            background-color: #76f0a9;
            color: white;
            color: rgb(0, 0, 0);
        }
        .alert-error {
            background-color: #e74c3c;
            color: white;
        }
        .alert-info {
            background-color: #189599; /* Light blue for logout message */
            color: white;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }


edit work order
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Work Order</title>
    <style>
        /* Reset defaults */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Body styling */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #bfd8df, #99adcc); /* Light gradient background */
            margin: 0;
            padding: 0;
        }

        /* Navbar styling */
        .navbar {
            background-color: #004080; /* Deep blue */
            display: flex;
            align-items: center;
            padding: 10px 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for elevation */
        }

        .navbar a {
            color: #fff;
            padding: 12px 20px;
            text-decoration: none;
            font-size: 1rem;
            font-weight: bold;
            margin-right: 15px;
            border-radius: 5px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .navbar a:hover {
            background-color: #ffd700; /* Gold for hover */
            color: #004080;
        }

        .navbar a.active {
            background-color: #ffd700; /* Gold for active link */
            color: #004080;
            font-weight: bold;
        }

        /* Container for form */
        .container {
            width: 600px; /* Decrease width of the form container */
            margin: 80px auto 20px; /* Space for the navbar and center alignment */
            padding: 20px;
            background: rgba(255, 255, 255, 0.9); /* Semi-transparent background */
            border-radius: 15px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 2.2rem; /* Slightly smaller heading */
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 1rem;
            margin-bottom: 8px;
            color: #333;
        }

        input, select, textarea, button {
            padding: 10px; /* Smaller padding for inputs */
            margin-bottom: 12px; /* Reduced space between inputs */
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 1rem;
        }

        input:focus, select:focus, textarea:focus {
            border-color: #3498db;
            outline: none;
        }

        button {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
            padding: 10px;
        }

        button:hover {
            background-color: #2980b9;
        }

        /* Flash message styling */
        .flashes {
            list-style-type: none;
            padding: 0;
            margin-bottom: 20px;
        }

        .flashes li {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }

        .alert-success {
            background-color: #2ecc71;
            color: white;
        }

        .alert-error {
            background-color: #e74c3c;
            color: white;
        }

        .alert-info {
            background-color: #3498db;
            color: white;
        }
        /* Flash message styling */
        .flashes {
            list-style-type: none;
            padding: 0;
            margin-bottom: 20px;
        }

        .flashes li {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            animation: fade-in 0.5s ease-in-out;
        }

        .alert-success {
            background-color: #2ecc71;
            color: white;
        }

        .alert-error {
            background-color: #e74c3c;
            color: white;
        }

        .alert-info {
            background-color: #3498db;
            color: white;
        }

        @keyframes fade-in {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    </style>
     <script>
        // Automatically hide flash messages after 3 seconds
        window.onload = function() {
            setTimeout(function() {
                const flashMessages = document.querySelectorAll('.flashes li');
                flashMessages.forEach(message => {
                    message.style.transition = "opacity 0.5s ease-out";
                    message.style.opacity = 0;
                    setTimeout(() => message.remove(), 500);
                });
            }, 3000);
        };
    </script>

</head>
<body>

    <!-- Navbar -->
    <div class="navbar">
        <a href="/" >Home</a>
        <a href="/machines">Machines</a>
        <a href="/employees">Employees</a>
        <a href="/workorders" class="active">Work Orders</a>
    </div>

    <!-- Edit Work Order Form -->
    <div class="container">
        <h1>Edit Work Order</h1>

        <!-- Flash messages for success or error -->
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
    <ul class="flashes">
        {% for category, message in messages %}
            <li class="alert alert-{{ category }}">{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
{% endwith %}

   
        <!-- Form to edit work order -->
        <form action="/edit_workorder/{{ work_order[0] }}" method="POST">
            <label for="machine_id">Machine:</label>
            <input type="text" name="machine_id" id="machine_id" value="{{ work_order_machine_name }}" disabled>
            <input  name="machine_id" value="{{ work_order[1] }}">

            <label for="employee_id">Employee:</label>
            <input type="text" name="employee_id" id="employee_id" value="{{ work_order_employee_name }}" disabled>
            <input type="hidden" name="employee_id" value="{{ work_order[2] }}">

            <label for="work_order_date">Work Order Date:</label>
            <input type="date" name="work_order_date" id="work_order_date" value="{{ work_order[3] }}" required {% if work_order[6] == 'Completed' %}disabled{% endif %}>

            <label for="due_date">Due Date:</label>
            <input type="date" name="due_date" id="due_date" value="{{ work_order[4] }}" {% if work_order[6] == 'Completed' %}disabled{% endif %}>

            <label for="task_description">Task Description:</label>
            <textarea name="task_description" id="task_description" {% if work_order[6] == 'Completed' %}disabled{% endif %}>{{ work_order[5] }}</textarea>

            <label for="status">Status:</label>
            <select name="status" id="status" {% if work_order[6] == 'Completed' %}disabled{% endif %}>
                <option value="Pending" {% if work_order[6] == 'Pending' %}selected{% endif %}>Pending</option>
                <option value="Completed" {% if work_order[6] == 'Completed' %}selected{% endif %}>Completed</option>
            </select>

            <button type="submit" {% if work_order[6] == 'Completed' %}disabled{% endif %}>Save</button>
        </form>
    </div>

</body>
</html>


route

@app.route('/edit_workorder/<int:work_order_id>', methods=['GET', 'POST'])
def edit_workorder(work_order_id):
    if 'logged_in' not in session:
        flash('Please log in to edit a work order.', 'error')
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM work_orders WHERE work_order_id = %s", (work_order_id,))
    work_order = cursor.fetchone()

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
                SET work_order_date = %s, due_date = %s, task_description = %s, status = %s 
                WHERE work_order_id = %s
                """,
                (work_order_date, due_date, task_description, status, work_order_id)
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
    SELECT e.employee_id, e.name
    FROM employees e
    LEFT JOIN work_orders w ON e.employee_id = w.employee_id AND w.status = 'Pending'
    WHERE e.status = 'Active'
    GROUP BY e.employee_id
    HAVING COUNT(w.work_order_id) <= 3
    """)
    employees = cursor.fetchall()


    return render_template('edit_workorder.html', work_order=work_order, machines=machines, employees=employees)
