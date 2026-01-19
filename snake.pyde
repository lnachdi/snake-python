import os
import random

PATH = os.getcwd()

#1. Configuration of the board using global variables (set to 600*600 pixels)
COL = 20
ROW = 20
CELL_SIZE = 30

WIDTH = COL * CELL_SIZE
HEIGHT = ROW * CELL_SIZE

#2. SNAKE ELEMENT CLASS: Represents a single segment of the snake, either the head or tail(body).

class SnakeElement():
    def __init__(self, col, row, is_head = False, img = None, body_color=None):
        self.col = col
        self.row = row
        self.is_head = is_head # True for head, false for body
        self.img = img
        if body_color is None:
            self.color = color(81,151,32) # Sets default color of body to green
        else:
            self.color=body_color
    
      #Draws the snake tail   
    def display(self, cell_size, direction=None):
        x= self.col*cell_size
        y = self.row* cell_size
        
        if self.is_head and self.img is not None: #Draws the head using the direction image
            image(self.img,x,y,cell_size, cell_size)
            
        else: #Draws the body as a colored ellipse
            noStroke()
            fill(self.color)
            ellipse(x+ cell_size /2, y+ cell_size /2, cell_size*0.9, cell_size*0.9)
            
  
        
#3. SNAKE CLASS: Controls movement, growth, direction, collision    

class Snake:
    def __init__(self, col, row, cell_size):
        self.col = col
        self.row = row
        self.cell_size =cell_size
        
        # Loads the head images
        self.head_up= loadImage(PATH + "/images/head_up.png")
        self.head_left= loadImage(PATH + "/images/head_left.png")
    
        
    
        # Starting position of snake on the board (center)
        start_col = col // 2
        start_row= row // 2
        
        # Start moving left
        self.direction=(-1,0)
        self.growth=0
        self.growth_colors=[] #colors for new body parts
        
        
        #Create the initial snake (head + the first 2 tails)
        self.elements = [SnakeElement(start_col, start_row, is_head = True, img= self.head_left), SnakeElement(start_col +1 , start_row), SnakeElement(start_col +2 , start_row)]
    
    #Changes movement direction    
    def set_direction(self, dx, dy):
        cur_dx,cur_dy = self.direction # to prevent 180 degree turns
        if dx == -cur_dx and dy == -cur_dy:
            return
        self.direction = (dx,dy)
     
    #Returns the head's coordinates   
    def head_pos(self):
        h = self.elements[0]
        return h.col, h.row
    
    #Picks which direction the head is rotated based on movement
    def get_head_img(self):
        if self.direction == (0, -1):      #up
            return self.head_up
        elif self.direction==(-1,0):       #left
            return self.head_left
        elif self.direction == (1, 0):     # right
            return self.head_left
        elif self.direction == (0, 1):     # down
            return self.head_up
        return self.head_left
    
    # Add growth of color to a queue
    def grow(self, body_color ,amount = 1):
        for x in range(amount):
            self.growth_colors.append(body_color)
    
    def move(self):
        dx,dy = self.direction
        head = self.elements[0]
        new_col = head.col + dx
        new_row = head.row + dy
        
       # Determines whether to grow the segment or not
        growing= False
        seg_color=None
        
        if self.growth_colors:
            seg_color = self.growth_colors.pop(0) # this step = growth with this color
            growing=True
            
        else:
            seg_color = None  # normal move, no growth

        # Creates new head
        new_head_img = self.get_head_img()
        new_head = SnakeElement(new_col, new_row,is_head=True,img=new_head_img,body_color=seg_color)

        self.elements.insert(0, new_head) # inserts new head at the front

        #Removes trailing tail if its not growing
        if not growing:
            self.elements.pop()
        else:
            tail = self.elements[-1]
            tail.color = seg_color
            

        
    # Checks for collision with its tail
    def collides_with_self(self):
        hc, hr = self.head_pos()
        for seg in self.elements[1:]:
            if seg.col == hc and seg.row == hr:
                return True
        return False

    # Checks if snake occupies cells
    def occupies(self, col, row):
        for seg in self.elements:
            if seg.col == col and seg.row == row:
                return True
        # return False


    #Draws all snake segments together
    def display(self):
        # ensure only first element is treated as head
        for i, seg in enumerate(self.elements):
            if i == 0:
                seg.is_head = True
                seg.img = self.get_head_img()
                seg.display(self.cell_size, self.direction)
            else:
                seg.is_head = False
                seg.img = None
                seg.display(self.cell_size)
            
            
#4. GAME CLASS: Controls all the game logic: fruit spawning, collision checks, score updates, key handling
class Game:
    def __init__(self, col, row, cell_size):
        self.col =col
        self.row= row
        self.cell_size=cell_size
        self.reset()
        
    #Resets game state
    def reset(self):
        self.score=0
        self.game_over=False
        self.snake= Snake(self.col,self.row,self.cell_size)
        self.fruit=None
        self.spawn_fruit()
    
    #Updates game every frame    
    def update(self):
        if self.game_over:
            return
        self.snake.move()
        hc,hr =self.snake.head_pos()
        
        #1. condition for wall collision
        if hc < 0 or hc >= self.col or hr<0 or hr>= self.row:
            self.game_over = True
            return
        
        #2. condition for collision with body
        if self.snake.collides_with_self():
            self.game_over= True
            return
        
        #3. condition for fruit collision (increases score value)
        if self. fruit is not None and hc == self.fruit.col and hr == self.fruit.row:
            self.score += self.fruit.score_value
            self.fruit.effects(self.snake)
            self.spawn_fruit()
    
    #Draws all the game elements        
    def display(self):
        self.snake.display()
        
        if self.fruit is not None:
            self.fruit.display(self.cell_size)
            
        # Score display on top left of screen
        fill(0)
        textAlign(LEFT, TOP)
        text("Score: " + str(self.score),5,5)
        
        # Game over message
        if self.game_over:
            fill(0)
            textAlign(CENTER,CENTER)
            text("Game over - Click mouse to restart", WIDTH / 2, HEIGHT / 2)
            
    #Functionality of keys and control where the snake moves
    def handle_key(self, keyCode):
        if keyCode == UP:
            self.snake.set_direction(0, -1)
        elif keyCode == DOWN:
            self.snake.set_direction(0, 1)
        elif keyCode == LEFT:
            self.snake.set_direction(-1, 0)
        elif keyCode == RIGHT:
            self.snake.set_direction(1, 0)
   
    
    # Mouse click to restart the game after losing/end of game        
    def handle_mouse(self):
        if self.game_over:
            self.reset()
            
    #Spwan fruits across the baord wherever its free - not overlapping with the snake
    def spawn_fruit(self):
        free_cells=[]
        for c in range(self.col):
            for r in range(self.row):
                if not self.snake.occupies (c,r):
                    free_cells.append((c,r))
        
        if not free_cells: #if snake body takes up all cells in the board
            self.game_over = True
            return
        col, row = random.choice(free_cells) # controls randomness of spawn
        
        # 50/50 equal chance of getting apple or banana
        if random.randint(0,1)==0:
            self.fruit = Apple(col, row)
        else:
            self.fruit = Banana(col, row)
            
    
#6. FRUIT CLASS: stores position, image, color, and score value        
class Fruit:
    def __init__(self, col, row, img_name, score_value, fruit_color):
        self.col = col
        self.row= row
        self.img =loadImage(PATH + "/images/" + img_name)
        self.score_value = score_value
        self.color = fruit_color
        
    def display(self, cell_size):
        x=self.col*cell_size
        y=self.row*cell_size
        image(self.img,x,y,cell_size,cell_size)
   
   # Snake grows with fruit color when eaten
    def effects(self, snake):
        snake.grow(self.color, 1)
    
#7. Apple and Banana Class inherit from Fruit class with unique color and image
class Apple(Fruit):
    def __init__(self,col,row):
        Fruit.__init__(self, col, row, "apple.png", 1, color(172,48,33))
        
class Banana(Fruit):
    def __init__(self,col,row):
        Fruit.__init__(self, col, row, "banana.png", 1, color(252,225,76))
        
        
        
#8. MAIN PROGRAM: Initialises game window, updates game after each frame, updates logic    

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    if frameCount%12 ==0 : #snake speed
        background(203)
        game.update()
        game.display()
        
def keyPressed():
    game.handle_key(keyCode)
        
def mousePressed():
    game.handle_mouse()
    
game=Game(COL, ROW, CELL_SIZE)
