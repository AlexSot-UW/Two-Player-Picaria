from graphics import *
import socket

# Define a function to print the game board
placed_tracker = 0
player1 = 'X'
player2 = 'O'

default = Circle(Point(1, 1), 1)

counter = 0

dataRec = ["", "", "", ""]

#Simulated Data
sim_data = [["1", "0"], ["2", "2"], ["0", "1"], ["0", "1", "1", "1"],
            ["1", "0", "2", "0"], ["2", "2", "2", "1"], ["1", "1", "2", "2"]]

myIp = "192.168.0.121"
myPort = 5005

theirIp = "192.168.0.133"

row = 0
col = 0

row_move = 0
col_move = 0

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

circle_board = [[default, default, default], [default, default, default],
                [default, default, default]]

end_game = False

win_length = 600
win_width = 600
win = GraphWin("Tic Tac Toe", win_length, win_width)
radius = win_length // 9

box_center = win_length // 6
box_length = win_length // 3

avail_circles = []
shapes = []  # Stores shapes to easily remove them during moves


#-----My Code
def receive_move(isPicaria):
  global dataRec, end_game, row, col, row_move, col_move, placed_tracker

  receive()
  row = int(dataRec[0])
  col = int(dataRec[1])
  if isPicaria:
    row_move = int(dataRec[2])
    col_move = int(dataRec[3])
    board[row][col] = ' '
    board[row_move][col_move] = player2
  else:
    board[row][col] = player2
  placed_tracker += 1
  if (check_win(board, player2)):
    win_message(player2)
    end_game = True


def receive():
  global counter, dataRec, board, end_game, row, col, row_move, col_move

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
  sock.bind((myIp, myPort))
  data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

  dataRec = sim_data[counter]
  counter += 1


def send_dud(values):
  print("dud")


def send_move(values):
  #148 -> aarens ip, andrew -> 137

  data = ""

  for x in values:
    x = str(x)
    data += x + "+"

  data = data[:-1]

  sock = socket.socket(
      socket.AF_INET,  # Internet
      socket.SOCK_DGRAM)  # UDP
  sock.sendto(data.encode(), (theirIp, myPort))


def board_setup():
  win.setBackground("black")
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


def available_spots(row, col):
  for i in range(-1, 2):
    for j in range(-1, 2):
      new_row = row + i
      new_col = col + j
      if new_row >= 0 and new_row < 3 and new_col >= 0 and new_col < 3 and board[
          new_row][new_col] == ' ':
        available_circle(new_row, new_col)


def isValidMove(row, col, row2, col2):
  if abs(row2 - row) <= 1 and abs(col2 - col) <= 1:
    return True
  return False


def getCoordinates():
  click_point = win.getMouse()
  x = int(click_point.getX())
  y = int(click_point.getY())

  x, y = point(x, y)

  row = y // box_length
  col = x // box_length
  return row, col


def circle():
  global row, col, row_move, col_move, cir, circle_board

  colour = 'red'

  tempRow = 0
  tempCol = 0

  if placed_tracker <= 6:
    tempRow = row
    tempCol = col
  else:
    tempRow = row_move
    tempCol = col_move

  center_x = (tempCol * box_length) + box_center
  center_y = (tempRow * box_length) + box_center

  cir = Circle(Point(center_x, center_y), radius / 2)
  if placed_tracker % 2 == 0:
    colour = 'red'
  else:
    colour = 'blue'
  cir.setFill(colour)
  cir.draw(win)
  circle_board[tempRow][tempCol] = cir


def available_circle(row, col):
  center_x = (col * box_length) + box_center
  center_y = (row * box_length) + box_center
  cir2 = Circle(Point(center_x, center_y), 10)
  cir2.setFill(color_rgb(0, 255, 0))
  cir2.draw(win)
  shapes.append(cir2)


def cross(isPicaria):
  global row, col, row_move, col_move

  tempRow = 0
  tempCol = 0

  if not isPicaria:
    tempRow = row
    tempCol = col
  else:
    tempRow = row_move
    tempCol = col_move

  center_x = (tempCol * box_length) + box_center
  center_y = (tempRow * box_length) + box_center

  line1 = Line(Point(center_x - radius, center_y - radius),
               Point(center_x + radius, center_y + radius))
  line2 = Line(Point(center_x + radius, center_y - radius),
               Point(center_x - radius, center_y + radius))
  line1.setOutline('red')
  line1.setWidth(7)
  line2.setOutline('red')
  line2.setWidth(7)
  line1.draw(win)
  line2.draw(win)


# remove current shape & available circles and replace them with black squares
def remove_avail_circles(row, col):
  global shapes
  for shape in shapes:
    shape.undraw()
  shapes = []  # clear the shapes list


def remove_shape():
  global circle_board, row, col
  #square = Rectangle(
  #   Point(box_length * col + 10, row * box_length + 10),
  #  Point(box_length * col + box_length - 10,
  #       box_length * row + box_length - 10))
  #square.setFill('black')
  #square.draw(win)
  circle_board[row][col].undraw()


def win_message(active_player):
  square = Rectangle(Point(0, 0), Point(win_length, win_width))
  square.setFill('black')
  square.draw(win)
  win_message = Text(Point(win_length // 2, win_width // 2),
                     active_player + " WON!")
  win_message.setSize(30)
  win_message.setTextColor(color_rgb(0, 255, 0))
  win_message.draw(win)


def placePieces():
  global placed_tracker, player1, row, col, end_game, placed_tracker

  while not end_game and placed_tracker < 6:
    row, col = getCoordinates()
    if (board[row][col] == ' '):
      board[row][col] = player1
      placed_tracker += 1
      circle()
      if check_win(board, player1):
        send_move([row, col])
        win_message(player1)
        end_game = True
        break
      send_move([row, col])
      receive_move(False)
      circle()
    else:
      print("Invalid move. Please try again.")


def movePieces():
  global player1, row, col, row_move, col_move, end_game, placed_tracker
  while not end_game:
    row, col = getCoordinates()
    if board[row][col] == player1:
      available_spots(row, col)
      row_move, col_move = getCoordinates()
      if board[row_move][col_move] == ' ' and isValidMove(
          row, col, row_move, col_move):
        board[row][col] = ' '
        board[row_move][col_move] = player1
        placed_tracker += 1
        remove_shape()
        circle()
        remove_avail_circles(row, col)
        if check_win(board, player1):
          win_message(player1)
          send_move([row, col, row_move, col_move])
          end_game = True
          break
        send_move([row, col, row_move, col_move])
      else:
        print("Please select valid coordinates.")
        remove_avail_circles(row, col)
    else:
      print(f"{player2}'s turn. Please select a piece.")

    receive_move(True)
    if not end_game:
      remove_shape()
      circle()
      remove_avail_circles(row, col)


# Define a function to play the tic tac toe game
def play_game():
  placePieces()
  movePieces()

  win.getMouse()


# Start the game
board_setup()
play_game()
