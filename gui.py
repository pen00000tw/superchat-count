from tkinter import *
from chat_downloader import ChatDownloader
import requests
import threading
class thisWindow:
    def __init__(self):
        self.win = Tk()
        self.canvas = Canvas(self.win, width = 800, height = 600, bg = 'white')
        self.canvas.pack(expand=YES, fill=BOTH)
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width/2-800/2)
        y = int(height/2-600/2)
        str1 = "800x600+"+ str(x) + "+" + str(y)
        self.win.geometry(str1)
        self.win.resizable(width=False, height=False)
        self.win.title("計算SC比例")
    def add_frame(self):
        self.frame = Frame(self.win, height = 580, width = 780,bg='pink')
        self.frame.place(x=10,y=10)

        self.label1 = Label(self.frame,text = "請填上該直播的url:")
        self.label1.config(font=("微軟正黑體", 12, 'bold'))
        self.label1.place(x = 50,y=30)

        self.url = Entry(self.frame, font='Courier 12',width=60)
        self.url.place(x=50, y=60)

        self.text = Text(self.win,height = 30, width = 95)
        self.text.place(x=60,y=100)
        self.button = Button(self.frame, text="計算",
                             font=('微軟正黑體', 15),
                             bg='gray', fg='white',
                             command=self.startingthread)
        self.button.place(x=660, y=37)
        self.win.mainloop()
    def startingthread(self):
        self.button['state'] = DISABLED
        self.button['text'] = "計算中"
        self.thread = threading.Thread(target = self.countSC)
        self.thread.start()
    def countSC(self):
        url = self.url.get()
        chat = ChatDownloader().get_chat(url,message_groups=['superchat'])
        result = dict()
        count = dict()
        result1 = dict()
        final = dict()
        total = 0
        self.text.delete(1.0,"end")
        for message in chat:
            if 'money' in message:
                self.text.insert("insert",chat.format(message) + "\n")
                self.text.see(END)
                #self.win.update()
                if message['money']['currency'] in result:
                    result[message['money']['currency']] = result[message['money']['currency']] + message['money']['amount']
                    count[message['money']['currency']] = count[message['money']['currency']] + 1
                else:
                    result[message['money']['currency']] = message['money']['amount']
                    count[message['money']['currency']] = 1
        #換算台幣and整理資料到final
        r=requests.get('https://api.exchangerate-api.com/v4/latest/TWD')
        currency=r.json()
        for cur in result.items():
            result1['before'] = round(result[cur[0]],2)
            if cur[0] in currency['rates']:
                result1['after'] = round(result[cur[0]] / currency['rates'][cur[0]],2)
            else:
                if cur[0] == '₱':                   #菲律賓幣例外處理
                    result1['after'] = round(result[cur[0]] / currency['rates']['PHP'],2)
                else:
                    result1['after'] = 0     #無法辨識幣別
            result1['count'] = count[cur[0]]
            final[cur[0]] = result1.copy()
        for i in final.items():
            total = total + i[1]['after']
        #排序
        final = sorted(final.items(),key = lambda final:final[1]['after'], reverse=True)
        #印出結果
        self.text.insert("insert","---------------------------\n")
        self.text.insert("insert","幣別".ljust(8) + "金額".ljust(13)+ "換算台幣".ljust(11)+"筆數".ljust(13) +"百分比\n")
        for i in final:
            self.text.insert("insert",str(i[0]).ljust(10))
            self.text.insert("insert",str(i[1]['before']).ljust(15))
            self.text.insert("insert",str(i[1]['after']).ljust(15))
            self.text.insert("insert",str(i[1]['count']).ljust(15))
            self.text.insert("insert",str(round(i[1]['after'] / total * 100,2)) + "%\n")
        self.text.insert("insert","---------------------------\n")
        self.text.insert("insert","總計 : NT$ " + str(round(total,2)))
        self.text.see(END)
        self.button['state'] = NORMAL
        self.button['text'] = "計算"
        #self.win.update()
        #self.win.mainloop()
if __name__ == "__main__":
    x = thisWindow()
    x.add_frame()