#-*-coding:utf-8-*-
import pygame,random,math,sys,time
from pygame.locals import *
pygame.init() #初始化 display,image,mix等模块
screen = pygame.display.set_mode((800,600))#设置窗口大小
pygame.display.set_caption("good time")#设置标题
background = pygame.image.load('images/timg1.jpg').convert()#导入图片
pic=pygame.image.load('images/block.png')
pic1=pygame.image.load('images/comb.png')
pic2=pygame.image.load('images/flame.png')
timer=pygame.time.Clock()#调用time模块的Clock函数来刷新运动
#-------------------设置变量------------------
speedx=1
speedy=1
flyx=1
flyy=1
#-------------------插入音乐------------------
pygame.mixer.music.load("music/botany1.mp3")
pygame.mixer.music.play(1000)
#------------------------定义方块类----------------------------
class Block(pygame.sprite.Sprite):
    scale=100
    pos=(0,0)
    xvel=1
    yvel=1
    def __init__(self,pos,speedx,speedy):#构造函数
        pygame.sprite.Sprite.__init__(self)#继承
        self.image=pic#导入图片
        self.scale=random.randint(20,100)#随机
        self.image=pygame.transform.smoothscale(self.image,(self.scale,self.scale))#一个快速的缩放函数
        self.rect=self.image.get_rect()#用一个矩形框起
        self.pos=pos #位置
        self.rect.x=self.pos[0]-self.rect.width/2 #位置在中心
        self.rect.y=self.pos[1]-self.rect.height/2
        self.xvel=speedx
        self.yvel=speedy
    def update(self):
        self.rect.x+=self.xvel#每次增加一点，移动
        self.rect.y+=self.yvel
        if self.rect.x <= 0 or self.rect.x + self.scale>=800: #碰壁反弹
            self.xvel=-self.xvel
        if self.rect.y <= 0 or self.rect.y + self.scale >=470:
            self.yvel=-self.yvel    
#---------------------------------定义炸弹类--------------------------        
class Bomb(pygame.sprite.Sprite):
    scale=100
    pos=(0,0)
    xvel=1
    yvel=1
    def __init__(self,pos,speedx,speedy):#构造函数
        pygame.sprite.Sprite.__init__(self)#继承
        self.image=pic1#导入图片
        self.scale=random.randint(30,80)#随机
        self.image=pygame.transform.smoothscale(self.image,(self.scale,self.scale))#一个快速的缩放函数
        self.rect=self.image.get_rect()#用一个矩形框起
        self.pos=pos #位置
        self.rect.x=self.pos[0]-self.rect.width/2 #位置在中心
        self.rect.y=self.pos[1]-self.rect.height/2
        self.xvel=speedx
        self.yvel=speedy
    def update(self):
        self.rect.x+=self.xvel#每次增加一点，移动
        self.rect.y+=self.yvel
        if self.rect.x <= 0 or self.rect.x + self.scale>=800: #碰壁反弹
            self.xvel=-self.xvel
        if self.rect.y <= 0 or self.rect.y + self.scale >=470:
            self.yvel=-self.yvel          
# ------------------------------------------序列图精灵类-----------------------------
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #扩展基本sprite类
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0,0.0) 
    #X property
    def _getx(self):
        return self.rect.x
    def _setx(self,value):
        self.rect.x = value
    X = property(_getx,_setx)
    #Y property
    def _gety(self):
        return self.rect.y
    def _sety(self,value):
        self.rect.y = value
    Y = property(_gety,_sety)
    #position property
    def _getpos(self):
        return self.rect.topleft
    def _setpos(self,pos):
        self.rect.topleft = pos
    position = property(_getpos,_setpos)
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1
    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame
    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)
#Point class
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    #X property
    def getx(self):
        return self.__x
    def setx(self, x):
        self.__x = x
    x = property(getx, setx)
    #Y property
    def gety(self):
        return self.__y
    def sety(self, y):
        self.__y = y
    y = property(gety, sety)
    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"
#-----------------------------定义子弹类-----------------------------------
class Flame(pygame.sprite.Sprite):
    pos=(0,0)
    xvel=1
    yvel=1
    def __init__(self,pos,speedx,speedy):#构造函数
        pygame.sprite.Sprite.__init__(self)#继承
        self.image=pic2#导入图片
        self.image=pygame.transform.smoothscale(self.image,(12,30))
        self.rect=self.image.get_rect()#用一个矩形框起
        self.pos=pos #位置
        self.rect.x=player.X + 40
        self.rect.y=player.Y
        self.xvel=speedx
        self.yvel=speedy
    def update(self):
        self.rect.y-=self.yvel
        #self.rect.x=player.X
        if self.rect.y <= 0:
            clicked_smiley=[]
            pos=self.rect.x,self.rect.y   #子弹位置
            for i in sprite_list:          #遍历精灵组列表
                if i.rect.collidepoint(pos):  
                    clicked_smiley+=[i]
            player_group1.remove(clicked_smiley)            
#--------------------------------------------------------------------------
def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #north
        velocity.y = -vel
    elif direction == 2: #east
        velocity.x = vel
    elif direction == 4: #south
        velocity.y = vel
    elif direction == 6: #west
        velocity.x = -vel
    return velocity
#--------------------------------------------------------------------------
def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2
#------------------------定义gameOver函数-----------------------------------
greyColour = pygame.Color(150,150,150)
def gameOver(screen):
    gameOverFont = pygame.font.SysFont("Times",50,italic=False)
    gameOverSurf = gameOverFont.render('Hit a bomb,Game Over',True,greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (380,240)
    screen.blit(gameOverSurf,gameOverRect)
    pygame.display.flip()
    time.sleep(30)
    pygame.quit()
    sys.exit()
#------------------------定义Pass函数-----------------------------------  
greyColour1 = pygame.Color(0,0,255)
def Pass(screen):
    gameOverFont = pygame.font.SysFont("Times",50,italic=False)
    gameOverSurf = gameOverFont.render('Pass through',True,greyColour1)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (380,240)
    screen.blit(gameOverSurf,gameOverRect)
    pygame.display.flip()
    time.sleep(30)
    pygame.quit()
    sys.exit()   
#---------------------------定义精灵组-------------------------------------
sprite_list = pygame.sprite.Group()#方块精灵组对象，列表
sprite_list1 = pygame.sprite.Group()#炸弹精灵组对象，列表
player_group = pygame.sprite.Group()#小人精灵组对象，列表
player_group1 = pygame.sprite.Group()#子弹精灵组对象，列表
#----------------------------创建小人精灵----------------------------------
player = MySprite()
player.load("images/farmer.png", 96, 96, 8)
player.position = 0, 500
player.direction = 4
#----------------主程序---------------------           
keep_going=True
flag=False
game_over = False
arrow_vel = 8.0
b=0
n=0
score=0
hot=False
while keep_going:
    timer.tick(30)
    ticks = pygame.time.get_ticks()
    #获取事件
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            keep_going=False
        #----------------------------控制小人方向--------------------------
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player.direction = 0
            player_moving = True
        elif keys[K_RIGHT]:
            player.direction = 2
            player_moving = True
        elif keys[K_DOWN]:
            player.direction = 4
            player_moving = True
        elif keys[K_LEFT]:
            player.direction = 6
            player_moving = True
        elif keys[K_SPACE]:
            hot=False
            yx=pygame.mixer.Sound("music/touch.wav")
            yx.play()
        else:
            player_moving = False      
    if not game_over:
            #set animation frames based on player's direction
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        if not player_moving:
            #stop animating when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            #move player in direction 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 3
            player.velocity.y *= 3
        #update player sprite
        player_group.update(ticks, 50)
         #manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0:
                player.X = 0
            elif player.X > 700:
                player.X = 700
            if player.Y < 400:
                player.Y = 400
            elif player.Y > 500:
                player.Y = 500
    #---------------------填充背景----------------------------------------------    
    screen.blit(background,(0,0))
    #--------------调用函数方块-----------------------
    if n<=200:
        speedx=random.randint(1,10)
        speedy=random.randint(1,5)
        x=random.randint(100,700)
        y=random.randint(100,400)
        newsmile1=Block((x,y),speedx,speedy)
        n+=1
    #----------------调用函数4个炸弹-----------------------
    if b<=3:
        speedx=random.randint(1,6)
        speedy=random.randint(1,5)
        x=random.randint(100,700)
        y=random.randint(100,400)
        newsmile2=Bomb((x,y),speedx,speedy)
        b+=1
    #-----------------调用函数子弹------------
    if hot==False:
        flyx=10
        flyy=10
        newsmile3=Flame((0,0),flyx,flyy)
        hot=True
#--------------------------------边缘检测-----------------------------------------
    collide=pygame.sprite.groupcollide(sprite_list,player_group1,True,False)
    if collide:
        score+=1
    fontobj=pygame.font.SysFont("Times",20,italic=False)
    text_score="score:" + str(score) 
    text=fontobj.render(text_score,True,(255,255,255))
    text_rect=text.get_rect()
    text_rect.top=560
    text_rect.centerx=screen.get_rect().centerx
    screen.blit(text,text_rect)
    if score==199:
        Pass(screen)
#--------------------------------边缘检测-----------------------------------------
    collide1=pygame.sprite.groupcollide(sprite_list1,player_group1,True,False)
    if collide1:
        gameOver(screen)
    fontobj=pygame.font.SysFont("stkaiti",20,italic=False)
    text_score=u"上下左右控制小人，按下一次空格键小人发射一枚子弹，碰到炸弹则输。由22组原创。"
    text=fontobj.render(text_score,True,(255,255,255))
    text_rect=text.get_rect()
    text_rect.top=575
    text_rect.centerx=screen.get_rect().centerx
    screen.blit(text,text_rect)  
    #------画方块-------------
    sprite_list.add(newsmile1)    
    sprite_list.update()
    sprite_list.draw(screen)
    #------画炸弹--------------
    sprite_list1.add(newsmile2)    
    sprite_list1.update()
    sprite_list1.draw(screen)
    #------画小人-------------
    player_group.add(player)
    player_group.update(ticks)
    player_group.draw(screen)
    #------画子弹------------
    player_group1.add(newsmile3)
    player_group1.update()
    player_group1.draw(screen)
    #更新屏幕
    pygame.display.update()
    timer.tick(60)
#结束
pygame.quit()


