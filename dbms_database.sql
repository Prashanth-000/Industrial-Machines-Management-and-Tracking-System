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

-- Insert into Machines Table
INSERT INTO machines (name, type, installation_date, manufacturer, model_number, warranty_period, status)
VALUES 
    ('CNC Lathe Machine', 'Electric', '2020-05-15', 'Haas Automation', 'HAAS2020', 36, 'Available'),
    ('Milling Machine', 'Diesel', '2019-11-12', 'Makino', 'MAKINO2019', 48, 'Not available'),
    ('Drilling Machine', 'Manual', '2018-07-10', 'Bosch', 'BOSCH2018', 24, 'Available'),
    ('Grinding Machine', 'Electric', '2021-03-22', 'Siemens', 'SIEM2021', 60, 'Available'),
    ('3D Printer', 'Electric', '2023-01-18', 'Creality', 'CR2023', 12, 'Not available');

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

-- Insert into Employees Table
INSERT INTO employees (name, phone_number, email, address, date_of_hire, status)
VALUES 
    ('John Doe', '9876543210', 'john.doe@example.com', '123 Industrial Area, NY', '2020-06-01', 'Active'),
    ('Jane Smith', '8765432109', 'jane.smith@example.com', '456 Tech Park, CA', '2019-12-15', 'Inactive'),
    ('Mike Johnson', '7654321098', 'mike.johnson@example.com', '789 Factory Lane, TX', '2021-04-20', 'Active'),
    ('Emily Davis', '6543210987', 'emily.davis@example.com', '101 Machinery St, FL', '2022-09-10', 'Active'),
    ('Robert Brown', '5432109876', 'robert.brown@example.com', '202 Maintenance Dr, WA', '2023-03-25', 'Inactive');

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

-- Insert into Maintenance Schedules Table
INSERT INTO maintenance_schedules (machine_id, employee_id, scheduled_date, maintenance_type, cost, status)
VALUES 
    (1, '2024-01-10', 'Oil Change', 150.00, 'Scheduled'),
    (2, '2024-02-05', 'Brake Inspection', 200.00, 'Scheduled'),
    (3, '2024-03-15', 'General Maintenance', 100.00, 'Scheduled'),
    (4,  '2024-04-10', 'Belt Replacement', 250.00, 'Completed'),
    (5,  '2024-05-01', 'Filter Cleaning', 80.00, 'Completed');


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

-- Insert into Work Orders Table
INSERT INTO work_orders (machine_id, employee_id, work_order_date, due_date, task_description, status)
VALUES 
    (1, 1, '2024-01-05', '2024-01-15', 'Replace coolant and check lubrication system.', 'Pending'),
    (2, 2, '2024-02-01', '2024-02-10', 'Inspect and replace brake assembly.', 'Pending'),
    (3, 3, '2024-03-10', '2024-03-20', 'Clean and realign drill head.', 'Completed'),
    (4, 4, '2024-04-01', '2024-04-08', 'Replace worn-out grinding wheel.', 'Completed'),
    (5, 5, '2024-05-01', '2024-05-05', 'Service filters and replace gaskets.', 'Pending');


-- Admins Table
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Insert into Admins Table
INSERT INTO admins (username, password, email)
VALUES 
    ('admin1', 'password123', 'admin1@example.com'),
    ('admin2', 'securepass456', 'admin2@example.com');


DELIMITER $$

CREATE TRIGGER after_work_order_insert
AFTER INSERT ON work_orders
FOR EACH ROW
BEGIN
    -- Set the machine state to 'Not available'
    UPDATE machines 
    SET status = 'Not available'
    WHERE machine_id = NEW.machine_id;

    -- Set the employee state to 'Inactive'
    UPDATE employees 
    SET status = 'Inactive'
    WHERE employee_id = NEW.employee_id;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER after_work_order_update
AFTER UPDATE ON work_orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'Completed' THEN
        -- Set the machine state back to 'Available'
        UPDATE machines 
        SET status = 'Available'
        WHERE machine_id = NEW.machine_id;

        -- Set the employee state back to 'Active'
        UPDATE employees 
        SET status = 'Active'
        WHERE employee_id = NEW.employee_id;
    END IF;
END$$

DELIMITER ;
