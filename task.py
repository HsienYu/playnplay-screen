import time
import os
import random
import fitz


path_dirs = os.path.dirname(__file__) + "/pdfs"

def getRandomFile(path):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(path)
  index = random.randrange(0, len(files))
  file_path = path + '/' + files[index]
  return file_path

while True:
    print('fetch msg and save to script_sample.jsonl')
    time.sleep(10)
    print('refactor script_sample.jsonl to script_sample.txt')
    time.sleep(10)
    print('uploading to google drive')
    time.sleep(10)

    # with fitz.open(getRandomFile(path_dirs)) as doc:
    #     for page in doc:
    #         text = page.get_text()
    #         time.sleep(5)
    #         print(text)
