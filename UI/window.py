from tkinter import *
from functools import partial
from tkinter import messagebox
import pyperclip
from Controller.controller import Controller


class PPMWindow:
    """
    Root Tkinter GUI frame
    """
    window = Tk()
    window.update()
    window.title("Personal Password Manager")
    controller = None
    screensize = '480x360'
    # References to sub-windows:
    initial_window = None
    login_window = None
    recovery_window = None
    reset_window = None
    password_vault_window = None
    entry_window = None

    def __init__(self):
        self.__val = 0

    @staticmethod
    def _clearwidgets():
        """
        clears window objects
        :return: void
        """
        for widget in PPMWindow.window.winfo_children():
            widget.destroy()


#class EntryWindow(PPMWindow):
#    """
#    New entry creation interface
#    """
#
#    def __init__(self):
#        super().__init__()
#        self.name_label = None
#        self.name_text = None
#        self.url_label = None
#        self.username_label = None
#        self.password_label = None
#        self.url_text = None
#        self.username_text = None
#        self.password_text = None
#        self.note_label = None
#        self.note_text = None
#        self.save_entry_button = None
#        self.cancel_button = None
#
#    def start(self):
#        super()._clearwidgets()
#        super().window.geometry(super().screensize)
#        self.name_label = Label(super().window, text="Name")
#        self.name_label.config(anchor=CENTER)
#        self.name_label.pack()
#        self.name_text = Entry(super().window, width=20)
#        self.name_text.pack()
#        self.name_text.focus()
#        self.url_label = Label(super().window, text="URL")
#        self.url_label.config(anchor=CENTER)
#        self.url_label.pack()
#        self.url_text = Entry(super().window, width=20)
#        self.url_text.pack()
#        self.url_text.focus()
#        self.username_label = Label(super().window, text="Username")
#        self.username_label.config(anchor=CENTER)
#        self.username_label.pack()
#        self.username_text = Entry(super().window, width=20)
#        self.username_text.pack()
#        self.username_text.focus()
#        self.password_label = Label(super().window, text="Password")
#        self.password_label.config(anchor=CENTER)
#        self.password_label.pack()
#        self.password_text = Entry(super().window, width=20)
#        self.password_text.pack()
#        self.note_label = Label(super().window, text="Note")
#        self.note_label.config(anchor=CENTER)
#        self.note_label.pack()
#        self.note_text = Text(
#            super().window,
#            undo=True,
#            height=5,
#            width=10
#        )
#        self.note_text.pack(fill=BOTH)
#        self.name_text.focus()
#
#        self.save_entry_button = Button(
#            super().window,
#            text="Save",
#            command=self.get_field_values
#        )
#        self.save_entry_button.pack(pady=5)
#
#        self.cancel_button = Button(
#            super().window, text="Cancel",
#            command=super().controller.ui.password_vault_window.start
#        )
#        self.cancel_button.pack(pady=5)
#
#    def get_field_values(self):
#        obj = {"name": self.name_text.get(), "url": self.url_text.get(), "username": self.username_text.get(),
#               "password": self.password_text.get(), "notes": self.note_text.get("1.0", "end - 1 chars")}
#        super().controller.addentry(obj)


class InitialWindow(PPMWindow):
    """
    Password database creation interface
    Requires a master password for encrypting entries
    """

    def __init__(self):
        super().__init__()
        self.master_password_label = None
        self.confirm_master_password_label = None
        self.master_password_text = None
        self.confirm_master_password_text = None
        self.save_master_password_button = None

    def start(self):
        super()._clearwidgets()
        super().window.geometry(super().screensize)
        self.master_password_label = Label(
            super().window,
            text="Choose a master password"
        )
        self.master_password_label.config(anchor=CENTER)
        self.master_password_label.pack()
        self.master_password_text = Entry(
            super().window,
            width=20,
            show="*"  # Hides password characters
        )
        self.master_password_text.pack()
        self.master_password_text.focus()
        self.confirm_master_password_label = Label(
            super().window,
            text="Confirm master password"
        )
        self.confirm_master_password_label.config(anchor=CENTER)
        self.confirm_master_password_label.pack()
        self.confirm_master_password_text = Entry(
            super().window,
            width=20,
            show="*"  # Hides password characters
        )
        self.confirm_master_password_text.pack()
        self.save_master_password_button = Button(
            super().window,
            text="Save",
            command=super().controller.savemasterpassword
        )
        self.save_master_password_button.pack(pady=5)

    def show_msg(self, msg):
        self.master_password_label.config(text=msg)

    def get_masterpwdtxt(self):
        mpwd = self.master_password_text.get()
        return mpwd

    def get_confirmpwdtxt(self):
        mpwd = self.confirm_master_password_text.get()
        return mpwd


class LoginWindow(PPMWindow):
    """
    Login interface
    """

    def __init__(self):
        super().__init__()
        self.master_password_entry_label = None
        self.error_text = None
        self.master_password_text = None
        self.open_vault_button = None
#        self.reset_button = None

    def start(self):
        super()._clearwidgets()
        super().window.geometry(super().screensize)
        self.master_password_entry_label = Label(
            super().window,
            text="Enter Master Password"
        )
        self.master_password_entry_label.config(anchor=CENTER)
        self.master_password_entry_label.pack()
        self.master_password_text = Entry(
            super().window,
            width=20,
            show="*"  # Hides password characters
        )
        self.master_password_text.pack()
        self.master_password_text.focus()
        self.error_text = Label(super().window)
        self.error_text.config(anchor=CENTER)
        self.error_text.pack(side=TOP)
        self.open_vault_button = Button(
            super().window, text="Open Password Vault",
            command=super().controller.checkpassword
        )
        self.open_vault_button.pack(pady=5)

#        self.reset_button = Button(
#            super().window,
#            text="Reset Password",
#            command="" # super().controller.resetpassword
#        )
#        self.reset_button.pack(pady=5)

    def get_masterpwdtxt(self):
        mpwd = self.master_password_text.get()
        return mpwd


#class RecoveryWindow(PPMWindow):
#    """
#    Menu enabling user to recover a forgotten password
#    """
#
#    def __init__(self):
#        super().__init__()
#        self.save_recovery_key_label = None
#        self.recovery_key_label = None
#        self.copy_button = None
#        self.open_vault_button = None
#
#    def copyKey(self):
#        pyperclip.copy(self.recovery_key_label.cget("text"))
#
#    def done(self):
#        super().controller.ui.password_vault_window.start()
#
#    def startRecovery(self, key):
#        super()._clearwidgets()
#        super().window.geometry(super().screensize)
#        self.save_recovery_key_label = Label(
#            super().window,
#            text="Save this key to be able to recover account"
#        )
#        self.save_recovery_key_label.config(anchor=CENTER)
#        self.save_recovery_key_label.pack()
#        self.recovery_key_label = Label(
#            super().window,
#            text=key
#        )
#        self.recovery_key_label.config(anchor=CENTER)
#        self.recovery_key_label.pack()
#        self.copy_button = Button(
#            super().window,
#            text="Copy Key",
#            command=self.copyKey
#        )
#        self.copy_button.pack(pady=5)
#        self.open_vault_button = Button(
#            super().window,
#            text="Done",
#            command=self.done
#        )
#        self.open_vault_button.pack(pady=5)
#
#
#class ResetWindow(PPMWindow):
#    """
#    This menu enables the user to change their master password
#    """
#
#    def __init__(self):
#        super().__init__()
#        self.enter_rkey_button = None
#        self.message_label = None
#        self.rkey_text = None
#        self.check_key_button = None
#
#    def start(self):
#        super()._clearwidgets()
#        super().window.geometry(super().screensize)
#        self.enter_rkey_button = Label(
#            super().window,
#            text="Enter Recovery Key"
#        )
#        self.enter_rkey_button.config(anchor=CENTER)
#        self.enter_rkey_button.pack()
#        self.rkey_text = Entry(super().window, width=20)
#        self.rkey_text.pack()
#        self.rkey_text.focus()
#        self.message_label = Label(super().window)
#        self.message_label.config(anchor=CENTER)
#        self.message_label.pack()
#        self.check_key_button = Button(
#            super().window,
#            text="Check Key",
#            command=super().controller.checkrecoverykey
#        )
#        self.check_key_button.pack(pady=5)


#class UserEntry(PPMWindow):
#    """
#    A UserEntry consists of:
#    Name, URL, Username, Password, and Note
#    """
#
#    def __init__(self, array, row):
#        super().__init__()
#        self.row = row
#        self.name_value = StringVar()
#        self.name_value.set(array[self.row]["name"])
#
#        self.name_field = Entry(
#            super().window,
#            textvariable=self.name_value,
#            fg="black",
#            bg="white",
#            bd=0,
#            state="readonly",
#            font=("Helvetica", 12),
#            justify=CENTER
#        )
#        self.name_field.grid(
#            column=0,
#            row=(self.row + 3)
#        )
#
#        self.url_value = StringVar()
#        self.url_value.set(array[self.row]["url"])
#
#        self.url_field = Entry(
#            super().window,
#            textvariable=self.url_value,
#            fg="black",
#            bg="white",
#            bd=0,
#            state="readonly",
#            font=("Helvetica", 12),
#            justify=CENTER
#        )
#        self.url_field.grid(
#            column=1,
#            row=(self.row + 3)
#        )
#
#        self.username_value = StringVar()
#        self.username_value.set(array[self.row]["username"])
#        self.username_field = Entry(
#            super().window,
#            textvariable=self.username_value,
#            fg="black",
#            bg="white",
#            bd=0,
#            state="readonly",
#            font=("Helvetica", 12),
#            justify=CENTER
#        )
#        self.username_field.grid(
#            column=2,
#            row=(self.row + 3)
#        )
#
#        self.password_value = StringVar()
#        self.password_value.set(array[self.row]["password"])
#        self.password_field = Entry(
#            super().window,
#            textvariable=self.password_value,
#            fg="black", bg="white", bd=0, state="readonly", font=("Helvetica", 12),
#            justify=CENTER,
#            show="*"
#        )
#        self.password_field.grid(
#            column=3,
#            row=(self.row + 3)
#        )
#
#        self.note_text = StringVar()
#        self.note_text.set(array[self.row]["notes"])
#
#        self.showpassword_button = Button(
#            super().window,
#            text="Show/Hide Password",
#            command=self.showpassword
#        )
#        self.showpassword_button.grid(
#            column=4,
#            row=(self.row + 3),
#            pady=10
#        )
#
#        self.shownote_button = Button(
#            super().window,
#            text="View Note",
#            command=self.shownote
#        )
#        self.shownote_button.grid(
#            column=5,
#            row=(self.row + 3),
#            pady=10
#        )
#
#        self.delete_button = Button(
#            super().window,
#            text="Delete",
#            command=partial(super().controller.deleteentry, array[self.row]["id"])
#        )
#        self.delete_button.grid(
#            column=6,
#            row=(self.row + 3),
#            pady=10
#        )
#
#    def showpassword(self):
#        if self.password_field["show"] == "":
#            self.password_field["show"] = "*"
#        else:
#            self.password_field["show"] = ""
#
#    def shownote(self):
#        notes = self.note_text.get()[2:-1]
#        lines = notes.split("\\n")
#        messagebox.showinfo("Note", "\n".join(lines))


class PasswordVaultWindow(PPMWindow):
    def __init__(self):
        super().__init__()
        self.name_label = None
        self.url_label = None
        self.username_label = None
        self.password_label = None
        self.add_entry_button = None
        self.search_button = None
        self.search_field = None
        self.lock_button = None

    def start(self):
        super()._clearwidgets()
        super().window.geometry('1280x720')
        super().window.resizable(height=None, width=None)
        self.add_entry_button = Button(
            super().window, text="Add Entry",
            command="" # super().controller.ui.entry_window.start
        )
        self.add_entry_button.grid(column=1, pady=20)

        self.search_button = Button(
            super().window,
            text="Search",
            command=""
        )
        self.search_button.grid(row=0, column=2)

        self.search_field = Entry(super().window)
        self.search_field.grid(row=0, column=3)

        self.lock_button = Button(
            super().window,
            text="Lock Vault",
            bg="red",
            command=super().controller.ui.login_window.start
        )
        self.lock_button.grid(row=0)

        self.name_label = Label(
            super().window,
            text="Name",
            font=('Helvetica', 14, 'bold')
        )
        self.name_label.grid(row=2, column=0, padx=80)

        self.url_label = Label(
            super().window,
            text="URL",
            font=('Helvetica', 14, 'bold')
        )
        self.url_label.grid(row=2, column=1, padx=80)

        self.username_label = Label(
            super().window,
            text="Username",
            font=('Helvetica', 14, 'bold')
        )
        self.username_label.grid(row=2, column=2, padx=80)

        self.password_label = Label(
            super().window,
            text="Password",
            font=('Helvetica', 14, 'bold')
        )
        self.password_label.grid(row=2, column=3, padx=80)

#        if super().controller.results is not None:
#            for i in range(len(super().controller.results)):
#                UserEntry(super().controller.results, i)


def main():
    controller = Controller()
    PPMWindow.controller = controller
    mainwindow = PPMWindow()
    controller.ui = mainwindow
    mainwindow.password_vault_window = PasswordVaultWindow()
#    mainwindow.entry_window = EntryWindow()
    mainwindow.login_window = LoginWindow()
#    mainwindow.recovery_window = RecoveryWindow()
#    mainwindow.reset_window = ResetWindow()
    mainwindow.initial_window = InitialWindow()

    if controller.db.cursor.fetchall():
        mainwindow.login_window.start()
    else:
        mainwindow.initial_window.start()
    mainwindow.window.mainloop()


if __name__ == '__main__':
    main()

