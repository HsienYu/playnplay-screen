from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import pythoncom
import win32com.client
import random
import time
import json
import os
import threading
import fitz
from pythonosc import udp_client
import argparse

#s=Service(ChromeDriverManager().install())

state = 0

app = Flask(__name__)

path_dirs = os.path.dirname(__file__) + "/pdfs"

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)



def getRandomFile(path):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(path)
  index = random.randrange(0, len(files))
  file_path = path + '/' + files[index]
  return file_path



def printpdf():
        global state
        try:
            state = 1
            options = Options()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome("chromedriver.exe",options=options)
            print(driver.session_id)
            scriptFile = getRandomFile(path_dirs)
            driver.get(scriptFile)
            print(f"generate script file and print {scriptFile}")
            time.sleep(1)
            # driver.get(r"C:\Users\uglycat\Documents\playnplay-screen\2022-10-19 12_47_07.535848.pdf")
            driver.execute_script('window.print();')
            time.sleep(1) #Adjust as necessary
            shell = win32com.client.Dispatch("WScript.Shell", pythoncom.CoInitialize())
            try:
                shell.SendKeys('^p')
                time.sleep(1) #Adjust as necessary
                shell.SendKeys('{ENTER}') #dismiss the print dialog box
            except pythoncom.com_error as details:
                pass
            time.sleep(25) #Adjust as necessary
            driver.quit()
            state = 0
        except Exception as e:
            print(e)
            driver.quit()
            state = 0


    
def readPDF():
    with fitz.open(getRandomFile(path_dirs)) as doc:
        for page in doc:
            text = page.get_text()
            #time.sleep(5)
            print(text)

def sendOSC():
    client.send_message("/sound", 1)
    time.sleep(1)


@app.route('/print')
def hello():
    # os.system('sudo python esc_printer.py')
    try:
        global state
        print (state)
        if state == 1:
            dump = {
                "status": "print is running"
            }
            return dump
        else:

            thread = threading.Thread(target=printpdf)
            thread.start()
            threadRead = threading.Thread(target=readPDF)
            threadRead.start()
            #threadOSC = threading.Thread(target=sendOSC)
            #threadOSC.start()
            dump = {
                "status": "success"
            }
            return dump
    except:
        dump = {
            "status": "failed"
        }
        return dump

@app.route('/read')
def readText():
    try:
        threadRead = threading.Thread(target=readPDF)
        threadRead.start()
        dump = {
            "status": "read success"
        }
        return dump
    except:
        dump = {
            "status": "reading failed"
        }
        return dump

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8090, debug = False)
    # printpdf()
    