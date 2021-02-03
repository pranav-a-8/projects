import socket
from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image,ImageTk

global state,gtype,gamesign,local,online,blab,render
state=[0,0,0,0,0,0,0,0,0]
gamesign={0:" ",1:"X",2:"O"}


root=Tk()
root.geometry("300x297")
img=Image.open("C:/Users/manu/PycharmProjects/pythonProject/ticpic.jpg")
local=PhotoImage(file="C:/Users/manu/Pictures/local1.png")
online=PhotoImage(file="C:/Users/manu/Pictures/online1.png")
render=ImageTk.PhotoImage(img)

myfont = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)

def evaluate():
    global state
    for row in range(0,3):
        if state[row*3]==state[row*3+1] and state[row*3]==state[row*3+2]:
            if state[row*3]==1:
                return -10
            elif state[row*3]==2:
                return 10
    for col in range(0,3):
        if state[col]==state[col+3] and state[col+6]==state[col+3]:
            if state[col]==1:
                return -10
            elif state[col]==2:
                return 10
    if state[0]==state[4] and state[4]==state[8] :
        if state[0] == 1:
            return -10
        elif state[0] == 2:
            return 10
    elif state[2]==state[4] and state[4]==state[6]:
        if state[2] == 1:
            return -10
        elif state[2] == 2:
            return 10
    return 0
def IsMovesLeft():
    global state
    for i in state:
        if i==0:
            return True
    return False
def minimax(depth,IsMaximisingPlayer):
    score=evaluate()
    if score==10:
        return 10
    elif score==-10:
        return -10
    if not IsMovesLeft():
        return 0
    if IsMaximisingPlayer:
        bestval=-1000
        for i in range(0,9):
            if state[i]==0:
                state[i]=2
                value=minimax(depth-1,False)
                bestval=max(bestval,value-depth)
                state[i]=0
        return bestval
    elif not IsMaximisingPlayer:
        bestval=1000
        for i in range(0,9):
            if state[i]==0:
                state[i]=1
                value=minimax(depth-1,True)
                bestval=min(bestval,value-depth)
                state[i]=0
        return bestval

def FindBestMove():
    bestval=-1000
    bestmove=0
    for i in range(0,9):
        if state[i]==0:
            state[i]=2
            moveval=minimax(0,False)
            state[i]=0
            if moveval > bestval:
                bestval = moveval
                bestmove = i
    return bestmove

def start():
    global gtype, b0, b1, b2, b3, b4, b5, b6, b7, b8,lab
    bc="white"
    fc="black"
    py=0
    px=18
    b0 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(0),font=myfont)
    b0.grid(row=0, column=0)
    b1 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(1),font=myfont)
    b1.grid(row=0, column=1)
    b2 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(2),font=myfont)
    b2.grid(row=0, column=2)
    b3 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(3),font=myfont)
    b3.grid(row=1, column=0)
    b4 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(4),font=myfont)
    b4.grid(row=1, column=1)
    b5 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(5),font=myfont)
    b5.grid(row=1, column=2)
    b6 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(6),font=myfont)
    b6.grid(row=2, column=0)
    b7 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(7),font=myfont)
    b7.grid(row=2, column=1)
    b8 = Button(root, text=' ', bg=bc, fg=fc, padx=px, pady=py, command=lambda:fun(8),font=myfont)
    b8.grid(row=2, column=2)
    lab = Label(root)
    lab.grid(row=3, column=0, columnspan=3)
    lab.config(text="Players Turn")

def hideall():
    global b0, b1, b2, b3, b4, b5, b6, b7, b8,lab
    b0.grid_forget()
    b1.grid_forget()
    b2.grid_forget()
    b3.grid_forget()
    b4.grid_forget()
    b5.grid_forget()
    b6.grid_forget()
    b7.grid_forget()
    b8.grid_forget()
    lab.grid_forget()

def fun(x):
    global state
    global b0, b1, b2, b3, b4, b5, b6, b7, b8
    px=7
    if x == 0:
        b0.config(text='X', state=DISABLED,padx=px)
    elif x == 1:
        b1.config(text='X', state=DISABLED,padx=px)
    elif x == 2:
        b2.config(text='X', state=DISABLED,padx=px)
    elif x == 3:
        b3.config(text='X', state=DISABLED,padx=px)
    elif x == 4:
        b4.config(text='X', state=DISABLED,padx=px)
    elif x == 5:
        b5.config(text='X', state=DISABLED,padx=px)
    elif x == 6:
        b6.config(text='X', state=DISABLED,padx=px)
    elif x == 7:
        b7.config(text='X', state=DISABLED,padx=px)
    elif x == 8:
        b8.config(text='X', state=DISABLED,padx=px)
    state[x] = 1
    if evaluate() == -10:
        resp = messagebox.askyesno("GAME OVER", "CONGRATS!!! YOU WON \n Do you wish to play again")
        if resp == 1:
            state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            hideall()
            main()

        else:
            root.destroy()
    elif not IsMovesLeft():
        resp = messagebox.askyesno("GAME OVER", " OH NO! ITS A TIE \n Do you wish to play again")
        if resp == 1:
            state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            hideall()
            main()
        else:
            root.destroy()
    y = FindBestMove()
    state[y] = 2
    if y == 0:
        b0.config(text='O', state=DISABLED,padx=px)
    elif y == 1:
        b1.config(text='O', state=DISABLED,padx=px)
    elif y == 2:
        b2.config(text='O', state=DISABLED,padx=px)
    elif y== 3:
        b3.config(text='O', state=DISABLED,padx=px)
    elif y == 4:
        b4.config(text='O', state=DISABLED,padx=px)
    elif y == 5:
        b5.config(text='O', state=DISABLED,padx=px)
    elif y == 6:
        b6.config(text='O', state=DISABLED,padx=px)
    elif y == 7:
        b7.config(text='O', state=DISABLED,padx=px)
    elif y == 8:
        b8.config(text='O', state=DISABLED,padx=px)

    if evaluate() == 10:
        resp = messagebox.askyesno("GAME OVER", "HAH, YOU ARE A LOSER !!!,\n Do you wish play again")
        if resp == 1:
            state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            hideall()
            main()
        else:
            root.destroy()
    elif not IsMovesLeft():
        resp = messagebox.askyesno("GAME OVER", " OH NO! ITS A TIE \n Do you wish to play again")
        if resp == 1:
            state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            hideall()
            main()
        else:
            root.destroy()






def playoffline():
    global gtype,uname,onl_but,ofl_but,blab
    root.geometry("279x309")
    gtype = "offline"
    blab.place_forget()
    uname.place_forget()
    onl_but.place_forget()
    ofl_but.place_forget()
    response = messagebox.askquestion("Do you wish to play first")
    if response =="yes":
        start()
    else:
        start()
def playonline():
    messagebox.showinfo("UNDER DEVELOPMENT","Sorry,This part of the game is under development,please contact the Devs to know more info")

def main():
    global gtype, uname,local,online,onl_but,ofl_but,blab,render
    blab = Label(root, image=render)
    blab.place(x=0, y=0)

    uname=Entry(root,text="USERNAME")
    uname.place(x=100,y=0)
    onl_but=Button(root,image=online,command=playonline,bd=0)
    onl_but.place(x=25,y=175)
    ofl_but=Button(root,image=local,command=playoffline,bd=0)
    ofl_but.place(x=175,y=175)

main()
root.mainloop()
