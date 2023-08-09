from line_bot_api import *
from events.basic import *
from events.oil import *
from events.Msg_template import *
from model.mongodb import *
import re
import twstock
import datetime

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
    #.get_profile可以傳回使用者的個人資料(名稱、照片、狀態消息等)
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    user_name = profile.display_name #使用者名稱

    emsg = event.message.text
    message_text = str(emsg).lower()
    msg = str(emsg).upper().strip()

    ############################使用說明############################
    if message_text == "@使用說明":
        about_us_event(event)
        Usage(event)
    
    ############################油價查詢############################
    if message_text == "@油價查詢":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        
    ############################股票查詢#############################
    if message_text == "@股價查詢":
        #push_message需要的參數:傳訊息的對象、要傳的訊息
        line_bot_api.push_message(uid,TextSendMessage("請輸入#股票代碼"))

    #只要偵測到使用者傳回"想知道股價"加上一個數字的字串，就會開啟快速回覆(Msg_template.py)
    if re.match("想知道股價[0-9]", msg):
        stockNumber = msg[5:9]
        btn_msg = stock_reply_other(stockNumber)
        line_bot_api.push_message(uid, btn_msg)
        return 0
    
    #只要偵測到使用者輸入"關注(股票代碼4碼)(大於或小於)(值)"就會將這些參數放到model資料夾的mongodb.py
    if re.match("關注[0-9]{4}[<>][0-9]",msg):
        stockNumber = msg[2:6]        
        content = write_my_stock(uid, user_name, stockNumber, msg[6:7], msg[7:])
        line_bot_api.push_message(uid, TextSendMessage(content))
    else:
        content = write_my_stock(uid, user_name, stockNumber, "未設定","未設定")
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0       
                                                    
    #只要偵測到使用者傳回#開頭的文字，就會傳回股票前五日的漲幅
    if (emsg.startswith("#")):
        text = emsg[1:]
        content = ""

        stock_rt = twstock.realtime.get(text)
        my_datetime = datetime.datetime.fromtimestamp(stock_rt["timestamp"]+8*60*60)
        my_time = my_datetime.strftime("%H:%M:%S")

        content += "%s (%s) %s\n" %(
            stock_rt["info"]["name"],
            stock_rt["info"]["code"],
            my_time
            )            
        content += "現價: %s / 開盤: %s\n"%(
            stock_rt["realtime"]["latest_trade_price"],
            stock_rt["realtime"]["open"]
            )
        content += "最高: %s / 最低: %s\n"%(
            stock_rt["realtime"]["high"],
            stock_rt["realtime"]["low"]
            )
        
        content += "量: %s\n" %(stock_rt["realtime"]["accumulate_trade_volume"])

        stock = twstock.Stock(text)
        content += "-----\n"
        content += "最近五日價格: \n"
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range(len(price5)):
            content += "[%s] %s\n" %(date5[i].strftime("%Y-%m-%d"), price5[i])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
            )
    ############################匯率區塊############################
    if re.match("幣別種類",emsg):
        message = show_Button()
        line_bot_api.reply_message(event.reply_token,message)





#######跟隨機器人後會做的事件#########
@handler.add(FollowEvent)
def handler_follow(event):
    welcome_msg = """Hello! 恭喜您成為kiwi機器人的第100個好友
這邊提供了一些功能，這段只是歡迎訊息而已
才不希望你點進來呢！"""
    line_bot_api.reply_message(
        event.reply_token, 
        TextSendMessage(text=welcome_msg))
    
#######解除跟隨後會做的事件########
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event) #這邊傳回事件會傳回一大串資料，其中一個是解除跟隨的使用者ID






if __name__=="__main__":
    app.run()