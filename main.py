import sys, json, base64, os
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./ui/main.ui", self)
        self.pushAccount.clicked.connect(lambda: self.goToScreen())
        self.pushIndonesia.clicked.connect(lambda: self.Indonesia('809'))
        self.pushEnglish.clicked.connect(lambda: self.Other('817'))
        self.pushEconomy.clicked.connect(lambda: self.Other('885'))
        self.pushPKWU.clicked.connect(lambda: self.Other('569'))
        self.pushPhysics.clicked.connect(lambda: self.Other('833'))
        self.pushMath1.clicked.connect(lambda: self.Other('970'))
        self.pushMath1.clicked.connect(lambda: self.Other('571'))
        self.pushPAI.clicked.connect(lambda: self.Other('1445'))
        self.pushHistory.clicked.connect(lambda: self.Other('593'))
        self.pushArt.clicked.connect(lambda: self.Other('593'))
        
    def goToScreen(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def Indonesia(self, id):
        self.goToBrowser(id)
        self.goToBrowser(id)
        self.progress_done(id)

    def Other(self, id):
        self.goToBrowser(id)
        self.progress_done(id)
        
    def goToBrowser(self, id):
        with open('login.json', 'r') as f:
            data = json.load(f)
            self.username = data['Username']
            password = base64.b64decode(data['Password'].encode("ascii")).decode("ascii")
            self.password = base64.b64decode(password).decode("ascii")
            
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
        
        driver.get(f'https://belajar.smansa-batam.sch.id/mod/attendance/view.php?id={id}')
        try:
            driver.find_element(By.PARTIAL_LINK_TEXT, "Submit attendance").click()
            try:
                driver.find_element(By.XPATH, '//*[@id="fgroup_id_statusarray"]/div[2]/fieldset/div/label[1]/span').click()
                driver.find_element(By.ID, 'id_submitbutton').click()
            except:
                pass
        except:
            pass
        
        driver.quit()
    
    def progress_done(self, id):
        popUp = QMessageBox()
        popUp.setText(f"Done submitting attendance on {id}")
        popUp.setIcon(QMessageBox.Information)
        popUp.setWindowTitle("Progress")
        popUp.exec()
    
class AccountWindow(QMainWindow):
    def __init__(self):
        super(AccountWindow, self).__init__()
        loadUi("./ui/account.ui", self)
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushSave.clicked.connect(lambda: self.goToScreen())
    
    def goToScreen(self):
        username = self.inputUsername.text()
        password = self.inputPassword.text()
        self.savePassword(username, password)
        widget.setCurrentIndex(widget.currentIndex()-1)
    
    def savePassword(self, username, password):
        password = base64.b64encode(password.encode("ascii")).decode("ascii")
        password = base64.b64encode(password.encode("ascii")).decode("ascii")
        if (username!='') and (password!=''):
            with open('login.json', 'w') as f:
                json.dump({'Username': username, 'Password': password}, f, ensure_ascii=False, indent=4)


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
    widget.addWidget(AccountWindow())
    widget.show()
    sys.exit(app.exec_())
    