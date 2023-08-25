# ---- Password Manager GUI -----

# --> Imported Libraries
from tkinter import *
from tkinter import messagebox
import PasswordManagerMain as backend

def add_Pw_GUI():
	# --> Define Window
	add_password_window = Tk()
	add_password_window.title("Add Password Menu")

	# --> Getting username, password and account
	def add_password():
		new_username = username_entry.get()
		new_password = password_entry.get()
		account = account_entry.get()

		if (len(new_username) < 3) or (len(new_username) > 15) or (" " in new_username):
			messagebox.showerror("Error", "Invalid Username!")
			return
		if (len(new_password) < 6) or (len(new_password) > 20) or (" " in new_password):
			messagebox.showerror("Error", "Invalid Password!")
			return

		backend.add_to_db(backend.encrypt_Password((new_username, new_password, account)), db_connection)
		messagebox.showinfo("Success", "Password added successfully!")
		add_password_window.destroy()

	def suggest_password():
		

		# --> Setting up GUI adding menu
		username_label = Label(add_password_window, text="Username:")
		username_label.pack()
		username_entry = Entry(add_password_window)
		username_entry.pack()

		password_label = Label(add_password_window, text="Password:")
		password_label.pack()
		password_entry = Entry(add_password_window, show="*")
		password_entry.pack(side="mid", padx = 5)

		suggest_label = Button(add_password_window, text="Suggest password!", command="")

		account_label = Label(add_password_window, text="Account:")
		account_label.pack()
		account_entry = Entry(add_password_window)
		account_entry.pack()

		add_button = Button(add_password_window, text="Add", command=add_password)
		add_button.pack()

def main_window():
	# --> Define Window
	mainWindow = Tk()
	mainWindow.title("Password Manager")

	def on_add_password():
		# --> Define Window
		add_password_window = Toplevel()
		add_password_window.title("Add Password Menu")

		# --> Getting username, password and account
		def add_password():
			new_username = username_entry.get()
			new_password = password_entry.get()
			account = account_entry.get()



			if (len(new_username) < 3) or (len(new_username) > 15) or (" " in new_username):
				messagebox.showerror("Error", "Invalid Username!")
				return
			if (len(new_password) < 6) or (len(new_password) > 20) or (" " in new_password):
				messagebox.showerror("Error", "Invalid Password!")
				return

			backend.add_to_db(backend.encrypt_Password((new_username, new_password, account)), db_connection)
			messagebox.showinfo("Success", "Password added successfully!")
			add_password_window.destroy()

		def suggest_password():
			suggestedPassword = backend.get_Suggestion()
			password_entry.insert(END, suggestedPassword)

		def show_password():
			state = password_entry.cget("show")

			if state == "*":
				password_entry.configure(show="")
				state = "show"
			else:
				password_entry.configure(show="*")
				state = "*"

			

		# --> Setting up GUI adding menu
		username_label = Label(add_password_window, text="Username:")
		username_label.pack()
		username_entry = Entry(add_password_window)
		username_entry.pack()

		password_label = Label(add_password_window, text="Password:")
		password_label.pack()
		password_entry = Entry(add_password_window, show="*")
		password_entry.pack()

		ButtonsPw = Frame(add_password_window)
		ButtonsPw.pack()

		suggest_button = Button(add_password_window, text="Suggest password!", command=suggest_password)
		suggest_button.pack(in_=ButtonsPw, side=LEFT)

		show_button = Button(add_password_window, text="Show password!", command=show_password)
		show_button.pack(in_=ButtonsPw, side=RIGHT)

		

		account_label = Label(add_password_window, text="Account:")
		account_label.pack()
		account_entry = Entry(add_password_window)
		account_entry.pack()

		add_button = Button(add_password_window, text="Add", command=add_password)
		add_button.pack()

	# --> Selecting password
	def on_get_password():
		get_window = Toplevel()
		get_window.title("Get Password")


		def get_password():
			account = account_entry.get()
			
			try:
				username, password = backend.decrypt_Password(db_connection, account)
				messagebox.showinfo("Information", f"Username: {username}\nPassword: {password}")
				#get_window.destroy()

			except: 
				messagebox.showerror("Error", "Please enter an valid account!")



		# --> Setting up GUI selecting window
		account_label = Label(get_window, text="Account:")
		account_label.pack()
		account_entry = Entry(get_window)
		account_entry.pack()

		get_button = Button(get_window, text="Get Password", command=get_password)
		get_button.pack()

	# --> Deleting password
	def on_delete_password():
		delete_window = Toplevel()
		delete_window.title("Delete Password")

		def delete_password():
			account = account_entry.get()

			if not account:
				messagebox.showerror("Error", "Please enter an account!")
				return

			backend.delete_of_db(db_connection, account)
			messagebox.showinfo("Success", "Password deleted successfully!")
			delete_window.destroy()

		# --> Setting up GUI deleting menu
		account_label = Label(delete_window, text="Account:")
		account_label.pack()
		account_entry = Entry(delete_window)
		account_entry.pack()

		delete_button = Button(delete_window, text="Delete Password", command=delete_password)
		delete_button.pack()

	# --> Setting up GUI main Menu
	add_button = Button(mainWindow, text="Add Password", command=on_add_password)
	add_button.pack(pady=10)

	get_button = Button(mainWindow, text="Get Password", command=on_get_password)
	get_button.pack(pady=10)

	delete_button = Button(mainWindow, text="Delete Password", command=on_delete_password)
	delete_button.pack(pady=10)

	mainWindow.mainloop()

if __name__ == "__main__":
	db_connection = backend.connectDb()
	main_window()
