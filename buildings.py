Buildings = {
  'goldmine': {'unit':{'size':2},'name':'Goldmine'},
  'castle': {'unit':{'size':4},'name':'Castle'},
  'start location': {'unit':{'size':4},'name':'Start Location'},
}
def find_building_by_name(name):
  return Buildings[name.lower()]

find_building_by_type = find_building_by_name
