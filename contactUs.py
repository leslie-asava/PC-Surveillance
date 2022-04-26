import win32com.client as win32


def send_email(name, email, content):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    mail.To = "ICU.help3.com"
    mail.Subject = 'Contact us feedback'
    mail.HTMLBody = '<h2>This email is from :' + name + '<h2>\n <h2> email: ' + email + '<h2>\n has sent the following message: \n <h2>' + content + '<h2>'

    mail.Send()
    print("email has been sent")