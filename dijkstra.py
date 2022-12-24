from tkinter import messagebox, Tk
import pygame
import sys

window_height = 500
window_width = 500

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j) -> None:
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        
    def draw(self, win, colour):
        pygame.draw.rect(win, colour, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))
        
    def setNeighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
            
# Creating the grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)
    
# Set neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].setNeighbours()
        
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)
        
def main():
    begin_search = False
    targetbox_set = False
    searching = True
    target_box = None
    completed = False
    
    while True:
        for event in pygame.event.get():
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # mouse controls
            elif event.type == pygame.MOUSEMOTION:
                # Draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                i = x // box_width
                j = y // box_height
                # Set Target
                if event.button == 3 and not targetbox_set:
                    if not grid[i][j].wall:
                        target_box = grid[i][j]
                        targetbox_set = True
                        target_box.target = True
                
                # Creates wall if mouse button is clicked but not dragged
                elif event.button == 1:
                    grid[i][j].wall = True
                    
            # Staring algorithm
            if event.type == pygame.KEYDOWN and targetbox_set:
                begin_search = True
                
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    completed = True
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solutions!")
                    searching = False
        # Display Graphics
        window.fill((0, 0, 0))
        
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (20, 20, 20))
                
                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))
                    
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (110, 110, 110))
                if box.target:
                    box.draw(window, (200, 200, 0))
            
        pygame.display.flip()
        if completed:
            Tk().wm_withdraw()
            messagebox.showinfo("PATH FOUND", "This path was " + str(len(path) + 1) + " pixels long")
            completed = False
main()