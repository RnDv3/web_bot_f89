import telegram.ext
import telegram
import time
from datetime import datetime
import json
import itertools
import gspread
import logging
import requests
import base64
import random

from PIL import Image, ImageChops
from pdf2image import convert_from_path
from telegram.ext import Updater, CommandHandler, CallbackContext, PollAnswerHandler, MessageHandler, Filters


import cv2
import project_julien.Web_BOT_Telegram.libs.openCV as imgCV
import project_julien.database_lib.db as db

# ===================================================================================== #
# Khởi tạo hệ thống
# ===================================================================================== #
# Cấu hình Telegram
API_KEY = "5418400024:AAHcynS46ert5Y5tR2LprwJN77L8KGX_8Rw" #Bot RnD_web_bot
Updater = telegram.ext.Updater(API_KEY, use_context = True)

# ===================================================================================== #
# Cấu hình sheet info
# Sheet Template
SHEET_ID_TEMP = "1QhSLwxCQEdhfAZ399_Ju3gzMfN0KgAxHSzUiEMW3fQY"

# Sheet list
SHEET_ID1 = "1cXWyL7OM6Bd_5p4JTwxJO6ysXWrc_BBqQcMrbwsX1X0"
SHEET_ID2 = "1DV3u3wSCjrP4UWq-UvEHZoFRSPQaywln2DiBUR0as2U"
SHEET_ID3 = "1BScCnqyIV1CDkSHAxIdoXJae4DkNehNRJ-dVRRqG9l4"
SHEET_ID4 = "1y9Saue633DREV6W2jSJQ0UEOF57nf6WM7Aa675oyBC0"
SHEET_ID5 = "16xEdtBEWOoI-rAV__djPEi909a3ORTUllb6EsGuyH8s"
SHEET_ID6 = "1-Xrn2rCgfnUfQk_xSwRYY2-7J7zvMtj1ePdyc6zMTjk"
SHEET_ID7 = "1-CK3LvVtQXc1aFVDdehb-Rmks_uqD8OYFWjBw_FVam4"
SHEET_ID8 = "1l6JOuUBqpM7-KR-NFPUsc4QYieGOH8guY2F4u4p9VnI"
SHEET_ID9 = "1GefFqGGhAd2ASrW8VhVXeZJ_Zr0wmUoGrAplwJj_4Y0"
SHEET_ID10 = "1ynd_VtSYKQXn65UQkjgbcrWHOK6hJDXsDwihGa7K4bw"

# Bắt đầu mở sheet
sa = gspread.oauth(authorized_user_filename='/root/project_julien/Web_Bot_F89/token.json')
# ss_main = sa.open_by_key(SHEET_ID)

print("Reload 10 sheet")
ss1 = sa.open_by_key(SHEET_ID1)
ss2 = sa.open_by_key(SHEET_ID2)
ss3 = sa.open_by_key(SHEET_ID3)
ss4 = sa.open_by_key(SHEET_ID4)
ss5 = sa.open_by_key(SHEET_ID5)
ss6 = sa.open_by_key(SHEET_ID6)
ss7 = sa.open_by_key(SHEET_ID7)
ss8 = sa.open_by_key(SHEET_ID8)
ss9 = sa.open_by_key(SHEET_ID9)
ss10 = sa.open_by_key(SHEET_ID10)
print("Reload 10 sheet done!")

# Define dictionary of sheet list
sheetList = {
    "sheet1" : [SHEET_ID1, ss1, True, 1],
    "sheet2" : [SHEET_ID2, ss2, True, 2],
    "sheet3" : [SHEET_ID3, ss3, True, 3],
    "sheet4" : [SHEET_ID4, ss4, True, 4],
    "sheet5" : [SHEET_ID5, ss5, True, 5],
    "sheet6" : [SHEET_ID6, ss6, True, 6],
    "sheet7" : [SHEET_ID7, ss7, True, 7],
    "sheet8" : [SHEET_ID8, ss8, True, 8],
    "sheet9" : [SHEET_ID9, ss9, True, 9],
    "sheet10" : [SHEET_ID10, ss10, True, 10],
}


# ===================================================================================== #
# Get one sheet from list
def getSheet(sheetList):
    for i in range(1, 100):
        sheetNum = random.randint(1, 10)

        if sheetList["sheet"+str(sheetNum)][2] == True:
            return sheetList["sheet"+str(sheetNum)]
        else:
            continue

    print("Don't have sheet already in list")
    return False


# ===================================================================================== #
# Get info from sheet Doanh Thu
def getImageInfoFromSheetDoanhThu(ss):
    global access_token
    # Get time info
    now = datetime.now()
    current_time = now.strftime("%d%m%Y%H%M%S")

    print("Start get image info...")
    # Khai Báo sheet Name
    wks_report = ss.worksheet("EX_DT")

    sheetData = wks_report.get("N6:P6")[0]
    print("sheetData: %s"%sheetData)
    access_token = sheetData[0]

    sizeImage = sheetData[1]
    print("sizeImage: %s"%sizeImage)

    rangeImage = sheetData[2]
    print("sizeRange: %s"%rangeImage)

    agentName = wks_report.get("L1")[0][0] + "_" + str(current_time)
    print("fileName: %s"%agentName)

    listVal = dict()
    listVal['sizeImage'] = sizeImage
    listVal['rangeImage'] = rangeImage
    listVal['agentName'] = agentName
    listVal['access_token'] = access_token

    return listVal



# Get info from sheet PMKT
def getImageInfoFromSheetPMKT(ss):
    global access_token
    # Get time info
    now = datetime.now()
    current_time = now.strftime("%d%m%Y%H%M%S")

    print("Start get image info...")
    # Khai Báo sheet Name
    wks_report = ss.worksheet("EX_REPORT_PMKT")

    sheetData = wks_report.get("K6:M6")[0]
    print("sheetData: %s"%sheetData)
    access_token = sheetData[0]

    sizeImage = sheetData[1]
    print("sizeImage: %s"%sizeImage)

    rangeImage = sheetData[2]
    print("sizeRange: %s"%rangeImage)

    agentName = wks_report.get("G2")[0][0] + "_" + str(current_time)
    print("fileName: %s"%agentName)

    listVal = dict()
    listVal['sizeImage'] = sizeImage
    listVal['rangeImage'] = rangeImage
    listVal['agentName'] = agentName
    listVal['access_token'] = access_token

    return listVal


# ===================================================================================== #
# Capture PDF and convert to PNG
def captureImageDoanhThu(access_token, sizeImage, rangeImage, name, SHEET_ID):
    
    url = 'https://docs.google.com/spreadsheets/d/'+SHEET_ID+'/export?export?exportFormat=pdf&format=pdf&gid=1073928221'\
    '&size='+sizeImage+'&scale=1&range='+rangeImage+'&horizontal_alignment=CENTER&vertical_alignment=MIDDLE&gridlines=false&printnotes=false&top_margin=0.00'\
    '&bottom_margin=0.00&left_margin=0.00&right_margin=0.00&gridlines=false'

    headers = {'Authorization': 'Bearer ' + access_token}

    # Dùng API để export PDF của sheet
    print("Start export PDF...")
    try:
        res = requests.get(url, headers=headers)
        print("Status: %s" %(res.status_code))

        if str(res.status_code)!= '200':
            print("Lỗi authen với trang tính: %s" %res)
            return None

    except BaseException as err:
        print(err)
        return None


    # Lưu lại
    with open("/root/project_julien/Web_BOT_Telegram/imageFolder/" + name + "DoanhThu.pdf", 'wb') as f:
        f.write(res.content)


    print("Start convert PNG")
    pages = convert_from_path('/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'DoanhThu.pdf', 500)
    for i, image in enumerate(pages):
        fname = '/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'DoanhThutmp.png'

    print("Start trim image and add Moc")
    imageTrim = imgCV.trimBlankImageV2(image)
    imageTrim.save(fname, "PNG")

    imgReport = cv2.imread(fname, cv2.IMREAD_COLOR)
    imgMoc = imgCV.addMoc(imgReport, "/root/project_julien/Web_BOT_Telegram/imageSource/bezvn_moc.png")
    cv2.imwrite('/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'DoanhThu.png', imgMoc)

    print("Trim image and add Moc Done")


# ===================================================================================== #
# Capture PDF and convert to PNG
def captureImagePMKT(access_token, sizeImage, rangeImage, name, SHEET_ID):
    
    url = 'https://docs.google.com/spreadsheets/d/'+SHEET_ID+'/export?export?exportFormat=pdf&format=pdf&gid=340168630'\
    '&size='+sizeImage+'&scale=4&range='+rangeImage+'&horizontal_alignment=CENTER&vertical_alignment=MIDDLE&gridlines=false&printnotes=false&top_margin=0.00'\
    '&bottom_margin=0.00&left_margin=0.00&right_margin=0.00&gridlines=false'

    headers = {'Authorization': 'Bearer ' + access_token}

    # Dùng API để export PDF của sheet
    print("Start export PDF...")
    try:
        res = requests.get(url, headers=headers)
        print("Status: %s" %(res.status_code))

        if str(res.status_code)!= '200':
            print("Lỗi authen với trang tính: %s" %res)
            return None

    except BaseException as err:
        print(err)
        return None


    # Lưu lại
    with open("/root/project_julien/Web_BOT_Telegram/imageFolder/" + name + "PMKT.pdf", 'wb') as f:
        f.write(res.content)


    print("Start convert PNG")
    pages = convert_from_path('/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'PMKT.pdf', 500)
    for i, image in enumerate(pages):
        fname = '/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'PMKTtmp.png'

    print("Start trim image and add Moc")
    imageTrim = imgCV.trimBlankImageV2(image)
    imageTrim.save(fname, "PNG")

    imgReport = cv2.imread(fname, cv2.IMREAD_COLOR)
    imgMoc = imgCV.addMoc(imgReport, "/root/project_julien/Web_BOT_Telegram/imageSource/bezvn_moc.png")
    cv2.imwrite('/root/project_julien/Web_BOT_Telegram/imageFolder/'+ name +'PMKT.png', imgMoc)

    print("Trim image and add Moc Done")


# ===================================================================================== #
# Send image Telegram PMKT
def sendImageDoanhThu(agentName, chatID, fileName, update= Updater):
    print("Send ImageDoanhThu To telegram via Bot Control"+agentName.split("_")[0])
    image_file = open('/root/project_julien/Web_BOT_Telegram/imageFolder/'+fileName+'DoanhThu.png', "rb")

    # Get group chat id from db by agentName
    groupChatID = db.getGroupIDFromAgentName(agentName.split("_")[0])["data"]

    # Send document to the group chat id
    Updater.bot.send_document(groupChatID, image_file)

# Send image Telegram DoanhThu
def sendImagePMKT(agentName, chatID, fileName, update= Updater):
    print("Send ImagePMKT To telegram via Bot Control"+agentName.split("_")[0])
    image_file = open('/root/project_julien/Web_BOT_Telegram/imageFolder/'+fileName+'PMKT.png', "rb")

    # Get group chat id from db by agentName
    groupChatID = db.getGroupIDFromAgentName(agentName.split("_")[0])["data"]

    # Send document to the group chat id
    Updater.bot.send_document(groupChatID, image_file)


def updateDataToSheet(ss, agentName, weekNum):
    sh_report = ss.worksheet("INFO")
    sh_report.update("A3:B3", [[int(weekNum), agentName]])


def main(chatID, agentName, weekNum):
    global sheetList
    try:
        sheetRecei = getSheet(sheetList)
        if sheetRecei == False:
            raise Exception("System is busy, try again!") 
        
        print("#1. main: receiver sheet: ")
        print(sheetRecei)

        # Block sheet to use
        sheetList["sheet"+str(sheetRecei[3])][2] = False
        # print(sheetList)

        # Update value to sheet
        print("#2. main: Update data to sheet ")
        updateDataToSheet(sheetRecei[1], agentName, weekNum)
        
        print("#3. main: Get Image Info and Capture Image Doanh Thu")
        listValDoanhThu = getImageInfoFromSheetDoanhThu(sheetRecei[1])
        captureImageDoanhThu(listValDoanhThu['access_token'], listValDoanhThu["sizeImage"], listValDoanhThu['rangeImage'], listValDoanhThu['agentName'], sheetRecei[0])

        print("#4. main: Get Image Info and Capture Image PMKT")
        listValPMKT = getImageInfoFromSheetPMKT(sheetRecei[1])
        captureImagePMKT(listValPMKT['access_token'], listValPMKT["sizeImage"], listValPMKT['rangeImage'], listValPMKT['agentName'], sheetRecei[0])
        
        # Send Image Doanh Thu + PMKT
        print("#5. main: Send Image Doanh Thu + PMKT To Group Agent")
        sendImageDoanhThu(listValDoanhThu['agentName'], chatID, listValDoanhThu['agentName'])
        sendImagePMKT(listValPMKT['agentName'], chatID, listValPMKT['agentName'])

        # Un-Block sheet to use
        print("#5. main: Unblock Sheet and Show Sheet Status")
        sheetList["sheet"+str(sheetRecei[3])][2] = True
        print(sheetList)

        print("#6. main: Process Done!")
        
        return True

    except BaseException as err:
        # Un-Block sheet to use
        sheetList["sheet"+str(sheetRecei[3])][2] = True
        print(err)
        print(sheetList)
        return err




