################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################
import game_grid
import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)


def start():
   grid_h, grid_w = 20, 12
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
   stddraw.setCanvasSize(canvas_w + 200, canvas_h)
   stddraw.setXscale(-0.5, grid_w + 5.0)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w

   grid = GameGrid(grid_h, grid_w)
   current_tetromino = create_tetromino()

   grid.current_tetromino = current_tetromino

   score = 0

   next_block = create_tetromino()
   # Next block'u oluşturduktan sonra grid nesnesine atama yap
   grid.next_block = next_block

   display_game_menu(grid_h, grid_w, score)

   while True:
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()
         if key_typed == "space":
            current_tetromino.move(key_typed, grid)
         elif key_typed in ["left", "right", "down"]:
            current_tetromino.move(key_typed, grid)
         stddraw.clearKeysTyped()

      if grid.remove_filled_lines():  # remove_filled_lines fonksiyonunun dönüş değeri ile kontrol ediliyor
         grid.score += 100  # Puanın doğrudan GameGrid nesnesinin bir özelliği üzerinden güncellenmesi
         grid.draw_score()  # Puanın ekrana çizilmesi
         if not grid.current_tetromino:
            next_block = create_tetromino()

      success = current_tetromino.move("down", grid)
      if not success:
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         game_over = grid.update_grid(tiles, pos)
         if game_over:
            break
         current_tetromino = next_block
         grid.current_tetromino = current_tetromino
         next_block = create_tetromino()
         # Next block'u oluşturduktan sonra grid nesnesine atama yap
         grid.next_block = next_block



      grid.display()

   print("Game over")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z','J','L','S','T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

def display_game_menu(grid_height, grid_width, score):
   # the colors used for the menu
   background_color = Color(245 , 245, 245)
   button_color = Color(245 , 245, 245)
   text_color = Color(14, 98, 148)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/Tetris_bg_v4.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Poppins Bold")
   stddraw.setFontSize(30)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)




   # the user interaction loop for the simple menu
   while True:



      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)

      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():

         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()

