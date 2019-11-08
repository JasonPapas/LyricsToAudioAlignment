import os
import re

def wait(prompt=""):
    print(prompt)
    input("PRESS ANY KEY CONTINUE...\n")

path = "LyricsText"

# pattern = "([0-9a-z]+ ){1,6}[a-z]+"
# for filename in os.listdir(path):
#     SongName = filename[:-4]
#     if re.fullmatch(pattern,SongName):
#         SongName=SongName.replace(" ","_")
#         dst = f"{path}/{SongName}.txt"
#         src = f"{path}/{filename}"
#         os.rename(src,dst)



#     # 15 seconds of fame.txt
with open("LyricsTextClear/15_seconds_of_fame.txt","r") as fread:
    a = fread.read()
    print(type(a))