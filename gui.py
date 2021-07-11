from tkinter import *
from chat_downloader import ChatDownloader
import requests

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
                             command=self.countSC)
        self.button.place(x=660, y=25)
        self.win.mainloop()
    def countSC(self):
        url = self.url.get()
        chat = ChatDownloader().get_chat(url,message_groups=['messages','superchat'])
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
                self.win.update()
                if message['money']['currency'] in result:
                    result[message['money']['currency']] = result[message['money']['currency']] + message['money']['amount']
                    count[message['money']['currency']] = count[message['money']['currency']] + 1
                else:
                    result[message['money']['currency']] = message['money']['amount']
                    count[message['money']['currency']] = 1
        #換算台幣
        r=requests.get('https://tw.rter.info/capi.php')
        currency=r.json()
        usd_to_twd = currency['USDTWD']['Exrate']
        for cur in result.items():
            tmp = 'USD' + cur[0]
            tmp = currency[tmp]['Exrate']
            result1['before'] = round(result[cur[0]],2)
            result1['after'] = round(result[cur[0]] / tmp * usd_to_twd,2)
            final[cur[0]] = result1.copy()
        for i in final.items():
            total = total + i[1]['after']
        #印出結果
        self.text.insert("insert","---------------------------\n")
        self.text.insert("insert","幣值".ljust(8) + "金額".ljust(13)+ "換算台幣".ljust(11)+"百分比\n")
        for i in final.items():
            self.text.insert("insert",str(i[0]).ljust(10))
            self.text.insert("insert",str(i[1]['before']).ljust(15))
            self.text.insert("insert",str(i[1]['after']).ljust(15))
            self.text.insert("insert",str(round(i[1]['after'] / total * 100,2)) + "%\n")
        self.text.insert("insert","---------------------------\n")
        self.text.insert("insert","總計 : NT$ " + str(total))
        self.win.update()
if __name__ == "__main__":
    x = thisWindow()
    x.add_frame()