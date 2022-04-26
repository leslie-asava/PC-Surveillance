import sys
import time
from datetime import datetime as dt
import os
import ctypes


# THIS SCRIPT NEED TO BE RUN AS ADMIN

# *****************************************
#       Administrator Check function
# *****************************************
def checkAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

# *****************************************
#           ADD WEBSITE FUNCTION
# *****************************************
def addWebsite ():
    while True:
        site = input("Input a Website:")
        if site[-4:] != ".com":
            print("please enter  a correct website!")
        else:
            break
            # If You Didn't Add www. This Is Add www.
    if "www" not in site:
        site = "www." + site
        # check if the input is in list, if not then add it to the list

    for x in websites_list:
        if site in websites_list:
            print("this website is already in list")
            break
    else:
        print("this website is not in list")
        with open("block list.txt", "a+") as sitefile:
            # Move read cursor to the start of file.
            sitefile.seek(0)
            # If file is not empty then append '\n'
            data = sitefile.read(100)
            if len(data) > 0:
                sitefile.write("\n")
            # Append text at the end of file
            sitefile.write(site)

        print(websites_list)
        print("the website is now in block list")

# *****************************************
#           FILTER WEBSITE FUNCTION
# *****************************************

def filterWebsite(startTime, endTime):
    # the start time and end time for the block
    if checkAdmin() == True:
        while True:
            # check if the current time is within the blocking hours
            if dt(dt.now().year, dt.now().month, dt.now().day, startTime) < dt.now() < dt(dt.now().year, dt.now().month,
                                                                                          dt.now().day, endTime):
                print("blocking hours")
                with open(hosts_path, 'r+') as file:
                    content = file.read()
                    for website in websites_list:
                        if website in content:
                            pass
                        else:
                            # mapping hostnames to the localhost IP address so that the websites will be blocked
                            file.write(redirect + " " + website + "\n")

            else:
                print("unblock websites")
                # this will remove the websites from the host file which will unblock them
                with open(hosts_path, 'r+') as file:
                    content = file.readlines()
                    # start reading the file from the start
                    file.seek(0)
                    for line in content:
                        if not any(website in line for website in websites_list):
                            file.write(line)
                    # removing the websites from host file
                    file.truncate()
                print("websites are unblocked now! enjoy")
            time.sleep(10)

    elif checkAdmin() == False:
        print("This Script Only Run Adminstrartor ! Please Run Adminstartor")
    #  input("Press Any Key To Exit...........")


# *****************************************
#           MAIN BODY OF CODE
# *****************************************


# Hosts path for Windows
hosts_path = "C:\Windows\System32\drivers\etc\hosts"
# localhost's IP
redirect = "127.0.0.1"


with open("block list.txt", "r") as website_file:
    websites_list = [line.rstrip() for line in website_file]
    #print(websites_list)

#choice = input("choose 1 to enter website \nchoose 2 to enable blocking")

# ---- adding websites to the list ------
#if choice == "1":
#    addWebsite()

# ---- ENABLE FILTER WEBSITE ------

# THIS WILL BE INPUT BY USER TO SPECIFY THE START AND END TIME FOR THE BLOCKING
#startTime = 0
#endTime = 2

#if choice == "2":
#    filterWebsite()
