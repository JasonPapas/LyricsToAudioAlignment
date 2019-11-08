import os 
import csv
import os.path as opath

def wait(prompt=""):
    print(prompt)
    input("PRESS A KEY TO CONTINUE...")

def get_bool(prompt):
    while True:
        try:
           return {'y':True, 'n':False}[input(prompt).lower()]
        except KeyError:
           print ("Invalid input please enter True or False!")

Data = "DAMPB_6903"

LyricPath = "SongLyrics"
songsGen = os.walk(LyricPath)
ExistedFiles = next(songsGen)[2]
ExistedSongs = []
for i,x in enumerate(ExistedFiles):
    ExistedFiles[i]= x.split('.')[0]
for File in ExistedFiles:
    FileSize = opath.getsize(f"{LyricPath}/{File}.txt")
    if FileSize > 3:
        ExistedSongs.append(File)
print(ExistedSongs)

SongsLeft = []
SongsNOTfound = ["adorn"]
with open(Data + "/ListOfSongs.csv","r") as CSV:
    reader = csv.DictReader(CSV)
    for row in reader:
        SongTitle = row["song_title"].lower()
        if SongTitle in ExistedSongs:
            pass
        elif SongTitle in SongsNOTfound:
            pass
        else:
            SongsLeft.append(row["song_title"])
print(len(SongsLeft))
with open("SongsLeft.txt","w") as f2:
    f2.write(f"Total Number of Songs ==  {len(SongsLeft)}\n\n")
CreateFiles = get_bool("Create Files? [y/n]")
for song in SongsLeft:
    with open("SongsLeft.txt","a") as csvfile:
        csvfile.write(f"{song}\n")   
    if CreateFiles:
        with open(f"{LyricPath}/{song}.txt","w+") as f:
            f.write("\n")

print(SongsLeft)