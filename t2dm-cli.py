import argparse
import os
import sys
import time

import selenium
from selenium import webdriver

__CHROMEDRIVERPATH__ = r"C:/chromedriver/chromedriver.exe"
__DEFAULTPMID__ = 30694322
__SLEEPTIME__ = 50

parser = argparse.ArgumentParser(description="Download single paper with PMID")

# get PMID
parser.add_argument(
    "--PMID",
    type=int,
    default=__DEFAULTPMID__,
    help="PMID of the paper to be downloaded",
)
# get folder_name
parser.add_argument(
    "--folder_name",
    type=str,
    default="temp",
    help="The folder name where the paper would be saved",
)
# get arguments
opt = parser.parse_args()
# access individual elements
global folder_name
folder_name = opt.folder_name

global PMID
PMID = opt.PMID


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


# initialize options
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": r"E:\Repos\GitHub\source\t2dm\temp",
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)

# create object of webdriver
global driver
driver = webdriver.Chrome(__CHROMEDRIVERPATH__, chrome_options=options)

# warning msg. turning this on will auto download PDFs. No prompt required.
print(
    "Auto-download PDF option. Not turning this on will result in the PDFs not being downloaded\n\nchrome://settings/content/pdfDocuments?search=pdf\n\n"
)
driver.get("chrome://settings/content/pdfDocuments?search=pdf")
time.sleep(15)
# access link subroutine

driver.get("https://sci-hub.se/")
# get search box
search_box = driver.find_element_by_name("request")

# send pmid to selenium browser
print("Sending keys.")
search_box.send_keys(str(PMID))
driver.execute_script(
    """
    var elem = arguments[0];
    var value = arguments[1]
    elem.value = value;
""",
    search_box,
    str(PMID),
)
# submit form. go to pdf page
driver.execute_script("javascript:document.forms[0].submit()")
# accessing pdf download buttons
element = driver.find_element_by_xpath("//div[@id='article']/iframe")
print(element.get_attribute("src"))
# download pdf
driver.get(str(element.get_attribute("src")))
print("Sleeping for download to get completed")
time.sleep(20)

pdf_files = get_pdfs()

if len(pdf_files) != 1:
    print("Cannot rename file, exiting")
    driver.close()
    sys.exit()

# rename files
rename_files(pdf_files[0], str(PMID), folder_name)
print(f"{pdf_files[0]} renamed to {str(PMID)}.pdf")

driver.close()
