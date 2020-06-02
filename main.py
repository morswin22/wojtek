import pygame
from tensorflow import keras
import numpy as np
import sys
import ctypes
from matrix import doolittle, cholesky

class Cell:
  def __init__(self, x, y, w, h, callback=None):
    self.create(w, h)
    self.pos = [x, y]
    self.evaluated = False
    self.ordered = False
    self.orderTick = None
    self.callback = callback
    self.text = None
    self.value = None

  def create(self, w, h):
    self.surface = pygame.Surface((w, h))
    self.surface.fill((0,0,0))
    self.width = w
    self.height = h

  def clear(self):
    self.surface.fill((0,0,0))
    self.evaluated = False

  def draw(self, screen, tick, evaluationTimeout):
    if self.evaluated:
      if self.text == None:
        global font
        self.text = font['big'].render(str(self.value), True, (255, 255, 255))
      w, h = self.text.get_size()
      screen.blit(self.text, (int(self.pos[0] + (self.width - w)/2), int(self.pos[1] + (self.height - h)/2)))
    else:
      screen.blit(self.surface, (self.pos[0], self.pos[1]))
    if self.ordered:
      left = self.orderTick + evaluationTimeout - tick
      pygame.draw.arc(screen, (255,255,255), pygame.Rect(self.pos[0] + self.width - 25, self.pos[1] + 5, 20, 20), np.pi / 2, (2 * np.pi * (left/evaluationTimeout)) + (np.pi/2), 2)
      if left < 0:
        self.evaluate()

  def order(self, tick):
    global matrix
    if matrix:
      x, y = self.pos[0] // self.width, self.pos[1] // self.height
      matrix[y][x] = None
    self.evaluated = False
    if tick:
      self.ordered = True
      self.orderTick = tick
    else:
      self.ordered = False

  def evaluate(self):
    pxarray = pygame.PixelArray(pygame.transform.scale(self.surface, (28, 28)))
    data = []
    for y in range(pxarray.shape[0]):
      row = []
      for x in range(pxarray.shape[1]):
        row.append([pxarray[x, y] / 16777215])
      data.append(row)
    del pxarray
    prediction = model.predict([data])[0]
    self.evaluated = True
    self.value = prediction.argmax()
    self.text = None
    self.ordered = False
    if self.callback:
      self.callback(self.value)
    else:
      global matrix
      x, y = self.pos[0] // self.width, self.pos[1] // self.height
      matrix[y][x] = self.value
      done = True
      for i in matrix:
        for j in i:
          if j == None:
            done = False
      if done:
        print("Dla macierzy", matrix)
        try:
          L, U = doolittle(matrix)
          print("Metoda LU")
          print("L", L)
          print("U", U)
        except:
          print("Tej macierzy nie da się rozłożyć metodą LU")
        try:
          L, Lt = cholesky(matrix)
          print("Rozkład Choleskiego")
          print("L", L)
          print("Lt", Lt)
        except:
          print("Tej macierzy nie da się rozłożyć dekompozycją Choleskiego")
        print("")


def roundline(surface, start, end, radius=1):
  dx = end[0]-start[0]
  dy = end[1]-start[1]
  distance = max(abs(dx), abs(dy))
  for i in range(distance):
    x = int(start[0] + float(i) / distance*dx)
    y = int(start[1] + float(i) / distance*dy)
    pygame.draw.circle(surface, (255, 255, 255), (x, y), radius)

def get_cell(cells, pos):
  for cell in cells:
    if (pos[0] < cell.pos[0] or pos[0] > cell.pos[0] + cell.width or pos[1] < cell.pos[1] or pos[1] > cell.pos[1] + cell.height) == False:
      return cell

def create_matrix(n):
  global cells, matrix, grid, status
  if n > 1:
    status = 1
    matrix = []
    for i in range(n):
      array = []
      for j in range(n):
        array.append(None)
      matrix.append(array)
    width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    size = n*140
    if size > width or size > height:
      size = min(width, height) - 20
    pygame.display.set_mode((size, size))
    pygame.display.set_caption('Macierz {}x{}'.format(n, n))
    cells = []
    cell_size = int(size/n)
    grid = []
    for i in range(1, n):
      grid.append([(0, i*cell_size), (size, i*cell_size)])
      grid.append([(i*cell_size, 0), (i*cell_size, size)])
    for i in range(n*n):
      x = i % n
      y = (i - x) // n
      cells.append(Cell(x*cell_size, y*cell_size, cell_size, cell_size))

model = keras.models.load_model('model.h5')
model.summary()

pygame.font.init()
screen = pygame.display.set_mode((140,140))
font = {
  "small": pygame.font.SysFont('Calibri', 16),
  "medium": pygame.font.SysFont('Calibri', 32),
  "big": pygame.font.SysFont('Calibri', 48)
}

draw_on = False
last_pos = (0, 0)
radius = 4
evaluationTimeout = 2500

cells = [Cell(0, 0, 140, 140, create_matrix)]
cell = None

status = 0
tick = None

matrix = None
grid = None

while 1:
  tick = pygame.time.get_ticks()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      screen.fill((0,0,0))
      cell = get_cell(cells, event.pos)
      if cell:
        if cell.ordered:
          cell.order(False)
        if cell.evaluated:
          cell.clear()
        pygame.draw.circle(cell.surface, (255, 255, 255), (event.pos[0] - cell.pos[0], event.pos[1] - cell.pos[1]), radius)
        draw_on = True
    elif event.type == pygame.MOUSEBUTTONUP:
      draw_on = False
      cell.order(tick)
    elif event.type == pygame.MOUSEMOTION:
      if draw_on and cell:
        pygame.draw.circle(cell.surface, (255, 255, 255), (event.pos[0] - cell.pos[0], event.pos[1] - cell.pos[1]), radius)
        roundline(cell.surface, (event.pos[0] - cell.pos[0], event.pos[1] - cell.pos[1]), (last_pos[0] - cell.pos[0], last_pos[1] - cell.pos[1]),  radius)
      last_pos = event.pos

  screen.fill((0,0,0))
  for c in cells:
    c.draw(screen, tick, evaluationTimeout)
  if status == 0:
    color = np.interp(tick, [0, 2000, 2500], [255, 255, 0])
    if color > 0:
      screen.blit(font['small'].render("Wybierz rozmiar", True, (color, color, color)), (16, 54))
      screen.blit(font['small'].render("macierzy (n x n)", True, (color, color, color)), (18, 74))
  elif status == 1:
    for line in grid:
      pygame.draw.line(screen, (255, 255, 255), line[0], line[1])
  pygame.display.update()
  pygame.time.delay(17)