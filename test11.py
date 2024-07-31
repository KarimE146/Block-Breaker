from tkinter import *
import time

# controls - left and right arrow keys to control the platform and bounce the ball to hit the bricks
# goal - your goal is to break all the bricks up top without letting the ball hit the bottom bourder
 
def clock():
    return time.perf_counter()

ball, velx, vely = None, 200, -200
field = None
previousTime = 0
keyboard = {'Left': False, 'Right': False}

plat = None
blocks = []

field_width = 400
field_height = 400

score = 0

def update_score():
    global score
    score += 10
    #adds to the score when you break a block
    
def hitBlock(block, x0, y0, x1, y1):
    bx0, by0, bx1, by1 = field.coords(block)
    if bx0 <= x1 <= bx1 and by0 <= y1 <= by1:
        
        #calls update score when it detects that the ball has hit a brick
        
        update_score()
        score_label['text'] = "Score: " + str(score)
        field.delete(block)
        blocks.remove(block)
            
         #removes the brick hit   
            
        if y0 < by0:
            return 'top'
        elif y0 > by1:
            return 'bottom'
        elif x0 < bx0:
            return 'left'
        else:
            return 'right'
        
    else:
        return 'no-collision'
    
def hitplat(plat, x0, y0, x1, y1):
    bx0, by0, bx1, by1 = field.coords(plat)
    if bx0 <= x1 <= bx1 and by0 <= y1 <= by1:
        if y0 < by0:
            return 'top'
        elif y0 > by1:
            return 'bottom'
        elif x0 < bx0:
            return 'left'
        else:
            return 'right'
    else:
        return 'no-collision'
    
    #returns which part of the platoform was hit by the ball

def ballPosition():
    x1, y1, x2, y2 = list(field.coords(ball))
    return [(x1+x2)/2, (y1+y2)/2]
    #updates ball coords

def startGame():
    global field, ball, plat, previousTime,score_label,score,timeDisplay,start_time
    root = Tk()
   
    field = Canvas(root, width=field_width, height=field_height, bg='black')
    field.pack()
    #sets up the canvas
        
    ball_x = field_width / 2
    ball_y = field_height / 2  
    ball = field.create_oval(ball_x - 5, ball_y - 5, ball_x + 5, ball_y + 5, fill='white')
    #makes the ball
    
    block_w = 3 # lets you pick how many blocks wide 
    block_l = 2 # lets you pick how many blocks high
    for i in range(block_w):
        for j in range(block_l):
            w = field_width/block_w
            h = field_height/25
            block = field.create_rectangle(1 + w*i, 0 + h*j, 1 + w*(i+1), 0 + h*(j+1), fill='light green')
            blocks.append(block)
    #sets up the rows and cloumns of bricks based on which number you choose        
    
  
    plat_width = field_width / 10 
    plat_height = field_height / 50  
    plat_x = (field_width - plat_width) / 2  
    plat_y = (field_height - plat_height) -20  
    plat = field.create_rectangle(plat_x, plat_y, plat_x + plat_width, plat_y + plat_height, fill='gray')
    #makes a platform thats size is relative to the field size

    def key_press(event):
        if event.keysym == 'Left':
            keyboard['Left'] = True
        if event.keysym == 'Right':
            keyboard['Right'] = True
    def key_release(event):
        if event.keysym == 'Left':
            keyboard['Left'] = False
        if event.keysym == 'Right':
            keyboard['Right'] = False
    #the controls for the platform        
            
    score_label = Label(root, text="Score: 0")
    score_label.pack(pady=10)
    #sets up the score label
    
    start_time = clock()
    pattern = 'Elapsed time: {0:.1f} seconds' 
    timeDisplay = Label(root)
    timeDisplay['text'] = pattern.format(clock())
    timeDisplay.pack()
    #sets up the timer and its label

    root.bind("<KeyPress>", key_press) 
    root.bind("<KeyRelease>", key_release) 
    previousTime = clock()
    animate()
    #starts the game

def animate():
    global velx, vely, score, start_time, previousTime

    time = clock()
    dt = time - previousTime
    previousTime = time

    # === Process keyboard events ===
    acceleration = 500
    if keyboard['Left']:
        plat_x = field.coords(plat)[0]
        if plat_x > 0:
            field.move(plat, -10, 0)
    if keyboard['Right']:
        plat_x = field.coords(plat)[2]
        if plat_x < field_width:
            field.move(plat, 10, 0)

    # === Update the game state ===
    x, y = ballPosition()

    # Collisions with walls
    if x + velx * dt > field_width or x + velx * dt < 0:
        velx *= -1
    if y + vely * dt < 0:
        vely *= -1
        
    #ends the game if the ball touches the bottom
    if y + vely * dt > field_height:
        field.destroy()  # Destroy the entire Tkinter window
        root = Tk()# Create a new Tkinter window for the loss message
        lose_message = Label(root, text="You Lost! :(", font=("Helvetica", 24))
        lose_message.pack(pady=50)
        root.mainloop()
        return

    x1 = x + velx * dt
    y1 = y + vely * dt

    for block in blocks[:]:  # Uses a copy of blocks list to iterate
        bl = hitBlock(block, x, y, x1, y1)
        if bl == 'left' or bl == 'right':
            velx *= -1
        elif bl == 'top' or bl == 'bottom':
            vely *= -1

    score_label['text'] = "Score: " + str(score)
    #constantly updates the score
    
    res = hitplat(plat, x, y, x1, y1)
    if res == 'left' or res == 'right':
        velx *= -1
    elif res == 'top' or res == 'bottom':
        vely *= -1
    #changes the velocity when the ball hits the platform
        
    #ends the game if there are no more bricks
    if len(blocks) == 0:
        field.destroy()  # Destroy the entire Tkinter window
        root = Tk()# Create a new Tkinter window for the victory message
        win_message = Label(root, text="You Won! :)", font=("Helvetica", 24))
        win_message.pack(pady=50)
        root.mainloop()
        return
        
        
    field.move(ball, velx * dt, vely * dt)

    elapsed_time = time - start_time
    pattern = 'Elapsed time: {0:.1f} seconds'
    timeDisplay['text'] = pattern.format(elapsed_time)
    #constantly updates the timer
    
    field.after(25, animate)  # Continue the animation loop

    
    
startGame()
mainloop()
