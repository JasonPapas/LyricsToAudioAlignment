"""
This script takes the files from the DAMP Dataset and copies some of them 
based on the carefully curated DAMPB Dataset. 
Which files are included in this Dataset are listed in the DAMPBPerfs.csv file.
"""
import os
import csv
import shutil ##shutil.copy(src, dst)
'make unique list list(dict.fromkeys(seq))'

class RawData():
    def __init__(self):
        self.SpkList = []
        self.UttList = []
        self.SongNames = []

    
    def SortLists(self):
        self.SpkList = sorted(self.SpkList)
        self.UttList = sorted(self.UttList)
        
        self.SongNames = list(dict.fromkeys(self.SongNames))
        self.SongNames = sorted(self.SongNames)


    def YieldSpk2Utt(self, utt):
        self.diktis = self.UttList.index(utt)
        Spk = self.UttList[self.diktis].split("_")[0]
        return f"{Spk} {self.UttList[self.diktis]}"
    

            
def wait(prompt=""):
    print(prompt)
    input("PRESS A KEY TO CONTINUE...")
        
def get_bool(prompt):
    while True:
        try:
           return {'y':True, 'n':False}[input(prompt).lower()]
        except KeyError:
           print ("Invalid input please enter True or False!")


def MakeDirStructure (newdir):
    print('~~ Reading through the data ~~')
    count=0
    for Spk in NewDataset.SpkList:
    ## MAKING DIRECTORIES FOR EACH SPEAKER    
    ## Creating DIrectories for speakers a.k.a singers
        SpkDir = newdir+ '/' + Spk
        print(SpkDir)
        try:
            # Create speaker Directory
            os.mkdir(SpkDir)
            print("~~Directory " , SpkDir ,  " Created ") 
        except FileExistsError:
            print("~~~~~Directory " , SpkDir ,  " already exists.")
        count+=1
         
def MakeOldLists():
    print("Creating OLD Lists ~~~~~~~~~!!!!!!!~~~~~~~~")
    with open("DAMPperfs.csv") as OldData:
        OldReader = csv.DictReader(OldData)
        OldSortedReader = sorted(OldReader, #sorts the utt and spk IDs values from A to Z 
                    key=lambda row:(int(row['plyrid']),int(row['perf_key'])),
                    reverse=False)
        for line in OldSortedReader:
            Utt = line["perf_key"]
            Spk = line["plyrid"]
            Song = line["songid"][1:].replace('_',' ')
            OldDataset.UttList.append(Utt)
            OldDataset.SpkList.append(Spk)
            OldDataset.SongNames.append(Song)
        wait(f"Number Of Old Songs : {len(OldDataset.SongNames)}")

    
def MakeNewLists():
    print("Creating NEW Lists ~~~~~~~~~!!!!!!!~~~~~~~~")
    with open("DAMPBperfs.csv","r") as NewData:
        NewReader = csv.DictReader(NewData)
        NewSortedReader = sorted(NewReader, #sorts the utt and spk IDs values from A to Z 
                    key=lambda row:(int(row['singer_account_id']),int(row['performance_id'])),
                    reverse=False)
        for line in NewSortedReader:
            #print(line)
            Utt = line["performance_id"]
            Spk = line["singer_account_id"]
            Song = line["song_title"][1:].replace('_',' ')
            if Spk  not in NewDataset.SpkList:
                NewDataset.SpkList.append(Spk)
            
            NewDataset.UttList.append(Utt)
            NewDataset.SongNames.append(Song)

        wait(f"Number Of New Songs : {len(NewDataset.SongNames)}")
    

def CopyFiles(olddir, newdir,FileType):
    print(f'~~ Copying files from {olddir} to {newdir}')
    
    failsafe = 0
    for count, utt in enumerate(OldDataset.UttList):
        if utt in NewDataset.UttList:
            CurrentSpk = NewDataset.YieldSpk2Utt(utt).split(" ")[0]
            OldPath = f"{olddir}/{utt}.{FileType}"
            if failsafe % 500 == 0:
                #print(f"## Copying file: {utt}.m4a from {OldPath} to {NewPath}##")
                print(f"Iteration: {count}  \t CurrentUtt: {utt} \t CURRENT UTT NUMBER: {failsafe}")
            if failsafe > 6903:
                wait("SOMETHING WENT TERRIBLY WRONG.")
            NewPath = f"{newdir}/{CurrentSpk}"
            # print(f"## Copying file: {utt}.m4a from {OldPath} to {NewPath}##")
            if os.path.isfile(f"{NewPath}/{utt}.{FileType}"):
                print(f"the File {NewPath}/{utt}.{FileType} already exists")
            else:
                shutil.copy(OldPath,NewPath)
            failsafe +=1

            NewDataset.UttList.remove(utt)



if __name__ == "__main__":
    # Create directory
    folders = ['audio', 'mfcc', 'pitch']
    FileTypes = ["m4a","csv", "csv"]
    OldPath = "DAMP_34621"
    NewPath = "DAMPB_6903"

    OldDataset = RawData()
    NewDataset = RawData()
    print("~~~~~~~~~~ Parsing data from DAMPB")
    MakeOldLists()
    OldDataset.SortLists()
    wait(f"Number Of Unique Old Songs : {len(OldDataset.SongNames)}")

    MakeFilesBool = get_bool('Make new directories for speaker and songs? [y/n]')


    if MakeFilesBool:
        for part in folders:
            print("## Creating Directories ##")
            print(f"We are at part: {part}")
            MakeDirStructure(f"{NewPath}/{part}")
        
    CopyFilesBool = get_bool('Copy files that belong to new list? [y/n]')
    if CopyFilesBool:
        for part in folders:        
            MakeNewLists()
            NewDataset.SortLists()
            print("## Copying Files ##")
            print(f"We are at part: {part}")
            FileType = FileTypes[folders.index(part)]  
            CopyFiles(f"{OldPath}/{part}",f"{NewPath}/{part}", FileType)
    else:
        MakeNewLists()
        NewDataset.SortLists()
        wait(f"Number Of Unique New Songs : {len(NewDataset.SongNames)}")
    print(f'~~The number of songs in DAMP Dataset (with {len(OldDataset.UttList)} Performances) is {len(OldDataset.SongNames)}\n')
    print(f'~#~#~The number of songs in DAMPB Dataset (with {len(NewDataset.UttList)} Performances) is {len(NewDataset.SongNames)}')
    
    for part in ["DAMP_34621","DAMPB_6903"]:
        FieldNames = ["song_number", "song_title"]
        if part == "DAMP_34621":
            data = OldDataset     
        else:
            data = NewDataset
        
        with open(f"{part}/ListOfSongs.csv","w", newline='') as wfile: 
            #newline='' is there so the resulting csv doesn't have its lines separated bys new line
                writer = csv.DictWriter(wfile,fieldnames=FieldNames)
                writer.writeheader()
                for counter,song in enumerate(data.SongNames):
                    row = {"song_number":counter+1, 
                            "song_title":data.SongNames[counter]
                        }
                    writer.writerow(row)



    

        