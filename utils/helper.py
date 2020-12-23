import argparse
import os
import sys
import time

import selenium
from selenium import webdriver

import pymongo
from pymongo import MongoClient


class MyDriver:
    def __init__(self, folder_name, **kwargs):
        self.__CHROMEDRIVERPATH__ = r"C:/chromedriver/chromedriver.exe"
        self.__DEFAULTPMID__ = 30694322
        self.__SLEEPTIME__ = 50

        self.folder_name = folder_name
        self.options = webdriver.ChromeOptions()

        prefs = {
            "download.default_directory": r"E:\Repos\GitHub\source\t2dm\temp",
            "download.prompt_for_download": False,
        }

        self.options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(
            self.__CHROMEDRIVERPATH__, chrome_options=self.options
        )

    def prompt_for_pdfs(self):
        print(
            "Auto-download PDF option. Not turning this on will result in the PDFs not being downloaded\n\nchrome://settings/content/pdfDocuments?search=pdf\n\n"
        )
        self.driver.get("chrome://settings/content/pdfDocuments?search=pdf")
        time.sleep(15)

    # def get_pdfs(self):
    #     path = "E:/Repos/GitHub/source/t2dm/temp"
    #     pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
    #     return pdf_files

    def get_pdfs(self):
        path = "E:/Repos/GitHub/source/t2dm/temp"
        pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
        return pdf_files

    def rename_files(self, src: str, dst: str, folder_name: str):
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

    def download(self, pmids: list):
        print(f"Total files are: {len(pmids)}")
        i = 1
        for pmid in pmids:
            print(f"Iteration {i}\nPMID: {pmid}")
            i += 1
            # go to link
            print("Accessing link.")
            self.driver.get("https://sci-hub.se/")
            search_box = self.driver.find_element_by_name("request")

            # send pmid to selenium browser
            print("Sending keys.")
            search_box.send_keys(str(pmid))
            self.driver.execute_script(
                """
                var elem = arguments[0];
                var value = arguments[1]
                elem.value = value;
            """,
                search_box,
                str(pmid),
            )
            print("Executing script.")
            value = self.driver.execute_script("return arguments[0].value", search_box)

            # check whether values are correct
            # print(f"value returned: {value}")
            # print("pmid: " + str(pmid))
            # print("check whether values match")
            if int(pmid) == int(value):
                print("PMID and entered value match.")
            else:
                break

            # click submit form
            print("Accessing PDF.")
            self.driver.execute_script("javascript:document.forms[0].submit()")

            # access pdf download buutons
            # print("accessing pdf download buttons")
            print("Downloading PDF.")
            element = self.driver.find_element_by_xpath("//div[@id='article']/iframe")
            print(element.get_attribute("src"))

            # download pdf

            self.driver.get(str(element.get_attribute("src")))

            print("Sleeping for download to get completed")
            time.sleep(20)

            # get_pdfs
            pdf_files = self.get_pdfs()

            # check whether size is 1
            if len(pdf_files) != 1:
                print("Cannot rename file, exiting")
                break

            # rename files
            self.rename_files(pdf_files[0], str(pmid), "insulin_mortality_odds_ratio")
            print(f"{pdf_files[0]} renamed to {str(pmid)}.pdf")

            # update equivalent document in mongodb
            print("Updating MongoDB")
            update(pmid)

            print("Sleeping")

            time.sleep(__SLEEPTIME__)


class MongoDriver:
    def __init__(self):
        self.__DATABASE__ = "t2dm"
        self.__COLLECTION__ = "allData"

        self.mongoClient = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongoClient[self.__DATABASE__]
        self.col = self.mongoClient[self.__COLLECTION__]

    def query_pmids_IAEOsR(self):
        query = self.col.find(
            {"insulin": 1, "adverse_events": 1, "odds_ratio": 1, "is_downloaded": 0}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_ICCT(self):
        query = self.col.find(
            {"insulin": 1, "cardiovascular": 1, "clinical_trial": 1, "is_downloaded": 0}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_ICCTs(self):
        query = self.col.find(
            {
                "insulin": 1,
                "cardiovascular": 1,
                "clinical_trials": 1,
                "is_downloaded": 0,
            }
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_ICHR(self):
        query = self.col.find(
            {"insulin": 1, "cardiovascular": 1, "hazard_ratio": 1, "is_downloaded": 0}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_ICHsR(self):
        query = self.col.find(
            {"insulin": 1, "cardiovascular": 1, "hazards_ratio": 1, "is_downloaded": 0}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_ICOR(self):
        query = self.col.find(
            {"insulin": 1, "cardiovascular": 1, "odd_ratio": 1, "is_downloaded": 0}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IDCCT(self):
        query = self.col.find(
            {
                "insulin": 1,
                "diabetic_complications": 1,
                "clinical_trial": 1,
                "is_downloaded": 0,
            }
        )
        pmids = []
        for data in query:
            pmids.append(data["pmids"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IDCOR(self):
        query = self.col.find(
            {
                "insulin": 1,
                "diabetic_complications": 1,
                "odds_ratio": 1,
                "is_downloaded": 0,
            }
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IMCT(self):
        query = self.col.find(
            {"insulin": 1, "mortality": 1, "clinical_trial": 1, "is_downloaded": 1}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IMCTs(self):
        query = self.col.find(
            {"insulin": 1, "mortality": 1, "clinical_trials": 1, "is_downloaded": 1}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IMHR(self):
        query = self.col.find(
            {"insulin": 1, "mortality": 1, "hazard_ratio": 1, "is_downloaded": 1}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IMHsR(self):
        query = self.col.find(
            {"insulin": 1, "mortality": 1, "hazards_ratio": 1, "is_downloaded": 1}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids

    def query_pmids_IMOsR(self):
        query = self.col.find(
            {"insulin": 1, "mortality": 1, "odds_ratio": 1, "is_downloaded": 1}
        )
        pmids = []
        for data in query:
            pmids.append(data["pmid"])
        pmids = [int(x) for x in pmids]
        return pmids
