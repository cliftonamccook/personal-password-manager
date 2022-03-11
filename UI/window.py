from tkinter import *
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
    password_vault_window = None

    @staticmethod
    def _clearwidgets():
        """
        clears window objects
        :return: void
        """
        for widget in PPMWindow.window.winfo_children():
            widget.destroy()


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

    def get_masterpwdtxt(self):
        mpwd = self.master_password_text.get()
        return mpwd


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
            command=""
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


def main():
    controller = Controller()
    PPMWindow.controller = controller
    mainwindow = PPMWindow()
    controller.ui = mainwindow
    mainwindow.password_vault_window = PasswordVaultWindow()
    mainwindow.login_window = LoginWindow()
    mainwindow.initial_window = InitialWindow()

    if controller.db.cursor.fetchall():
        mainwindow.login_window.start()
    else:
        mainwindow.initial_window.start()
    mainwindow.window.mainloop()


if __name__ == '__main__':
    main()
