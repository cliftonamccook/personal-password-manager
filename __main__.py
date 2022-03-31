from Controller.controller import Controller
from UI.window import PPMWindow


def main():
    controller = Controller()
    app = PPMWindow(controller)
    app.start()
    app.mainloop()
    

if __name__ == '__main__':
    main()
