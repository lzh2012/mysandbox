#严重警告:程序内路径最好都是相对路径,绝对路径的话换台电脑就不行了...

from game_info import *
#from mysandbox.lib.better_pygame import *
import mysandbox.lib.better_python as bp
#import mysandbox.lib.pycpp as pc
import mysandbox.lib.xes_api as xes_api
import mysandbox.lib.uploader as cdn
import mysandbox.lib.better_tkinter as bt

import sys
import random
import time
import pickle
import os
import tkinter

import pygame
import easygui


def r1b1c():
    global root
    root.destroy()
def r1b2c():
    global root,map_area,level,py
    p=easygui.fileopenbox()
    is_choose_file=True
    if p is None:
        is_choose_file=False
    else:
        with open(p,"rb") as f:
            l=pickle.load(f)
            try:#mysandbox a1.0_02+
                level=l["level"]
                py=l["player"]
            except:#mysandbox a1.0_01+
                level=l
            for r in range(len(level)):
                map_area[level[r][0]][level[r][1]].bid=level[r][2]
                map_area[level[r][0]][level[r][1]].img=blocki[level[r][2]]
    if is_choose_file:
        root.destroy()
def r1b3c():
    global root
    root2=tkinter.Toplevel()
    root2.geometry("512x256")
    root2.title("mysandbox help")

    p1=bt.TkImage("mysandbox/img/UI/bg/window_help.png")
    l1=tkinter.Label(root2,image=p1)
    l1.place(x=0,y=0)
    
    root2.mainloop()


root=tkinter.Tk()
root.geometry("512x256")
root.title("mysandbox")

p1=bt.TkImage("mysandbox/img/UI/bg/window_bg.png")
l1=tkinter.Label(root,image=p1)
l1.place(x=0,y=0)
b1=tkinter.Button(root,text="新的游戏",command=r1b1c)
b1.place(x=32,y=64)
b2=tkinter.Button(root,text="加载游戏",command=r1b2c)
b2.place(x=32,y=100)
b3=tkinter.Button(root,text="帮助",command=r1b3c)
b3.place(x=32,y=136)

root.mainloop()
del b1,b2,l1,b3,p1
#print(b1)

pygame.init()
screen=pygame.display.set_mode((12*64,12*64),pygame.RESIZABLE)
pygame.display.set_caption("mysandbox")#窗口名称
pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load('mysandbox/img/UI/MS.png'),(64,64)))#窗口图标
#pygame.mouse.set_visible(False)#隐藏窗口内鼠标
pygame.key.set_repeat(pygame.KEYDOWN,int(1),)#设置按键间隔
screen.fill((255,255,255))#染色画布

py=Point()

print_info=False
clock=pygame.time.Clock()
fps=100
puts_block=0
level=[]
down_high=0

def show_text(text,color=(0,0,0),pos=(0,0),size=30):
    global screen
    screen.blit(pygame.font.SysFont('kaiti', size).render((text),True,color),pos)
    
def printSystem(): 
    global screen
    psx=13#int(ssize[0]/64)#+int(py.x)#pygame_screen_x
    psy=13#int(ssize[1]/64)#+int(py.y)#pygame_screen_y
#    psx,psy=255,255
#    print(psx,psy)
    for j in range(psy):
        if j+py.y > -1 and j+py.y<256:
            for i in range(psx):
                if i+py.x > -1 and i+py.x <256:
                    screen.blit(map_area[i+int(py.x)][j+int(py.y)].img,(i*64-py.x%1*64,j*64-py.y%1*64))
        screen.blit(steve,(0,0))
#    for r in range(10)
#        if r==py.hp%2

def setBlock(x,y,i):
    global map_area
    map_area[x][y].bid=i
    map_area[x][y].img=blocki[i]

def getBlock(x,y):
    return map_area[x][y].bid

def createFilef(path):
    if not os.path.exists(path):
        os.makedirs(path)

def xround(n):
    return int(n+0.5)

#open_save=input("Open file?(y/n)")
#if open_save == "y":
#    with open("save.mslevel","rb") as f:
#        level=pickle.load(f)
#    for r in range(len(level)):
#        map_area[level[r][0]][level[r][1]].bid=level[r][2]
#        map_area[level[r][0]][level[r][1]].img=blocki[level[r][2]]

while True:
#    c=size=pygame.display.get_surface().get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit pygame...")
            pygame.mixer.music.stop()
            pygame.quit()
            print("Save world...")
            nam=easygui.enterbox(msg="请输入存档名称(输入_不存档)")
            createFilef("save")
            if nam == "_" or nam == None:
                print("Down!")
                sys.exit()
            with open("save/"+nam+".mslevel","wb") as f:
                pickle.dump({"player":py,"level":level},f,protocol=2)
            print("Down!")
#            print("Quit main...")
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == ord("w"):# or event.key == ord(" ") and getBlock(xround(py.x),int(py.y-1)) == 0:
#                _jump=True
                py.y-=0.01
            elif event.key == ord("a"):
                py.x-=0.003
            elif event.key == ord("s"):
                py.y+=0.003
            elif event.key == ord("d"):
                py.x+=0.003
            elif event.key == pygame.K_F3:
#                print("a")
                if print_info:
                    print_info=False
                else:
                    print_info=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
#            print(event.button)#1=左2=中3=右4=上滑5=下滑
            x, y = pygame.mouse.get_pos()
            x = int((x)//64)
            y = int((y)//64)
            if event.button == 1:
#                print(x,y,py.x,py.y)
                map_area[int(py.x)+x][int(py.y)+y].bid=0
                map_area[int(py.x)+x][int(py.y)+y].img=blocki[0]
                level.append((int(py.x)+x,int(py.y)+y,0))
            elif event.button == 3:
#                print(x,y,py.x,py.y)
                if map_area[int(py.x)+x][int(py.y)+y].bid==0:
                    map_area[int(py.x)+x][int(py.y)+y].bid=puts_block
                    map_area[int(py.x)+x][int(py.y)+y].img=blocki[puts_block]
                    level.append((int(py.x)+x,int(py.y)+y,puts_block))
            elif event.button == 4:
                if puts_block<1:
                    puts_block=len(block)-1
                else:
                    puts_block-=1
            elif event.button == 5:
                if puts_block>len(block)-1-1:
                    puts_block=0
                else:
                    puts_block+=1
    if pygame.mixer.music.get_busy() == False:#当前没有背景音乐
#        print("Aaa")
        pygame.mixer.music.load("mysandbox/sound/music/calm"+str(bp.rand(1,4,time.time()))+".ogg")#随机加载背景音乐
        pygame.mixer.music.play()#播放

    printSystem()
    if print_info:
        show_text("Mysandbox a1.1-pre1",size=28)
        show_text("xy:"+str(0-py.x)+" "+str(0-py.y),pos=(0,28),size=28)
        show_text(f"hp:{py.hp}",pos=(0,56),size=28)
#    print(int(py.x),int(py.y+1))
    if getBlock(xround(py.x),int(py.y+1)) == 0:
        py.y+=0.03
        down_high+=0.03
    else:
        if down_high>3:
            py.hp-=int(down_high-3)
        down_high=0
    screen.blit(blocki[puts_block],(12*64-32-64,32))
    pygame.display.update()
    screen.fill((255,255,255))
    clock.tick(fps)
