from Tkinter import *
import tkFileDialog
import Tkinter
import tkFont
import Tkinter as tk
import os, sys
from threading import Thread
import subprocess

path="Music"
dirs=os.listdir(path)
value="0"
song="0"
count = len(dirs)
num=-1
me=0
def music(value, args):
	os.system('mplayer "Music/'+value+'"')
def music2(son, args):
	os.system('mplayer "Music/'+son+'"')

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
	
	Thread(target=music, args=(value,1)).start()	

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
