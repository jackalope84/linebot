# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('N1XGuA/A8gXSGwrVYa4NTe5S1lDdrhsqTNLs5pSXnChAvDJbqqLoH8LfiEJLTVkU78GyvAe3tc0Z7LgKknbEBjLyTIv79y6veLI06KPOqj9riAtEv/OTQVdD8H/IRk1slwskreDKY8Vmb7gk0GLyqwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('3794d107101f65d85bbf2c49451bc84f')

line_bot_api.push_message('Ua95780ca83976847d0bbf0c4b2fc45c8', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        flex_message = TextSendMessage(text='請點選您想去的國家',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="日本", text="Japan")),
                                   QuickReplyButton(action=MessageAction(label="台灣", text="Taiwan")),
                                   QuickReplyButton(action=MessageAction(label="新加坡", text="Singapore")),
                                   QuickReplyButton(action=MessageAction(label="韓國", text="Korea")),
                                   QuickReplyButton(action=MessageAction(label="中國", text="China")),
                                   QuickReplyButton(action=MessageAction(label="美國", text="US"))
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
