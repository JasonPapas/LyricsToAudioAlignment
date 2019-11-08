import os
import csv

'''
<NSN> = Non Speaker Noise phoneme for noises 




Observations for types of singing for songs:
    - Blue Christmas : by Elvis Prisley : very prolonged endings for some words e.g. blue
    - 


'''
KaldiPATH = "/home/jason/kaldi/egs/jason"

def CreateUtts(csvFilePath):
    Utterances = []
    with open("csvFilePath","r") as fread:
        reader=csv.DictReader(fread)
        for row in reader:
            Utterances.append(row["performance_id"])
    Utterances.sort()
    return Utterances

def Utt2Song(Utt):
    with open("DAMPBperfs.csv","r") as fread:
        reader = csv.DictReader(fread)

        for row in reader:
            if Utt == row["performance_id"]:
                Song4Utt = row["song_title"][1:]
                break
    return Song4Utt

def Song2String(SongName):
    SongPath = f"LyricsTextClear/{SongName}.txt"
    if os.path.getsize(SongPath) > 10:
        with open(SongPath,"r") as fread:
            out = fread.read()
        return out
    else:
        return None


def main():

    print("~~~~~~Creating the text file ~~~~~~~~\n")
    
    global KaldiPATH
    DataDir = "DAMPB_kaldi/data/train"
    
    Utterances = CreateUtts("DAMPBperfs.csv")
    

    ##Creating text FILE 
    
    with open(f"{KaldiPATH}/{DataDir}/text","w+") as fwrite:
        # count=0
        for Utt in Utterances:            ##TODO: Seperate Utterances further by Song. Create new folders for each song ?
            Song4Utt = Utt2Song(Utt)        # so it can work with lesser than 300 songs.
            
            if Song2String(Song4Utt) != None:
                transcript = Song2String(Song4Utt)
                
                fwrite.write(Utt + " " + transcript + "\n")
                # if count > 10:
            #     break
            # count+=1 
    print("#~#~ DONE with text file ~#~#")

            





if __name__ == '__main__': 
      
    # Calling main() function 
    main() 