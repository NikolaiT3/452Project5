from Tkinter import *
from math import *
import thread
import random
import time
import glob

# ===============================
# IMPORT FILE FUNCTION
# ===============================
def inputFile(path):
  print path
  filenames = glob.glob(path+"*.txt")
  print filenames
  text =[]
  for file in filenames:
      text += open(file,'r')
  return sanitize_input(text)

# ===============================
# SANITIZE INPUT FUNCTION
# ===============================
def sanitize_input(text):
  sanitized_text = []
  for word in text:

#       Get rid of punctuation, convert to lower, remove new line characters
#       text = text.translate(None, string.punctuation).lower()

      sanitize = re.sub("[^\w']|_", " ", word.lower())
      words = list(sanitize.split())

#       List of lists to keep books structure
      sanitized_text.append(words)
      sanitized_text = input_toNumber(sanitized_text)
  return sanitized_text

def input_toNumber(text):
  sanitized_number = []
  for word in text:
      temp = []
      for number in word:
          new = float(number)
          temp.append(new)
      sanitized_number.append(temp)
  return sanitized_number

inputBlocks = inputFile("./inputs/Blocks/")
inputEnds = inputFile('./inputs/End/')[0]
inputStarts = inputFile('./inputs/Start/')[0]

print inputBlocks
print inputStarts
print inputEnds

