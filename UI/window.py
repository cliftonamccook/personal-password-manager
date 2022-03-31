from tkinter import *
from tkinter import messagebox
from UI.image import PPMLogo
import pyperclip
from functools import partial


class PPMWindow(Tk):
    def __init__(self, controller): # *args, **kwargs
        Tk.__init__(self) # , *args, **kwargs
        self.controller = controller
        self.geometry('1280x720')
        self.title("Personal Password Manager")
        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

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
            width=20,
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
            width=20,
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
        Label(self, image=self.im).pack()

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
        self.name_text = Entry(self, width=20)
        self.name_text.pack()
        self.name_text.focus()
        self.url_label = Label(self, text="URL")
        self.url_label.config(anchor=CENTER)
        self.url_label.pack()
        self.url_text = Entry(self, width=20)
        self.url_text.pack()
        self.url_text.focus()
        self.username_label = Label(self, text="Username")
        self.username_label.config(anchor=CENTER)
        self.username_label.pack()
        self.username_text = Entry(self, width=20)
        self.username_text.pack()
        self.username_text.focus()
        self.password_label = Label(self, text="Password")
        self.password_label.config(anchor=CENTER)
        self.password_label.pack()
        self.password_text = Entry(self, width=20)
        self.password_text.pack()
        self.note_label = Label(self, text="Note")
        self.note_label.config(anchor=CENTER)
        self.note_label.pack()
        self.note_text = Text(
            self,
            undo=True,
            height=5,
            width=10
        )
        self.note_text.pack(fill=BOTH)
        self.name_text.focus()

        self.save_entry_button = Button(
            self,
            text="Save",
            command=self.addEntry
        )
        self.save_entry_button.pack(pady=5)

        self.cancel_button = Button(
            self, 
            text="Cancel",
            command=lambda: controller.show_frame(PasswordVaultFrame)
        )
        self.cancel_button.pack(pady=5)

    def addEntry(self):
        obj = {"name": self.name_text.get(), "url": self.url_text.get(), "username": self.username_text.get(),
               "password": self.password_text.get(), "notes": self.note_text.get("1.0", "end - 1 chars")}
        self.root.controller.addentry(obj)
        self.root.reloadvault()


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
            width=20,
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
        Label(self, image=self.im).pack()


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

    def checkRK(self, txt):
        rk = self.rkey_text.get()
        self.root.controller.checkrecoverykey(txt)
        if self.root.controller.messages["checked"]:
            self.root.show_frame(InitialFrame)
        else:
            self.rkey_text.delete(0, 'end')
            self.message_label.config(text='Wrong Key')


class RecoveryFrame(Frame):
    def __init__(self, parent, controller, key=""):
        Frame.__init__(self, parent)
        self.root = controller
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
            command=self.copyKey
        )
        self.copy_button.pack(pady=5)
        self.open_vault_button = Button(
            self,
            text="Done",
            command=self.done
        )
        self.open_vault_button.pack(pady=5)

    def copyKey(self):
        pyperclip.copy(self.recovery_key_label.cget("text"))

    def done(self):
        self.root.show_frame(PasswordVaultFrame)


class UserEntry(Frame):
    """
    A UserEntry consists of:
    Name, URL, Username, Password, and Note
    """

    def __init__(self, parent, controller, array, row):
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.row = row
        self.name_value = StringVar()
        self.name_value.set(array[self.row].name)

        self.name_field = Entry(
            self,
            textvariable=self.name_value,
            fg="black",
            bg="white",
            bd=0,
            state="readonly",
            font=("Helvetica", 12),
            justify=CENTER
        )
        self.name_field.grid(
            column=0,
            row=(self.row + 3)
        )

        self.url_value = StringVar()
        self.url_value.set(array[self.row].url)

        self.url_field = Entry(
            self,
            textvariable=self.url_value,
            fg="black",
            bg="white",
            bd=0,
            state="readonly",
            font=("Helvetica", 12),
            justify=CENTER
        )
        self.url_field.grid(
            column=1,
            row=(self.row + 3)
        )

        self.username_value = StringVar()
        self.username_value.set(array[self.row].username)
        self.username_field = Entry(
            self,
            textvariable=self.username_value,
            fg="black",
            bg="white",
            bd=0,
            state="readonly",
            font=("Helvetica", 12),
            justify=CENTER
        )
        self.username_field.grid(
            column=2,
            row=(self.row + 3)
        )

        self.password_value = StringVar()
        self.password_value.set(array[self.row].password)
        self.password_field = Entry(
            self,
            textvariable=self.password_value,
            fg="black", bg="white", bd=0, state="readonly", font=("Helvetica", 12),
            justify=CENTER,
            show="*"
        )
        self.password_field.grid(
            column=3,
            row=(self.row + 3)
        )

        self.note_text = StringVar()
        self.note_text.set(array[self.row].notes)

        self.showpassword_button = Button(
            self,
            text="Show/Hide Password",
            command=self.showpassword
        )
        self.showpassword_button.grid(
            column=4,
            row=(self.row + 3),
            pady=10
        )

        self.shownote_button = Button(
            self,
            text="View Note",
            command=self.shownote
        )
        self.shownote_button.grid(
            column=5,
            row=(self.row + 3),
            pady=10
        )

        self.delete_button = Button(
            self,
            text="Delete",
            command=partial(self.root.controller.deleteentry, array[self.row].id)
        )
        self.delete_button.grid(
            column=6,
            row=(self.row + 3),
            pady=10
        )

    def showpassword(self):
        if self.password_field["show"] == "":
            self.password_field["show"] = "*"
        else:
            self.password_field["show"] = ""

    def shownote(self):
        notes = self.note_text.get()[2:-1]
        lines = notes.split("\\n")
        messagebox.showinfo("Note", "\n".join(lines))


class PasswordVaultFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.root = controller
        self.add_entry_button = Button(
            self, text="Add Entry",
            command=lambda: controller.show_frame(EntryFrame) # self.controller.ui.entry_window.start
        )
        self.add_entry_button.grid(column=1, pady=20)

        self.search_button = Button(
            self,
            text="Search",
            command=self.searchString # self.controller.search
        )
        self.search_button.grid(row=0, column=2)

        self.search_field = Entry(self)
        self.search_field.grid(row=0, column=3)

        self.lock_button = Button(
            self,
            text="Lock Vault",
            bg="red",
            command=self.lock # self.controller.ui.login_window.start
        )
        self.lock_button.grid(row=0)

        self.refresh = Button(
            self,
            text="Refresh All Entries",
            bg="green",
            fg="white",
            command=self.refresh # self.controller.refreshall
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

        self.blocks = {}
        self.notes = {}

        if self.root.controller.entryman.entries is not None:
            for i in range(len(self.root.controller.entryman.entries)):
                # print(self.root.controller.entryman.entries,i)
                # UserEntry(self.parent, self.root, self.root.controller.entryman.entries, i)


                id = self.root.controller.entryman.entries[i].id
                name = StringVar()
                name.set(self.root.controller.entryman.entries[i].name)
                url = StringVar()
                url.set(self.root.controller.entryman.entries[i].url)
                username = StringVar()
                username.set(self.root.controller.entryman.entries[i].username)
                password = StringVar()
                password.set(self.root.controller.entryman.entries[i].password)
                notes = StringVar()
                notes.set(self.root.controller.entryman.entries[i].notes)
                self.notes[id] = notes

                entryblock = {}

                Entry(self, state="readonly", textvariable=name).grid(row=i+4, column=0)
                Entry(self, state="readonly", textvariable=url).grid(row=i+4, column=1)
                Entry(self, state="readonly", textvariable=username).grid(row=i+4, column=2)
                Entry(self, show='', state="readonly", textvariable=password).grid(row=i+4, column=3)
                # entryblock["blockshowhide"] = Button(self, text="Show/Hide Password", command=partial(self.showpassword, id)).grid(column=4, row=(i+4), pady=10)
                Button(self, text="Show Note", command=partial(self.shownote, id)).grid(column=5, row=(i+4), pady=10)
                Button(self, text="Delete", command=partial(self.remove, id)).grid(column=6, row=(i+4), pady=10)

                self.blocks[id] = entryblock

            print(self.blocks)
        else:
            print("yow")

    def searchString(self):
        txt = self.search_field.get()
        self.root.controller.search(txt)
        # self.root.show_frame(PasswordVaultFrame)
        self.root.reloadvault()


    def refresh(self):
        self.root.controller.refreshall()
        self.root.reloadvault()

    def lock(self):
        self.root.frames[LoginFrame].master_password_text.delete(0, 'end')
        self.root.show_frame(LoginFrame)

    def remove(self, ID):
        self.root.controller.deleteentry(ID)
        self.root.reloadvault()


    # def showpassword(self, id):
    #     print(id)
    #     if self.blocks[id]["blockpwd"]["show"] == "":
    #         self.blocks[id]["blockpwd"]["show"] = "*"
    #     else:
    #         self.blocks[id]["blockpwd"]["show"] = ""
        # if self.pwd["show"] == "":
        #     self.pwd["show"] = "*"
        # else:
        #     self.pwd["show"] = ""

    def shownote(self, id):
        notes = self.notes[id].get()[2:-1]
        lines = notes.split("\\n")
        messagebox.showinfo("Note", "\n".join(lines))
        # txt = "\n".join(lines)
        # simpledialog.askstring(title="Your Notes", prompt="", initialvalue=txt)

# app = PPMWindow()
# app.mainloop()