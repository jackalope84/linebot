# -*- coding: utf-8 -*-
import openai

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
    openai.api_key = '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'
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
    )
    message =  response.choices[0].message.content.replace('\n','')
    line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
