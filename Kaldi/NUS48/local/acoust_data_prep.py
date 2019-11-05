import os
import argparse
import sys
if sys.platform == "linux" or sys.platform == "linux2":
    # linux
	sys.path.append(r"/mnt/HDD_Storage/Dev/LyricsToAudio/Data")
elif sys.platform == "win32":
    # Windows...
	sys.path.append(r"B:\Dev\LyricsToAudio\Data") 
from ClearLyrics import ClearSentence

#TODO: 1) make the wav.scp and utt2spk functions that make the corresponding files.
#	   2) documentate what type of folder structure this script works with.

def CreateUttID(UttType): #returns the utt_name and path to utt audio file
	# print(os.getcwd())
	root, CurrentCorpus = os.path.split(os.getcwd())
	if CurrentCorpus == "nus-smc-corpus_48":
		if (UttType in ["sing", "read"]): 
			Utt_ID_list = []
			UttPath = []
			for Spk in os.listdir("audio"): #iterating through the Speaker in DataDir
				# UttType = "sing"
				CWD = f"audio/{Spk}/{UttType}" #CWD == Current Working Directory
				# print(Spk, CWD)
				for file in os.listdir(CWD):
					# print(filename)
					FileName, FileExt = os.path.splitext(file)
					# print(FileExt)
					if FileExt == ".wav":
						Utt_ID_list.append(FileName)
						UttPath.append(os.path.abspath(os.curdir) + f"/{CWD}/{file}")
			
			return Utt_ID_list, UttPath
		else:
			while (UttType  not in ["sing", "read"]):
				print("You must specify the kind of audio to be prepared.")
				UttType = input("Enter wether you want the sung " + \
								"or spoken audio data? [sing/read]")
	else: 
		print("! ! ! Wrong Directory ! ! ! ")
		print(f"Current Directory: {root}/{CurrentCorpus} \n \n")
		sys.exit()


def MakingTextFile(DataDir, UttType): 
	"""
	Here we make the text file. Which has the format:  utt-id WORD1 WORD2 WORD3 ...

	For NUS48 Dataset, DataDir must go inside nus-sms-corpus_48 folder.

	"""
	OldDir = os.getcwd()
	#changing to the Data Directory
	os.chdir(DataDir)

	
	SongDict = {}
	print("1st instance of CreateUttID")
	Utt_ID_list, _ = CreateUttID(UttType)

	for file in os.listdir("lyrics"): #iterating through the songs in DataDir
		CWD = f"lyrics/{file}"
		song, _ = os.path.splitext(file)
		with open(CWD,"r") as fread:
			sentence = fread.read()
			SongDict[song] = ClearSentence(sentence)
	
	#writing the text file
	os.chdir(OldDir)
	_, last_dir = os.path.split(os.getcwd())
	if last_dir == "local":	
		os.chdir(os.pardir)	
	
	with open("data/train/text","w+") as fwrite:
		for utt in Utt_ID_list:
			CurrSong = utt.split("-")[1].split(".")[0]
			# print(CurrSong)
			fwrite.write(f"{utt} {SongDict[CurrSong]}\n")
	
	
	# print(os.getcwd())

def MakingWavFile(DataDir, UttType):
	"""
	Here we make the text file. Which has the format: file_id path/file

	For NUS48 Dataset:
		1) DataDir must go inside nus-sms-corpus_48 folder.
		2) I haven't segmented the audio files so: file_id == utt_id

	"""
	OldDir = os.getcwd()
	#changing to the Data Directory
	os.chdir(DataDir)
	print("2nd instance of CreateUttID")
	Utt_ID_list, UttPath = CreateUttID(UttType)

	os.chdir(OldDir)
	_ , last_dir = os.path.split(os.getcwd())
	if last_dir == "local":	
		os.chdir(os.pardir)
	with open("data/train/wav.scp","w+") as fwrite:
		for path2utt, utt in zip(UttPath, Utt_ID_list):
			#TODO: make it so it works with cases of non-wav files. Add in the string 
			#	   command so Kaldi can on the fly convert it to wav.
			#	   special case with .m4a files. for all the others use sox.
			fwrite.write(f"{utt} {path2utt}\n")

def MakingUtt2spkFile(DataDir, UttType):
	"""
	Here we make the utt2spk file. Which has the format: utt_id spkr

	For NUS48 Dataset:
		1) DataDir must go inside nus-sms-corpus_48/audio folder.

	"""
	OldDir = os.getcwd()
	os.chdir(DataDir)
	
	print("3rd instance of CreateUttID")
	os.chdir(os.pardir) #FIXME: very very very πρόχειτη λύση
	Utt_ID_list, _ = CreateUttID(UttType)
	
	os.chdir("audio")	#FIXME: very very very πρόχειτη λύση
	Spk_ID = os.listdir(os.curdir)	

	os.chdir(OldDir)

	with open("data/train/utt2spk","w+") as fwrite:
		for spk in Spk_ID:
			for utt in Utt_ID_list:
				if utt.split("-")[0] == spk:
					fwrite.write(f"{utt} {spk}\n")
	
	_ , last_dir = os.path.split(os.getcwd())
	if last_dir == "local":	
		os.chdir(os.pardir)



def main():
	parser = argparse.ArgumentParser(description="Preparing the necessary files for Kaldi.")
	parser.add_argument("DataDir", 
						help="The location to the data files that you want to prepare.", 
						type=str)
	parser.add_argument("DstDir",
						help="The location to write the new files. e.g. text,wav.scp,etc.",
						type=str)
	parser.add_argument('-t','--text',
						help="Makes the 'text' file. " + \
							"This file's format is: utt_id WORD1 WORD2 WORD3 ...",
						action="store_true")
	parser.add_argument('-w', '--wav',
						help="Makes the 'wav.scp' file. "+ \
							"This file's format is: file_id path/file",
						action="store_true")
	parser.add_argument('-u','--utt2spk',
						help="Makes the the 'utt2spk' file. "+ \
							"This file's format is: utt_id speaker_id",
						action="store_true")
	# parser.add_argument('-words',
	# 					help="Makes the the 'words.txt' file. "+ \
	# 						"This file contains all the unique words in the lyrics.",
	# 					action="store_true")
	args = parser.parse_args()

	UttType = input("Enter wether you want the sung " +\
					"or spoken audio data? [sing/read]")
	if args.text:
		#Making the text file
		MakingTextFile(args.DataDir, UttType)
	if args.wav:
		#Making the wav.scp file
		MakingWavFile(args.DataDir, UttType)
	if args.utt2spk:
		path = args.DataDir + "/audio"
		MakingUtt2spkFile(path, UttType)
	# if args.words:
    # 	MakingWordsFile(args.DataDir, args.DstDir)

if __name__ == "__main__":
	sys.exit(main())