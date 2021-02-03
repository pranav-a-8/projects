import socket
from tkinter import *
import threading
from tkinter import messagebox

global online
global UL,UE,IPL,IPE,UB
import sys
import time

online = ['everyone']
SERVER = ""
header = 2048  # specifies the max no of bytes which can be transmitted via socket
port = 5050  # specifies the port through which communications take place
addr = (SERVER, port)
format = 'utf-8'  # format by which messages are encoded
DISCONN_MSG = "!!!DISC!!!"  # keyword for disconnecting a client
global run
run=True
def wexit():                     #function to exit
    global run
    time.sleep(0.5)
    sys.exit()



def start():
    global online,run
    global UL, UE, IPL, IPE, UB
    if not UE.get():                 #if the user didn't gave any username ,then the program prompts the user to add one
        messagebox.showwarning(title="Invalid Username", message="Please enter a valid username")
    else:
        name = UE.get()
        SERVER = IPE.get()
        addr = (SERVER, port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #defines a socket for the client to connect with the server

        def close_client():                                           #function to close the program
            global run
            client.send(DISCONN_MSG.encode(format))                   #when the user closes the program ,a disconnection prompt is send to the server
            run = False
            thr.join()
            threading.Thread(target=wexit).start()
            root.destroy()                                            #gui is closed
        try:
            client.connect(addr)                                      # connects to socket
        except Exception as e:
            messagebox.showerror("Couldn't connect",e)                # if the client couldn't connect,the reason is displayed
            UL.destroy()
            UE.destroy()
            UB.destroy()
            IPE.destroy()
            IPL.destroy()
            start_client()
        else:
            client.send(name.encode(format))                          #asks the server if the username is available
            resp=client.recv(header).decode(format)
            if resp=="REJECTED":                                      #if its unavailable,then prompts user to change it
                messagebox.showwarning("Username Taken!","Please use another username as this one is already in use")
                pass
            elif resp=="APPROVED":
                UL.destroy()
                UE.destroy()
                UB.destroy()
                IPE.destroy()
                IPL.destroy()
                clicked = StringVar()
                clicked.set('everyone')

                T = Text(root, height=8, width=30, fg="black", bd=3, state="disabled")     #defines the layout of the gui
                E = Text(root, height=1, width=30, bd=3)
                STM = OptionMenu(root, clicked, *online)
                STM.configure(font=('Segoe Print', 12, "bold"))
                T.grid(row=0, column=0)
                E.grid(row=1, column=0)
                T.configure(font=('Segoe Print', 12, "italic"))
                E.configure(font=('Segoe Print', 12, "italic"))
                E.insert(END,"Type your messages here.")
                STM.grid(row=0, column=1)

                def send():                                                                 #function which sends messages
                    global online
                    if clicked.get() == 'everyone':
                        send_to = online
                        if 'everyone' in send_to:
                            send_to.pop(send_to.index("everyone"))   #if the user wishes to send to everyone,then the message is sent to all connected users
                    else:
                        s = str(clicked.get())
                        send_to = []
                        send_to.append(s)                                                   #else its send to a single user
                    msg = E.get('1.0', END)
                    if msg and len(send_to) != 0:         #the code below changes the text color to red and back to black when displaying name of the user
                        T.config(state="normal")
                        T.insert(END, name + ':')
                        p1 = T.index("end-1c linestart")
                        p2 = T.index("end-1c")
                        T.tag_add("a", p1, p2)
                        T.tag_config("a", foreground="red")
                        T.insert(END, ' ' + msg)
                        T.see("end")
                        T.config(state="disabled")
                        E.delete("1.0", "end")

                    for i in send_to:
                        client.send((i + "@m:" + msg).encode(format))              #message is send to the selected user(s)

                S = Button(root, text="SEND", command=send)                        #configures part of the gui and displays a welcome message
                S.configure(font=('Segoe Print', 12, "bold"))
                S.grid(row=2, column=1)
                T.config(state="normal")
                T.insert(END, "WELCOME " + name + " !\n")
                tl = len(name) + 10
                T.tag_add("welcome", "1.0", "1." + str(tl))
                T.tag_config("welcome", foreground="green")
                T.config(state="disabled")

                def a():
                    global online,run
                    while run:
                        root.protocol('WM_DELETE_WINDOW', close_client)
                        message = client.recv(header).decode(format)            #this thread listens to the server for incoming messages and displays them
                        if message:
                            if message[:5] == "@onl:":
                                m = eval(message[5:])
                                message = ''
                                online = m
                                online.append('everyone')
                                online.pop(online.index(name))
                                STM = OptionMenu(root, clicked, *online)
                                STM.configure(font=('Segoe Print', 12, "bold"))
                                STM.grid(row=0, column=1)
                            elif "@m:" in message:
                                for i in range(0, len(message) - 4):
                                    if message[i:i + 3] == "@m:":                        #the code below changes the colour of the name of the sender to blue
                                        T.config(state="normal")
                                        T.insert(END, message[:i] + ':')
                                        p1 = T.index("end-1c linestart")
                                        p2 = T.index("end-1c")
                                        T.tag_add("b", p1, p2)
                                        T.tag_config("b", foreground="blue")
                                        T.insert(END, " " + message[i + 3:])
                                        T.see("end")
                                        T.config(state="disabled")

                thr=threading.Thread(target=a)                      #the listening thread is started
                thr.start()
root = Tk()
root.title("MESSENGER")
def start_client():                                                    #starts the initialaisation process
    global UL, UE, IPL, IPE, UB
    UL = Label(root, text="Username")
    UE = Entry(root)                                                   #username entry widget
    IPL = Label(root, text="Server IP Address")
    IPE = Entry(root)                                                  #ip-address entry widget
    IPE.insert(END, SERVER)
    UE.insert(END, "anon")
    UB = Button(root, text="ENTER", command=start)
    UL.grid(row=0, column=0)
    UE.grid(row=0, column=1)
    IPE.grid(row=1, column=1)
    IPL.grid(row=1, column=0)
    UB.grid(row=0, column=2, rowspan=2)
start_client()                                               #starts the client

root.mainloop()                                              #starts the mainloop of the gui
