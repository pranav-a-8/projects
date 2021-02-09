import socket                            #socket is used for communication through th enetwork
import threading                         #threading is used for creating multiple threads
import mysql.connector                   #for connecting with mysql
import time
from tkinter import *                    #tkinter is used to make the graphical user interface
from tkinter import messagebox           #for prompts and messageboxes
global T
mydb = mysql.connector.connect(host="localhost", user="root", passwd="")  #connects to mysql
mycursor = mydb.cursor()
mycursor.execute("create database messaging")
mycursor.execute("use messaging")     #creates and uses the database messaging
mycursor.execute("create table online(name varchar(15) Primary key,ip varchar(18))")  # creates a table online which has info regarding who is online
mydb.commit()    #commits the changes to db
mycursor.execute("create table messages(mno int(3),fro varchar(15),too varchar(15),message varchar(60))")  # creates a table messages which acts as a temporary buffer for to messages to stay
mydb.commit()    #commits the changes to db

root = Tk()     #initiates a root window where all the tkinter widgets are put
root.title("MESSENGER SERVER")
def stop_server():    # function to stop the server as it may show abnormal behaviour if we forcefully close it
    global run
    response=messagebox.askyesno("Warning!!!","Do you really wish to stop the server?")
    if response==1:
        mycursor.execute("drop database messaging")
        mydb.commit()
        root.destroy()

root.protocol('WM_DELETE_WINDOW', stop_server)

                         # we need two tables,online(shows the members who are online along with their connection details) and messages(has the messages)
header = 2048                                         # specifies the max no of bytes which can be transmitted via socket
port = 5050                                           # specifies the port through which communications take place
SERVER = socket.gethostbyname(socket.gethostname())   #gets the ip address of the localhost
addr = (SERVER, port)
format = 'utf-8'                                      # format by which messages are encoded
DISCONN_MSG = "!!!DISC!!!"                            #keyword for disconnecting a client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)                                     #connects to socket


def handle_client(conn, addr):                        #function to handle clients
    run=True
    msg = conn.recv(header).decode(format)            #receives and decrypts the message
    name=msg                                          #the first message send by the client will be its username
    if msg:
        command = "select count(*) from online where name like %s;", (name,)   #to check if there is anyone online with the same username
        mycursor.execute(*command)
        ans = mycursor.fetchall()
        a=int(str(ans)[2])
        if a==0:
            conn.send("APPROVED".encode(format))                               #if there is no one online ,then the connection is approved
            message="insert into online values(%s,%s);",(name,addr[0],)
            T.insert(END,name+" has connected via "+addr[0])
            mycursor.execute(*message)
            mydb.commit()
        elif a==1:
            conn.send("REJECTED".encode(format))                                #if someone is online,then the connection is rejected
            conn.close()
            run=False
            pass

    def name_checker(a, b):                                   #this is a function i made to check if a string is present in another string
        if a in b:
            return True
    def msg_forward(name,conn):                               # this is the function which repeatedly checks the database for any messages which are addressed to the given client
        while run:
            mycursor.execute("select too from messages")      #checks if there are any messages which are addressed to the particular client
            ans = mycursor.fetchall()
            if name_checker(name,str(ans)):
                command="select mno from messages where too like %s order by mno",(name,)          #the messages addressed to the client are ranked by which came first and their ranks are taken
                mycursor.execute(*command)
                ans = mycursor.fetchall()                                                          # if any such message is found the messages are ranked according to which came first
                queue=list(ans[0])                                                                 # their ranks are added to a list
                for i in queue:
                    command="select fro ,message from messages where too like %s and mno = %s",(name,str(i),)
                    mycursor.execute(*command)                                                    # the message and its senders name are taken to be forwarded to the client
                    ans = mycursor.fetchall()  # here ans is a tuple inside a list
                    conn.send((str(ans[0][0])+"@m:"+str(ans[0][1])).encode(format))               #the message and its senders name is forwarded to the client ,here '@m:' acts as a seperator between the name of the sender and the message
                    command="delete from messages where too like %s and mno = %s",(name,str(i),)  #once the message is send ,it is deleted from the database
                    mycursor.execute(*command)
                    mydb.commit()
            mycursor.execute("select name from online")                                              #finds the names of the clients who are online
            ans = mycursor.fetchall()
            online=[]
            for i in ans:
                s=str(i)
                l=len(s)
                count=0
                p=""
                for j in range(0,l):
                    if count ==1:
                        p+=s[j]
                    if s[j]=="'":
                        count+=1
                    if count==1 and s[j+1]=="'":
                        break
                online.append(p)
            conn.send(("@onl:"+str(online)).encode(format))                         #list of all online clients is forwarded to the particular client
            time.sleep(1)                                                           #waits 1 second before checking again
    t = threading.Thread(target=msg_forward,args=(name,conn))                       # declares a thread which handles message forwarding to this client while the rest of initial thread handles the messages which are send by our client
    t.start()                                                                       #starts the thread
    mno=1                                                                           #sets the rank of the first message as 1
    while run:
        msg = conn.recv(header).decode(format)                                      #listens for incoming messages from the client
        if msg:                                                                     # if a message is found ,it is added to the messages database
            for i in range(0,len(msg)-3):                                           # the loop ends at index len(msg)-3 because we know the message cant be nil
                if msg[i:i+3]=="@m:":
                    text,to=msg[i+3:],msg[:i]
                    insert_stmt = ("insert into messages(mno,fro,too,message)"    
                                   "values(%s,%s,%s,%s)")
                    data = (mno,name,to,text)
                    try:
                        mycursor.execute(insert_stmt, data)
                        mydb.commit()
                    except:
                        mydb.rollback()
            if msg==DISCONN_MSG:                                    # if the disconnect message is send by the client then the connection with the client is closed
                T.insert(END,"\n"+name+" has disconnected.\n")
                command = "delete from online where name like %s;", (name,)
                mycursor.execute(*command)
                mydb.commit()
                run=False
                conn.close()

        mno+=1                                              #updates the rank of the message


def main(): #main thread
    global T
    T = Text(root, height=18, width=48)                                            #text box to display data regarding the details of the connected clients
    T.pack()
    exit_button = Button(root, text="STOP SERVER", fg="red", command=stop_server)  #button to stop the server as if we forcefully close the server the database still remains and can cause trouble for the next instance
    exit_button.pack()
    T.insert(END, "[STARTING] server is starting...\n")
    server.listen()
    T.insert(END,f"[LISTENING] Server is listening on {SERVER}\n")

    def next():                                                #this thread accepts incoming clients and starts a thread for each client
        global T
        while True:
            conn, addr = server.accept()                       #accepts an incoming connection and takes their connection id and ip address
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()                                     #starts the handle client thread
            T.insert(END,f"[ACTIVE CONNECTIONS] {(threading.activeCount()-1)/2}\n")

    threading.Thread(target=next).start()                      # starts the listening process

    root.mainloop()                                            #starts the mainloop of the gui


main()
