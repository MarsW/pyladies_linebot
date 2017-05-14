# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

handler = WebhookHandler('Your_Channel_Secret') 
line_bot_api = LineBotApi('Your_Channel_Access_Token') 


@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# ================= 機器人區塊 Start =================
@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
    msg = event.message.text #message from user

    # 針對使用者各種訊息的回覆 Start =========
    reply = ""
    # msg=input("msg=")         #input()是在terminal/cmd鍵盤輸入的，這裡是用line傳進來的
    chg_word = ["想吃飯","不想吃這個","換一個"]
    find = False
    for i in chg_word:
        if i in msg:
            find = True
    print(find)
    if find:
        import random
        choice = ["麥當勞", "7-11", "烏龍麵", "自助餐"]
        index = random.randint(0,len(choice)-1)
        print(choice[index])
        print("建議你可以吃"+choice[index])   #print會印在Heroku log中，不會在line出現
        reply = "建議你可以吃"+choice[index]
    elif msg=="我很滿意你的服務":
        print("希望你有個愉快的一餐")
        reply = "希望你有個愉快的一餐"
    else:
        print("我聽不懂你在說什麼！")
        reply = "我聽不懂你在說什麼！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

    # 針對使用者各種訊息的回覆 End =========

# ================= 機器人區塊 End =================

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
