from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import sys

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver=webdriver.Chrome(options=chrome_options)

driver.get(
    "https://search.earth911.com/"
)

try:
    search_cat=driver.find_element(By.NAME,value="what")
    search_cat.send_keys("Electronics")
except Exception as e:
    print("Error searching the category. ")
    sys.exit(1)

try:
    zipcode=driver.find_element(By.NAME,value="where")
    zipcode.send_keys("10001")
except Exception as e:
    print("Error searching the Zipcode. ")
    sys.exit(1)

try:
    search_button=driver.find_element(By.ID,value="submit-location-search")
    search_button.click()
except Exception as e:
    print("Error searching. ")
    sys.exit(1)

try:
    range=driver.find_element(By.XPATH,value='//*[@id="search-results"]/div[1]/div/label/select')
    range.click()

    range_input=driver.find_element(By.XPATH,value='//*[@id="search-results"]/div[1]/div/label/select/option[5]')
    range_input.click()
except Exception as e:
    print("Error in range.")
    sys.exit(1)

time.sleep(5)
try:
    close_popup=driver.find_element(By.CLASS_NAME,value='_close')
    close_popup.click()
except Exception as e:
    pass

try:
    listing_links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, ".result-item div.description h2.title a")]
except Exception as e:
    print("Listing links not found.")
    listing_links=[]

try:
    with open('data.csv',mode='w',newline='',encoding='utf-8-sig') as file:
        writer=csv.writer(file)
        writer.writerow(["Business_Name","last_update_date","street_address","materials_accepted"])

        for listing in listing_links[:5]:
            try:
                driver.get(listing)
                time.sleep(2)

                business_name = "N/A"
                formatted_date = "N/A"
                street_name = ""
                materials_acc = ""

                try:
                    business_name=driver.find_element(By.CLASS_NAME,value="back-to").text.split("-")[0]
                    print(business_name)
                except NoSuchElementException:
                    business_name="N/A"

                try:
                    last_date=driver.find_element(By.CLASS_NAME,value="last-verified").text
                    last_date=last_date.replace("Updated","").strip()
                    date_obj=datetime.strptime(last_date,"%b %d, %Y")
                    formatted_date=date_obj.strftime("%Y-%m-%d")
                except NoSuchElementException:
                    formatted_date="N/A"

                try:
                    addrs=driver.find_elements(By.CSS_SELECTOR,value=".contact .addr")
                    address_parts=[addr.text.strip() for addr in addrs]
                    if address_parts[0] == address_parts[1]:
                        street_name="N/A"
                    else:
                        if len(address_parts[0])==0:
                            street_name=address_parts[1]
                        elif len(address_parts[1])==0:
                            street_name=address_parts[0]
                        else:
                            street_name=", ".join(address_parts)
                except NoSuchElementException:
                    street_name="N/A"


                try:
                    materials=driver.find_elements(By.CLASS_NAME,value="material")

                    material_list=[material.text.strip() for material in materials]
                    materials_acc=", ".join(material_list)

                except NoSuchElementException:
                    materials_acc="N/A"

                try:
                    back = driver.find_element(By.LINK_TEXT, value="Back")
                    back.click()
                except NoSuchElementException:
                    driver.back()

                writer.writerow([business_name,formatted_date,street_name,materials_acc])

            except Exception as e:
                print("Error processing listing.")

except Exception as e:
    print("Error processing the data.")

print("Scraping completed successfully.")


