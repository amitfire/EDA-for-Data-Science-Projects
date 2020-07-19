#import pdftables_api
import csv
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re
#import requests
import os, time
#from bs4 import BeautifulSoup


class PdfHelper(object):
   
    
    def extract_from_pdf(self, path):
        f = open('workfile', 'w')
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
        elem = []
        elem2 = []
        listOfDict = []
        elem4 = []
        lenStart = 0
        #df = text.split(" ")
        with open('textfromPDF.txt', 'w') as f:
            #reader = csv.reader(csvfile)
            f.write(text)
        
        #print(text)

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

    

    # @keyword('Extract from CSV')
    # def extract_data_from_csv(self,path):
    #

pdf = PdfHelper()
pdf.extract_from_pdf('C:/Users/DELL/effectofsalinitandsodicityonplantgrowth.pdf')
