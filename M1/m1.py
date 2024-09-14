from graphics import *
import socket

#Variables used by game functions:
placed_tracker = 0  #Variable keeps track of number of moves played
#Following variables used by the program internally to keep track of game
player1 = 'X'
player2 = 'O'
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

#Move variables:
row = 0
col = 0
row_move = 0
col_move = 0

#Connection variables:
myIp = "192.168.0.121"
myPort = 5005
theirIp = "192.168.0.133"

dataRec = ["", "", "", ""]  #Received data

end_game = False  #Variable keeps track whether game has ended or not

#Graphics variables:
win_length = 600
win_width = 600
win = GraphWin("Tic Tac Toe", win_length, win_width)
radius = win_length // 9

box_center = win_length // 6
box_length = win_length // 3

avail_circles = []
shapes = []  # Stores shapes to easily remove them during moves

#Creates an array full of default circle objects:
default = Circle(Point(1, 1), 1)
circle_board = [[default, default, default], [default, default, default],
                [default, default, default]]


#Receive and send functions
def receive_move(
    isPicaria
):  #Wrapper method which processes data received from other player
  global dataRec, end_game, row, col, row_move, col_move, placed_tracker

  receive()  #Receives data from other player

  #Processes data
  row = int(dataRec[0])
  col = int(dataRec[1])
  if isPicaria:  #Reads two more variables, if currently in Picaria mode
    row_move = int(dataRec[2])
    col_move = int(dataRec[3])

    #Updates board:
    board[row][col] = ' '
    board[row_move][col_move] = player2
  else:
    #Updates board:
    board[row][col] = player2
  placed_tracker += 1  #Updatesmove tracker variable

  #Checks if the game has ended or not
  if (check_win(board, player2)):
    win_message(player2)
    end_game = True


#Function receives data from other machine:
def receive():
  global dataRec, board, end_game, row, col, row_move, col_move

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
  sock.bind((myIp, myPort))
  data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

  #Decodes received data into an array of strings
  dataRec = data.decode().split("+")


#Function sends data (values) to other machine
def send_move(values):
  data = ""

  #Encodes data
  for x in values:
    x = str(x)
    data += x + "+"

  #Removes redundant value from end of string array
  data = data[:-1]

  #Sends data
  sock = socket.socket(
      socket.AF_INET,  # Internet
      socket.SOCK_DGRAM)  # UDP
  sock.sendto(data.encode(), (theirIp, myPort))


#Set's up board
def board_setup():
  win.setBackground("black")  #Sets background colour
  offset = 100

  # Draw vertical lines
  for i in range(3):
    line1 = Line(Point(i * box_length + offset, offset),
                 Point(i * box_length + offset, win_length - offset))
    line1.setOutline('white')
    line1.setWidth(7)
    line1.draw(win)

  # Draw horizontal lines
  for i in range(3):
    line2 = Line(Point(offset, i * box_length + offset),
                 Point(win_length - offset, i * box_length + offset))
    line2.setOutline('white')
    line2.setWidth(7)
    line2.draw(win)

  # Draw diagonals
  diag = Line(Point(offset, offset),
              Point(win_length - offset, win_length - offset))
  diag.setOutline('white')
  diag.setWidth(7)
  diag.draw(win)
  diag2 = Line(Point(offset, win_length - offset),
               Point(win_length - offset, offset))
  diag2.setOutline('white')
  diag2.setWidth(7)
  diag2.draw(win)

  small_diag = Line(Point(offset + box_length, offset),
                    Point(offset + box_length * 2, offset + box_length))
  small_diag.setOutline('white')
  small_diag.setWidth(7)
  small_diag.draw(win)

  small_diag2 = Line(Point(offset + box_length * 2, offset + box_length),
                     Point(offset + box_length, offset + box_length * 2))
  small_diag2.setOutline('white')
  small_diag2.setWidth(7)
  small_diag2.draw(win)

  small_diag3 = Line(Point(offset + box_length, offset + box_length * 2),
                     Point(offset, offset + box_length))
  small_diag3.setOutline('white')
  small_diag3.setWidth(7)
  small_diag3.draw(win)

  small_diag4 = Line(Point(offset, offset + box_length),
                     Point(offset + box_length, offset))
  small_diag4.setOutline('white')
  small_diag4.setWidth(7)
  small_diag4.draw(win)


# Define a function to check if a player has won
def check_win(board, player):
  # Check rows
  for row in board:
    if row.count(player) == 3:
      return True
  # Check columns
  for i in range(3):
    if board[0][i] == board[1][i] == board[2][i] == player:
      return True
  # Check diagonals
  if board[0][0] == board[1][1] == board[2][2] == player:
    return True
  if board[0][2] == board[1][1] == board[2][0] == player:
    return True
  return False


#Draws points (small circle)
def point(x, y):
  if x < box_length and y < box_length:
    x = box_center
    y = x
  elif x < box_length and y > box_length and y < box_length * 2:
    x = box_center
    y = x + box_length
  elif x < box_length and y > box_length * 2:
    x = box_center
    y = x + box_length * 2
  elif x < box_length * 2 and x > box_length and y < box_length:
    x = box_center + box_length
    y = box_center
  elif x < box_length * 2 and x > box_length and y > box_length and y < box_length * 2:
    x = box_center + box_length
    y = box_center + box_length
  elif x > box_length and x < box_length * 2 and y > box_length * 2:
    x = box_center + box_length
    y = box_center + box_length * 2
  elif x > box_length and y < box_length:
    x = box_center + box_length * 2
    y = box_center
  elif x > box_length * 2 and y < box_length * 2 and y > box_length:
    x = box_length * 2 + box_center
    y = box_length + box_center
  elif x > box_length * 2 and y > box_length * 2:
    x = box_center + box_length * 2
    y = x
  return x, y


#Lists all the available spots for the player to move their piece into (Picaria Mode)
def available_spots(row, col):
  for i in range(-1, 2):
    for j in range(-1, 2):
      new_row = row + i
      new_col = col + j
      if new_row >= 0 and new_row < 3 and new_col >= 0 and new_col < 3 and board[
          new_row][new_col] == ' ':
        available_circle(new_row, new_col)


#Checks if move made by player is valid (Picaria Mode)
def isValidMove(row, col, row2, col2):
  if abs(row2 - row) <= 1 and abs(col2 - col) <= 1:
    return True
  return False


#Gets coordinates of mouse click and processes them into values between 0-2
def getCoordinates():
  click_point = win.getMouse()
  x = int(click_point.getX())
  y = int(click_point.getY())

  x, y = point(x, y)

  row = y // box_length
  col = x // box_length
  return row, col


#Draws circle on screen (players peice)
def circle():
  global row, col, row_move, col_move, cir, circle_board

  colour = 'red'  #Colour of the current peice being drawn

  tempRow = 0
  tempCol = 0

  #Sets the tempRow, tempCol vairables based on if it is Picaria mode or not
  if placed_tracker <= 6:
    tempRow = row
    tempCol = col
  else:
    tempRow = row_move
    tempCol = col_move

  #Calculates center of circle
  center_x = (tempCol * box_length) + box_center
  center_y = (tempRow * box_length) + box_center

  cir = Circle(Point(center_x, center_y), radius / 2)

  #Checks whether to draw red or blue coloured circle
  if placed_tracker % 2 == 0:
    colour = 'red'
  else:
    colour = 'blue'

  #Draws circle on board
  cir.setFill(colour)
  cir.draw(win)

  #Adds drawn circle to array of circles
  circle_board[tempRow][tempCol] = cir


#Draws circles on spots available for move
def available_circle(row, col):
  center_x = (col * box_length) + box_center
  center_y = (row * box_length) + box_center
  cir2 = Circle(Point(center_x, center_y), 10)
  cir2.setFill(color_rgb(0, 255, 0))
  cir2.draw(win)
  shapes.append(cir2)


# remove current shape & available circles and replace them with black squares
def remove_avail_circles(row, col):
  global shapes
  for shape in shapes:
    shape.undraw()
  shapes = []  # clear the shapes list


#Removes circle from the screen, as well as from circle_board array
def remove_shape():
  global circle_board, row, col
  circle_board[row][col].undraw()


#Prints win message on the screen
def win_message(active_player):
  square = Rectangle(Point(0, 0), Point(win_length, win_width))
  square.setFill('black')
  square.draw(win)
  win_message = Text(Point(win_length // 2, win_width // 2),
                     active_player + " WON!")
  win_message.setSize(30)
  win_message.setTextColor(color_rgb(0, 255, 0))
  win_message.draw(win)


#-------------
#Game function
#-------------


#First half of the game, where peices are placed on the board
def placePieces():
  global placed_tracker, player1, row, col, end_game, placed_tracker

  #Runs loop while game hasn't yet ended, and less then 6 pieces have been placed on the board
  while not end_game and placed_tracker < 6:
    row, col = getCoordinates()  #Gets coordinates of mouse click

    #Checks if there are no pieces on spot of press
    if (board[row][col] == ' '):
      board[row][col] = player1  #Updates board array
      placed_tracker += 1  #Increase the placed_tracker variable by 1

      circle()  #Draws a circle on the board

      #Checks if the player has won the game
      if check_win(board, player1):
        send_move([row, col])  #Sends the winning move to other player
        win_message(player1)  #Prints win message
        end_game = True  #Sets end game variable to true
        break
      send_move([row, col])
      receive_move(False)  #Receives/processes move from other player
      circle()  #Draws other players circle on screen
    else:
      print("Invalid move. Please try again.")


#Second half of the game where peices can be moved around the board:
def movePieces():
  global player1, row, col, row_move, col_move, end_game, placed_tracker

  while not end_game:
    row, col = getCoordinates()  #Gets coordinates of mouse click
    if board[row][col] == player1:  #Checks if valid piece is selected
      available_spots(row, col)  #Displays available move spots

      row_move, col_move = getCoordinates(
      )  #Gets coordinates of spot to move piece onto

      #Checks if move to be made is valid
      if board[row_move][col_move] == ' ' and isValidMove(
          row, col, row_move, col_move):
        #Updates board array
        board[row][col] = ' '
        board[row_move][col_move] = player1

        placed_tracker += 1

        #Updates screen
        remove_shape()
        circle()
        remove_avail_circles(row, col)

        #Checks if player has won
        if check_win(board, player1):
          win_message(player1)  #Prints win message
          send_move([row, col, row_move,
                     col_move])  #Sends move to other player
          end_game = True
          break
        send_move([row, col, row_move, col_move])  #Sends move to other player
      else:  #Asks for valid coordinates to be selected
        print("Please select valid coordinates.")
        remove_avail_circles(row, col)  #Removes available circles
    else:
      print(f"{player2}'s turn. Please select a piece.")

    receive_move(True)  #Receives and processes other players move
    if not end_game:
      remove_shape()  #Removes shape from screen
      circle()  #Draws circle on screen
      remove_avail_circles(row, col)  #Removes available circles from screen


#Main function which executes play function
def play_game():
  placePieces()
  movePieces()


# Start the game
board_setup()
play_game()
