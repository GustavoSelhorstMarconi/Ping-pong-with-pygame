import pygame, sys, random

def ball_animation():
  global ball_speed_x, ball_speed_y, counterPlayer, counterOpponent, multiplier
  ball.x += int(ball_speed_x * multiplier)
  ball.y += int(ball_speed_y * multiplier)

  if ball.top <= 0 or ball.bottom >= screen_height:
    ball_speed_y *= -1
  if ball.left <= 0:
    ball_restart()
    counterPlayer += 1
  if ball.right >= screen_width:
    ball_restart()
    counterOpponent += 1

  if ball.colliderect(player) or ball.colliderect(opponent):
    multiplier += 0.1
    ball_speed_x *= -1

def player_animation():
  player.y += player_speed
  if player.top <= 0:
    player.top = 0
  if player.bottom >= screen_height:
    player.bottom = screen_height

def opponent_ai():
  if opponent.top < ball.y:
    opponent.top += opponent_speed
  if opponent.bottom > ball.y:
    opponent.bottom -= opponent_speed
  if opponent.top <= 0:
    opponent.top = 0
  if opponent.bottom >= screen_height:
    opponent.bottom = screen_height

def opponent_animation():
  opponent.y += opponent_speed
  if opponent.top <= 0:
    opponent.top = 0
  if opponent.bottom >= screen_height:
    opponent.bottom = screen_height

def ball_restart():
  global ball_speed_x, ball_speed_y, multiplier
  ball.center = (screen_width/2, screen_height/2)
  ball_speed_y *= random.choice((1, -1))
  ball_speed_x *= random.choice((1, -1))
  multiplier = 1
  
# General setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Fonts texts
font = pygame.font.get_default_font()
fontesys = pygame.font.SysFont(font, 60)
fonteWin = pygame.font.SysFont(font, 40)
fonteSuper = pygame.font.SysFont(font, 18)

# Setting up the main window
screen_width = 914
screen_height = 686
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)
superPlayer = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 20, 20)
superOpponent = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 20, 20)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
player_color = (15, 82, 186)
opponent_color = (217, 2, 5)
super_color = (238, 173, 45)
colorTxtSuper = (242, 79, 0)

ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))
super_player_speed = 7 * random.choice((1, -1))
super_opponent_speed = 7 * random.choice((1, -1))

# Control variables
canMove = True
canMoveOpponent = True
canMovePlayer = True
playerSuperFull = False
opponentSuperFull = False
readyForSuperPlayer = False
readyForSuperOpponent = False
moveSuperPlayer = False
moveSuperOpponent = False
resetSuperPlayer = False
resetSuperOpponent = False
lockOpponent = False
lockPlayer = False
player_speed = 0
opponent_speed = 0
counterPlayer = 0
counterOpponent	= 0
countPlayer = 0
countOpponent = 0
multiplier = 1
maxPoint = 12
freeSuperPlayer = 0
freeSuperOpponent = 0
timeSuper = 120

# Declaration of texts
txtVictoryPlayer = fonteWin.render('The Winner Is: Blue', 1, player_color)
txtVictoryOpponent = fonteWin.render('The Winner Is: Red', 1, opponent_color)
txtSuperPlayer = fonteSuper.render('Press <- to use SUPER', 1, colorTxtSuper)
txtSuperOpponent = fonteSuper.render('Press D to use SUPER', 1, colorTxtSuper)

while True:
  # Handling input
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN and canMovePlayer == True and canMove == True:
        player_speed += 7
        if playerSuperFull == False:
          countPlayer += 3
      if event.key == pygame.K_UP and canMovePlayer == True and canMove == True:
        player_speed -= 7
        if playerSuperFull == False:
          countPlayer += 3
      if event.key == pygame.K_w and canMoveOpponent == True and canMove == True:
        opponent_speed -= 7
        if opponentSuperFull == False:
          countOpponent += 3
      if event.key == pygame.K_s and canMoveOpponent == True and canMove == True:
        opponent_speed += 7
        if opponentSuperFull == False:
          countOpponent += 3

      if event.key == pygame.K_LEFT and playerSuperFull == True:
        readyForSuperPlayer = True
        resetSuperPlayer = True
        superPlayer.x = screen_width/2
        superPlayer.y = screen_height/2
        freeSuperOpponent = 0

      if event.key == pygame.K_d and opponentSuperFull == True:
        readyForSuperOpponent = True
        resetSuperOpponent = True
        superOpponent.x = screen_width/2
        superOpponent.y = screen_height/2
        freeSuperPlayer = 0
      
      # Bug verify
      if event.key == pygame.K_w and 0 < freeSuperOpponent < timeSuper:
        lockOpponent = True
      if event.key == pygame.K_s and 0 < freeSuperOpponent < timeSuper:
        lockOpponent = True

      if event.key == pygame.K_UP and 0 < freeSuperPlayer < timeSuper:
        lockPlayer = True
      if event.key == pygame.K_DOWN and 0 < freeSuperPlayer < timeSuper:
        lockPlayer = True
      
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_DOWN and canMovePlayer == True and canMove == True:
        player_speed -= 7
      if event.key == pygame.K_UP and canMovePlayer == True and canMove == True:
        player_speed += 7
      if event.key == pygame.K_w and canMoveOpponent == True and canMove == True:
        opponent_speed += 7
      if event.key == pygame.K_s and canMoveOpponent == True and canMove == True:
        opponent_speed -= 7

      # Bug verify
      if event.key == pygame.K_w and lockOpponent == True:
        opponent_speed = 0
        lockOpponent = False
      if event.key == pygame.K_s and lockOpponent == True:
        opponent_speed = 0
        lockOpponent = False
      if event.key == pygame.K_UP and lockPlayer == True:
        player_speed = 0
        lockPlayer = False
      if event.key == pygame.K_DOWN and lockPlayer == True:
        player_speed = 0
        lockPlayer = False

  ball_animation()
  player_animation()
  opponent_animation()
  #opponent_ai()

  # Visuals
  screen.fill(bg_color)
  pygame.draw.rect(screen, player_color, player)
  pygame.draw.rect(screen, opponent_color, opponent)
  pygame.draw.ellipse(screen, light_grey, ball)
  pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

  # Messages
  txtPlayer = fontesys.render(str(counterPlayer), 1, (200, 200, 255))
  txtOpponent = fontesys.render(str(counterOpponent), 1, (200, 200, 255))
  screen.blit(txtPlayer, (screen_width/2 + 20, 70))
  screen.blit(txtOpponent, (screen_width/2 - 45, 70))
  
  pygame.draw.rect(screen, super_color, pygame.Rect(screen_height, screen_height - 80, 0 + countPlayer, 30))
  pygame.draw.rect(screen, super_color, pygame.Rect(50, screen_height - 80, 0 + countOpponent, 30))

  # Use super
  if countPlayer >= 150:
    screen.blit(txtSuperPlayer, (screen_height + 9, screen_height - 72))
    playerSuperFull = True

  if countOpponent >= 150:
    screen.blit(txtSuperOpponent, (59, screen_height - 72))
    opponentSuperFull = True

  # Victory
  if counterPlayer >= maxPoint:
    screen.blit(txtVictoryPlayer, (screen_width/2 - 140, screen_height/2 + 20))
    ball_speed_x = 0
    ball_speed_y = 0
    opponent_speed = 0
    canMoveOpponent = False
    canMovePlayer = False

  if counterOpponent >= maxPoint:
    screen.blit(txtVictoryOpponent, (screen_width/2 - 155, screen_height/2 + 20))
    ball_speed_x = 0
    ball_speed_y = 0
    opponent_speed = 0
    canMoveOpponent = False
    canMovePlayer = False

  if readyForSuperPlayer == True:
    pygame.draw.ellipse(screen, player_color, superPlayer)
    if resetSuperPlayer == True:
      pygame.draw.rect(screen, pygame.Color('grey12'), pygame.Rect(screen_height, screen_height - 80, 160, 30))
      countPlayer = 0
      resetSuperPlayer = False
      playerSuperFull = False
    superPlayer.x -= 7
    superPlayer.y += super_player_speed
    if superPlayer.top <= 0 or superPlayer.bottom >= screen_height:
      super_player_speed *= -1
    if superPlayer.colliderect(opponent) and freeSuperOpponent <= 120:
      canMoveOpponent = False
      readyForSuperPlayer = False
      opponent_speed = 0
      pygame.draw.ellipse(screen, player_color, pygame.Rect(1500, 1500, 1501, 1501))
  
  if canMoveOpponent == False:
    freeSuperOpponent += 1
  if freeSuperOpponent == timeSuper:
    canMoveOpponent = True

  if readyForSuperOpponent == True:
    pygame.draw.ellipse(screen, opponent_color, superOpponent)
    if resetSuperOpponent == True:
      pygame.draw.rect(screen, pygame.Color('grey12'), pygame.Rect(50, screen_height - 80, 160, 30))
      countOpponent = 0
      resetSuperOpponent = False
      opponentSuperFull = False
    superOpponent.x += 7
    superOpponent.y += super_opponent_speed
    if superOpponent.top <= 0 or superOpponent.bottom >= screen_height:
      super_opponent_speed *= -1
    if superOpponent.colliderect(player):
      canMovePlayer = False
      readyForSuperOpponent = False
      player_speed = 0
      pygame.draw.ellipse(screen, player_color, pygame.Rect(-100, -100, -99, -99))
    
  if canMovePlayer == False:
    freeSuperPlayer += 1
  if freeSuperPlayer == 120:
    canMovePlayer = True

  pygame.display.update()
  # Updating the window
  pygame.display.flip()
  clock.tick(60)