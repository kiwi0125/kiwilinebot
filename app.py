from line_bot_api import *
from events.basic import *

app = Flask(__name__)

#自己的Channel Access Token(在Messaging API底下)
line_bot_api = LineBotApi("wR6RWNy+d1LEYGfPCD0AbGehrEI+cPTQxChN5KftrpfD7JZbuwKIoj1Ys41AL8+S2tehpIAOJVeZihxBVyZnMi8YPeHpQT9PeMRzc+UfkGwoxcSYIc9H+5yLPh3HSvsR4cagMIIFHybDESjA0+CiewdB04t89/1O/w1cDnyilFU=")
#自己的Channel secret(在Basic Settings底下)
handler = WebhookHandler("5c7720c80fc66096c32f76253778ded8")

#監聽所有來自/callback的Post Request
@app.route("/callback", methods=["POST"])
def callback():
    #get X-Line-Signature header value
    signature = request.headers["X-Line_Signature"]

    #get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    #header webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

#處理訊息(這邊是回傳同樣的訊息)
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = TextSendMessage(text=event.message.text)
#     line_bot_api.reply_message(event.reply_token, message)

#處理訊息(這邊是歡迎訊息)
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     emoji = [
#             {"index":0,
#              "productId":"5ac21b4f031a6752fb806d59",
#              "emojiId":"011"
#                 },

#             {"index":1,
#              "productId":"5ac21b4f031a6752fb806d59",
#              "emojiId":"035"
#                 },
#             {"index":2,
#              "productId":"5ac21b4f031a6752fb806d59",
#              "emojiId":"049"
#                 },
#             {"index":3,
#              "productId":"5ac21b4f031a6752fb806d59",
#              "emojiId":"035"
#                 }
#             ]
#     #歡迎訊息
#     text_message = TextSendMessage(text="""$$$$
# Hello! 恭喜您成為kiwi機器人的第100個好友
# 這邊提供了一些功能，這段只是歡迎訊息而已
# 才不希望你點進來呢！""",emojis=emoji)
    
#     #貼圖訊息
#     sticker_message = StickerMessage(
#         package_id = "11537",
#         sticker_id = "52002769")
    
#     #將歡迎訊息、貼圖訊息放到機器人裡面回復
#     line_bot_api.reply_message(
#         event.reply_token,
#         [text_message, sticker_message])

#只要是對輸入訊息(message_text)的處理，都在這裡
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    if message_text == "@使用說明":
        about_us_event(event)
        Usage(event)
    
    if event.message.text == "@使用說明":
        buttons_template = TemplateSendMessage(
            alt_text="小幫手 template",
            template=ButtonsTemplate(
                title="選擇服務",
                text="請選擇",
                thumbnail_image_url="https://i.imgur.com/QqZ7Bix.jpg",
                actions=[
                    MessageTemplateAction(
                        label = "油價查詢",
                        text = "油價查詢"
                    ),
                        MessageTemplateAction(
                            label = "匯率查詢",
                            text = "匯率查詢"
                    ),
                        MessageTemplateAction(
                            label = "股價查詢",
                            text = "股價查詢"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        
if __name__=="__main__":
    app.run()