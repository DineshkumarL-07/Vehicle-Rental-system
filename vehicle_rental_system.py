import pyodbc
import re
pyodbc.drivers()
pattern = "^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w"

class VehicleRentalSystem:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={MySQL ODBC 8.2 Unicode Driver};'
                                   'SERVER=127.0.0.1;'
                                   'PORT=3306;'
                                   'DATABASE=console;'
                                   'USER=root;'
                                   'PASSWORD=dineshsql7;'
                                   'TRUSTED_CONNECTION=Yes;')

        self.cursor = self.conn.cursor()

    def admin_use(self):
        print(f"1: View Vehicles\n2: Search Vehicle\n3: Add vehicle\n4: Modify Vehicle Details\n5: Change the Security deposit amount\n6: Report\n7: Fine and regulation details")
        to_do = int(input("Enter Your Option:"))
        admin = veh.view_vehicles() if to_do==1 else veh.search_vehicle() if to_do==2 else veh.add_vehicle() if to_do==3 else veh.modify_vehicle() if to_do==4 else veh.change_security_deposit() if to_do==5 else veh.vehicle_report() if to_do==6 else veh.fine() if to_do==7 else print("Enter Valid Option")
    
    def renters_use(self):
        print(f"1: View the Vehicles\n2: Add an vehicle to the cart\n3: Remove the vehicle from the cart\n4: Rent an Vehicle\n5: History of rentals\n")
        get = int(input("Enter Your Option:"))
        user = veh.view_user_data() if get==1 else veh.add_to_cart() if get==2 else veh.remove_from_cart() if get==3 else veh.rent_vehicle() if get==4 else veh.history_of_user() if get==5 else print("Enter an valid option")
        
    def view_vehicles(self):
        query = "SELECT * FROM vehicle_details ORDER BY v_ID"
        print("List of the vehicles and details:\n")
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"ID: {row.v_ID}, Vehicle Brand: {row.v_brandname}, Type: {row.v_type}, Price: {row.v_rentalprice}")

    def search_vehicle(self):
        search_key = input("Enter the key to Search in Vehicles: ")
        query = "SELECT * FROM vehicle_details WHERE v_brandname LIKE ? OR v_number=?"
        self.cursor.execute(query,f"%{search_key}%",f"%{search_key}%")
        rows = self.cursor.fetchall()
        if not rows:
            print("Not found vehicle")
        else:
            print("The searched vehicles are: ")
            for row in rows:
                print(f"ID: {row.v_ID}, Vehicle Brand: {row.v_brandname}, Type: {row.v_type}, Price: {row.v_rentalprice}, Detail: {row.v_detail}")

    def add_vehicle(self):
        print("You can add")
        num = int(input("Enter the vehicle number to add:"))
        brand = input("Enter the vehicle brand name:")
        model = input("Enter the model:")
        price = int(input("Enter the rental price of the vehicle:"))
        c_b = input("Enter bike or car:")
        detail = input("Enter the status of the vehicle:")
        ID_v = int(input("Enter the id for vehicle:"))
        query = """INSERT INTO vehicle_details (v_number, v_brandname, v_model, v_rentalprice, v_type, v_detail, v_ID)
            VALUES(?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, num, brand, model, price, c_b, detail, ID_v)
        self.conn.commit()
        print("The vehicle details was added!")

    def modify_vehicle(self):
        print("You can modify")
        id = int(input("Enter vehicle ID to modify vehicle detail:"))
        status = input("Enter the vehicle detail:")
        query = "UPDATE vehicle_details SET v_detail = ? WHERE v_ID = ?"
        self.cursor.execute(query, status, id)
        self.conn.commit()
        print("The vehicle detail was modified!")

    def change_security_deposit(self):
        print("You can change")
        price = int(input("Enter the price of security deposit:"))
        type_v = input("Enter the vehicle type either Bike or Car:")
        query = "UPDATE vehicle_details SET v_rentalprice = ? WHERE v_type = ?"
        self.cursor.execute(query, price, type_v)
        self.conn.commit()
        print("The vehicle security deposit wae changed")

    def fine(self):
        print("update the fine and regulations")
        u_id = int(input("Enter the user ID:"))
        v_id = int(input("Enter the vehicle ID:"))
        damage_lable = input("Get the damage from the user[LIKE 'LOW','MEDIUM','HIGH']:")
        query = "SELECT v_returndate FROM user_data WHERE user_ID = ?"
        current_date = input("Enter the current date:")
        self.cursor.execute(query,u_id)
        row = self.cursor.fetchone()
        days = 0
        if row.v_returndate == current_date:
            print("The vehicle return on same day!")
            days += 1
        km = int(input("Enter the kms travel by the vehicle:"))
        query_1 = "SELECT v_rentalprice FROM vehicle_details WHERE v_ID = ?"
        self.cursor.execute(query_1,v_id)
        price = self.cursor.fetchone()
        if km > 500:
            rental_price = price.v_rentalprice * 0.15
            print(f"Additional charge is applied for the user ID:{u_id} for travelled above 500 kms on same day")
            print(f"The additional charge amount is {rental_price}")
        tot_price = 30000 - rental_price
        query_2 = "SELECT v_type FROM vehicle_details WHERE v_ID = ?"
        self.cursor.execute(query_2,v_id)
        vehicle_type = self.cursor.fetchone()
        if vehicle_type.v_type == "Car" and damage_lable!="None":
            charges = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.75}
            rent = price.v_rentprice * charges[damage_lable]
        tot_price -= rent
        print(f"Here is your balance caution deposit amount:{tot_price}")
        query_3 = """INSERT INTO user_admin (user_ID, v_ID, caution_deposit, damage_label, v_returndate, days)
                    VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query_3, u_id, v_id, tot_price, damage_lable, current_date, days)
        self.conn.commit()

    def vehicle_report(self):
        print("Your report")
    
    def view_user_data(self):
        query = "SELECT * FROM vehicle_details WHERE v_detail='Available'"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print("The Available vehicles are:")
        for row in rows:
            print(f"ID: {row.v_ID}, Vehicle Brand: {row.v_brandname}, Type: {row.v_type}, Price: {row.v_rentalprice}, Model: {row.v_model}")

    def add_to_cart(self):
        u_id = int(input("Enter your id:"))
        print("You can add only one vehicle to the cart")
        v_id = int(input("Enter an vehicle ID for rent: "))
        query_1 = "SELECT * FROM vehicle_details where WHERE v_ID = ?"
        self.cursor.execute(query_1, v_id)
        temp = self.cursor.fetchone()
        if temp.v_type=="Bike":
            print("The Minimum security deposit for your choosen vehicle ID is 3000")
        elif temp.v_type=="Car":
            print("The Minimum security deposit for your choosen vehicle ID is 10000")
        price = int(input("Enter your security deposit amount:"))
        date = input("Enter your rented vehicle return date in this format (yyyy/mm/dd) :")
        query = """INSERT INTO user_data (user_ID, v_ID, v_returndate, security_deposit)
                VALUES(?, ?, ?, ?)"""
        self.cursor.execute(query, u_id, v_id, date, price)
        self.conn.commit()
        print("The vehicle was added to the cart!")


    def remove_from_cart(self):
        u_id = int(input("Enter your id:"))
        v_id = int(input("Enter an vehicle id to remove from cart:"))
        query = "DELETE FROM user_data WHERE user_ID = ? AND v_ID = ?"
        self.cursor.execute(query, u_id, v_id)
        self.conn.commit()
        print("The vehicle was removed from the cart!")

    def rent_vehicle(self):
        u_id = int(input("Enter your ID:"))
        query = "SELECT v_ID FROM user_data WHERE user_ID = ?"
        self.cursor.execute(query, u_id)
        temp = self.cursor.fetchone()
        print(f"The vehicle ID {temp.v_ID} was rented successfully")

    def history_of_user(self):
        u_id = int(input("Enter your ID:"))
        query = "SELECT * FROM user_data WHERE user_ID = ?"
        self.cursor.execute(query, u_id)
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"User ID: {row.user_ID}, vehicle ID: {row.v_ID}")

    def display_message(self,email_id,password):
        if "admin" in email_id:
            if re.search(pattern,email_id) and len(password)>7:
                print("Welcome Admin\n")
                veh.admin_use()
            else:
                print("Enter an valid MailID or password")
        elif re.search(pattern,email_id) and len(password)>7:
            print("Welcome User")
            veh.renters_use()
        else:
            print("Enter an valid MailID or password")

print("WELCOME TO VEHICLE RENTEL SHOP\n")
email_id = input("Enter your EmailID:")
password = input("Enter your Password:")
print()
veh = VehicleRentalSystem()
veh.display_message(email_id,password)