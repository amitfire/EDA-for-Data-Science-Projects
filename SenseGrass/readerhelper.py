import pdftables_api
from robot.api.deco import keyword
from robot.api import logger
import csv
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re
import easyimap
import requests
import os, wget,time
from bs4 import BeautifulSoup
from robot.libraries.BuiltIn import BuiltIn


class PdfHelper(object):
   
    @keyword('Extract Data from Email in readable form')
    def extract_from_email(self, path):
        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)
            break

        text = retstr.getvalue()
        filepath.close()
        device.close()
        retstr.close()
        elem = []
        elem2 = []
        mergedElem = []
        listOfDict = []
        elem4 = []
        # print text
        df = text.split("\n")
        # print df
        for ele in df[0:20:2]:
            elem4.append(ele.lower())
        #print ele
        rem_policy = [n for n in df[19:len(df)] if n != 'Policy']
        rem_Time = [n for n in rem_policy if n != 'Time']
        rem_space = [n for n in rem_Time if n != '']
        # print rem_space

        for i in range(0, len(rem_space), 3):
            elem2.append(rem_space[i:i + 3])
        # print elem2
        for i in range(0, len(elem2) / 2):
            a = elem2[i] + elem2[i + 7]
            mergedElem.append(a)
        # print mergedElem
        for elem in mergedElem:
            #  print len(elem)
            diction = {}
            if (len(elem) == 6):
                diction["Keyword"] = elem[0]
                diction["Category"] = elem[1]
                diction["User"] = elem[2]
                diction["Policy"] = elem[3]+" Policy"
                diction["Date"] = elem[4]
                diction["Time"] = elem[5]
                listOfDict.append(diction)

        return (listOfDict, elem4)

    @keyword('Extract Data From PDF in readable form')
    def extract_from_pdf(self, path, dict_decide):
        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)
            break

        text = retstr.getvalue()
        filepath.close()
        device.close()
        retstr.close()
        elem = []
        elem2 = []
        listOfDict = []
        elem4 = []
        lenStart = 0
        df = text.split("\n")
##        for ele in df[0:20:2]:
##            elem4.append(ele.lower())
##        # print ele
##        if dict_decide['userType'] == 'ou':
##            lenStart = 28
##        else:
##            lenStart = 26
##        for ele in df[lenStart:len(df):2]:
##            elem.append(ele)
##        # print elem
##        for i in range(0, len(elem), 6):
##            elem2.append(elem[i:i + 6])
##        for elem in elem2:
##            diction = {}
##            if (len(elem) == 6):
##                diction["Keyword"] = elem[0]
##                diction["Policy"] = elem[1]
##                diction["Date"] = elem[2]
##                diction["Category"] = elem[3]
##                diction["User"] = elem[4]
##                diction["Time"] = elem[5]
##                listOfDict.append(diction)
##        for i in range(len(listOfDict)):
##            print listOfDict[i]

        return (listOfDict, elem4)

    @keyword('Convert to CSV')
    def convert_to_csv(self, path):

        c = pdftables_api.Client('ibwnjyocbrcj')
        c.csv(str(path), 'Activity_Report_in_CSV')  # replace c.xlsx with c.csv to convert to CSV
        cwd = os.getcwd()
        filename = str(cwd + "/Activity_Report_in_CSV.csv")
        # df = pandas.read_csv(str(cwd +"/Activity_Report_in_CSV.csv"), delimiter=',')
        data = []
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)

        return data

    @keyword('Log Time')
    def pdf_to_text(self, path, timecomp):
        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)

        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        filepath.close()
        device.close()
        retstr.close()
        resp = self.check_log_time(text, timecomp)
        return resp

    @keyword('Process expected Data')
    def verify_email_body(self, soup):
        extracted_data_params = {}
        tables = soup.findChildren('table')
        my_table = tables[2]
        rows = my_table.findChildren(['tr'])
        for row in rows:
            # print row
            cells = row.find_all('td')
            for i in range(1, len(cells)):
                extracted_data_params[cells[0].text.strip()] = cells[1].text.strip()
        logger.console(extracted_data_params)
        return extracted_data_params
        # for i in range(len(expected_parms)):
        #     expected_data_params['Policy'] =

    @keyword('Email Verification')
    def connect_to_email(self, loginUser):
        if os.path.exists("pdf_email.pdf"):
            os.remove("pdf_email.pdf")
        else:
            logger.console("The file does not exist")
        image_url = ''
        login = str(loginUser)
        password = 'Demo123!'
        extracted_email = {}
        imapper = easyimap.connect('imap.gmail.com', login, password, mailbox='INBOX')
        imapper.change_mailbox('INBOX')
        logger.console("Email Connection established with User: " + login)
        time.sleep(5)
        for mail in imapper.unseen(limit=1):
            # mail = imapper.mail(mail_id)
            logger.console(mail.from_addr)
            logger.console(mail.title)
        if mail.title == "":
            logger.console("Subject:" + mail.title + "  ###############--FOUND EMAIL--##############\n")
            soup = BeautifulSoup(mail.body, 'html.parser')
            extracted_email = self.verify_email_body(soup)
            pdf_link = soup.find_all('a')[2]
            logger.console("Link for PDF from EMAIL:" + pdf_link['href'])
            image_url = pdf_link['href']

            if "amazonaws.com" in image_url:
                logger.console("Url for downlaoding pdf extracted from Email :" + image_url)
                results_path = BuiltIn().get_variable_value("${UserReportFilePath}")
                path = results_path + "\pdf_email.pdf"
                wget.download(image_url, path)
                # os.syst.em("curl  " + image_url + "> pdf_email.pdf")
                response = requests.get(image_url)
                with open('pdf_email.pdf', 'wb') as f:
                    f.write(response.content)

                return path, extracted_email

        return False, extracted_email

    
                return False

    # @keyword('Extract from CSV')
    # def extract_data_from_csv(self,path):
    #
