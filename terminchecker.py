import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
from playsound import playsound


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued")
    page.locator("[id=\"\\33 87843\"]").get_by_role("button", name="+").click()
    page.get_by_role("button", name="Weiter zur Terminauswahl").click()
    page.get_by_text("Es sind keine Termine für die").click()
    
    content = page.content()
    text = "Es sind keine Termine für die"
    
    global appointmentAvailable
    c = 0
    words = content.split()


    for i in range(len(words)):
        word = words[i]
        
        if 'Es' in word and 'sind' in words[i+1]:
            #print(word)
            #print(words[i+1])
            c = c + 1

    

    if c == 2:
        appointmentAvailable = False
    else: 
        appointmentAvailable = True
    

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    while(True):
        run(playwright)
        if appointmentAvailable:
            print('Appointment available')
            playsound('ding.wav')
        else:
            print('Appointment not available')
        time.sleep(5)

