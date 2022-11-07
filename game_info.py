import mysandbox.lib.perlin as perlin

import pygame

import sys
import time
import random

#void:可穿过
#ore:可烧制
#open:可打开
#fuel:可燃烧,可当燃料
#seed:可种植植物
#plant:可生长
#food:可食用


block=\
[
    ["  ","空气","255;255;255",["void"],1,64],#显示符 名称 颜色 特性 硬度 堆叠限制
    ["石","圆石","70;70;70",["ore"],3,10],
    ["炉","熔炉","50;50;50",["open","ore"],2,10],#是的,熔炉是可以被烧制回石头的
    ["煤","煤炭","0;0;0",["fuel"],2,64],
    ["石","石头","100;100;100",["ore"],3,10],
    ["工","工作台","200;200;0",["fuel","open"],2,10],
    ["草","草方块","0;200;0",[],1,64],
    ["板","木板","200;200;0",["fuel"],2,10],
    ["叶","树叶","0;255;0",["fuel"],1,3],
    ["木","木头","200;200;0",["fuel"],2,10],
    ["地","耕地","100;100;0",["seed"],1,64],
    ["种","种子","200;0;0",["plant"],1,64],
    ["麦","小麦","200;200;0",["food"],1,64],
    ["泥","泥土","",[],1,64]
]
#blocki=[pygame.image.load("mysandbox/img/blocks/block_0.png"),pygame.image.load("mysandbox/img/blocks/block_no_texture.png")]
#blocki[0]=pygame.transform.scale(blocki[0],(64,64))
#blocki[1]=pygame.transform.scale(blocki[1],(64,64))
blocki=\
[
    pygame.image.load("mysandbox/img/blocks/air.png"),
    pygame.image.load("mysandbox/img/blocks/cobblestone.png"),
    pygame.image.load("mysandbox/img/blocks/furnace_front_off.png"),
    pygame.image.load("mysandbox/img/blocks/coal_ore.png"),
    pygame.image.load("mysandbox/img/blocks/stone.png"),
    pygame.image.load("mysandbox/img/blocks/crafting_table_side.png"),
    pygame.image.load("mysandbox/img/blocks/grass_side.png"),
    pygame.image.load("mysandbox/img/blocks/planks_oak.png"),
    pygame.image.load("mysandbox/img/blocks/new_leaves.png"),
    pygame.image.load("mysandbox/img/blocks/log_oak.png"),
    pygame.image.load("mysandbox/img/blocks/farmland_dry.png"),
    pygame.image.load("mysandbox/img/blocks/wheat_stage_0.png"),
    pygame.image.load("mysandbox/img/blocks/wheat_stage_7.png"),
    pygame.image.load("mysandbox/img/blocks/dirt.png")
]
entityi=\
[
    
]
sounds=\
[
#    sound("")
]
for i in range(len(blocki)):
    blocki[i]=pygame.transform.scale(blocki[i],(64,64))
for i in range(len(entityi)):
    entityi[i]=pygame.transform.scale(entityi[i],(64,64))
entity=\
[
    ["??","未知","255;255;0",["void"],32767,32767],
    ["猪","猪","235;0;0",[],2,2],
    ["村,民","村民-0","100;100;0,100;100;0",["open","big"],20,2]#TOD
]
ore=\
[
    [1,4,1],#什么 烧制成什么 燃料数量 烧制数量
    [2,4,1],
    [4,0,1]
]
crafting=\
[
    [
        1,1,1,\
        1,1,1,\
        1,1,1,\
        2,1#9*圆石->熔炉*1
    ],#1,2,3,4,5,6,7,8,9,合成成什么,一次合成数量
    [
        0,7,0,\
        0,7,0,\
        0,7,0,\
        len(block)-1+1,1#3*木板->木锹*1
    ],
    [
        0,0,0,\
        0,9,0,\
        0,0,0,\
        7,4#1*木头->木板*4
    ]
]
item=\
[
    ["锹","木锹","0;0;0",["fuel"],3,16]#显示字符 名称 颜色 特性 耐久 堆叠限制
]

steve=pygame.image.load("mysandbox/img/entities/steve.png")
#print(type(steve))
steve=pygame.transform.scale(steve,(64,64))

brick_block=pygame.image.load("mysandbox/img/blocks/brick.png")
grass_block=pygame.image.load("mysandbox/img/blocks/grass_side.png")
air_block=pygame.image.load("mysandbox/img/blocks/air.png")
brick_block=pygame.transform.scale(brick_block,(64,64))
grass_block=pygame.transform.scale(grass_block,(64,64))
air_block=pygame.transform.scale(air_block,(64,64))

def clear():
    cout<<"\033c"

def xround(n):
    return int(0.5+n)

class Inventory:
    def __init__(self,x,y,max_):
        self.x=x
        self.y=y
        self.inventory=[[0]*self.x for i in range(self.y)]
        self.damage=[[0]*self.x for i in range(self.y)]
        self.num=[[0]*self.x for i in range(self.y)]
        if max_ == -1:
            self.max_ = -1
        elif max_ == -2:
            self.max_ = 65535
    def push(self,i):#存进
        for f in range(self.x):#存在且在堆叠限制以内
            for r in range(self.y):
#                print(r,f)
                if self.inventory[r][f] == i and self.num[r][f] < self.max_ if self.max_ != -1 else block[i][6]:
                    self.num[r][f]+=1
                    return
        for f in range(self.x):#背包内不存在该物品
            for r in range(self.y):
                if self.inventory[r][f] == 0 and self.num[r][f] < self.max_ if self.max_ != -1 else block[i][6]:
                    self.inventory[r][f] = i
                    self.num[r][f]+=1
                    return
        return "full"#背包满了
    def pull(self,i):#取出
        for f in range(self.x):#存在
            for r in range(self.y):
#                print(r,f)
                if self.inventory[r][f] == i and self.num[r][f] > 0:
                    self.num[r][f]-=1
                    if self.num[r][f] == 0:
                        self.inventory[r][f] = 0
                    return
        return "lack"
    def printI(self):
        for f in range(self.x):
            for r in range(self.y):
                print(str(self.inventory[r][f])+"*"+str(self.num[r][f])+"_"+str(self.damage[r][f]),end=" ")
#            print("\n----------------")
            print()
        print("----------------")

class Point:
    def __init__(self,x=0,y=0,r=4,f=9,max_=-1,hp=20):
        self.x=x
        self.y=y
        self.inventory=Inventory(r,f,max_)
        self.hp=hp
        
class Block:
    def __init__(self,img,iid):
        self.img=img
        self.bid=iid
        self.rect=self.img.get_rect()
        self.mask=pygame.mask.from_surface(self.img)
pp=perlin.noise1d(4,3,256,256)
#print(len(pp))
#print(pp)
map_area=[]
for i in range(256):
    aa=[]
    for j in range(256):
        aa.append(Block(blocki[0],0))
    map_area.append(aa)
    aa=[]
for i in range(256):
    for j in range(xround(pp[i])):
        map_area[i][j]=Block(grass_block,6)
#del aa
#print(map_area[0][1].bid)
#map_area[0][0].bid=0
#print(map_area[0][1].bid)
