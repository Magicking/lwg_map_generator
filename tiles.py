Tiles = {
  'tree 1': {'unit':{'size':1},'name':'Tree 1'},
  'tree 2': {'unit':{'size':1},'name':'Tree 2'},
  'tree 3': {'unit':{'size':1},'name':'Tree 3'},
}
def find_tile_by_name(name):
  return Tiles[name.lower()]

find_tile_by_type = find_tile_by_name
