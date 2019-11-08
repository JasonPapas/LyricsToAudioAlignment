import os
import csv

def wait(prompt=""):
    print(prompt)
    input("PRESS ANY KEY TO CONTINUE...")

'''
This program prepares the txt files 
where the lyrics from the songs will go to.


'''
AllSongs = []
SongsLeft = []
CompletedSongs = [] #songs that we have their lyrics already

LyricsPath = "LyricsText"

with open("DAMPBperfs.csv","r") as fread1:
    reader = csv.DictReader(fread1)
    for row in reader:
        song = row["song_title"][1:]
        # print(song)
        # song = song.replace("_"," ")
        AllSongs.append(song)
    
AllSongs = list(dict.fromkeys(AllSongs))
AllSongs.sort()
SongsLeft = [i for i in AllSongs]      ## i python kanei reference an baleis list2 = list1

print(len(AllSongs))
    
for i in range(len(AllSongs)): #skips the first 40 songs because i've already transcribed the lyrics
    song = AllSongs[i]
    #print(song, i)
    if i+1 < 40:
        CompletedSongs.append(song)
        SongsLeft.remove(song)
    
songsFileNames = next(os.walk("LyricsText"))[2] #creates a list with the filenames in the LyricsText directory

for count, song in enumerate(SongsLeft):
    SongPath = f"{LyricsPath}/{song}.txt"
    if not os.path.isfile(SongPath):
        with open(SongPath,"w+") as fwrite2:
            fwrite2.write("")
    if os.path.getsize(SongPath) > 5:
        CompletedSongs.append(song)
        SongsLeft.remove(song)
        wait(song)
# #debugging prints
# print(os.path.getsize("LyricsText/behind_blue_eyes.txt"))
# print(SongsLeft[0] ,  len(SongsLeft))
# print(CompletedSongs[40], len(CompletedSongs))

with open(f"!AllSongs.csv","w+",newline="") as fwrite1: # creates a csv file with All the Songs (301) 
    header = ["SongCount","SongTitle"]
    writer = csv.DictWriter(fwrite1,fieldnames=header)
    writer.writeheader()
    for count, song in enumerate(AllSongs):
        writer.writerow({"SongCount":count+1, "SongTitle":song})

with open(f"!SongsLeft.csv","w+") as fwrite3:          # creates a csv file with the Songs that are left to transcribe 
    fwrite3.write(f"Number of Songs Left : {len(SongsLeft)}\n\n")
    for song in SongsLeft:
        fwrite3.write(f"{song}\n")




