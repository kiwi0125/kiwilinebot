from line_bot_api import *

def stock_reply_other(stockNumber):
    content_text = "即時股價和K線圖"
    text_message = TextSendMessage(
                                text = content_text, 
                                quick_reply=QuickReply(
                                                    items=[
                                                        QuickReplyButton(
                                                                        action=MessageAction(
                                                                                            label="查詢5日漲幅",
                                                                                            text="#"+stockNumber
                                                                                            )
                                                                        ),
                                                        QuickReplyButton(
                                                                        action=MessageAction(
                                                                                            label="K線圖",
                                                                                            text="@K"+stockNumber
                                                                                            )
                                                                        )
                                                            ]
                                                        )
                                    )
    return text_message

# 幣別種類Button
def show_Button():
    flex_message = FlexSendMessage(
            alt_text="幣別種類",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "幣別種類",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#AA2B1D"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "美金",
                            "text": "USD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#EA0000",
                            "margin": "sm",
                            "height": "md"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "日圓",
                            "text": "JPY"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#CE0000",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "港幣",
                            "text": "HKD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#AE0000",
                            "margin": "sm"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "英鎊",
                            "text": "GBP"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#FF359A",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "澳幣",
                            "text": "AUD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#FF0080",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "加幣",
                            "text": "CAD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#F00078",
                            "margin": "sm"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "法郎",
                            "text": "CHF"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#FF00FF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "新加坡",
                            "text": "SGD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#E800E8",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "南非幣",
                            "text": "ZAR"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#D200D2",
                            "margin": "sm"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "瑞典幣",
                            "text": "SEK"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#9F35FF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "泰幣",
                            "text": "THB"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#921AFF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "菲比索",
                            "text": "PHP"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#8600FF",
                            "margin": "sm"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "印尼幣",
                            "text": "IDR"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#6A6AFF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "韓元",
                            "text": "KRW"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#4A4AFF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "馬來幣",
                            "text": "MYR"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#2828FF",
                            "margin": "sm"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "越南盾",
                            "text": "VND"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#2894FF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "人民幣",
                            "text": "CNY"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#0080FF",
                            "margin": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "紐元",
                            "text": "NZD"
                            },
                            "gravity": "center",
                            "style": "primary",
                            "color": "#0072E3",
                            "margin": "sm"
                        }
                        ]
                    }
                    ]
                }
                }
            )
    return flex_message