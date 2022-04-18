from config import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

def key_checker(keys, valid_file, no_valid_file, counter, our_len):
    driver = webdriver.Firefox(executable_path = r"./geckodriver")
    driver.get("https://redeem.microsoft.com/")

    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "i0116"))).send_keys(login)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "KmsiCheckboxField"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "wb_auto_blend_container")))

    counter = 0
    for key in keys:
        counter += 1
        input_key = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "tokenString")))
        input_key.send_keys(key)
        time.sleep(0.3)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'cli_inlineErrorMessage')))
            out = "no valid"
            #out = driver.find_element(By.CLASS_NAME,'cli_inlineErrorMessage').text
        except:
            out = "valid"
        if out == "valid":
            valid_file.write("{}/n".formatkey)
        else:
            no_valid_file.write(key)
        if counter % num_keys_to_out == 0  or counter == len(keys):
            print("{} / {} ".format(counter, len(keys)))
        input_key.clear()
    driver.close() 
