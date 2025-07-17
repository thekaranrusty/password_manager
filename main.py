from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json


FONT_NAME = "Courier"
ALPHABETS_LC = list(string.ascii_lowercase)
ALPHABETS_UC = list(string.ascii_uppercase)
SPECIAL_CHAR = ['!','@','#','$','%','^','&','*','-','/']
NUMBERS = [str(n) for n in range(10)]
new_password = ""

window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text = "Website:", font=(FONT_NAME,11,"normal"), fg="black")
website_label.grid(column=0,row=2)
website = Entry(width=33)
website.grid(column=1,row=2)

email_label = Label(text = "Email/Username:", font=(FONT_NAME,11,"normal"), fg="black")
email_label.grid(column=0,row=3)
email = Entry(width=51)
email.grid(column=1,row=3, columnspan= 2)

password_label = Label(text = "Password:", font=(FONT_NAME,11,"normal"), fg="black")
password_label.grid(column=0,row=4)
password = Entry(width=33)
password.grid(column=1,row=4)

def generate_password():
    global new_password
    new_password = ""
    password.delete(0,END)
    password_length = random.randint(8,10)
    r = 0
    uc = 0
    lc = 0
    sp = 0
    nm = 0
    for i in range(password_length):
        if i==0:
            r = random.randint(0,1)
        else:
            r = random.randint(0,3)
        if r == 0:
            new_password += random.choice(ALPHABETS_UC)
            uc += 1
        elif r == 1:
            new_password += random.choice(ALPHABETS_LC)
            lc +=1
        elif r == 2:
            new_password += random.choice(SPECIAL_CHAR)
            sp += 1
        else :
            new_password += random.choice(NUMBERS)
            nm += 1
    if uc == 0 or lc == 0 or sp ==0 or nm == 0:
        generate_password()

    password.insert(0, string=new_password)
    pyperclip.copy(new_password)

def submit():
    web = website.get().strip().lower()
    pas = password.get()
    em = email.get().strip()

    new_data = {
        web: {
           "email": em,
            "password" : pas
        }
    }

    if web!= "" and  pas != "" and em != "":

        try:
            with open("data.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                # saving updated data
                json.dump(new_data, data_file, indent=4)

        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", 'w') as data_file:
                #saving updated data
                json.dump(data, data_file, indent=4)

        finally:
            website.delete(0, END)
            email.delete(0, END)
            password.delete(0, END)

            messagebox.showinfo(title="Successful", message="All your details are added successfully.")

    else:
        messagebox.showwarning(title="OOPS", message="Please don't leave any fields empty!")


def search_details():
    web = website.get().strip().lower()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No records exists")

    else:
        if web in data:
            messagebox.showinfo(title="Saved Details", message=f"Website: {web} \nEmail/Username: "
                                                               f"{data[web]["email"]} \nPassword: "
                                                               f"{data[web]["password"]}")
            pyperclip.copy(data[web]["password"])

        else:
            messagebox.showwarning(title="OOPS", message="Data not found")

password_btn = Button(text="Generate Password", command=generate_password , highlightthickness=0)
password_btn.grid(column=2, row=4, sticky='w')

submit_btn = Button(text="Add", command=submit, highlightthickness=0, width=43)
submit_btn.grid(column=1, row=5, columnspan=2)

search_btn = Button(text="Search", command= search_details, highlightthickness=0, width=14)
search_btn.grid(column=2, row=2)

window.mainloop()