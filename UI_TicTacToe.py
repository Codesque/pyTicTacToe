

from time import time
import pygame 
from pygame import mixer 
import random  

from TTT_PVP import GameEngine

PIXEL = 100 
BLACK = (0,0,0) 
WHITE = (255,255,255) 
RED = (125 , 0 , 0) 
LIGHT_RED = (255,100,100) 
DARK_RED = (40 , 0 , 0)

class XOX(pygame.sprite.Sprite): 

    def __init__(self , text ,screen_w , screen_h , sizeBorder = 120 , velBorder = 20) -> None:
        super().__init__()  
        self.size = random.randint(30 , sizeBorder)  
        self.sb = sizeBorder
        self.swidth , self.sheight = screen_w , screen_h
        self.font = pygame.font.SysFont("Corbell" , self.size)   
        self.ticks = pygame.time.get_ticks()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.image = self.font.render(text , True , self.color) 
        self.rect = self.image.get_rect()  
        self.vel_y = random.randint(1,velBorder) 
        self.vb = velBorder  
        self.vel_x0 , self.vel_x = 5 , 5 
        self.vel_x0_delta  = random.choice((-2,2)) 
        self.vel_x_delta = self.vel_x0_delta   
        self.once = True 


    def create_XOX(self):  
        rand = random.choice( (-1,1)) 
        if rand == -1 : 

            self.size = random.randint(30 , self.sb) 
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.rect.midtop = (random.randint(PIXEL//4 , self.swidth//3 - PIXEL//4 ) , random.randint(PIXEL//8 , self.sheight//6 - PIXEL//8 ))   
            self.vel_x = self.vel_x0   
            randv = random.choice((-2,2))
            self.vel_x_delta , self.vel_x0_delta =  randv , randv 
            

        elif rand == 1 : 
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))  
            self.rect.midtop = (random.randint(2*self.swidth//3 + PIXEL//4 , self.sheight - PIXEL//4 ) , random.randint(PIXEL//8 , self.sheight//6 - PIXEL//8 ))
            self.vel_x = self.vel_x0  
            randv = random.choice((-2,2))
            self.vel_x_delta , self.vel_x0_delta =  randv , randv 

    def movement(self , time : int , border = 5000):  

        if  not((0 < self.rect.centerx < self.swidth//3 - PIXEL//2) or (2*self.swidth//3 < self.rect.centerx < self.swidth - PIXEL//2)) and self.once:  
            self.vel_x_delta = -(self.vel_x_delta)   
            self.vel_x = self.vel_x0 
            self.once = False  

        elif (0 < self.rect.centerx < self.swidth//3 - PIXEL//2) or (2*self.swidth//3 +2 *PIXEL < self.rect.centerx < self.swidth - PIXEL//2) : 
            self.once = True 

            
            
        self.rect.centery += self.vel_y 
        self.rect.centerx -= self.vel_x 

        self.vel_x += self.vel_x_delta 

        if self.rect.top > self.sheight : 
            self.create_XOX()  
            

        













class UI_TicTacToe : 

    def __init__(self  , width = 500 , height = 500 ) -> None: 


        
        pygame.init() 
        mixer.init()  
        pygame.font.init()
        self.w , self.h = 500 , 500 
        self.window = pygame.display.set_mode((self.w , self.h))   
        pygame.display.set_caption("pyTicTacToe")    
        self.isExecuted = False 
  
        

        self.but_color = BLACK  
        self.rainbow1 = (random.randint(0,255) , random.randint(0,255) , random.randint(0,255) ) 
        self.rainbow2 = (random.randint(0,255) , random.randint(0,255) , random.randint(0,255) )  

        
        self.but1_bg_color , self.but2_bg_color , self.but3_bg_color = WHITE , WHITE , WHITE
        self.but1_selected = False 
        self.but2_selected = False 
        self.but3_selected = False  


        # for color breezing : 
        self.r , self.g , self.b = self.rainbow1  
        self.increase , self.once = False , True 


        self.muted = False 
        self.red = (255 , 0 , 0) 
        self.increase = False 
        self.PLAYER_VS_PLAYER = pygame.USEREVENT + 1  
        self.PLAYER_VS_BOT = pygame.USEREVENT + 2
        self.EXIT = pygame.USEREVENT + 3  
        self.PAUSE_UNPAUSE = pygame.USEREVENT + 4

        self.fps = pygame.time.Clock()  


        mixer.Channel(0).set_volume(0.7)
        mixer.Channel(0).play(mixer.Sound("pyTictactoe/sounds/bg_music.mp3") , -1) 

        self.sprite_XOX = pygame.sprite.Group() 
        self.sprite_XOX.add( XOX("X" , self.w , self.h) , XOX("O" , self.w , self.h) , XOX("X" , self.w , self.h))
        self.running = True 



    def events(self , mouse_pos : tuple): 
        
        for e in pygame.event.get(): 

            if e.type == pygame.QUIT: 
                self.running = False 
                pygame.quit() 
                quit()   

            if e.type == self.PLAYER_VS_PLAYER : 
                # run player vs player game  
                mixer.Channel(0).stop() 
                 
                game = GameEngine(self.window) 
                game.execute(self.window) 
                self.isExecuted = True

            if e.type == self.PLAYER_VS_BOT : 
                # run player vs bot game 
                pass  

            if e.type == self.PAUSE_UNPAUSE : 
                # pause/unpause the music 

                if not self.muted :
                    mixer.Channel(0).pause() 
                    self.muted = True 
                elif self.muted : 
                    mixer.Channel(0).unpause() 
                    self.muted = False 






    def draw_ticLines(self):  

        x0 , y0 = 7*self.w//24 , self.h //30  
        a = 75

        x1 = pygame.draw.rect(self.window , BLACK , pygame.Rect(x0 , y0 , a , a ) , 5) 
        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+a , y0 , a , a ) , 5)  
        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+2*a , y0 , a , a ) , 5)  

        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0 , y0+a , a , a ) , 5) 
        o1 =pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+a , y0+a , a , a ) , 5)  
        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+2*a , y0+a , a , a ) , 5)  

        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0 , y0+a+a , a , a ) , 5) 
        pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+a , y0 +a+a, a , a ) , 5)  
        x2 = pygame.draw.rect(self.window , BLACK , pygame.Rect(x0+2*a , y0+a+a , a , a ) , 5)  

        font_xox = pygame.font.SysFont("Corbell" , a)  
        text_x1 = font_xox.render("X" , True , self.rainbow1 )  
        self.window.blit(text_x1 , (x1.centerx - x1.w//4 , x1.centery - x1.h//4  , 3*a , 3*a ))  

        text_x2 = font_xox.render("X" , True , self.rainbow2)  
        self.window.blit(text_x2 , (x2.centerx - x2.w//4 , x2.centery - x2.h//4  , 3*a , 3*a ))  


        text_o1 = font_xox.render("O" , True , self.red)  
        self.window.blit(text_o1, (o1.centerx - o1.w//4 , o1.centery - o1.h//4  , 3*a , 3*a )) 

    def buttons(self , mouse_pos : tuple ,  font_str = "Corbel"):  

        width = 100 
        height = 60 
        x = self.w // 2 - width//2
        y = self.h // 2
        border_len = 4   
        blank = 70 


        

        font = pygame.font.SysFont(font_str , 30) 
        text1 = font.render("PLAYER VS PLAYER" , True , self.but_color ,self.but1_bg_color )  
        text2 = font.render("PLAYER VS BOT" , True , self.but_color , self.but2_bg_color) 
        text3 = font.render("EXIT" , True , self.but_color , self.but3_bg_color)


        rect1 = pygame.draw.rect(self.window , BLACK , pygame.Rect(x -75, y  , width+150 , height) , border_len)   
        self.window.blit(text1 , (rect1.centerx - 23*rect1.width//48 , rect1.centery - rect1.height//4 ) )  

        rect2 = pygame.draw.rect(self.window , BLACK , pygame.Rect(x - 75 , y + blank , width + 150 , height) , border_len)   
        self.window.blit(text2 , (rect2.centerx - 5*rect2.width//12 , rect2.centery - rect2.height//4  ) )  

        rect3 = pygame.draw.rect(self.window , BLACK , pygame.Rect(x  , y + 2 * blank , width  , height) , border_len)   
        self.window.blit(text3 , (rect3.centerx - rect3.width//4 , rect3.centery - rect3.height//4  ) )  

        leftkey , _ , _ = mouse_pressed 
        if rect1.collidepoint(mouse_pos): 
            self.but1_bg_color = (self.r , self.g , self.b) 
            self.but1_selected = True    
            if leftkey and not self.isExecuted: 
                pygame.event.post(pygame.event.Event(self.PLAYER_VS_PLAYER)) 
            if self.isExecuted : 
                self.isExecuted = False 
            

        else : 
            self.but1_bg_color = WHITE 
            self.but1_selected = False 

        if rect2.collidepoint(mouse_pos): 
            self.but2_bg_color = (self.r , self.b , self.g)  
            self.but2_selected = True   
            if leftkey : 
                pygame.event.post(pygame.event.Event(self.PLAYER_VS_BOT)) 
        else :  
            self.but2_bg_color = WHITE 
            self.but2_selected = False 

        if rect3.collidepoint(mouse_pos): 
            self.but3_bg_color = (self.g , self.r , self.b )  
            self.but3_selected = True  
            if leftkey : 
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        else : 
            self.but3_bg_color = WHITE 
            self.but3_selected = False 
       





    def changeColor(self): 

        self.rainbow1 = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255)  ) 
        self.rainbow2 = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255)  )  
        r , _ , _ = self.red 
        if not self.increase :  
            r -= 1 
            if r <= 20 : 
                self.increase = True 
            self.red = (r, 0 , 0)   

        else : 
            r += 1 
            if r >= 254 : 
                self.increase = False 
            self.red = (r,0,0)  




    def colorBreezing(self): 
        
        cons = 20
        if not self.increase :  

            self.rainbow1 = (self.r , self.g , self.b) 
            self.rainbow2 = (self.b , self.r , self.g) 
            self.red = (self.g , self.r , self.b)

            if not(self.r >= 255) : 
                self.r += cons 
                self.r = min( self.r , 255) 

            elif not (self.g <= 0) : 
                self.g -= cons  
                self.g = max( self.g , 0 )

            elif not (self.b >= 255): 
                self.b += cons 
                self.b = min( self.b , 255) 

            else :  
                self.increase = True  


        if  self.increase : 


            self.rainbow1 = (self.r , self.g , self.b) 
            self.rainbow2 = (self.b , self.r , self.g) 
            self.red = (self.g , self.r , self.b)
            if not(self.r <= 0) : 
                self.r -= cons  
                self.r = max(self.r , 0)

            elif not (self.g >= 255) : 
                self.g += cons  
                self.g = min( self.g, 255)

            elif not (self.b <= 0): 
                self.b -= cons  
                self.b = max( self.b,0)

            else :  
                self.increase = False 


    def applyEvents(self ,runtime : int ,  mouse_positions : tuple , mouse_press : tuple): 

        
        self.window.fill(WHITE) 
        self.sprite_XOX.draw(self.window)   
        for xox in self.sprite_XOX.sprites(): 
            if isinstance(xox , XOX): 
                xox.movement(runtime , 4) 

            
            
            
        self.sprite_XOX.update()  
        self.draw_ticLines()
        self.buttons(mouse_positions) 


        self.colorBreezing()
        self.fps.tick(20)  
        pygame.display.update() 

    def pause_unpause(self): 
        keys = pygame.key.get_pressed() 

        if keys[pygame.K_P] : 
            pygame.event.post()


if __name__ == "__main__": 

    program = UI_TicTacToe() 
    
    while program.running : 
        ticks = pygame.time.get_ticks()  
        mouse_positions = pygame.mouse.get_pos()  
        mouse_pressed = pygame.mouse.get_pressed()
        program.events(mouse_positions) 
        program.applyEvents( ticks , mouse_positions , mouse_pressed)

     

    

                


        



                


    

