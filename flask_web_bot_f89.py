from flask import Flask,request,json,render_template
import subprocess
from flask import jsonify

import project_julien.database_lib.db as db
import project_julien.Web_Bot_F89.captureDoanhThu as captureDoanhThu

app = Flask(__name__, template_folder='/root/project_julien/Web_Bot_F89')


# --------------------------------------------------------------- #
# Test server and intro
# --------------------------------------------------------------- #
@app.route('/')
def hello():
    return 'Welcome to RnD server!'

@app.route('/test')
def testSV():
    return "test"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# --------------------------------------------------------------- #
# API
# --------------------------------------------------------------- #
# Get danh sách nhóm trên PM BOT Control
@app.route('/getAgentGroupList')
def getAgentGroupList():
    print("\n\n/getAgentGroupList: Start get agent group list...")

    name = request.args.get("name")
    chatID = request.args.get("chatID")
    print("/getAgentGroupList: chatID: %s -- Name: %s" %(chatID, name))
    
    rsp = db.getAgentListFromChatID(chatID)

    return rsp


# --------------------------------------------------------------- #
# Xử lý web cho bot web
# --------------------------------------------------------------- #
@app.route('/home')
def webBotHome():
    redirect = request.args.get("redirect")
    print("/home: redirect: %s" %redirect)

    # Xử lý redirect thông qua link, fix lỗi không chuyển trang trên Android Phone
    if redirect == 'captureDoanhThu':
        return render_template("viewDoanhThu.html")

    elif redirect == 'captureThucLai':
        return render_template("viewThucLai.html")

    return render_template("index_f89.html")


@app.route('/webBotHandle')
def webBotHandle():
    
    chatID = request.args.get("chatID")
    agentName = request.args.get("agentName")
    captureType = request.args.get("captureType")

    print("=========== /webBotHandle: Start captureType: %s - chatID: %s - agentName: %s" %(captureType, chatID, agentName))
    if captureType == 'captureDoanhThu':
        weekNum = request.args.get("weekNum")
        print("webBotHandle: weekNum: %s" %weekNum)

        status = captureDoanhThu.main(chatID, agentName, weekNum)

    elif captureType == 'captureThucLai':
        BGType = request.args.get("ThucLai")
        print("webBotHandle: ThucLai: %s" %BGType)

    else:
        status = False

    print("========== /webBotHandle: Capture: %s Done chatID: %s - agentName: %s" %(captureType, chatID, agentName))
    if status == True:
        return {'status': 'success'}
    else:
        return {'status': 'false'}


if __name__ == '__main__':
    app.run(debug=True, host="172.16.2.116", port=3002)