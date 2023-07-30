import mysql.connector
import csv
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Railway_Management"
)
cursor = db.cursor()
passenger_entries = []
train_chart_frame = None
train_listbox = None

# Function to create train chart
def create_train_chart():
    global train_chart_frame
    train_chart_frame = Frame(root)
    train_chart_frame.pack(pady=10)

    # Column headings
    train_name_label = Label(train_chart_frame, text="Train Name", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
    train_name_label.grid(row=0, column=0)
    arrival_time_label = Label(train_chart_frame, text="Arrival Time", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
    arrival_time_label.grid(row=0, column=1)
    ticket_cost_label = Label(train_chart_frame, text="Ticket Cost", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
    ticket_cost_label.grid(row=0, column=2)

    with open('train_data.csv', 'r') as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader):
            train_name = row['Train Name']
            arrival_time = row['Arrival Time']
            ticket_cost = row['Ticket Cost']

            train_name_entry = Entry(train_chart_frame, font=("Arial", 12), fg="black", bg="light yellow", relief="ridge")
            train_name_entry.insert(0, train_name)
            train_name_entry.grid(row=i+1, column=0)

            arrival_time_entry = Entry(train_chart_frame, font=("Arial", 12), fg="black", bg="light yellow", relief="ridge")
            arrival_time_entry.insert(0, arrival_time)
            arrival_time_entry.grid(row=i+1, column=1)

            ticket_cost_entry = Entry(train_chart_frame, font=("Arial", 12), fg="black", bg="light yellow", relief="ridge")
            ticket_cost_entry.insert(0, ticket_cost)
            ticket_cost_entry.grid(row=i+1, column=2)

# Function to search trains
def search_trains():
    source = source_entry.get()
    destination = destination_entry.get()

    # Read train data from CSV file
    with open('train_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        trains = [row for row in reader if row['Source'] == source and row['Destination'] == destination]

    if len(trains) == 0:
        messagebox.showinfo("No Trains", "No trains found for the given source and destination.")
    else:
        # Clear the train chart
        train_chart_frame.destroy()

        # Create a new frame for specific trains
        specific_trains_frame = Frame(root)
        specific_trains_frame.pack(pady=10)

        # Column headings
        train_name_label = Label(specific_trains_frame, text="Train Name", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
        train_name_label.grid(row=0, column=0)
        arrival_time_label = Label(specific_trains_frame, text="Arrival Time", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
        arrival_time_label.grid(row=0, column=1)
        ticket_cost_label = Label(specific_trains_frame, text="Ticket Cost", font=("Arial", 12, "bold"), fg="black", bg="light yellow", padx=10, pady=5)
        ticket_cost_label.grid(row=0, column=2)

        # Clear the previous train listbox
        train_listbox.delete(0, END)

        # Display specific trains
        for i, train in enumerate(trains):
            train_name = train['Train Name']
            arrival_time = train['Arrival Time']
            ticket_cost = train['Ticket Cost']

            train_listbox.insert(END, f"Train: {train_name}\nArrival: {arrival_time}\nDestination: {ticket_cost}")

# Function to add passenger details
def add_passenger():
    passenger_count = passenger_count_entry.get()
    if not passenger_count.isdigit():
        messagebox.showinfo("Invalid Input", "Please enter a valid number of passengers.")
        return

    passenger_count = int(passenger_count)
    if passenger_count <= 0:
        messagebox.showinfo("Invalid Input", "Please enter a valid number of passengers.")
        return

    global passenger_details_window
    passenger_details_window = Toplevel(root)
    passenger_details_window.title("Passenger Details")
    passenger_details_window.geometry("400x300")
    passenger_details_window.config(bg="light blue")

    for i in range(passenger_count):
        passenger_frame = Frame(passenger_details_window, bg="light blue")
        passenger_frame.pack(pady=5)

        name_label = Label(passenger_frame, text=f"Passenger {i+1} Name:", font=("Arial", 12, "italic"), fg="black", bg="light blue")
        name_label.grid(row=0, column=0, padx=5)
        name_entry = Entry(passenger_frame)
        name_entry.grid(row=0, column=1)
        passenger_entries.append(name_entry)

        age_label = Label(passenger_frame, text=f"Passenger {i+1} Age:", font=("Arial", 12, "italic"), fg="black", bg="light blue")
        age_label.grid(row=1, column=0, padx=5)
        age_entry = Entry(passenger_frame)
        age_entry.grid(row=1, column=1)
        passenger_entries.append(age_entry)

    confirm_button = Button(passenger_details_window, text="Confirm Booking", command=confirm_booking, font=("Arial", 12, "bold"))
    confirm_button.pack(pady=10)

    # Disable Add Passenger Details button
    add_passenger_button.config(state=DISABLED)

# Function to confirm the booking and save data
def confirm_booking():
    selected_train_index = train_listbox.curselection()
    if len(selected_train_index) == 0:
        messagebox.showinfo("No Train Selected", "Please select a train to book a ticket.")
        return

    selected_train = train_listbox.get(selected_train_index[0])
    train_name = selected_train.split("\n")[0].split(": ")[1]
    arrival_time = selected_train.split("\n")[1].split(": ")[1]
    ticket_cost = selected_train.split("\n")[2].split(": ")[1]

    passenger_details = []
    for i in range(0, len(passenger_entries), 2):
        name = passenger_entries[i].get()
        age = passenger_entries[i + 1].get()
        if name and age:
            passenger_details.append((name, age))

    if not passenger_details:
        messagebox.showinfo("No Passenger Details", "Please enter passenger details.")
        return

    # Save ticket data to the database
    query = "INSERT INTO tickets (train_name, arrival_time, ticket_cost, name, age) VALUES (%s, %s, %s, %s, %s)"
    values = [(train_name, arrival_time, ticket_cost, name, age) for name, age in passenger_details]
    cursor.executemany(query, values)
    db.commit()

    # Generate a decorative bill
    bill_window = Toplevel(root)
    bill_window.title("Ticket Details")
    bill_window.geometry("400x300")
    bill_window.config(bg="light blue")

    bill_label = Label(bill_window, text="Ticket Details", font=("Arial", 16, "bold"), fg="black", bg="light green")
    bill_label.pack(pady=10)

    ticket_text = f"Train Name: {train_name}\nArrival Time: {arrival_time}\nTicket Cost: {ticket_cost}\n\nPassenger Details:\n"
    for name, age in passenger_details:
        ticket_text += f"Name: {name}\tAge: {age}\n"
    ticket_label = Label(bill_window, text=ticket_text, font=("Arial", 12, "italic"), fg="black", bg="light yellow")
    ticket_label.pack(pady=10)

    # Clear passenger details
    for entry in passenger_entries:
        entry.delete(0, END)

    # Enable Add Passenger Details button
    add_passenger_button.config(state=NORMAL)

    messagebox.showinfo("Booking Confirmed", "Ticket booked successfully!")
    passenger_details_window.destroy()

# Tkinter GUI setup
root = Tk()
root.title("Railway Reservation System")
root.geometry("1920x1080")

# Background image
background_image = Image.open("railway.jpeg")
background_photo = ImageTk.PhotoImage(background_image.resize((1920, 1080), Image.ANTIALIAS))
background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Heading
heading_label = Label(root, text="Railway Reservation System", font=("Arial", 24, "bold"), fg="white", bg="pink")
heading_label.pack(pady=20)

# GUI Elements for train search
train_chart_frame = Frame(root)
train_chart_frame.pack(pady=10)
create_train_chart()

source_label = Label(root, text="Source:", font=("Arial", 14, "italic"), fg="black", bg="pink")
source_label.pack()
source_entry = Entry(root, font=("Arial", 14))
source_entry.pack()

destination_label = Label(root, text="Destination:", font=("Arial", 14, "italic"), fg="black", bg="pink")
destination_label.pack()
destination_entry = Entry(root, font=("Arial", 14))
destination_entry.pack()

search_button = Button(root, text="Search Trains", command=search_trains, font=("Arial", 14, "bold"))
search_button.pack(pady=10)

train_listbox = Listbox(root, width=70, height=10, font=("Arial", 14))
train_listbox.pack(padx=20)

passenger_count_label = Label(root, text="Number of Passengers:", font=("Arial", 14, "italic"), fg="black", bg="pink")
passenger_count_label.pack()
passenger_count_entry = Entry(root, font=("Arial", 14))
passenger_count_entry.pack()

add_passenger_button = Button(root, text="Add Passenger Details", command=add_passenger, font=("Arial", 14, "bold"))
add_passenger_button.pack(pady=10)

# Execute the Tkinter event loop
root.mainloop()

# Close the database connection
db.close()
