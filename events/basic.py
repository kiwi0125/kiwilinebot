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
    
    #將歡迎訊息、貼圖訊息放到機器人裡面回復
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message])