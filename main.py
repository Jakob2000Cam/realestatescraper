from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime


PATH = "/usr/bin/chromedriver"
driver = webdriver.Chrome(PATH)

num_pages = 43

addresses = []
communes = []
prices = []
bedrooms = []
bedroom_bool = False
bathrooms = []
bathroom_bool = False
living_spaces = []
living_space_bool = False
land_areas = []
land_area_bool = False
dates_available = []
date_available_bool = False



for p in range(num_pages):

    driver.get("https://www.immoweb.be/en/search/house/for-sale/brussels/province?countries=BE&page=" + str(p+1) + "&orderBy=relevance")

    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="uc-btn-accept-banner"]'))).click()

    except:
        pass

    for counter in range(30):
        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card__title-link"))
            )

        except:
            print("error")
            driver.quit()
        try:
            elements[counter].click()
            address = driver.find_elements_by_class_name("classified__information--address-row")
            price = driver.find_element_by_class_name("classified__price")
            info = driver.find_elements_by_class_name("overview__text")


            if len(address) == 2:
                if address[0].text != "":
                    addresses.append(address[0].text)
                else:
                    addresses.append(0)

                if address[1].text != "":
                    communes.append(address[1].text)
                else:
                    communes.append(0)
            else:
                if address[0].text != "":
                    communes.append(address[0].text)
                else:
                    communes.append(0)

                addresses.append(0)

            prices.append(price.text)

            for entry in info:

                if "bedroom" in entry.text:
                    bedrooms.append(entry.text)
                    bedroom_bool = True

                if ("livable" in entry.text or "m²" in entry.text) and "land" not in entry.text:
                    living_spaces.append(entry.text)
                    living_space_bool = True

                if "land" in entry.text:
                    land_areas.append(entry.text)
                    land_area_bool = True

                if "bathroom" in entry.text:
                    bathrooms.append(entry.text)
                    bathroom_bool = True

                if "date" in entry.text:
                    dates_available.append(entry.text)
                    date_available_bool = True



            if not bedroom_bool:
                bedrooms.append(0)
            if not living_space_bool:
                living_spaces.append(0)
            if not land_area_bool:
                land_areas.append(0)
            if not bathroom_bool:
                bathrooms.append(0)
            if not date_available_bool:
                dates_available.append(0)

            bedroom_bool = False
            living_space_bool = False
            land_area_bool = False
            bathroom_bool = False
            date_available_bool = False


            #print(info[0].text, info[1].text, info[2].text, len(info))
            print("Finished item " + str(counter))
            driver.back()

        except:
            print("error2")
            driver.quit()

    print("Finished page " + str(p))

print(len(addresses), len(communes),len(prices), len(bedrooms), len(bathrooms), len(living_spaces), len(land_areas),len(dates_available))

d = {"Address":addresses,"Commune":communes, "Price": prices, "Bedrooms":bedrooms, "Bathrooms":bathrooms, "Living Space":living_spaces, "Land Area": land_areas, "Date Available": dates_available}
all_real_estate = pd.DataFrame(data=d)
all_real_estate.to_excel(str("RealEstate"+str(datetime.date.today)+".xlsx"))

print(all_real_estate.head())

driver.close()
