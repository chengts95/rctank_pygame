import time

import numpy as np
import pygame
from pygame.locals import *

from udplib import UDP
try:
    from rc_cmd import speed_cmd
except ImportError:
    print("using python encoder")
    from cmds import speed_cmd

def show_text(surface_handle, pos, text, color, font_bold = False, font_size = 13, font_italic = False):   
    ''''' 
    Function:文字处理函数 
    Input：surface_handle：surface句柄 
           pos：文字显示位置 
           color:文字颜色 
           font_bold:是否加粗 
           font_size:字体大小 
           font_italic:是否斜体 
    Output: NONE 
    author: socrates 
    blog:http://blog.csdn.net/dyx1024 
    date:2012-04-15 
    '''         
    #获取系统字体，并设置文字大小  
    cur_font = pygame.font.SysFont("宋体", font_size)  
      
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)  
      
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)  
      
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
      
    #绘制文字  
    surface_handle.blit(text_fmt, pos)    

speed_table={
    b'w':lambda x,y:( x,y+1 ),
    b'a':lambda x,y: (x-1,y),
    b's':lambda x,y: (x,y-1),
    b'd':lambda x,y: (x+1,y)
}
MODIFIER=1
MAX_SPEED=140
MAX_ANGLE=90
MAX_SPEED*=MODIFIER
MAX_ANGLE*=MODIFIER
def get_trackspeed(x,y):
    l1=y
    x1=x
    if y>0:
        if x>0:
            if y+x>MAX_SPEED:
                l1=MAX_SPEED-x
        else:
            if y-x>MAX_SPEED:
                l1=MAX_SPEED+x
        y1=l1
    else:
        if x>0:
            if y-x<-MAX_SPEED:
                l1=-MAX_SPEED+x
        else:
            if y+x<-MAX_SPEED:
                l1=-MAX_SPEED-x
        y1=l1
        
    # x1=y*np.sin(np.radians(x))
    # l1=0
    # if y>0:
    #     if x1>0:
    #         l1=y-x1
    #     else:
    #         l1=y+x1
    #     y1=l1
    # else:
    #     if x1>0:
    #         l1=y+x1
    #     else:
    #         l1=y-x1
    #     y1=l1
    return int((x1+y1)/2),int((y1-x1)/2)

def cal_speed(cmd,x_speed,y_speed):
    for i in cmd:

        f=speed_table.get(bytes(chr(i),'utf-8'))
        if f:
            x_speed,y_speed=f(x_speed,y_speed)
        else:
            return 0,0

    if x_speed>MAX_ANGLE:
        x_speed=MAX_ANGLE

    if x_speed<-MAX_ANGLE:
        x_speed=-MAX_ANGLE

    l1=y_speed
    if y_speed>0:
        if x_speed>0:
            if y_speed+x_speed>MAX_SPEED:
                l1=MAX_SPEED-x_speed
        else:
            if y_speed-x_speed>MAX_SPEED:
                l1=MAX_SPEED+x_speed
        
    else:
        if x_speed>0:
            if y_speed-x_speed<-MAX_SPEED:
                l1=-MAX_SPEED+x_speed
        else:
            if y_speed+x_speed<-MAX_SPEED:
                l1=-MAX_SPEED-x_speed
    y_speed=l1
    



    return x_speed,y_speed


if __name__ == "__main__":
        pygame.init()
        l_speed,r_speed=0,0
        x_speed,y_speed=0,0
        over = False

        u = UDP(9000)

        clock = pygame.time.Clock()
        key = np.zeros(323)
        screen_width, screen_height = 600, 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        diff=0
        while not over:
            diff+=1

            clock.tick(200)
            key[:] = pygame.key.get_pressed()

            cmd = b''
            if key.any():
                if key[K_w]:
                    cmd += b'w'
                if key[K_a]:
                    cmd += b'a'
                    if x_speed>0:
                        x_speed=0
                if key[K_s]:
                    cmd += b's'

                if key[K_d]:
                    cmd += b'd'
                    if x_speed<0:
                        x_speed=0
                if key[K_h]:
                    cmd += b'h'
                x_speed,y_speed=cal_speed(cmd,x_speed,y_speed)

            else:
                x_speed=0



            l_speed,r_speed=get_trackspeed(x_speed,y_speed)
            if diff == 8:
                diff=0
                screen.fill((0, 0, 0)) 
                show_text(screen, (0, 20), "X:%d"%(x_speed), (255, 255, 0), True, 20)  
                show_text(screen, (100, 20), "Y:%d"%(y_speed), (255, 255, 0), True, 20)  
                show_text(screen, (0, 40), "left:%d"%(l_speed), (255, 255, 0), True, 20)  
                show_text(screen, (100, 40), "right:%d"%(r_speed), (255, 255, 0), True, 20) 
                pygame.display.flip()  
            cmd=speed_cmd(l_speed,r_speed)
            u.send(cmd)
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    over = True
                    u.send(speed_cmd(0,0))
