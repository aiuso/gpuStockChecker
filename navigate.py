from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dotenv import load_dotenv
import global_vars as g
import os


load_dotenv()


##### Browser Navigation

def search(url):
    g.driver.get(url)


def open_browser():
    g.options = Options()
    g.options.binary_location = os.getenv('binary_path')  # chrome binary path
    g.options.add_experimental_option("excludeSwitches", ["enable-automation"])
    g.options.add_experimental_option('useAutomationExtension', False)
    g.driver = webdriver.Chrome(options=g.options)  # if in path, no need to specify

