import mysql.connector
con = mysql.connector.connect(host="localhost", user="root", passwd="your_password_here")
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS FOOD")
cur.execute("USE FOOD")
cur.execute("""CREATE TABLE IF NOT EXISTS Donors (
  donor_id   INT AUTO_INCREMENT PRIMARY KEY,
  donor_name  VARCHAR(50),
  donor_phone VARCHAR(10),
  donor_city  VARCHAR(30))""")

cur.execute("""CREATE TABLE IF NOT EXISTS NGOs (
  ngo_id   INT AUTO_INCREMENT PRIMARY KEY,
  ngo_name  VARCHAR(50),
  ngo_phone VARCHAR(10))""")

cur.execute("""CREATE TABLE IF NOT EXISTS Donations (
  donation_id INT AUTO_INCREMENT PRIMARY KEY,
  donor_id   INT,
  ngo_id     INT,
  food_item  VARCHAR(50),
  meals      INT,
  donate_date DATE,
  status     VARCHAR(10) DEFAULT 'Available')""")
con.commit()
def add_donor():
  name = input("Donor name: ")
  phone = input("Phone: ")
  city = input("City: ")
  q = "INSERT INTO Donors (donor_name, donor_phone, donor_city) VALUES ('{}', '{}', '{}')".format(name, phone, city)
  cur.execute(q)
  con.commit()
  print("Donor added. Your Donor ID is", cur.lastrowid)
def add_ngo():
  name = input("NGO name: ")
  phone = input("Phone: ")
  q = "INSERT INTO NGOs (ngo_name, ngo_phone) VALUES ('{}', '{}')".format(name, phone)
  cur.execute(q)
  con.commit()
  print("NGO added. Your NGO ID is", cur.lastrowid)
def post_food():
  donor_id = int(input("Your Donor ID: "))
  item = input("Food item: ")
  meals = int(input("Number of meals: "))
  q = "INSERT INTO Donations (donor_id, food_item, meals, donate_date) VALUES ({}, '{}', {}, CURDATE())".format(donor_id, item, meals)
  cur.execute(q)
  con.commit()
  print("Food posted. Donation ID is", cur.lastrowid)
def view_food():
  cur.execute("""SELECT donation_id, donor_name, donor_phone, donor_city, food_item, meals
            FROM Donations NATURAL JOIN Donors
            WHERE status = 'Available'""")
  rows = cur.fetchall()
  if len(rows) == 0:
    print("No food available now.")
  for r in rows:
    print("ID:", r[0], "| Donor:", r[1], "| Phone:", r[2], "| City:", r[3],
      "| Food:", r[4], "| Meals:", r[5])

def accept_food():
  ngo_id = int(input("Your NGO ID: "))
  donation_id = int(input("Donation ID to accept: "))
  q = "UPDATE Donations SET ngo_id = {}, status = 'Accepted' WHERE donation_id = {} AND status = 'Available'".format(ngo_id, donation_id)
  cur.execute(q)
  con.commit()
  if cur.rowcount == 1:
    print("Pickup accepted. Please collect the food.")
  else:
    print("Wrong ID or food already taken.")
def monthly_report():
  cur.execute("""SELECT MONTHNAME(donate_date), YEAR(donate_date), SUM(meals)
            FROM Donations
            WHERE status = 'Accepted'
            GROUP BY YEAR(donate_date), MONTH(donate_date), MONTHNAME(donate_date)
            ORDER BY YEAR(donate_date), MONTH(donate_date)""")
  rows = cur.fetchall()
  if len(rows) == 0:
    print("No accepted donations yet.")
  for r in rows:
    print(r[0], r[1], ": total meals =", r[2])
def pickup_details():
  cur.execute("""SELECT donation_id, donor_name, ngo_name, food_item, meals
            FROM Donations NATURAL JOIN Donors NATURAL JOIN NGOs
            WHERE status = 'Accepted'""")
  rows = cur.fetchall()
  if len(rows) == 0:
    print("No completed pickups yet.")
  for r in rows:
    print("ID:", r[0], "| Donor:", r[1], "| NGO:", r[2], "| Food:", r[3], "| Meals:", r[4])
while True:
  print("\n===== FOOD DONATION TRACKER =====")
  print("1. Add Donor")
  print("2. Add NGO")
  print("3. Post Food")
  print("4. View Available Food")
  print("5. NGO Accepts Pickup")
  print("6. Monthly Meals Report")
  print("7. Pickup Details")
  print("0. Exit")
  ch = input("Enter choice: ")

  if ch == "1":
    add_donor()
  elif ch == "2":
    add_ngo()
  elif ch == "3":
    post_food()
  elif ch == "4":
    view_food()
  elif ch == "5":
    accept_food()
  elif ch == "6":
    monthly_report()
  elif ch == "7":
    pickup_details()
  elif ch == "0":
    print("Thank you!")
    break
  else:
    print("Invalid choice")

con.close()
