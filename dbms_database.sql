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
    employee_id INT NOT NULL,
    scheduled_date DATE NOT NULL,
    maintenance_type VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2),
    status ENUM('Scheduled', 'Completed') NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- Insert into Maintenance Schedules Table
INSERT INTO maintenance_schedules (machine_id, employee_id, scheduled_date, maintenance_type, cost, status)
VALUES 
    (1, 1, '2024-01-10', 'Oil Change', 150.00, 'Scheduled'),
    (2, 2, '2024-02-05', 'Brake Inspection', 200.00, 'Scheduled'),
    (3, 3, '2024-03-15', 'General Maintenance', 100.00, 'Scheduled'),
    (4, 4, '2024-04-10', 'Belt Replacement', 250.00, 'Completed'),
    (5, 5, '2024-05-01', 'Filter Cleaning', 80.00, 'Completed');

-- Machine Parts Repair Table
CREATE TABLE machine_parts_repair (
    repair_id INT AUTO_INCREMENT PRIMARY KEY,
    maintenance_schedule_id INT NOT NULL,
    part_name VARCHAR(255) NOT NULL,
    repair_date DATE,
    vendor_name VARCHAR(255),
    repair_notes TEXT,
    FOREIGN KEY (maintenance_schedule_id) REFERENCES maintenance_schedules(schedule_id) ON DELETE CASCADE
);

-- Insert into Machine Parts Repair Table
INSERT INTO machine_parts_repair (maintenance_schedule_id, part_name, repair_date, vendor_name)
VALUES 
    (1, 'Control Panel', '2024-01-12', 'Tech Supplies Co.'),
    (2, 'Brake Pad', '2024-02-07', 'Machinery Parts Inc.'),
    (3, 'Drill Bit', '2024-03-17', 'Industrial Tools Ltd.'),
    (4, 'Grinding Wheel', '2024-04-12', 'Precision Tools Pvt.'),
    (5, 'Filter Cartridge', '2024-05-03', 'Filtration Experts LLC');

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

-- Machine Usage Logs Table
CREATE TABLE machine_usage_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    usage_date DATE NOT NULL,
    duration_in_hours INT NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);

-- Insert into Machine Usage Logs Table
INSERT INTO machine_usage_logs (machine_id, usage_date, duration_in_hours, purpose)
VALUES 
    (1, '2024-01-03', 5, 'Machining prototype parts.'),
    (2, '2024-01-10', 8, 'Fabricating custom components.'),
    (3, '2024-01-15', 3, 'Drilling holes for assembly line.'),
    (4, '2024-01-18', 6, 'Grinding precision tools.'),
    (5, '2024-01-20', 4, '3D printing demonstration models.');

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
