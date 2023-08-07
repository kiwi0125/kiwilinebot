from line_bot_api import *


def about_us_event(event):
    emoji = [
            {"index":0,
             "productId":"5ac21b4f031a6752fb806d59",
             "emojiId":"011"
                },

            {"index":1,
             "productId":"5ac21b4f031a6752fb806d59",
             "emojiId":"035"
                },
            {"index":2,
             "productId":"5ac21b4f031a6752fb806d59",
             "emojiId":"049"
                },
            {"index":3,
             "productId":"5ac21b4f031a6752fb806d59",
             "emojiId":"035"
                }
            ]
    #歡迎訊息
    text_message = TextSendMessage(text="""$$$$
Hello! 恭喜您成為kiwi機器人的第100個好友
這邊提供了一些功能，這段只是歡迎訊息而已
才不希望你點進來呢！""",emojis=emoji)
    
    #貼圖訊息
    sticker_message = StickerMessage(
        package_id = "11537",
        sticker_id = "52002769")
    
    #建立一個template message
    buttons_template = TemplateSendMessage(
            alt_text="小幫手 template",
            template=ButtonsTemplate(
                title="選擇服務",
                text="請選擇",
                #這邊放tempalte message的圖片網址
                thumbnail_image_url="https://i.imgur.com/QqZ7Bix.jpg",
                actions=[
                    MessageTemplateAction(
                        label = "油價查詢", #按鈕上的文字
                        text = "油價查詢"   #按下去會傳這個訊息
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

    #將歡迎訊息、貼圖訊息跟Template message放到機器人裡面回復
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, buttons_template])

#####推訊息的函數#####
def push_msg(event,msg):
    try:
        user_id = event.source.user_id
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    except:
        room_id = event.source.room_id
        line_bot_api.push_message(room_id,TextSendMessage(text=msg))

#####傳回使用說明的函數#####
def Usage(event):
    push_msg(event, "👉查詢方法\
             \n \
             \nkiwi可以查詢\n📌油價\n📌匯率\n📌股價\
             \n\n📌油價通知\n    ➡輸入「油價查詢」 \
             \n\n📌匯率通知\n    ➡輸入「查詢匯率」 \
             \n\n📌匯率兌換\n    ➡換匯USD/TWD \
             \n\n📌股價查詢\n    ➡輸入#股票代號")
    
