import sys, json, time, os, threading
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class browserThread(threading.Thread):
    def __init__(self, type, id):
        threading.Thread.__init__(self)
        self.type = type
        self.id = id
        with open('login.json', 'r') as f:
            data = json.load(f)
            self.username = data['Username']
            self.password = data['Password']
        
    def run(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")

        path = Service('./driver/chromedriver.exe')
        driver = webdriver.Chrome(service=path, options=options)
        driver.get("https://belajar.smansa-batam.sch.id/login/index.php")
        
        input_user = driver.find_element(By.ID, 'username')
        input_pass = driver.find_element(By.ID, 'password')
        input_user.send_keys(self.username)
        input_pass.send_keys(self.password)
        driver.find_element(By.ID, 'loginbtn').click()
        
        popUp = QMessageBox()
        popUp.setIcon(QMessageBox.Information)
        popUp.setWindowTitle("Task Done!")
            
        if self.type == 1:
            popUp.setText(f"Submitted attendance on {id}")
            driver.get(f'https://belajar.smansa-batam.sch.id/mod/attendance/view.php?id={self.id}')
            try:
                driver.find_element(By.PARTIAL_LINK_TEXT, "Submit attendance").click()
                try:
                    while True:
                        driver.find_element(By.XPATH, '//*[@id="fgroup_id_statusarray"]/div[2]/fieldset/div/label[1]/span').click()
                        driver.find_element(By.ID, 'id_submitbutton').click()
                except:
                    pass
            except:
                pass
            
        elif self.type == 2:
            popUp.setText(f"Done farming experience points on {id}")
            driver.get(f'https://belajar.smansa-batam.sch.id/course/view.php?id={self.id}')
            links, linkz = driver.find_elements(By.TAG_NAME, 'a'), []
            for link in links:
                link = link.get_attribute("href")
                items = ['attendance', 'googlemeet', 'url', 'page', 'assign', 'forum']
                for item in items:
                    if link.find(item) != -1:
                        linkz.append(link)
            for x in linkz:
                driver.get(x)
                
        driver.quit()
        popUp.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./ui/main.ui", self)
        self.pushAttendance.clicked.connect(lambda: widget.setCurrentIndex(1))
        self.pushAccount.clicked.connect(lambda: widget.setCurrentIndex(2))
        self.pushFarming.clicked.connect(lambda: widget.setCurrentIndex(3))


class AttendanceWindow(QMainWindow):
    def __init__(self):
        super(AttendanceWindow, self).__init__()
        loadUi("./ui/attendance.ui", self)
        self.pushBack.clicked.connect(lambda: widget.setCurrentIndex(0))
        self.pushIndonesia.clicked.connect(lambda: browserThread(1, 809).start())
        self.pushEnglish.clicked.connect(lambda: browserThread(1, 817).start())
        self.pushEconomy.clicked.connect(lambda: browserThread(1, 885).start())
        self.pushPKWU.clicked.connect(lambda: browserThread(1, 569).start())
        self.pushPhysics.clicked.connect(lambda: browserThread(1, 833).start())
        self.pushMath1.clicked.connect(lambda: browserThread(1, 970).start())
        self.pushMath2.clicked.connect(lambda: browserThread(1, 571).start())
        self.pushPAI.clicked.connect(lambda: browserThread(1, 1445).start())
        self.pushHistory.clicked.connect(lambda: browserThread(1, 593).start())
        self.pushArt.clicked.connect(lambda: browserThread(1, 598).start())


class AccountWindow(QMainWindow):
    def __init__(self):
        super(AccountWindow, self).__init__()
        loadUi("./ui/account.ui", self)
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushSave.clicked.connect(lambda: self.goToScreen())

    def goToScreen(self):
        username = self.inputUsername.text()
        password = self.inputPassword.text()
        if (username!='') and (password!=''):
            with open('login.json', 'w') as f:
                json.dump({'Username': username, 'Password': password}, f, ensure_ascii=False, indent=4)
        widget.setCurrentIndex(0)


class FarmingWindow(QMainWindow):
    def __init__(self):
        super(FarmingWindow, self).__init__()
        loadUi("./ui/farming.ui", self)
        self.pushBack.clicked.connect(lambda: widget.setCurrentIndex(0))
        self.pushIndonesia.clicked.connect(lambda: browserThread(2, 23).start())
        self.pushEnglish.clicked.connect(lambda: browserThread(2, 26).start())
        self.pushEconomy.clicked.connect(lambda: browserThread(2, 90).start())
        self.pushPKWU.clicked.connect(lambda: browserThread(2, 77).start())
        self.pushPhysics.clicked.connect(lambda: browserThread(2, 44).start())
        self.pushMath1.clicked.connect(lambda: browserThread(2, 34).start())
        self.pushMath2.clicked.connect(lambda: browserThread(2, 38).start())
        self.pushPAI.clicked.connect(lambda: browserThread(2, 10).start())
        self.pushHistory.clicked.connect(lambda: browserThread(2, 57).start())
        self.pushArt.clicked.connect(lambda: browserThread(2, 84).start())


if __name__ == '__main__':
    if os.path.isfile('login.json') == False:
        with open('login.json', 'w') as f:
            json.dump({'Username': 'None', 'Password': 'None'}, f, ensure_ascii=False, indent=4)

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle("Attendance")
    widget.setMinimumSize(QSize(320, 240))
    widget.setMaximumSize(QSize(320, 240))

    icon = QIcon()
    icon.addFile(u"./images/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
    icon.addFile(u"./images/icon.ico", QSize(), QIcon.Selected, QIcon.On)
    widget.setWindowIcon(icon)

    widget.addWidget(MainWindow())
    widget.addWidget(AttendanceWindow())
    widget.addWidget(AccountWindow())
    widget.addWidget(FarmingWindow())
    widget.show()
    sys.exit(app.exec_())