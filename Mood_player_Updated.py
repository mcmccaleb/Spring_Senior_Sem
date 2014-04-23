from Tkinter import *
import tkFileDialog
import Tkinter
import tkFont
import Tkinter as tk
import os, sys
from threading import Thread
import subprocess

path="music"
dirs=os.listdir(path)
value="0"
song="0"
count = len(dirs)
num=-1
me=0


import os
#use the subprocess module to call the essentia extractor that will return gaia values
import subprocess
from os import listdir
from os.path import isfile, join
import shelve
import json
import numpy as np
import math
import random

numCharacteristics = 12

#now: test code, and debug startup process before moving onto generation

def main(song, mood):
    #check in the shelve module to see if this is the first time MoodPlay has been used on this computer
    #if so:
    dbname = 'moodplay.db'
    db = shelve.open(dbname)
    try:
        openYet = db['openYet?']
    except:
        openYet = False
        db.close()
        startup(dbname)
    try:
        print("openYet is " + str(openYet))
        songList = db['songList']
        matrix = db['similarityMatrix']
    finally:
        db.close()
    #onclickMood:
#        onclickMood(mood)
 #   onclickplay:
#        onClickPlay(dbname, songName, mood, time)
    #printMatrix(matrix, songList)
    db = shelve.open(dbname)
    # songList = db['songList']
    # for song in songList:
    #     print song
    # song = input('Enter a song choice')
    # mood = 'Happy'
    time = 'afternoon'
    db.close()
    onClickPlay(dbname, song, mood, time)
        
    

def startup(dbname):
    songID = 0
    #first arg ("./streaming_extractor_archivemusic") = extractor to be called
    #second arg(../../../audio.mp3) = music file
    #third arg (returnfile2) = output file (from which the needed information -- gaia stuff -- will be read)
    #go into relevant directory, check for song files
    songList = []
    songStringList = []
    bigCharacteristicList = []
    
    thisDir = os.getcwd()
    songID = 0
    #print(thisDir)
    musicDir = thisDir + '/music'
    print(musicDir)
    #os.listdir(musicDir)
    filenames = next(os.walk(musicDir))[2]
    for filename in filenames:
        songList.append(filename)
        print filename
    """for f in thisDir:
        print("in for loop, f is " + f)
        if isfile(f):
            songList.append(f)"""
    #subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[0], "audioTest"])
    # I know the following is roundabout, but it works...
    #songList = songList[:3]
    for song in songList:
        similarityList = []
        songString = str(song) + str(songID) + ".json"
        songStringList.append(songString)
        print("song equals " + song + " and songID equals " + str(songID))
        subprocess.call(["./streaming_extractor_archivemusic", "music/" + filenames[songID], songString])
        songID+=1
        #now: go into songString, and create an array for that song with its properties
        #then add that to the big list of songs
        json_data = open(songString)
        data = json.load(json_data)
        danceable = data["highlevel"]["danceability"]["all"]["danceable"]
        similarityList.append(danceable)
        female = data["highlevel"]["gender"]["all"]["female"]
        similarityList.append(female)
        instrumental = data["highlevel"]["voice_instrumental"]["all"]["instrumental"]
        similarityList.append(instrumental)
        chord_scale = data["tonal"]["chords_scale"]
        if chord_scale == "major":
            chord_scale = 1
        else:
            chord_scale = 0
        print("danceable is " + str(danceable))
        print("female is " + str(female))
        print("instrumental is " + str(instrumental))
        print("chord_scale is " + str(chord_scale))
        similarityList.append(chord_scale)
        genreList= ("alternative", "blues", "electronic", "funksoulrnb", "jazz", "pop", "raphiphop", "rock")
        for genre in genreList:
            item = data["highlevel"]["genre_dortmund"]["all"][genre]
            similarityList.append(item)
            print(genre + ": " + str(item))
        bigCharacteristicList.append(similarityList)

    for LIST in bigCharacteristicList:
        for item in LIST:
            print(item)

    numSongs = len(songList)
    similarityProfiles = np.empty((numSongs, numSongs))
    for song1 in songList:
        index1 = songList.index(song1)
        for song2 in songList:
            index2 = songList.index(song2)
            characteristicNum = 0
            similaritySum = 0
            while characteristicNum < numCharacteristics:
                print("index1 is " + str(index1))
                print("index2 is " + str(index2))
                print("characteristicNum is " + str(characteristicNum))
                similaritySum += pow(bigCharacteristicList[index1][characteristicNum], 2)
                similaritySum += pow(bigCharacteristicList[index2][characteristicNum], 2)
                characteristicNum += 1
            #only fill in top right triangle
            similaritySum = math.sqrt(similaritySum)
            if index1 > index2:
                similarityProfiles[index1][index2] = similaritySum
            #similarityProfiles[index2][index1] = similaritySum
    database = shelve.open(dbname)
    try:
        database['openYet?'] = True
        database['similarityMatrix'] = similarityProfiles
        database['songList'] = songList
        database['songStringList'] = songStringList
        database['bigCharacteristicList'] = bigCharacteristicList
    finally:
        database.close()

    """
    #index of the song whose similarity list we are computing
    index1 = 0
    #index of the songs we're comparing it to
    index2 = 0
    noCompare = 0
    Sum = 0
    for song in songList:
        noCompare = songList.index(song)
        if (index2 != noCompare):
            characteristicNum = 0
            for characteristic in bigCharacteristicsList[index2]:
                Sum += characteristic^2 + bigCharacteristicsList[index1][characteristicNum]
                characteristicNum += 1
        index+=1
       alternative = data["highlevel"]["genre_dortmund"]["all"]["alternative"]
        blues = data["highlevel"]["genre_dortmund"]["all"]["blues"]
        electronic = data["highlevel"]["genre_dortmund"]["all"]["electronic"]
        funksoul = data["highlevel"]["genre_dortmund"]["all"]["funksoulrnb"]
        jazz = data["highlevel"]["genre_dortmund"]["all"]["jazz"]"""
        #now can access any descriptors with data[key1][key2]
    #add all of these things to a shelve module
    #create a boolean within the shelve module that will explain that we have already made this list
        #sum of squared distances (Euclidean distance)

        #features: danceability, chords, instrumental, female, alternative, blues, electronic, folkcountry, funksoulrnb, jazz, pop, raphiphop, rock

"""
def playList(generatedList):
    for song in generatedList:
        play using mplayer"""

def createPlaylist(generationSongList, generationNumList, totalSum):
    generatedList = []
    #helpindex = 1
    #print("generation song list is: ")
    # for song in generationSongList:
    #     print song
    #print("total sum is: " + str(totalSum))
    # helpindex2 = 1
    # print ("generation num list is: ")
    # for num in generationNumList:
    #     print(str(helpindex2) + " num: " + str(num))
    #     helpindex2 += 1
    while len(generationSongList) > 1:
        #print ("try: " + str(helpindex))
        randomNum = random.uniform(0, totalSum)
        numInList = generationNumList[0]
        currIndex = 0
        # print("currIndex is " + str(currIndex))
        # print("randomNum is " + str(randomNum))
        # print("numInList is: " + str(numInList))
        while randomNum > numInList:
            currIndex += 1
            #error below!
            numInList = generationNumList[currIndex]
            #print("numInList is now: " + str(numInList))
        #now: numInList is just greater than the number generation
        #print("currIndex is " + str(currIndex))
        #print("numInList is " + str(numInList))
        
        if currIndex ==0:
            songPicked = generationSongList.pop(0)
        else:
            songPicked = generationSongList.pop(currIndex - 1)
        generatedList.append(songPicked)
        if currIndex ==0 and len(generationSongList) > 0:
            sumExtracted = generationNumList[currIndex + 1] - generationNumList[currIndex]
            numTakenOut = generationNumList.pop(currIndex + 1)
            indexToFix = currIndex + 1
            
        elif len(generationSongList) > 0:
            sumExtracted = generationNumList[currIndex] - generationNumList[currIndex - 1]
            #print("sum Extracted was: "+ str(sumExtracted))
            numTakenOut = generationNumList.pop(currIndex)
            #print("numTakenOut was " + str(numTakenOut))
            indexToFix = currIndex
        for i in range (currIndex, len(generationNumList)):
            #print("generationNumList[" + str(i) + "] was: " + str(generationNumList[i]))
            generationNumList[i] = generationNumList[i] - sumExtracted
            #print("generationNumList[" + str(i) + "] is now: " + str(generationNumList[i]))
        totalSum = totalSum - sumExtracted
        #print("total sum is now " + str(totalSum))
        # helpindex2 = 1
        # print ("generation num list is: ")
        # for num in generationNumList:
        #     print(str(helpindex2) + " num: " + str(num))
        #     helpindex2 += 1
        # print ("try: " + str(helpindex))
        # for song in generationSongList:
        #     print song
        #     play_list_display.insert(END,song)
        # helpindex +=1
    generatedList.append(generationSongList[0])
    for song in generatedList:
        print(song)
        play_list_display.insert(END,song)
    #playList(generatedList)
    #print("Bool was " + str(boolAlreadyGenerated))
    #playList(generatedList)

def createGenerationProfile(dbname, songName, mood, time):
    print("FROM SCRATCH")
    db = shelve.open(dbname)
    songList = db['songList']
    similarityMatrix = db['similarityMatrix']
    indexSongPlayed = songList.index(songName)
    totalSum = 0
    similarity = 0
    generationNumList = []
    generationSongList = []
    generationNumListToSave = []
    generationSongListToSave = []
    #create generation profile info for the similarity between the song being played and each other song
    for song in songList:
        indexSong2 = songList.index(song)
        if indexSongPlayed > indexSong2:
            similarity = similarityMatrix[indexSongPlayed][indexSong2]
        elif indexSongPlayed < indexSong2:
            similarity = similarityMatrix[indexSong2][indexSongPlayed]
        elif indexSongPlayed == indexSong2:
            continue
        #print("adding song " + song + "to list")
        generationSongList.append(song)
        totalSum += similarity
        generationNum = totalSum
        generationNumList.append(generationNum)

    #add in songPicked to generationProfile to be saved
    generationSongListToSave = list(generationSongList)
    generationNumListToSave = list(generationNumList)
    totalSumToSave = totalSum
    songPlayed = songList[indexSongPlayed]
    generationSongListToSave.append(songPlayed)
    similaritySongPlayed = 5
    generationNumSongPlayed = totalSumToSave + similaritySongPlayed
    generationNumListToSave.append(generationNumSongPlayed)
    totalSumToSave = generationNumSongPlayed

    if mood != 'None':
        db[mood+'bool'] = True
        db[mood+'generationSongList'] = generationSongListToSave
        db[mood+'generationNumList'] = generationNumListToSave
        db[mood+'totalSum'] = totalSumToSave
    else:
        print ("time is " + time)
        db[time + 'bool'] = True
        db[time+'generationSongList'] = generationSongListToSave
        db[time+'generationNumList'] = generationNumListToSave
        db[time+'totalSum'] = totalSumToSave
        #print("totalSumToSave is " + str(totalSumToSave))
        #print("db[time + bool] is " +  str(db[time + 'bool']))
    db.close()
    # print("THIS THE PLACE")
    # print ("generation num list is: ")
    # for num in generationNumList:
    #     print num
    # print ("totalSum is: " + str(totalSum))
    createPlaylist(generationSongList, generationNumList, totalSum)

def onClickPlay(dbname, songName, mood, time):
    #first: play song
    #then: find other things to play
    #check to see whether there is already a generation list for this mood or time
    db = shelve.open(dbname)
    if mood != 'None':
        try:
            moodFound = db[mood + 'bool']
            generationSongList = db[mood + 'generationSongList'];
            generationNumList = db[mood + 'generationNumList'];
            totalSum = db[mood + 'totalSum'];
            db.close()
            createPlaylist(generationSongList, generationNumList, totalSum)
        except:
            moodFound = False
            db.close()
            createGenerationProfile(dbname, songName, mood, time)
    else:
        # print("Going to test: db[" + time + "+ 'bool']")
        # print("db[time + bool] is " + str(db[time + 'bool']))
        # timeFound = db[time + 'bool']
        # generationSongList = db[time + 'generationSongList'];
        # generationNumList = db[time + 'generationNumList'];
        # totalSum = db[time + 'totalSum'];
        # db.close()
        # createPlaylist(generationSongList, generationNumList, totalSum)
        try:
            timeFound = db[time + 'bool']
            generationSongList = db[time + 'generationSongList'];
            generationNumList = db[time + 'generationNumList'];
            totalSum = db[time + 'totalSum'];
            #print ("Using already defined list.")
            db.close()
            #print ("Closed database, about to call createPlaylist")
            createPlaylist(generationSongList, generationNumList, totalSum)
            #print ("Called create playlist, shouldn't call except...")
        except:
            print("got into except in onClickPlay")
            #timeFound = False
            db.close()
            createGenerationProfile(dbname, songName, mood, time)




def printMatrix(testMatrix, songList):
    for i in range(len(songList)):
        for j in range(len(songList)):
            print("i: " + str(i) + " j: " + str(j))
            print(str(testMatrix[i][j]) + '\n')
        """print ' ',
        for i in range(len(testMatrix[1])):  # Make it work with non square matrices.
              print i,
        print
        for i, element in enumerate(testMatrix):
              print i, ' '.join(element)"""

#main()


def music(value, args):
	os.system('padsp mplayer "music/'+value+'"')
def music2(son, args):
	os.system('padsp mplayer "music/'+son+'"')

#click songs in list to play sets song to value for play button
def select(evt):
	global value
	value=play_list_display.get(play_list_display.curselection())
	current_song.insert(0, value)
	print value
#time selecter
def time_select(evt):
	time=time_box.get(time_box.curselection())
	print time
#mood selector
def mood_select(evt):
	Mood=mood_name.get(mood_name.curselection())
	current_mood.insert(0,Mood)
	print Mood
#play button for the song	
def play():
	global count
	Thread(target=music, args=(value,1)).start()
	mood_entry=mood_str.get()
	play_list_display.delete(0, count)
	play_list_display.insert(0, value)
	main(value, mood_entry)

# def playList(generatedList):
# 	for i in range (len(generatedList)):
# 		Thread(target=music, args=(generatedList[i],1)).start()

#gets the next song in the playlist or directory
def next():
	global count
	global num
	global me
	if num==count-1:
		num=0
	elif num!=count:
		num+=1
	current_song.insert(0,dirs[num])
	Thread(target=music2, args=(dirs[num],1)).start()
	
	
	
def Mood():#when pushed sends to the playlist_files listbox
	mood_entry=mood_str.get()
	mood_name.insert(END,mood_entry)
	#print mood_entry
def like():
	print "like"
def dislike():
	print "dislike"
#def pause():
	#p=commands.getoutput("p")
#	print "p"
#def stop():
#	Return 
#def main():
root=tk.Tk()
root.title('Player')
root.geometry('470x150+750+300')
	
mood_str=Tkinter.StringVar()
time_str=Tkinter.StringVar()
#play button
play_button = Button(root, width = 5, height = 1, text='Play',
                           fg='Orange', command = play, bg="black")
play_button.place(x=0, y=0)
#next button
next_button = Button(root, width = 5, height = 1, text='Next',
                           fg='Orange', command = next,  bg="black")
next_button.place(x=70, y=0)
#thumbs up
like_button=Button(root, width = 5, height = 1, text='Like',
                           fg='Orange', command = like,  bg="black")
like_button.place(x=0, y=100)
#thumbs down
dislike_button=Button(root, width = 5, height = 1, text='Dislike',
                           fg='Orange', command = dislike,  bg="black")
dislike_button.place(x=70, y=100)
#pause button
#pause_button=Button(root, width = 5, height = 1, text='Pause',
         #                  fg='Orange', command = pause,  #bg="black")
#pause_button.place(x=140, y=0)
#stop button
#stop_button=Button(root, width = 5, height = 1, text='Stop',
 #                          fg='Orange', command = stop,  bg="black")
#stop_button.place(x=210, y=0)
#entry box for mood and button
mood=Entry(root, textvariable=mood_str)
mood.place(x=0, y=30)
mood_button = Button(root, width = 5, height = 1, text='Mood',
                           fg='Orange', command = Mood, bg="black")
mood_button.place(x=170, y=30)
mood_label=Label(text="Current Mood")
mood_label.place(x=0, y=60)
current_mood=Listbox(root,width=18, height=1)
current_mood.place(x=0, y=80)
#current song box
current_label=Label(text="Current Song")
current_label.place(x=305, y=5)
current_song=Listbox(root, width=18, height=1)
current_song.place(x=305, y=25)
#Time selector
time_selector=Label(text="Time Selector")
time_selector.place(x=200, y=75)
time_box=Listbox(root, width=10, height=3)
time_box.place(x=200, y=95)
#times names
time_box.insert(0,"Morning")
time_box.insert(1,"Afternoon")
time_box.insert(2,"Evening")
time_box.bind('<<ListboxSelect>>',time_select)
#where you can select and enter moods
mood_selector=Label(text="Mood Selecter")
mood_selector.place(x=305, y=60)
#mood selection box
mood_name=Listbox(root, width=18,height=3)
mood_name.place(x=305, y=80)
mood_name.bind('<<ListboxSelect>>',mood_select)
#all music window
play_list_window=Toplevel(root, height=350, width=300)
play_list_window.title('Playlist')
play_list_display=Listbox(play_list_window, width=0)
play_list_display.bind('<<ListboxSelect>>', select)
play_list_display.pack() 



for song in dirs:
	play_list_display.insert(END,song)	
	


play_list_window.mainloop()
root.mainloop()
#main()
