from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    messagebox.showinfo("Success", "Password has been copied to clipboard")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def clear_entries():
    web_entry.delete(0, END)
    password_entry.delete(0, END)

def write_data():
    web_data = web_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()

    new_data = {web_data:{"Email":email_data,"Password":password_data}}

    if len(web_data) == 0 or len(email_data) == 0 or len(password_data) == 0:
        messagebox.showerror("Error", "Please fill all fields")

    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
                clear_entries()
        else:
            if web_data in data:
                user_choice = messagebox.askokcancel(
                    title=web_data,
                    message="The data exists. Do you want to overwrite it?"
                )

                if user_choice:
                    data[web_data]["Email"] = email_data
                    data[web_data]["Password"] = password_data

                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)
                    clear_entries()

            else:
                confirm = messagebox.askokcancel(
                    title=web_data,
                    message=f"The details are:\n"
                            f"Website: {web_data}\n"
                            f"Email: {email_data}\n"
                            f"Password:{'*'*len(password_data)}\n"
                )

                if confirm:
                    data.update(new_data)

                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)
                    clear_entries()

#--------------------------password hide and show----------#
def show_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="•")

#-----------------------------SEARCH DETAILS--------------------------#
def search_details():
    website = web_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved data found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Data file is corrupted.")
    else:
        if website in data:
            email_entry.delete(0, END)
            email_entry.insert(0, data[website]["Email"])

            password_entry.delete(0, END)
            password_entry.insert(0, data[website]["Password"])
        else:
            messagebox.showinfo("DATA", "No data found for this website.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file = "logo.png")
logo = canvas.create_image(100, 100, image=lock_img)
canvas.grid(row = 0, column = 1)

#labels
web_label = Label(text = "Website Name")
web_label.grid(row = 1, column = 0)
email_label = Label(text = "Email Address")
email_label.grid(row = 2, column = 0)
password_label = Label(text = "Password")
password_label.grid(row = 3, column = 0)

#entries
web_entry = Entry(width = 35)
web_entry.focus()
web_entry.grid(row = 1, column = 1, columnspan = 2)
email_entry = Entry(width = 35)
email_entry.grid(row = 2, column = 1,columnspan = 2)
password_entry = Entry(width=35, show="*")
password_entry.grid(column=1, row=3, columnspan = 2)

#buttons
gen_pass_bt = Button(text = "Generate Password", command = generate_password)
gen_pass_bt.grid(row = 4, column = 2, columnspan = 2)

add_pass_bt = Button(text = "Add", width = 36, command= write_data)
add_pass_bt.grid(row = 5, column = 1, columnspan = 2)

search_bt = Button(text = "Search", command = search_details)
search_bt.grid(row = 1, column = 2, columnspan = 2)

show_var = BooleanVar()
show_button = Checkbutton(
    text="Show password",
    variable=show_var,
    command=show_password
)
show_button.grid(column=3, row=3)

window.mainloop()