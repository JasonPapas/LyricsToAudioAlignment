import os
import sys
from copy import deepcopy
if sys.platform == "linux" or sys.platform == "linux2":
	# linux
	sys.path.append(r"/mnt/HDD_Storage/Dev/LyricsToAudio/Data")
elif sys.platform == "win32":
	# Windows...
	sys.path.append(r"B:\Dev\LyricsToAudio\Data") #For ATHENA RC Computer
from ClearLyrics import ClearSentence

def replace(list , old_str, new_str):
	return [new_str if x == old_str else x for x in list]

def read_lines(file_path):
	with open(file_path,"r") as fread:
		reader= fread.read()
		rows = reader.split("\n")
		if rows[-1] == "" :
			# print(f"i'm in file: {file_path}\n rows[-2]== \"{rows[-2]}\"\n")
			rows = rows[:-1]
			# print("~~~~~I'm inside IF in read_lines")
			
	return rows

def AllWords(DataDir,DstDir):
	# """
	# Gathering AllWords of the Dataset. Uniquefy them 
	# And Also having a dictionary with format 'Song_ID': ['WORD1','WORD2', ...]
	# where Song_ID is a string: 01,02,03, ..., 19,20
	# returning the dictionary and writing a file called words.txt with the unique words
	# """
	AllWords = []
	All_Words_song_dict = {}
	
	for song_file in os.listdir(f"{DataDir}/lyrics"):
		with open(f"{DataDir}/lyrics/{song_file}","r") as fread:
			CurrLyrics = fread.read()
			# print(CurrLyrics)
			
			song, _ = os.path.splitext(song_file)
			clear_lyrics_list = ClearSentence(CurrLyrics).split(" ")
			All_Words_song_dict[song] = clear_lyrics_list
			for word in clear_lyrics_list:
				AllWords.append(word)
	
	# AllWords_list = AllWords.split(" ")
	UniqueWords = sorted(list(dict.fromkeys(AllWords))) # we sort and uniquefy the words.
	UniqueWords = UniqueWords[1:]	#we remove a blank "" element
	with open(f"{DstDir}/words.txt","w+") as fwrite:
		writer = "\n".join(UniqueWords)
		fwrite.writelines(writer)
	# print(UniqueWords)
	# print(Words_per_song)
	return All_Words_song_dict

def phones4utt(DataDir,utt_list):
	#
	#where utt_id is a string with format: '<spkr_id>-<song_id>' (e.g.: 'ADIZ-01')
	#Input: 
	# 		DataDIr: the general directory of the Dataset
	#		utt_list: a list with all the utts we want phones for
	#Output:
	#		phones_per_utt: dictionary with keys the utt_id 
	# 									and values a list with all the phones for each utt
	#################
	phones_per_utt = {}
	for utt in utt_list:
		spkr = utt.split("-")[0]
		CWD = os.path.join(DataDir,"audio",spkr,"sing")
		utt_file = f"{utt}.txt"
		phones = []
		with open(os.path.join(CWD,utt_file),"r") as fread:
			reader = fread.read()
			#reading the lines of the file
			lines = reader.split("\n")
			for line in lines:
				if line != "":
					# if utt_name == "ADIZ-09":
					# 	temp = line.split(" ")[2]
					# 	print(temp, i)
					phones.append(line.split(" ")[2])
		phones_per_utt[utt] = phones
	return phones_per_utt

def Create_utt2paths_lists(WavDir):
	print("#######\nExtracting abs paths for Utts" + \
		f"in directory {WavDir}\n#######")
	utt_list, path_list = [], []
	for file in os.listdir(WavDir):
		file_name, _= os.path.splitext(file)
		path_list.append(os.path.join(WavDir,file))
		utt_list.append(file_name)
	return utt_list, path_list

def Create_utt_song_spkr_list(WavDir):
	print("#######\nExtracting Utts and songs names from file names" + \
		f"from directory:\n{WavDir}\n########")
	# good_utts_dir = "ready_good_utts"
	utt_list, song_list, spkr_list= [],[],[]
	for file in os.listdir(WavDir):
		file_name, file_ext = os.path.splitext(file)
		if file_ext == ".wav":
			utt_list.append(file_name)
	utt_list = sorted(utt_list)
	for utt in utt_list:
		spkr,song = utt.split("-")
		song_list.append(song)
		spkr_list.append(spkr)
		print(utt,spkr,song)

	return utt_list,song_list, spkr_list

def check_if_elem_of_2lists_match(list1,list2):
	c1,c2,c3 = 0,0,0
	diff = len(list1)-len(list2)	
		
	if diff > 0:
		i=0
		print("\n#############")
		print("WRONG!\n")
		
		for i, phone_seq in enumerate(list2):
			phones = phone_seq.replace(":"," ")
			
			print(list1[i]+" "+phones)
		print("#############\n")
		c1+=1
	elif diff<0:
		print("\n#############")
		print("WRONG!\n")
		for i in range(len(list1)):
			phones = list2[i].replace(":"," ")
			
			print(list1[i]+" "+phones)
		print("#############\n")
		c2+=1
	else:
		print("right!")
		c3+=1
	cwrong = c1+c2
	tot = c1+c2+c3
	print(f"Number of mismatches: {cwrong}/{tot} \nNumber of matches: {c3}/{tot}")