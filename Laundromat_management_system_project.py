import json
import os
from datetime import datetime
DATA_FILE = "customers.json"
ORDERS_FILE = "orders.json"

# constants
TAXRATE = 0.06
COSTLAB = 0.50
ADMIN_PASSWORD = "sher2026"

def load_customers():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return{"maharjan9803" : 20.00, "Shrestha0099": 10.00, "Bajra1234": 2.20}
    
def save_customers():
    with open(DATA_FILE, "w") as f:
        json.dump(customer, f, indent=2)
        
customer = load_customers()

def load_orders():
    try:
        with open(ORDERS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return[]
    
def save_orders():
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

orders = load_orders()

def save_receipt(order):
    os.makedirs("receipt", exist_ok=True)
    
    stamp = order["date"].replace(" ", "_").replace(":", "-")
    filename = f"receipt/receipt_{order['customer_id']}_{stamp}.txt"

    with open(filename, "w") as f:
        f.write("SHER LAUNDROMAT\n")
        f.write("-" * 25 + "\n")
        f.write(f"Date:      {order['date']}\n")
        f.write(f"Customer:  {order['customer_id']}\n")
        f.write(f"Pounds:    {order['pounds']} lbs\n")
        f.write("-" * 25 + "\n")
        f.write(f"Subtotal:  ${order['subtotal']:.2f}\n")
        f.write(f"Taxes:     ${order['taxes']:.2f}\n")
        f.write(f"Total:     ${order['total']:.2f}\n")
        f.write("-" * 25 + "\n")
        f.write("Thank you!\n")
        print("Receipt saved to:", os.path.abspath(filename))

def check_admin():
    attempts = 3
    while attempts > 0:
        password = input("\nEnter the admin password: ")
        if password == ADMIN_PASSWORD:
            return True
        attempts -= 1
        print(f"Wrong password. {attempts} tries left.")
    return False
            
def calculate(customerid):
    """
    Docstring for calculate. This function calculates the subtotal, taxes and total amount of a customer
    
    :param customerid: it is derived from the input of service 1

    :returned
        subtotal: it is the product of input pound of laundry and the cost per pound,
        taxes: it is the product of subtotal and tax rate
        total: it is the sum of subtotal and taxes
    """
    # Getting lbs
    lbs = float(input("\nEnter the number of pounds of your laundry: "))
    while lbs <= 0:
        print("\nInvalid! Pounds must be positive and non zero.")
        lbs = float(input("\nEnter the number of pounds of your laundry: "))
        
    # Calculate total due
    subtotal = lbs * COSTLAB
    taxes = subtotal * TAXRATE
    total = subtotal + taxes
        
    # Adding total amount to the dictionary
    customer[customerid] += total
    save_customers()
    order = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "customer_id": customerid,
        "pounds":lbs,
        "subtotal": round(subtotal, 2),
        "taxes": round(taxes, 2),
        "total": round(total, 2)
        }
    orders.append(order)
    save_orders()
    save_receipt(order)
    
    return subtotal, taxes, total


def update_rate(update_service):
    """
    Docstring for update_rate. This function is used to update the rates of cost and taxes
    
    :param update_service: it is derived from service 2 to find the necessary update service
    """
    # Accessing global variable for updating
    global TAXRATE, COSTLAB
        
    # Updating the charges
    if update_service == '1':
        TAXRATE = (float(input("Enter the new taxrate in percentage: ")) / 100)
        print("Your new taxrate is ", TAXRATE)

    elif update_service == '2':
        COSTLAB = float(input("Enter the new costlab: "))
        print("Your new cost per pound is $", COSTLAB)

    elif update_service == '3':
        print("Cancelled")


def display_customer():
    """
    Docstring for display_customer. 
    This function prints the whole customer list with customer ID and their total amount over time.
    """
    # Printing the customer list
    print("\n\tCustomer List")
    print("-" * 30)
    print(f"{'Customer ID':<20}| {'Total':>5}")
    print("-" * 30)
    for customerid, total in customer.items():
        print(f"{customerid:<20}| ${total:.2f}")
    print()
 
def display_orders():
     print("\n\tOrder History")
     print("-" * 60)
     print(f"{'Date':<18}| {'Customer':<14}| {'Lbs':>5} | {'Total':>7}")
     print("-" * 60)
     for order in orders:
         print(f"{order['date']:<18}| {order['customer_id']:<14}| {order['pounds']:>5.1f} | ${order['total']:>6.2f}")
     print(f"\nTotal orders: {len(orders)}\n")

# Welcome message
print("\nWelcome! To the Sher laundromat!")

#Starting outer loop
service = 0

#Adding outer loop until the user choses option 4
while service != '5':
    
    # Printing the menu
    print("\n1. Calculate the total")
    print("2. Update the charges")
    print("3. Print customer list")
    print("4. Print order history")
    print("5. Quit")
    
    # Getting the user input
    service = input("\nPlease choose your option from number (1-5) for the type of service you looking for: ")
    while service not in ['1', '2', '3', '4', '5']:
        print("\nInvalid choice! Please enter a number from 1-5.")
        service = input("\nPlease choose your option from number (1-4) for the type of service you looking for: ")
    
    # Getting the user's option
    if service == '1':
         # Getting customerid from the user
        customerid = input("\nPlease enter your customer ID: ")
        go_back = False

        while customerid not in customer:
            print(f"\nError: {customerid} does not exist.")
            # Checking if user wants to create new customer
            create_new = input("\nWould you like to create a new account? (yes/no): ").lower()
                
            while create_new not in ["yes", "no", "y", "n"]:
                print("\nInvalid input! Please enter 'yes' or 'no'.")
                create_new = input("\nWould you like to create a new account? (yes/no): ").lower()
                    
            if create_new in ["yes", "y"]:
                # Initialize new customer with $0 balance
                customer[customerid] = 0.00
                save_customers()
                print(f"New account created for '{customerid}'!")
                break

            else:
                # Checking if user would like to re-enter valid customer ID
                re_enter = input("\nWould you like to enter valid customer ID? (yes/no): ").lower()
                
                while re_enter not in ["yes", "no", "y", "n"]:
                    print("\nInvalid input! Please enter 'yes' or 'no'.")
                    re_enter = input("\nWould you like to  enter valid customer ID? (yes/no): ").lower()
                
                if re_enter in ["yes", "y"]:  
                    customerid = input("\nPlease re-enter a valid customer ID: ")
                else:
                    # Going back to the main menu
                    go_back = True
                    break
        
        if not go_back:
            # Assigning the returned values respectively
            subtotal, taxes, total = calculate(customerid)

            # Printing the receipt
            print(f"\n{'Subtotal':<10}: ${subtotal:.2f}")
            print(f"{'Taxes':<10}: ${taxes:.2f}")
            print(f"{'Total':<10}: ${total:.2f}\n")

    elif service == '2':
        if not check_admin():
            print("\nAccess denied. Returning to the main menu.")
            continue
        
        # Update menu
        print("\n1. Change the Tax rate")
        print("2. Change the cost rate")
        print("3. Cancel")
            
        # Getting the user's input
        update_service = input("\nChoose the option you want to update: ")
        while update_service not in ['1', '2', '3']:
            print("\nInvalid choice! Please enter 1, 2, or 3.")
            update_service = input("\nChoose the option you want to update (1-3): ")
            
        update_rate(update_service)

    elif service == '3':
       display_customer()
            
    elif service == '4':
        display_orders()

    elif service == '5':
        print("\nThank you for using Sher Laundromat...\n")
