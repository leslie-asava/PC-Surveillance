from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service



s=Service('./chromedriver')
chrome_options = ChromeOptions()
chrome_options.add_extension('adblock.crx')
driver = webdriver.Chrome(service=s,options=chrome_options )
driver.get('https://www.google.co')

