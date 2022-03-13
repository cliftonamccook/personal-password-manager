from UI.window import PPMWindow, PasswordVaultWindow, LoginWindow, InitialWindow
from Controller.controller import Controller

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