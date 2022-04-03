from tkinter import *
from tkinter import messagebox
from UI.image import PPMLogo
import pyperclip
from functools import partial


class PPMWindow(Tk):
    """
    Root GUI Window
    """

    def __init__(self, controller):
        Tk.__init__(self)
        self.controller = controller
        self.geometry('1280x720')
        self.title("Personal Password Manager")
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.con = container
        self.frames = {}

        for F in (EntryFrame, PasswordVaultFrame, LoginFrame, ResetFrame, InitialFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def start(self):
        if self.controller.db.cursor.fetchall():
            self.show_frame(LoginFrame)
        else:
            self.show_frame(InitialFrame)
        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def reloadvault(self):
        self.frames[PasswordVaultFrame] = None
        f = PasswordVaultFrame(self.con, self)
        self.frames[PasswordVaultFrame] = f
        f.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PasswordVaultFrame)


class InitialFrame(Frame):
    """
    Password database creation interface
    Requires a master password for encrypting entries
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.imageData = PPMLogo.imageData
        self.master_password_label = Label(
            self,
            text="Choose a master password"
        )
        self.master_password_label.config(anchor=CENTER)
        self.master_password_label.pack()
        self.master_password_text = Entry(
            self,
            width=40,
            show="*"  # Hides password characters
        )
        self.master_password_text.pack()
        self.master_password_text.focus()
        self.confirm_master_password_label = Label(
            self,
            text="Confirm master password"
        )
        self.confirm_master_password_label.config(anchor=CENTER)
        self.confirm_master_password_label.pack()
        self.confirm_master_password_text = Entry(
            self,
            width=40,
            show="*"  # Hides password characters
        )
        self.confirm_master_password_text.pack()
        self.save_master_password_button = Button(
            self,
            text="Save",
            command=self.savepwd
        )
        self.save_master_password_button.pack(pady=5)
        self.im = PhotoImage(data=self.imageData)
        Label(self, image=self.im).pack(pady=100)

    def savepwd(self):
        pwd = self.master_password_text.get()
        cpwd = self.confirm_master_password_text.get()
        self.root.controller.savemasterpassword(pwd, cpwd)
        key = self.root.controller.messages["key"]
        if key != "":
            frame = RecoveryFrame(self.parent, self.root, key)
            self.root.frames[RecoveryFrame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.root.show_frame(RecoveryFrame)
        else:
            self.master_password_label.config(text="Passwords don't match")


class EntryFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.name_label = Label(self, text="Name")
        self.name_label.config(anchor=CENTER)
        self.name_label.pack()
        self.name_text = Entry(self, width=40)
        self.name_text.pack()
        self.name_text.focus()
        self.url_label = Label(self, text="URL")
        self.url_label.config(anchor=CENTER)
        self.url_label.pack()
        self.url_text = Entry(self, width=40)
        self.url_text.pack()
        self.url_text.focus()
        self.username_label = Label(self, text="Username")
        self.username_label.config(anchor=CENTER)
        self.username_label.pack()
        self.username_text = Entry(self, width=40)
        self.username_text.pack()
        self.username_text.focus()
        self.password_label = Label(self, text="Password")
        self.password_label.config(anchor=CENTER)
        self.password_label.pack()
        self.password_text = Entry(self, width=40)
        self.password_text.pack()
        self.note_label = Label(self, text="Note")
        self.note_label.config(anchor=CENTER)
        self.note_label.pack()
        self.note_text = Text(
            self,
            undo=True,
            height=10,
            width=40
        )
        self.note_text.pack(fill='y')
        self.name_text.focus()

        self.save_entry_button = Button(
            self,
            text="Save",
            command=self.saveEntry
        )
        self.save_entry_button.pack(pady=5)

        self.cancel_button = Button(
            self,
            text="Cancel",
            command=lambda: controller.show_frame(PasswordVaultFrame)
        )
        self.cancel_button.pack(pady=5)

    def saveEntry(self):
        obj = {
            "name": self.name_text.get(),
            "url": self.url_text.get(),
            "username": self.username_text.get(),
            "password": self.password_text.get(),
            "notes": self.note_text.get("1.0", "end - 1 chars")
        }
        self.root.controller.addentry(obj)
        self.clearfields()
        self.root.reloadvault()

    def clearfields(self):
        self.name_text.delete(0,'end')
        self.url_text.delete(0,'end')
        self.username_text.delete(0,'end')
        self.password_text.delete(0,'end')
        self.note_text.delete(1.0,'end')


class LoginFrame(Frame):
    def __init__(self, parent, controller) -> None:
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.imageData = PPMLogo.imageData
        self.master_password_entry_label = Label(
            self,
            text="Enter Master Password"
        )
        self.master_password_entry_label.config(anchor=CENTER)
        self.master_password_entry_label.pack()
        self.master_password_text = Entry(
            self,
            width=40,
            show="*"  # Hides password characters
        )
        self.master_password_text.pack()
        self.master_password_text.focus()
        self.error_text = Label(self)
        self.error_text.config(anchor=CENTER)
        self.error_text.pack(side=TOP)
        self.open_vault_button = Button(
            self, text="Open Password Vault",
            command=self.login
        )
        self.open_vault_button.pack(pady=5)
        self.reset_button = Button(
            self,
            text="Reset Password",
            command=lambda: controller.show_frame(ResetFrame)
        )
        self.reset_button.pack(pady=5)

        self.im = PhotoImage(data=self.imageData)
        Label(self, image=self.im).pack(pady=100)

    def login(self):
        k = self.master_password_text.get()
        self.root.controller.openvault(k)
        if self.root.controller.messages["Password"]:
            self.root.reloadvault()
        else:
            self.master_password_text.delete(0, 'end')
            self.error_text.config(text="Wrong Password")


class ResetFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.root = controller
        self.enter_rkey_button = Label(
            self,
            text="Enter Recovery Key"
        )
        self.enter_rkey_button.config(anchor=CENTER)
        self.enter_rkey_button.pack()
        self.rkey_text = Entry(self, width=20)
        self.rkey_text.pack()
        self.rkey_text.focus()
        self.message_label = Label(self)
        self.message_label.config(anchor=CENTER)
        self.message_label.pack()
        self.check_key_button = Button(
            self,
            text="Check Key",
            command=self.checkRK
        )
        self.check_key_button.pack(pady=5)

    def checkRK(self):
        rk = self.rkey_text.get()
        self.root.controller.checkrecoverykey(rk)
        if self.root.controller.messages["checked"]:
            self.root.show_frame(InitialFrame)
        else:
            self.rkey_text.delete(0, 'end')
            self.message_label.config(text='Wrong Key')


class RecoveryFrame(Frame):
    def __init__(self, parent, controller, key=""):
        Frame.__init__(self, parent)
        self.save_recovery_key_label = Label(
            self,
            text="Save this key to be able to recover account"
        )
        self.save_recovery_key_label.config(anchor=CENTER)
        self.save_recovery_key_label.pack()
        self.recovery_key_label = Label(
            self,
            text=key
        )
        self.recovery_key_label.config(anchor=CENTER)
        self.recovery_key_label.pack()
        self.copy_button = Button(
            self,
            text="Copy Key",
            command=lambda: pyperclip.copy(self.recovery_key_label.cget("text"))
        )
        self.copy_button.pack(pady=5)
        self.open_vault_button = Button(
            self,
            text="Done",
            command=lambda: controller.show_frame(PasswordVaultFrame)
        )
        self.open_vault_button.pack(pady=5)


class PasswordVaultFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.add_entry_button = Button(
            self, text="Add Entry",
            command=self.addentry
        )
        self.add_entry_button.grid(column=1, pady=20)

        self.search_button = Button(
            self,
            text="Search",
            command=self.searchString
        )
        self.search_button.grid(row=0, column=2)

        self.search_field = Entry(self)
        self.search_field.grid(row=0, column=3)

        self.lock_button = Button(
            self,
            text="Lock Vault",
            bg="red",
            command=self.lock
        )
        self.lock_button.grid(row=0)

        self.refresh = Button(
            self,
            text="Refresh All Entries",
            bg="green",
            fg="white",
            command=self.refresh
        )
        self.refresh.grid(row=0, column=4)

        self.name_label = Label(
            self,
            text="Name",
            font=('Helvetica', 14, 'bold')
        )
        self.name_label.grid(row=2, column=0, padx=80)

        self.url_label = Label(
            self,
            text="URL",
            font=('Helvetica', 14, 'bold')
        )
        self.url_label.grid(row=2, column=1, padx=80)

        self.username_label = Label(
            self,
            text="Username",
            font=('Helvetica', 14, 'bold')
        )
        self.username_label.grid(row=2, column=2, padx=80)

        self.password_label = Label(
            self,
            text="Password",
            font=('Helvetica', 14, 'bold')
        )
        self.password_label.grid(row=2, column=3, padx=80)

        self.notes = {}
        self.entries = self.root.controller.entryman.entries

        if self.entries is not None:
            for i in range(len(self.entries)):
                id = self.entries[i].id
                name = StringVar()
                name.set(self.entries[i].name)
                url = StringVar()
                url.set(self.entries[i].url)
                username = StringVar()
                username.set(self.entries[i].username)
                password = StringVar()
                password.set(self.entries[i].password)
                notes = StringVar()
                notes.set(self.entries[i].notes)
                self.notes[id] = notes

                Entry(self, state="readonly", textvariable=name).grid(row=i + 4, column=0)
                Entry(self, state="readonly", textvariable=url).grid(row=i + 4, column=1)
                Entry(self, state="readonly", textvariable=username).grid(row=i + 4, column=2)
                Entry(self, show='', state="readonly", textvariable=password).grid(row=i + 4, column=3)
                Button(self, text="Show Note", command=partial(self.shownote, id)).grid(column=5, row=(i + 4), pady=10)
                Button(self, text="Delete", command=partial(self.remove, id)).grid(column=6, row=(i + 4), pady=10)

    def searchString(self):
        txt = self.search_field.get()
        self.root.controller.search(txt)
        self.root.reloadvault()

    def refresh(self):
        self.root.controller.refreshall()
        self.root.reloadvault()

    def lock(self):
        self.root.frames[LoginFrame].master_password_text.delete(0, 'end')
        self.root.show_frame(LoginFrame)

    def remove(self, id: int):
        self.root.controller.deleteentry(id)
        self.root.reloadvault()

    def shownote(self, id: int):
        notes = self.notes[id].get()[2:-1]
        lines = notes.split("\\n")
        messagebox.showinfo("Note", "\n".join(lines))

    def addentry(self):
        self.root.show_frame(EntryFrame)
