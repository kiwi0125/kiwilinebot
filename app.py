from line_bot_api import *
from events.basic import *
from events.oil import *
from events.Msg_template import *
from events.EXRate import *
from model.mongodb import *
import re
import twstock
import datetime
import schedule
import time

app = Flask(__name__)

#####連接資料庫，去抓使用者的選股######
def cache_users_stock():
    db=constructor_stock()
    nameList = db.list_collection_names()
    users = []
    for i in range(len(nameList)):
        collect = db[nameList[i]]
        cel = list(collect.find({"tag":"stock"}))
        users.append(cel)
    return users


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
        return 0
    
    #只要偵測到使用者輸入"股票清單"，就會回傳使用者的選股條件
    if re.match("股票清單",msg):
        line_bot_api.push_message(uid, TextSendMessage("稍等一下，股票查詢中..."))
        content = show_stock_setting(user_name, uid)
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0

    #刪除指定股票的選股資料
    if re.match("刪除[0-9]{4}",msg):
        content = delete_my_stock(user_name, msg[2:])
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0
    
    #刪除使用者所有的選股資料
    if re.match("清空股票",msg):
        content = delete_my_allstock(user_name, uid)
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0

    #當使用者輸入"股價提醒"的時候，會根據設定好的時間，去爬股市價格出來
    #並根據篩選條件(<>=)去判斷，若股價跟關注價格符合條件，就會回傳"符合>的執行條件"
    #
    if re.match("股價提醒",msg):
        
        def look_stock_price(stock, condition, price, userID):
            print("現在正在執行look_stock_price函數")
            url = "https://tw.stock.yahoo.com/q/q?s=" + stock
            list_req = requests.get(url)
            print("現在正在執行requests方法")
            soup = BeautifulSoup(list_req.content, "html.parser")
            print("現在正在建立爬蟲方法")
            getstock = soup.findAll(class_="Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)").text
            print("現在正在爬蟲")
            content = stock + "當前股市價格為: " +getstock

            if condition == "<":
                content += "\n篩選條件為: < "+price
                if float(getstock) < float(price):
                    content += "\n符合" + getstock + "<" + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text= content))
            elif condition == ">":
                content += "\n篩選條件為: > "+price
                if float(getstock) > float(price):
                    content += "\n符合" + getstock + ">" + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text= content))
            elif condition == "=":
                content += "\n篩選條件為: = "+price
                if float(getstock) == float(price):
                    content += "\n符合" + getstock + "=" + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text= content))
        def job():
            dataList = cache_users_stock()
            for i in range(len(dataList)):
                for k in range(len(dataList[i])):
                    look_stock_price(dataList[i][k]['favorite_stock'], dataList[i][k]['condition'], dataList[i][k]['price'], dataList[i][k]['userID'])
        schedule.every(30).seconds.do(job).tag("daily-tasts-stock"+uid, "second")#每10秒執行一次
        #schedule.every().hour.do(job) #每小時執行一次
        #schedule.every().day.at("17:19").do(job) #每天17:19執行一次
        #schedule.every().monday.do(job) #每周一執行一次
        #schedule.every().wednesday.at("14:45").do(job) #每周三14:45執行一次
        
        while True:
            schedule.run_pending()
            time.sleep(1)

                  
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
    #使用者輸入"幣別種類"，就會回傳各種幣別的flex message
    if re.match("幣別種類",emsg):
        message = show_Button()
        line_bot_api.reply_message(event.reply_token,message)

    #使用者輸入查詢匯率XXX，就會回傳指定幣別的匯率
    if re.match("查詢匯率[A-Z]{3}",msg):
        msg = msg[4:]
        content = showCurrency(msg)
        line_bot_api.push_message(uid, TextSendMessage(content))

    #使用者輸入換匯/XXX/XXX/NUM，就可以回覆轉換過後的結果
    if re.match("換匯[A-Z]{3}/[A-Z]{3}/[0-9]",msg):
        line_bot_api.push_message(uid,TextSendMessage("將為您做外匯計算..."))
        content = getExchangeRate(msg)
        line_bot_api.push_message(uid, TextSendMessage(content))





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