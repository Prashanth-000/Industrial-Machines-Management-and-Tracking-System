CREATE DATABASE IF NOT EXISTS dbms_database;
USE dbms_database;

-- Machines Table
CREATE TABLE machines (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('Electric', 'Diesel', 'Manual') NOT NULL,
    installation_date DATE NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    model_number VARCHAR(255),
    warranty_period INT NOT NULL,
    status ENUM('Available', 'Not available') NOT NULL
);

-- Employees Table
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(255),
    address TEXT,
    date_of_hire DATE,
    status ENUM('Active', 'Inactive') NOT NULL
);

-- Maintenance Schedules Table
CREATE TABLE maintenance_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    scheduled_date DATE NOT NULL,
    maintenance_type VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2),
    status ENUM('Scheduled', 'Completed') NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);


CREATE TABLE expenses (
    temp_expense_id INT AUTO_INCREMENT PRIMARY KEY,
    maintenance_schedule_id INT NOT NULL,
    expense_name VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2),
    notes TEXT,
    FOREIGN KEY (maintenance_schedule_id) REFERENCES maintenance_schedules(schedule_id) ON DELETE CASCADE
);

-- Work Orders Table
CREATE TABLE work_orders (
    work_order_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    employee_id INT NOT NULL,
    work_order_date DATE NOT NULL,
    due_date DATE,
    task_description TEXT,
    status ENUM('Pending', 'Completed') NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);


-- Admins Table
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

--Trigger for work order dates
DELIMITER //
CREATE TRIGGER validate_workorder_dates
BEFORE INSERT ON work_orders
FOR EACH ROW
BEGIN
    IF NEW.work_order_date > NEW.due_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Work order date cannot be later than the due date.';
    END IF;
END;//
CREATE TRIGGER validate_workorder_dates_update
BEFORE UPDATE ON work_orders
FOR EACH ROW
BEGIN
    IF NEW.work_order_date > NEW.due_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Work order date cannot be later than the due date.';
    END IF;
END;
//
DELIMITER;

