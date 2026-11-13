-- Food Donation Tracker - database structure (MySQL / MariaDB)
-- This is exactly what food_tracker.py creates by itself on first run.
-- It is provided so the back end can be read, created or inspected
-- in MySQL Workbench or the mysql command line without Python:
--     mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS FOOD;
USE FOOD;

CREATE TABLE IF NOT EXISTS Donors (
 donor_id INT AUTO_INCREMENT PRIMARY KEY,
 donor_name VARCHAR(50),
 donor_phone VARCHAR(10),
 donor_city VARCHAR(30));

CREATE TABLE IF NOT EXISTS NGOs (
 ngo_id INT AUTO_INCREMENT PRIMARY KEY,
 ngo_name VARCHAR(50),
 ngo_phone VARCHAR(10));

CREATE TABLE IF NOT EXISTS Donations (
 donation_id INT AUTO_INCREMENT PRIMARY KEY,
 donor_id INT,
 ngo_id INT,
 food_item VARCHAR(50),
 meals INT,
 donate_date DATE,
 status VARCHAR(10) DEFAULT 'Available');
