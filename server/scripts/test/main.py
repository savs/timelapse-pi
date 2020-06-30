from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from dailyProcess import runDailyProcess, previewToday


def menu():
    menu = ConsoleMenu("Timelapse Server Console")
    menu.append_item(FunctionItem("Process the past", runDailyProcess))
    menu.append_item(FunctionItem("Preview today", previewToday))
    menu.show()


menu()
