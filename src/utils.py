import sys

def printToConsole(data, title):
  print('-----------------------------', file=sys.stderr)
  print(title, data, file=sys.stderr)
  print('-----------------------------', file=sys.stderr)
  