
import pygame 
from pygame import mixer 
import random  
import time

PIXEL = 50 

BLACK = (0,0,0) 
WHITE = (255,255,255) 
RED = (255,0,0)  
GRAY = (200,200 , 200) 



class GameEngine : 

    def __init__(self , window : pygame.Surface ) -> None: 

        pygame.init()  
        pygame.font.init()
        mixer.init() 

        mixer.Channel(0).play(mixer.Sound("pyTictactoe/sounds/bg_music.mp3"))

        self.w , self.h = window.get_size()  
        self.muted = False 
        self.PAUSE_UNPAUSE = pygame.USEREVENT + 1 
        self.paper =[  ['_'  for _ in range(3)  ] for _ in range(3) ]   
        self.drawWhat = [] # this will be like     [ 'X' , row , col  ]  
        self.col , self.row = 3 , 3 # if 3 comes out that means list index is out of the range  
        self.rects = {} 
        self.color_x = RED 
        self.color_o = BLACK 
        self.total_turn_left = 9 
        self.fps = pygame.time.Clock() 
        self.once_x , self.once_o = True , True  
        self.player1_won , self.player2_won = False , False 

        self.len1 , self.len2 = (self.w - 2 * PIXEL)//3  , (self.h - 2* PIXEL)//3 

        self.turn_player1 , self.turn_player2 = True , False  
        self.running = True    


    



    def events(self , window : pygame.Surface):  

        for e in pygame.event.get(): 

            if e.type == pygame.QUIT: 
                self.running = False  

            if e.type == self.PAUSE_UNPAUSE: 
                if not self.muted :
                    mixer.Channel(0).pause() 
                    self.muted = True 
                elif self.muted : 
                    mixer.Channel(0).unpause() 
                    self.muted = False 

    
    def apply_MouseController(self , mouse_pos : tuple , mouse_press : tuple):  
        leftKey , _ , _ = mouse_press 
        pos_x , pos_y = mouse_pos 

        def check_x(): 
        
            if PIXEL < pos_x < self.len1 : 
                self.col = 0 

            elif self.len1 < pos_x < 2*self.len1 : 
                self.col = 1 

            elif 2*self.len1 < pos_x < 3*self.len1 : 
                self.col = 2    

            return self.col  

        def check_y( ): 

            if PIXEL < pos_y < self.len2 : 
                self.row = 0 

            elif self.len2 < pos_y < 2 * self.len2 : 
                self.row = 1 

            elif 2*self.len2 < pos_y < 3 * self.len2 : 
                self.row = 2  

            return self.row   

          
        col , row = check_x() , check_y()
        
        try:
            if self.turn_player1 and self.paper[row][col] == "_":   
                
                if leftKey :  
                    self.total_turn_left -= 1 
                    self.paper[row][col] = 'X' 
                    self.turn_player1 = False 
                    self.turn_player2 = not (self.turn_player1) 

            elif self.turn_player2 : 
                if leftKey and self.paper[row][col] == "_" : 
                    self.total_turn_left -= 1 
                    
                    self.paper[row][col] = "O" 
                    self.turn_player2 = False 
                    self.turn_player1 = not ( self.turn_player2)   

        except: 
            pass  


    def blitzingEffect(self):   
        global RED

        if self.turn_player1  and self.total_turn_left > 0: 

            self.color_o = BLACK 
            r , g , b = self.color_x  

            if r != 0 and self.once_x: 
                r = max( r - 10,0) 
                g = min(g + 5 , 255)

            else : 
                self.once_x = False  
                if g != 0 : 

                    g = max( g-3,0) 
                    b = min( b + 10,255)  
                    r = min( r + 3 , 255 ) 

                else : 
                    if r != 255 or g != 0 or b != 0 : 
                        r = min( r+10 ,255) 
                        g = max(g-7 , 0 ) 
                        b = max(b - 4 , 0) 

                    else : 
                        self.once_x = True  

            self.color_x = (r,g,b)

        elif self.turn_player2  and self.total_turn_left > 0: 
            self.color_x = RED 
            r , g , b = self.color_o

            if g != 255 and self.once_o: 
                r = max( r - 10,0) 
                g = min(g + 10 , 255)

            else : 
                self.once_o = False  
                if g != 0 : 

                    g = max( g-10,0) 
                    b = min( b + 10,255)  
                    r = min( r + 10 , 255 ) 

                else : 
                    if r != 255 and g != 0 and b != 0 : 
                        r = min( r+10 ,255) 
                        g = max(g-10 , 0 ) 
                        b = max(b - 10 , 0) 

                    else : 
                        self.once_o = True    

            self.color_o = (r,g,b)
        else : 
            self.color_x = RED 
            self.color_o = BLACK 
            self.once_o = True 
            self.once_x = True 

        

        





    def apply_Draw(self , window : pygame.Surface): 
        window.fill(WHITE) 
        i,j = 1 , 1 
        while j <= 3 : 
            while i <= 3 :  
                self.rects[str(10*j+i)] = pygame.draw.rect(window , BLACK , pygame.Rect(PIXEL + ((i-1) * self.len1)  
                , PIXEL + ((j-1) * self.len2) , self.len1 , self.len2 ),5) 
                i += 1 
            i = 1
            j += 1   


        font_w , font_h = (self.w//3 , self.h//3)
        myFont = pygame.font.SysFont("Corbell" , font_w , font_h  )
        
        self.blitzingEffect()

        if self.total_turn_left > 0 :
            for col , rows in enumerate(self.paper): 

                for row , sign in enumerate(rows):  

                    

                    if sign == "X" :   
                        text_x = myFont.render("X" , False , self.color_x  )
                        w , h = text_x.get_width() , text_x.get_height()  
                        rect = self.rects[str(10*(col+1) + row + 1 )]    
                        if isinstance(rect , pygame.Rect):
                            window.blit(text_x , (rect.centerx - w//2 , rect.centery - h//2 , rect.w , rect.h)  )  

                    if sign == "O" :   
                        text_o = myFont.render("O" , False , self.color_o )  
                        w , h = text_o.get_width() , text_o.get_height() 
                        rect = self.rects[str(10*(col+1) + row + 1 )]   
                        if isinstance(rect , pygame.Rect):
                            window.blit(text_o , (rect.centerx - w//2  , rect.centery - h//2 , rect.w , rect.h) )   

    def isGameOver(self): 

        if self.total_turn_left == 0 : 
            return True 
        for i in range(3): 
            row = self.paper[i][:]
            col = [ sub[i] for sub in self.paper]
            if row[0] == row[1] and row[1] == row[2] and row[0] != "_" : 
                self.total_turn_left = -1   
                #print("TEST1 ")
                if row[0] == "X": 
                    self.player1_won = True 
                else : 
                    self.player2_won = True 
                return True  
            
            elif col[0] == col[1] and col[1] == col[2] and col[0] != "_": 
                self.total_turn_left = -1  
                #print("TEST2")
                if col[0] == "X": 
                    self.player1_won = True 
                else : 
                    self.player2_won = True 
                
                return True 

             

        if self.paper[0][0] == self.paper[1][1] and self.paper[1][1] == self.paper[2][2] and self.paper[0][0] != "_": 
            self.total_turn_left = -1  
            #print("TEST3") 
            if self.paper[0][0] == "X": 
                self.player1_won = True 
            else : 
                self.player2_won = True 
            
            return True 

        if self.paper[0][2] == self.paper[1][1] and self.paper[1][1] == self.paper[2][0] and self.paper[0][2]  != "_":  
            #print("TEST4")
            self.total_turn_left = -1 
            if self.paper[0][0] == "X": 
                self.player1_won = True 
            else : 
                self.player2_won = True 
            
            return True  

        return False  


    def gameOver(self , window : pygame.Surface):             
            window.fill(WHITE) 
            pygame.display.update()
            go_font = pygame.font.SysFont("Corbell" , 100) 
            go_surface = go_font.render("GAME OVER" , True , RED )  
            go_rect = go_surface.get_rect()  
            go_rect.midtop = (self.w//2 , self.h//4) 
            window.blit(go_surface , go_rect)  

            f_font = pygame.font.SysFont("Corbell" , 30) 

            if self.player1_won :  
                f_surface = f_font.render("PLAYER 1 WINS , CONGRATS PLAYER1 !" , True , RED)   
                f_rect = f_surface.get_rect() 
                f_rect.midtop = (self.w//2 , 3 * self.h//4)
                window.blit(f_surface , f_rect)  
                pygame.display.update()
                time.sleep(4) 
                self.running = False 
                  

            elif self.player2_won : 
                f_surface = f_font.render("PLAYER2 WINS , CONGRATS PLAYER2 !" , True , RED)   
                f_rect = f_surface.get_rect() 
                f_rect.midtop = (self.w//2 , 3 * self.h//4)
                window.blit(f_surface , f_rect)  
                pygame.display.update()
                time.sleep(4) 
                self.running = False 
                   

            else :  
                f_surface = f_font.render("DRAW!" , True , RED)   
                f_rect = f_surface.get_rect() 
                f_rect.midtop = (self.w//2 , 3 * self.h//4)
                window.blit(f_surface , f_rect)   
                pygame.display.update()
                time.sleep(4)
                self.running = False 
                






    def apply_pause_unpause(self): 

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_p]:
            pygame.event.post(pygame.event.Event( self.PAUSE_UNPAUSE))

        

        


    def applyEvents(self , window : pygame.Surface , mouse_positions : tuple , mouse_pressed : tuple): 
        
        self.apply_MouseController(mouse_positions , mouse_pressed)  
        self.apply_Draw(window)  
        if self.isGameOver():
            self.gameOver(window)  
        self.fps.tick(10) 
        self.apply_pause_unpause()
        pygame.display.update() 

    def execute(self , window : pygame.Surface):
        game = GameEngine(window)  
        while game.running : 
            pos , press = pygame.mouse.get_pos() , pygame.mouse.get_pressed()
            game.events(window) 
            game.applyEvents(window , pos , press)  





        