#modified from aubio demo code on github
#https://github.com/aubio/aubio/blob/master/python/demos/demo_tempo.py
#file functions taken from course notes

#this file takes in a sound file and adds the name of the file as well as the
#median bpm to a text file for the game to access when setting the speed of the 
#arrows

#to run, open terminal and do the following steps:
#1. place your audio file in the same folder as this file
#2. use the command "cd" to parse through your folders to get to the folder 
#holding this file 
#(EX: cd Documents --> cd tp)
#3. type in "python bpmdetector.py" followed by a space and your sound filename
#4. check the file "songs.txt" and see your newly added song and its median bpm

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)


import sys
from aubio import tempo, source

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

filename = sys.argv[1]

samplerate = 0

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = o.get_last_s()
        beats.append(this_beat)
    total_frames += read
    if read < hop_s: break

if len(beats) > 1:
    # do plotting
    from numpy import mean, median, diff
    import matplotlib.pyplot as plt
    bpms = 60./ diff(beats)
    writeFile("songs.txt", "\n" + filename + "," + str(median(bpms)))
    print('mean period: %.2fbpm, median: %.2fbpm' % (mean(bpms), median(bpms)))

else:
    print('mean period: %.2fbpm, median: %.2fbpm' % (0, 0))
    print('plotting %s' % filename)