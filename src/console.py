import tkinter as tk
from PIL import ImageTk,Image,ImageOps
import threading 
import string
import time

import sprigatito
import user

class console:
    def __init__(self):
        self.size = "1000x700"
        self.base = tk.Tk()
        self.base.geometry(self.size)
        self.base.title("ProjectSprigatito - v0.1 Console")
        
        self.frame1 = tk.Frame(self.base,relief=tk.RAISED,bd=1,padx=10,pady=10)
        self.exitbutton = tk.Button(self.frame1,width=10,height=5,text="終了",command=lambda:self.base.destroy())
        self.exitbutton.pack()
        self.movebutton = tk.Button(self.frame1,width=10,height=5,text="上に移動\n（デモ）",command=lambda:self.moveup())
        self.movebutton.pack()
        self.movedbutton = tk.Button(self.frame1,width=10,height=5,text="下に移動\n（デモ）",command=lambda:self.movedown())
        self.movedbutton.pack()
        self.reversebutton = tk.Button(self.frame1,width=10,height=5,text="反転\n（デモ）",command=lambda:self.reverse())
        self.reversebutton.pack()
        self.pushbutton = tk.Button(self.frame1,width=10,height=5,text="送信",command=lambda:self.push())
        self.pushbutton.pack(side=tk.BOTTOM)
        
        self.frame1.pack(side=tk.LEFT,fill=tk.BOTH)

        self.frame2 = tk.Frame(self.base,relief=tk.RAISED,bd=1,padx=10,pady=10)
        self.canvas = tk.Canvas(self.frame2,bg="#000",width=850,height=500)
        
        self.Sprigatitoimage = Image.open("./img/Sprigatito.png")
        self.Sprigatitoimg = ImageTk.PhotoImage(self.Sprigatitoimage)
        self.Sprigatito = sprigatito.Sprigatito()
        
        self.Sprigatito.setModelPosX(425) #初期値：425（中央）
        self.Sprigatito.setModelPosY(250) #初期値：250（中央）
        self.User = user.user()
        self.imgid = self.canvas.create_image(
            self.Sprigatito.getModelPosX(),
            self.Sprigatito.getModelPosY(),
            image=self.Sprigatitoimg
        )
        self.outlabel = tk.Label(self.frame2,text="出力")
        self.outputbox = tk.Text(self.frame2,width=10,height=7)
        self.outputbox.configure(state="disabled")
        self.inlabel = tk.Label(self.frame2,text="入力")
        self.inputbox = tk.Text(self.frame2,width=10,height=1)

        self.canvas.pack()
        self.outlabel.pack()
        self.outputbox.pack(fill=tk.BOTH)
        self.inlabel.pack()
        self.inputbox.pack(fill=tk.BOTH)
        self.frame2.pack(side=tk.BOTTOM,fill=tk.BOTH)

        #th1 = threading.Thread(target=self.moveup)
        #th1.start()

    def moveup(self):
        for i in range(10):
            self.canvas.move(self.imgid,0,-5)
            self.canvas.update()
            time.sleep(0.03)
        self.Sprigatito.setModelPosY(self.Sprigatito.getModelPosY()-50)
    def movedown(self):
        for i in range(10):
            self.canvas.move(self.imgid,0,5)
            self.canvas.update()
            time.sleep(0.03)
        self.Sprigatito.setModelPosY(self.Sprigatito.getModelPosY()+50)
    def reverse(self):
            self.canvas.delete(self.imgid)
            self.Sprigatitoimage = ImageOps.mirror(self.Sprigatitoimage)
            self.Sprigatitoimg = ImageTk.PhotoImage(self.Sprigatitoimage)
            self.imgid = self.canvas.create_image(
                self.Sprigatito.getModelPosX(),
                self.Sprigatito.getModelPosY(),
                image=self.Sprigatitoimg
            )    

    def push(self):
        text = self.inputbox.get("1.0","end")
        if not text.isspace():
            text = text.replace("\n","")
            self.inputbox.delete("1.0","end")
            self.insertoutput(self.User.getUserName()+":"+text)
            self.Sprigatito.send(text)
            self.insertoutput(self.Sprigatito.getModelName()+":"+self.Sprigatito.getSendMessage())

    def insertoutput(self,text):
            self.outputbox.configure(state="normal")
            self.outputbox.insert("end",text+"\n")
            self.outputbox.configure(state="disabled")