CREATE DATABASE IF NOT EXISTS hospital_system;
USE hospital_system;

CREATE TABLE Patient (
    patient_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    gender CHAR(1),
    birth_date DATE,
    phone VARCHAR(20),
    address VARCHAR(200),
    insurance_number VARCHAR(30)
);

CREATE TABLE Department (
    dept_id VARCHAR(10) PRIMARY KEY,
    dept_name VARCHAR(50),
    location VARCHAR(50),
    phone VARCHAR(20),
    director_id VARCHAR(10)
);

CREATE TABLE Doctor (
    doctor_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    gender CHAR(1),
    title VARCHAR(20),
    specialty VARCHAR(50),
    phone VARCHAR(20),
    dept_id VARCHAR(10),
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

CREATE TABLE Medicine (
    medicine_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    specification VARCHAR(50),
    unit_price DECIMAL(10,2),
    manufacturer VARCHAR(100),
    stock_quantity INT
);

CREATE TABLE MedicalRecord (
    record_id VARCHAR(20) PRIMARY KEY,
    visit_date DATE,
    symptoms TEXT,
    diagnosis TEXT,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(10),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE PrescriptionDetail (
    record_id VARCHAR(20),
    medicine_id VARCHAR(10),
    quantity INT,
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    PRIMARY KEY (record_id, medicine_id),
    FOREIGN KEY (record_id) REFERENCES MedicalRecord(record_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
);
