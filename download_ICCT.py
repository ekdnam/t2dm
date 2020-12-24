# getting the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import glob
import os
import sys

# pymongo to access mongodb
import pymongo
from pymongo import MongoClient

# selenium webdriver
import selenium
from selenium import webdriver


__DATABASE__ = "t2dm"
__COLLECTION__ = "allData"
__SLEEPTIME__ = 30
__FOLDERNAME__ = "insulin_cardiovascular_clinical_trial"
# init mongo connection
mongoClient = MongoClient("mongodb://localhost:27017/")
db = mongoClient[__DATABASE__]
col = db[__COLLECTION__]

# run mongo queries
query = col.find(
    {"insulin": 1, "cardiovascular": 1, "clinical_trial": 1, "is_downloaded": 0}
)
pmids = []

# get pmid from result of query
for data in query:
    pmids.append(data["pmid"])

# as pmids are in float format, convert them to int
pmids = [int(x) for x in pmids]

# init chrome options. this is to ensure that files are downloaded automatically,
# and are downloaded in the '\temp' directory
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": r"E:\Repos\GitHub\source\t2dm\temp",
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)

# init the chrome driver
driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe", chrome_options=options)

print("Please turn: chrome://settings/content/pdfDocuments?search=pdf to on")

driver.get("chrome://settings/content/pdfDocuments?search=pdf")
time.sleep(20)

# the main function that downloads the pdfs
def download(pmids):
    print(f"Total files are: {len(pmids)}")
    i = 1

    for pmid in pmids:
        try:
            print(f"Iteration {i}\nPMID: {pmid}. Remaining: {len(pmids) - i}")
            i += 1
            # go to link
            print("\nAccessing link.")
            driver.get("https://sci-hub.se/")
            search_box = driver.find_element_by_name("request")

            # send pmid to selenium browser
            # print("Sending keys.")
            search_box.send_keys(str(pmid))
            driver.execute_script(
                """
                var elem = arguments[0];
                var value = arguments[1]
                elem.value = value;
            """,
                search_box,
                str(pmid),
            )
            # print("Executing script.")
            value = driver.execute_script("return arguments[0].value", search_box)

            # check whether values are correct
            # print(f"value returned: {value}")
            # print("pmid: " + str(pmid))
            # print("check whether values match")
            if int(pmid) == int(value):
                print("PMID and entered value match.")
            else:
                break

            # click submit form
            print("\nAccessing PDF.")
            driver.execute_script("javascript:document.forms[0].submit()")

            # access pdf download buutons
            # print("accessing pdf download buttons")
            print("Downloading PDF.")
            element = driver.find_element_by_xpath("//div[@id='article']/iframe")
            print(element.get_attribute("src"))

            # download pdf

            driver.get(str(element.get_attribute("src")))

            print("Downloading PDF")
            time.sleep(20)

            # get_pdfs
            pdf_files = get_pdfs()

            # check whether size is 1
            if len(pdf_files) != 1:
                print("Cannot rename file, exiting")
                driver.quit()
                sys.exit()
                break

            # rename files
            rename_files(pdf_files[0], str(pmid), __FOLDERNAME__)
            print(f"{pdf_files[0]} renamed to {str(pmid)}.pdf")

            # update equivalent document in mongodb
            print("Updating MongoDB")
            update(pmid)

            print("Sleeping")

            time.sleep(__SLEEPTIME__)
        except KeyboardInterrupt:
            # update_not_downloaded(pmid)
            # continue
            print("exiting")
            break
        except:
            download_error(pmid)
            continue


def get_pdfs():
    path = "E:/Repos/GitHub/source/t2dm/temp"
    pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
    return pdf_files


def rename_files(src: str, dst: str, folder_name: str):
    filepath = f"temp/{src}"
    filepath = filepath.replace("/", "\\")
    cwd = os.getcwd()
    old_path = os.path.join(cwd, filepath)
    #     newfilepath = f"papers/{folder_name}/{dst}.pdf"
    newfilepath = f"papers/{folder_name}/"
    newfilepath = newfilepath.replace("/", "\\")
    new_path = os.path.join(cwd, newfilepath)
    print("Old path " + old_path)
    print(newfilepath)
    if os.path.exists(old_path):
        os.rename(old_path, new_path + dst + ".pdf")
    else:
        print("File does not exist")


def update(pmid: int):
    myquery = {"pmid": pmid}
    newvalues = {"$set": {"is_downloaded": 1}}
    col.update_one(myquery, newvalues)


def download_error(pmid: int):
    myquery = {"pmid": pmid}
    newvalues = {"$set": {"download_error": 1}}
    col.update_one(myquery, newvalues)


def get_actual_filename(name):
    dirs = name.split("\\")
    # disk letter
    test_name = [dirs[0].upper()]
    for d in dirs[1:]:
        test_name += ["%s[%s]" % (d[:-1], d[-1])]
    res = glob.glob("\\".join(test_name))
    if not res:
        # File not found
        return None
    return res[0]


download(pmids)
