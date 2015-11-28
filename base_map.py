import json
import math
from buildings import find_building_by_name, find_building_by_type
from tiles import find_tile_by_name, find_tile_by_type

from maze import make_maze, val_maz

def _name_generator():
  return 'unamed'

def _get_middle(p, size):
  x, y = p
  x = x + size / 2
  y = y + size / 2
  return (x, y)

def _inside_circle(pc, p, r_max=7):
  xc, yc = pc
  x, y   = p
  r = (xc - x)**2 + (yc - y)**2
  return math.sqrt(r) < r_max

def _rectangle_inside_rectangle(sq_out, sq_in):
  so_u, so_d = sq_out
  si_u, si_d = sq_in

  # u----+
  # |u--+|
  # ||  ||
  # |+--d|
  # +----d
  # u: upper left corner
  # d: down right corner

  if so_u[0] < si_u[0] and so_u[1] < si_u[1]:   # upper corner check
    if so_d[0] > si_d[0] and so_d[1] > si_d[1]: # down  corner check
      return True
  return False

def _square_inside_square(sq_out, p, size):
  return _rectangle_inside_rectangle(sq_out, ((p[0]       , p[1]),
                                              (p[0] + size, p[1] + size)))

class BaseMap:
  def __init__(s, height=64, width=64, name=_name_generator()):
    s.p = {}
    s.height = height
    s.width  = width
    s.set_p('name', name)
    s.set_p('buildings', [])
    s.set_p('defaultTiles', ['Ground n %d' % x for x in [6,7,8,5,1,2,3,4]])
    s.set_p('globalVars', {'maxSupply': 100,
                           'mineDist': 7,
                           'startGold': 300})
    s.set_p('groundTiles', [])
    s.set_p('heightmap', '0' * s.width * s.height)
    s.set_p('players', [{'ai':'normal AI','slot':'open','team':'any'} for _ in range(6)])
    s.set_p('tiles', [])
    s.set_p('unitData', {})
    s.set_p('units', [])

  def set_p(s, name, data):
    ''' Set propertie '''
    s.p[name] = data

  def get_p(s, name):
    ''' Get propertie '''
    return s.p[name]

  def add_b(s, b, o, p):
    ''' Add building '''
    b = find_building_by_type(b)
    if not s.check_map(p, b['unit']['size'], b['name']):
      return False
    buildings = s.get_p('buildings')
    buildings.append({'owner':o,'type':b['name'],'waypoint':[],'x':p[0],'y':p[1]})
    s.set_p('buildings', buildings)
    return True

  def add_t(s, b, p):
    ''' Add tiles '''
    b = find_tile_by_type(b)
    if not s.check_map(p, b['unit']['size'], b['name']):
      return False
    tiles = s.get_p('tiles')
    tiles.append({'type':b['name'],'x':p[0],'y':p[1]})
    s.set_p('tiles', tiles)
    return True

  def check_map(s, p, size, t):
    ''' Check if position is available'''
    sq_b = ((1, 1), (s.height, s.width))
    if not _square_inside_square(sq_b, p, size):
      return False
    buildings = s.get_p('buildings')
    tiles = s.get_p('tiles')

    for b in buildings:
      if (b['type'] == 'Goldmine' and (t == 'Start Location' or t == 'Castle')) or (
         t == 'Goldmine' and (b['type'] == 'Start Location' or b['type'] == 'Castle')):
        pc = _get_middle((b['x'], b['y']), size)
        _p = _get_middle(p, size)
        if _inside_circle(pc, _p):
          return False
        continue
      _b  = find_building_by_name(b['type'])
      _sz = _b['unit']['size']
      sq_b = ((b['x'], b['y']), (b['x'] + _sz, b['y'] + _sz))
      if _square_inside_square(sq_b, p, size):
        return False
    for t in tiles:
      _t  = find_tile_by_name(t['type'])
      _sz = _t['unit']['size']
      sq_t = ((t['x'], t['y']), (t['x'] + _sz, t['y'] + _sz))
      if _square_inside_square(sq_t, p, size):
        return False
    return True

  def stream_map(s, f):
    _p = s.p
    _p['x'] = s.width
    _p['y'] = s.height
    f.write(json.dumps(_p))

if __name__ == '__main__':
  import sys
  mz = make_maze(21,32)
  h = w = i = 0
  for c in mz:
    if c == '\n':
      w = i
      i = 0
      h += 1
      continue
    i += 1
  m = BaseMap(height=h, width=w)
  #m.add_b('start location', 1, (1,1))
  for y in range(h):
    for x in range(w):
      if val_maz(mz, x, y, w) == '+': m.add_t('tree 1', (x, y))
      if val_maz(mz, x, y, w) == '-': m.add_t('tree 2', (x, y))
      if val_maz(mz, x, y, w) == '|': m.add_t('tree 3', (x, y))
  m.stream_map(sys.stdout)
