import pygame
import threading
import random
import time
from pygame.locals import *
################################################################################
# pygame starts here
pygame.mixer.init()
pygame.init()
pygame.time.set_timer(USEREVENT+1,5000)
################################################################################
#color
white=[255,255,255]
black=[0,0,0]
red=[255,0,0]
brown=[51,25,0]

################################################################################
pygame.mixer.music.load('song.mp3')
################################################################################
display_width=1000
extra_display_height=100
display_height=305
lead_x_change=0
lead_y_change=0
wall_pos=[]
ladder_pos=[]
broken_ladder_pos=[]
coin_pos=[]
fire_ball=[]
width_border=5
coin_width=15
man_width=15
man_height=25
queen_width=35
queen_height=45
donkey_width=15
donkey_height=30
donkey_speed=5
height=60
block_size=12 # for fire balls
coin_count=0
speed_ball=4
jump_speed=-7
jump_val=False
gameExit=False
speed=5
min_gap=25
FPS=30
level=0
ladder_width=20
font=pygame.font.SysFont(None,40)
gameDisplay=pygame.display.set_mode((display_width,display_height+extra_display_height))
clock=pygame.time.Clock()

################################################################################
def text_objects(text,color):
	textSurface=font.render(text,True,color)
	return textSurface,textSurface.get_rect()

def message_to_screen(msg,x,y):
	textSurf,textRect= text_objects(msg,red)
	textRect.center=(x,y)
	gameDisplay.blit(textSurf,textRect)
	#pygame.display.update()
################################################################################
def sleep(msg,x,y,s,t):
	gameDisplay.fill(white)
	message_to_screen(msg,x,y)
	if s!=-1:
		message_to_screen(str("Your score is:"+str(s*5)),x,y+30)
	pygame.display.update()
	time.sleep(t)
################################################################################
class Person():
	score=0
	life = 3
	lead_x=width_border+man_width
	lead_y=6*height-man_height
	def attack(self,x):
		global level,jump_speed,jump_val,fire_ball,coin_count
		fire_ball=[]
		jump_val=False
		jump_speed=0
		level=0
		self.lead_x=width_border+man_width
		self.lead_y=6*height-man_height
		self.life-=1
		if self.score>=5 and x==1:
			self.score-=5
			coin_count-=5
		if x!=0 and self.life!=0:
			sleep("You are caught",display_width/2,(display_height+extra_display_height)/2,self.score,2)
		if self.life==0:
			sleep("Game over",display_width/2,(display_height+extra_display_height)/2,self.score,2)
	def score_increase(self):
		self.score+=1
	def caught_queen(self):
		global coin_count,FPS,speed_ball,donkey_speed,speed
		speed_ball+=2
		speed+=2
		donkey_speed+=2
		self.score+=10
		coin_count+=10
		sleep("You had succeded",display_width/2,(display_height+extra_display_height)/2,self.score,2)
		self.life+=1
	 	self.attack(0)
	def check_life(self):
		if self.life<=0:
			print("YOU ARE FINISHED.")
		else:
			print(str(self.life)+'life left')
	def move_left(self):
		global lead_x_change
		self.lead_x+=lead_x_change
	def move_right(self):
		global lead_x_change
		self.lead_x+=lead_x_change
	def jump(self):
		self.lead_y+=jump_speed
	def collision_wall(self):
		global lead_x_change,lead_y_change
		if self.lead_x<width_border:
			lead_x_change=0
			lead_y_change=0
			self.lead_x+=5
	       	elif self.lead_x>display_width-4*width_border:
			lead_x_change=0
			lead_y_change=0
			self.lead_x-=7
		if self.lead_y<width_border:
			lead_x_change=0
			lead_y_change=0
			self.lead_y+=4
		elif self.lead_y>6*height:#display_height-2*width_border:
			lead_x_change=0
			lead_y_change=0
			self.lead_y-=4
	def print_data(self):
		global coin_count
		self.score=coin_count
		message_to_screen(str("SCORE:"+str(self.score*5)),14*width_border,display_height+extra_display_height-4*width_border)
		message_to_screen(str("LIFES:"),display_width/2,display_height+extra_display_height-4*width_border)
		life_imgage=pygame.image.load('life.png')
		life_imgage1=pygame.transform.scale(life_imgage,(30,30))
		for i in range(self.life):
			gameDisplay.blit(life_imgage1,(display_width/2+(i+1)*50,display_height+extra_display_height-4*width_border-18))
#gameExit=True
################################################################################
class Player(Person):
	def Player_position(self):
		return (self.lead_x,self.lead_y)
	def move_up(self):
		global level,ladder_pos
		if ladder_pos[4-level]<=self.lead_x<ladder_pos[4-level]+min_gap:
			level+=1
			self.lead_y-=height
	def move_down(self):
		global level,ladder_pos
		if level>0 and ladder_pos[5-level]<=self.lead_x<ladder_pos[5-level]+min_gap:
			level-=1
			self.lead_y+=height
	def player_display(self):
		man_image=pygame.image.load('man.png')
		man_image1=pygame.transform.scale(man_image,(man_width,man_height))
		gameDisplay.blit(man_image1,(self.lead_x,self.lead_y))
################################################################################
class Donkey(Person):
	def position(self):
		pass
	def player_display(self):
		self.lead_y=height-donkey_height
		donkey_imgage=pygame.image.load('donkey.png')
		donkey_imgage1=pygame.transform.scale(donkey_imgage,(donkey_width,donkey_height))
		gameDisplay.blit(donkey_imgage1,(self.lead_x,self.lead_y))
################################################################################
class Board():
#a=""
	def floor(self): #for randonmly creating floor
		global wall_pos
		wall_pos=[]
		for i in range(5):
			if i>=1:
				if i%2==0:
					c=random.randrange(display_width/2+min_gap,display_width-min_gap)
				else:
					c=random.randrange(min_gap,display_width/2)
			else:
					c=random.randrange(display_width/2+min_gap,display_width-min_gap-150)

			wall_pos.append(c)
	def ladder(self):
		global ladder_pos
		ladder_pos=[]
		for i in range(5):
			if i>=1:
				if i%2==0:
					c1=random.randrange(ladder_width,display_width/2)
				else:
					c1=random.randrange(display_width/2+ladder_width,display_width-3*ladder_width)
				c=wall_pos[i-1]
				if i<4:
					d=wall_pos[i+1]
				else:
			 		d=c
				while (c-min_gap<c1<=c+min_gap) or (d-min_gap<c1<=d+min_gap) or (i>0 and ladder_pos[i-1]<=c1<=ladder_pos[i-1]+ladder_width):
					if i%2==0:
						c1=random.randrange(ladder_width,display_width/2)
					else:
						c1=random.randrange(display_width/2+ladder_width,display_width-3*ladder_width)
			else:
					c1=random.randrange(display_width/4,display_width/2)
					while wall_pos[0]-min_gap<=c1<=wall_pos[0]+min_gap:
						c1=random.randrange(display_width/4,display_width/2)
			ladder_pos.append(c1)
	def broken_ladder(self):
		global broken_ladder_pos
		broken_ladder_pos=[]
		for i in range(5):
			if ladder_pos[i]>=display_width/2:
				c1=random.randrange(ladder_width,display_width/2)
			else:
				c1=random.randrange(display_width/2+ladder_width,display_width-ladder_width)
			c=wall_pos[i]
			if i<4:
				d=wall_pos[i+1]
			else:
			 	d=c
			while (c-min_gap<c1<=c+min_gap) or (d-min_gap<c1<=d+min_gap) or (i>0 and c1==ladder_pos[i-1]) or ladder_pos[i]-ladder_width<=c1<=ladder_pos[i]+ladder_width or (i>0 and c1==broken_ladder_pos[i-1]):
				c1=random.randrange(ladder_width,display_width-ladder_width)
			broken_ladder_pos.append(c1)
	def coin(self):
		global coin_pos
		coin_pos=[]
		for i in range(5):
			c1=random.randrange(ladder_width,display_width/2)
			c2=random.randrange(display_width/2+coin_width,display_width-coin_width-width_border)
			coin_pos.append(c1)
			coin_pos.append(c2)
	def fill_borders(self):
		ladder_image=pygame.image.load('ladder.jpg')
		ladder_image1=pygame.transform.scale(ladder_image,(ladder_width,height))
		broken_ladder_image=pygame.image.load('broken_ladder.jpg')
		broken_ladder_image1=pygame.transform.scale(broken_ladder_image,(ladder_width,15))
		broken_ladder_image_lower=pygame.image.load('broken_ladder_lower.jpg')
		broken_ladder_image1_lower=pygame.transform.scale(broken_ladder_image_lower,(ladder_width,15))
		coin_image=pygame.image.load('coin.png')
		coin_image1=pygame.transform.scale(coin_image,(coin_width,coin_width))
		queen_image=pygame.image.load('queen.png')
		queen_image1=pygame.transform.scale(queen_image,(queen_width,queen_height))
		gameDisplay.fill(white)
		pygame.draw.rect(gameDisplay,brown,[0,0,display_width,width_border])
		pygame.draw.rect(gameDisplay,brown,[0,0,width_border,display_height+5*height])
		pygame.draw.rect(gameDisplay,brown,[display_width-width_border,0,width_border,display_height+5*height])
		pygame.draw.rect(gameDisplay,brown,[0,6*height,display_width,width_border])
		pygame.draw.rect(gameDisplay,brown,[0,display_height+extra_display_height-width_border,display_width,width_border])
#	pygame.draw.rect(gameDisplay,brown,[display_width-100,35,100,width_border])
		i=0
		while i<5:
			pygame.draw.rect(gameDisplay,brown,[0,(i+1)*height,wall_pos[i],width_border])
			pygame.draw.rect(gameDisplay,brown,[wall_pos[i]+min_gap,(i+1)*height,display_width-(wall_pos[i]+min_gap),width_border])
			gameDisplay.blit(ladder_image1,(ladder_pos[i],(i+1)*height))
			if coin_pos[2*i]!=None:
				gameDisplay.blit(coin_image1,(coin_pos[2*i],(i+1)*height-coin_width))
			if coin_pos[2*i+1]!=None:	
				gameDisplay.blit(coin_image1,(coin_pos[2*i+1],(i+1)*height-coin_width))
#	if i%2==0:
			gameDisplay.blit(broken_ladder_image1,(broken_ladder_pos[i],(i+1)*height))
			gameDisplay.blit(broken_ladder_image1_lower,(broken_ladder_pos[i],(i+2)*height-15))
			i+=1
		gameDisplay.blit(queen_image1,(display_width-queen_width,60-queen_height))
#		pygame.draw.rect(gameDisplay,red,[lead_x,lead_y,10,10])#block_size,block_size])
################################################################################
class Fireball():
	def create_fireball(self,x,y):
		global fire_ball
		c=random.randrange(0,1000)
		fire_ball.append([pygame.Rect(x,y,block_size,block_size),1,5,c%3])
	def update(self,player):
		global fire_ball,speed_ball
		fireball_image=pygame.image.load('fireball.png')
		fireball_image1=pygame.transform.scale(fireball_image,(block_size,block_size))
		global level
		for ball in fire_ball:
			if player.lead_x<=ball[0].x<=player.lead_x+man_width and level==ball[2]:
				if not(ball[0].y-player.lead_y>=block_size+13):
					player.attack(1)
			if ball[2]>=1 and ladder_pos[5-ball[2]]<=ball[0].x<=ladder_pos[5-ball[2]]+ladder_width and ball[3]==1:
				ball[0].x-=speed_ball
				ball[2]-=1
				c=random.randrange(0,1000)
				ball[3]=c%3
			elif ball[2]>=1 and ball[3]==0 and wall_pos[5-ball[2]]<=ball[0].x<=wall_pos[5-ball[2]]+min_gap:
				ball[0].x-=speed_ball
				ball[2]-=1
				c=random.randrange(0,1000)
				ball[3]=c%3
			elif ball[2]>=1 and ball[3]==2 and broken_ladder_pos[5-ball[2]]<=ball[0].x<=broken_ladder_pos[5-ball[2]]+min_gap:
				ball[0].x-=speed_ball
				ball[2]-=1
				c=random.randrange(0,1000)
				ball[3]=c%3
			if ball[0].x<=2*width_border and ball[2]==0:
				fire_ball.remove(ball)
			else:
				ball[0].y=(6-ball[2])*height-block_size
				if ball[0].x<=width_border:
					ball[0].x=width_border+10
					ball[1]=1
				elif ball[0].x>=display_width-5*width_border:
					ball[0].x=display_width-4*width_border-10
					ball[1]=0
				if ball[1]==1:
					ball[0].x=ball[0].x+speed_ball
				else:
					ball[0].x=ball[0].x-speed_ball
				gameDisplay.blit(fireball_image1,(ball[0].x,ball[0].y))

################################################################################
def coin_collect(x,y):
	global coin_count
	if level>=1:
		if coin_pos[2*(5-level)]!=None and coin_pos[2*(5-level)]<=x<=coin_pos[2*(5-level)]+coin_width:
			coin_pos[2*(5-level)]=None
			coin_count+=1
		if coin_pos[2*(5-level)+1]!=None and coin_pos[2*(5-level)+1]<=x<=coin_pos[2*(5-level)+1]+coin_width:
			coin_pos[2*(5-level)+1]=None
			coin_count+=1

################################################################################
def fall_down(x,y):
	global level
	if level>=1:
		if wall_pos[5-level]<=x<=wall_pos[5-level]+min_gap and not(0<=y%height<=width_border+20):
			return 1
		else:
			return 0
	
################################################################################
################################################################################
def gameLoop():
	global gameExit
	gameExit=False
	donkey=Donkey()
	player=Player()
	fireball=Fireball()
	var1=Board()
	var1.floor()
	var1.ladder()
	var1.broken_ladder()
	var1.coin()
	donkey_direction=0#for right
	global lead_x_change
	global lead_y_change
	global level
	global jump_speed
	global jump_val
	while not gameExit:
		var1.fill_borders()
		donkey.player_display()
		fireball.update(player)
		var=lead_x_change
		if donkey_direction==0 and donkey.lead_x<wall_pos[0]:
			lead_x_change=donkey_speed
			donkey.move_right()
		elif donkey_direction==0 and donkey.lead_x>=wall_pos[0]:
			donkey_direction=1
			lead_x_change=-donkey_speed
			donkey.move_left()
		elif donkey_direction==1 and donkey.lead_x>width_border:
			lead_x_change=-donkey_speed
			donkey.move_left()
		elif donkey_direction==1 and donkey.lead_x<=width_border:
			donkey_direction=0
			lead_x_change=donkey_speed
			donkey.move_right()
		lead_x_change=var
		player.player_display()
		if donkey.lead_x<=player.lead_x<=donkey.lead_x+man_width and level==5:#and donkey.lead_y==player.lead_y:
			player.attack(1)
		coin_collect(player.lead_x,player.lead_y)
		for event in pygame.event.get():
			if event.type==USEREVENT+1:
				fireball.create_fireball(donkey.lead_x,donkey.lead_y)
			if event.type == pygame.QUIT:
				gameExit=True
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_a:
					lead_x_change=-1*speed
					lead_y_change=0
				elif event.key==pygame.K_d:
					lead_x_change=speed
					lead_y_change=0
				elif event.key==pygame.K_w:
					lead_x_change=0
					lead_y_change=-1*speed
				elif event.key==pygame.K_s:
					lead_x_change=0
					lead_y_change=speed
				elif event.key==pygame.K_SPACE and jump_val==False:
					jump_val=True
					jump_speed=-5	
				elif event.key==pygame.K_q:
					gameExit=True
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_a:
					lead_x_change=0
				elif event.key==pygame.K_d:
					lead_x_change=0
				elif event.key==pygame.K_w:
					lead_y_change=0
				elif event.key==pygame.K_s:
					lead_y_change=0
		d=fall_down(player.lead_x,player.lead_y)
		if d==1:
			player.lead_y+=height
			level-=1
		if lead_x_change<0:
			player.move_left()
			player.collision_wall()
		elif lead_x_change>0:
			player.move_right()
			player.collision_wall()
		if lead_y_change>0 :#and width_border<lead_y<=display_height-width_border:
			player.move_down()
			player.collision_wall()
		elif lead_y_change<0 :#and width_border<lead_y<=display_height-width_border:
			player.move_up()
			player.collision_wall()
		if jump_val==True:
		 	jump_speed+=0.5
		 	player.jump()
		if jump_speed==4.5:
		 	jump_val=False
		 	jump_speed=-7
		if player.life<=0:
			gameExit=True
		if display_width-queen_width-man_width<=player.lead_x<=display_width-queen_width and player.lead_y<=60-man_height<=player.lead_y+man_height:
		 	player.caught_queen()
			var1.floor()
			var1.ladder()
			var1.broken_ladder()
			var1.coin()
		player.print_data()
		pygame.display.update()
#		if player.life==0:
#			sleep("Your final score was:",display_width/2,(display_height+extra_display_height)/2,player.score,5)
		clock.tick(FPS)
	pygame.quit()
	quit()

################################################################################

sleep("Press 'w' to move up on ladders.",display_width/2,(display_height+extra_display_height)/2,-1,1)
sleep("Press 's' to move Down on ladders.",display_width/2,(display_height+extra_display_height)/2,-1,1)
sleep("Press 'a' to move Left.",display_width/2,(display_height+extra_display_height)/2,-1,1)
sleep("Press 'd' to move Right.",display_width/2,(display_height+extra_display_height)/2,-1,1)
sleep("Press 'space' to jumpover fire balls.",display_width/2,(display_height+extra_display_height)/2,-1,1)
sleep("Best of luck.",display_width/2,(display_height+extra_display_height)/2,-1,1)
pygame.mixer.music.play()
gameLoop()
pygame.mixer.music.stop()
