# import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
# from PySide2.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import sqlite3
import re
from HomePage import Ui_HomePage
from keylogging import *
from screenshot import *
from adblock import *
from filterWebsite import *
from contactUs import *

## Thread to run the screenshot function
class ScreenshotThread(QThread):

    done = pyqtSignal(int)
    usertime = None

    def __init__(self):
        super().__init__()

    def run(self):
        screenshot(self.usertime)

## Thread to run the keylogging function
class KeyloggingThread(QThread):

    done = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        keylogging()


## Thread to filter websites
class FilterWebsitesThread(QThread):

    done = pyqtSignal(int)
    startTime = None
    endTime = None

    def __init__(self):
        super().__init__()

    def run(self):
        startTime = int(self.startTime)
        endTime = int(self.endTime)

        filterWebsite(startTime,endTime)

## Thread to send email
class SendEmailThread(QThread):

    done = pyqtSignal(int)
    uname = None
    email = None
    content = None

    def __init__(self):
        super().__init__()

    def run(self):
        uname = self.uname
        email = self.email
        content = self.content

        send_email(uname, email, content)


class StartPage(QDialog):
    def __init__(self):
        super(StartPage, self).__init__()
        uic.loadUi('StartPage.ui', self)
        self.logo.setPixmap(QPixmap('ICU_logo_.png'))
        self.login.clicked.connect(self.gotologin)
        self.registerr.clicked.connect(self.gotoregister)

    @staticmethod
    def gotologin():
        widget.setCurrentIndex(1)

    @staticmethod
    def gotoregister():
        widget.setCurrentIndex(2)


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Login.ui', self)
        self.loginICON.setPixmap(QPixmap('loginn.png'))
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginFunction)
        self.createAcc.clicked.connect(self.showRegister)

    @staticmethod
    def showHomePage():
        widget.setCurrentIndex(3)

    @staticmethod
    def showRegister():
        widget.setCurrentIndex(2)

    def loginFunction(self):
        user = self.userNameField.text()
        password = self.passwordField.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("الرجاء تعبئة جميع الحقول")
        else:
            conn = sqlite3.connect("Accounts.db")
            cur = conn.cursor()
            query = 'SELECT Password FROM login WHERE Username =\'' + user + "\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in")
                self.showHomePage()

            else:
                self.error.setText("اسم المستخدم أو كلمة المرور غير صحيحة")


class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        uic.loadUi('Register.ui', self)
        self.regICON.setPixmap(QPixmap('signup.png'))
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registrr.clicked.connect(self.registerFunction)
        self.gotologin.clicked.connect(self.showLogin)

    @staticmethod
    def showLogin():
        widget.setCurrentIndex(1)

    def registerFunction(self):
        user = self.userNameField.text()
        Mobilenum = self.MobileNumField.text()
        email = self.emailField.text()
        password = self.passwordField.text()
        confirmPassword = self.confirmpasswordField.text()
        # regex = '^[A-Z a-z 0-9]+[\._]?[A-Z a-z 0-9]+[@]\w+[.]\w{2,3}$'

        if len(user) == 0 or len(Mobilenum) == 0 or len(password) == 0 or len(confirmPassword) == 0 or len(email) == 0:
            self.error.setText(" الرجاء تعبئة جميع الحقول")

        elif password != confirmPassword:
            self.error.setText(" كلمة المرور غير متطابقة ")

        # elif len(Mobilenum) != 10:
        #    self.error.setText(" يجب أن يكون رقم الجوال مكون من 10 أرقام ")

        # elif not re.fullmatch((regex, email)):
        #    self.error.setText(" الرجا التأكد من اللإيميل المدخل ")

        else:
            conn = sqlite3.connect("Accounts.db")
            cur = conn.cursor()

            if (len(password) < 8) or not re.search("[a-z]", password) or not re.search("[A-Z]", password) \
                    or not re.search("[0-9]", password):
                self.error.setText("  يجب أن يكون طول كلمة المرور 8 على الأقل "
                                   "\nوتحوي على حروف وأرقام(حرف واحد كبير ورقم على الأقل ")

            elif cur.execute('SELECT Password FROM login WHERE Username =\'' + user + "\'"):
                if cur.fetchone():
                    self.error.setText("اسم المستخدم مستخدم بالفعل!")
                else:
                    user_info = [user, Mobilenum, password, email]
                    cur.execute('INSERT INTO login (Username , MobileNumber, Password, Email) '
                                'VALUES  (?,?,?,?) ', user_info)
                    conn.commit()
                    conn.close()
                    self.error.setText("  تم التسجيل بنجاح  ")


def addWeb(self, val, site):
    print("enter to fun.2")
    value = val
    while True:
        if value == 1:
            break

        else:
            # If You Didn't Add www. This Is Add www.
            if "www" not in site:
                site = "www." + site
                # check if the input is in list, if not then add it to the list

            for x in websites_list:
                if site in websites_list:
                    self.ui.msg.setText("هذا الموقع موجود بالفعل في القائمة")
                    break
            else:
                # print("this website is not in list")
                with open("block list.txt", "a+") as sitefile:
                    # Move read cursor to the start of file.
                    sitefile.seek(0)
                    # If file is not empty then append '\n'
                    data = sitefile.read(100)
                    if len(data) > 0:
                        sitefile.write("\n")
                    # Append text at the end of file
                    sitefile.write(site)
                    # self.ui.msg.setText("the website is now in block list")
                    self.ui.msg.setText("تمت الإضافة بنجاح")
                    print("website Successfully added")
                    print(websites_list)
                    break

                #print(websites_list)
                #self.ui.msg.setText("Successfully")

    pass


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        self.ui.logoutIcon.setPixmap(QPixmap('logoutICON_.png'))
        self.ui.menuIcon.setPixmap(QPixmap('menu_.png'))
        self.ui.LogOut.clicked.connect(self.gotoStrtPage)

        ## Connect interface with Keylogging service ##
        self.ui.keylogging.clicked.connect(
            lambda: self.ui.body.setCurrentWidget(self.ui.Kpage)
        )
        self.ui.submitK.clicked.connect(self.gotoKeylogging)
        self.ui.openKlogFile.clicked.connect(openlogfile)

        ## Connect interface with Screenshot service ##
        self.ui.secreenshot.clicked.connect(
            lambda: self.ui.body.setCurrentWidget(self.ui.Spage)
        )
        self.ui.submitS.clicked.connect(self.gotoScreenshot)
        self.ui.openSlogFile.clicked.connect(useropenfile)

        ## Connect interface with Ad Block service ##
        self.ui.adBlock.clicked.connect(
            lambda: self.ui.body.setCurrentWidget(self.ui.Apage)
        )
        self.ui.openAfile.clicked.connect(open_folder)
        self.ui.Download.clicked.connect(open_file)

        ## Connect interface with FilterWebsite service ##
        self.ui.filterWeb.clicked.connect(
            lambda: self.ui.body.setCurrentWidget(self.ui.Fpage)
        )
        self.ui.submitF_2.clicked.connect(self.gotoAddWebsite)
        self.ui.submitF.clicked.connect(self.gotoFilterWebsite)

        ## Connect interface with Contact us service ##
        self.ui.contactUs.clicked.connect(
            lambda: self.ui.body.setCurrentWidget(self.ui.Cpage)
        )
        self.ui.send.clicked.connect(self.gotoSendEmail)


        ## Create threads
        self.screenshot_thread = ScreenshotThread()
        self.keylogging_thread = KeyloggingThread()
        self.filter_websites_thread = FilterWebsitesThread()
        self.send_email_thread = SendEmailThread()

    def gotoKeylogging(self):
        #while True:
        if self.ui.enableKservice.isChecked():
            print("keylogging fun")
            self.keylogging_thread.start()

    def gotoScreenshot(self):
        usertime = self.ui.time.text()
        #while True:
        if self.ui.enableSservice.isChecked():
            self.screenshot_thread.usertime = usertime
            self.screenshot_thread.start()

    def gotoAddWebsite(self):
        site = self.ui.BlackLitField.text()
        if site[-4:] != ".com":
            print("enter fun1 and if 1")
            self.ui.msg.setText("Please enter a valid website!")
            addWeb(self, 1, site)
        else:
            addWeb(self, 0, site)

    def gotoFilterWebsite(self):
        startTime = self.ui.StartTime.text()
        endTime = self.ui.EndTime.text()
        if self.ui.enableFservice.isChecked():
            if checkAdmin():
                self.filter_websites_thread.startTime = startTime
                self.filter_websites_thread.endTime = endTime
                self.filter_websites_thread.start()

            elif not checkAdmin():
                self.ui.checkAdmin.setText("This program runs only as an administrator! Please reboot and choose run as administrator")

    def gotoSendEmail(self):
        uname = self.ui.userNameField.text()
        email = self.ui.emailField.text()
        content = self.ui.commantField.text()

        self.send_email_thread.uname = uname
        self.send_email_thread.email = email
        self.send_email_thread.content = content

        self.send_email_thread.start()
        

    def gotoStrtPage(self):
        widget.setCurrentIndex(0)


# main
app = QApplication(sys.argv)
Start_page = StartPage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(Start_page)
widget.setCurrentIndex(3)
login = Login()
widget.addWidget(login)
widget.setCurrentIndex(2)
register = Register()
widget.addWidget(register)
widget.setCurrentIndex(1)
homePage = HomePage()
widget.addWidget(homePage)
widget.setCurrentIndex(0)
widget.setFixedHeight(600)
widget.setFixedWidth(750)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Exiting")
