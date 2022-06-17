###############################################################
# Script to generate an srt format subtitles file sync'd
# to a salsa video. Works best with VLC player.
#
# Subtitles file is generated in the same folder and named
# subtitle.srt. If the file already exists it will be
# overwritten.
#
# https://docs.fileformat.com/video/srt/
#
# How to use this script:
# 1. Estimate the interval by counting the time between
#    4 8-counts in the *audio* and then dividing that by 32.
#    The longer you count and divide the more accurate your
#    starting estimate will be. 
# 2. Guess the offset by looking at the slider in the video
#    player.
# 3. Run the script to generate the subtitles, load it in vlc
#    with your video and check the alignment.
# 4. Start by fine-tuning the offset for the first count. Make
#    sure you can match the first "1".
# 5. When the 1 is at th right spot, tune the interval to get
#    the 8 in the right spot in the *audio*.
# 6. Listen till the end and see if the subtitles are running
#    ahead (increase the interval) or slipping backwards (
#    reduce the interval).
# 7. Hope that the teacher did the moves in time to the music!
#
#    This will work best with videos with music as the tempo
#    will be consistent. When teachers count, their tempo can
#    vary throughout the video.
###############################################################
#!/bin/python

import sys

if len(sys.argv) != 3:
    print(f"Usage:\nsubtitles.py <interval in millisecs> <offset in millisecs>\ninterval: time between two counts (e.g. between 1 and 2)\noffset: time from the start of the video when the subtitles should start")
    exit(-1)

intervalMs = int(sys.argv[1])
offsetMs = int(sys.argv[2])

if debug:
    print(f"intervalMS = {intervalMs}")

displayTimeMs = intervalMs - 20 # The time for which the number stays on screen
MAX_COUNT = 200 # Max subtitle lines to be generated

totalLengthHrs = intervalMs * MAX_COUNT / 1000 / 60 / 60

if totalLengthHrs > 24:
    print(f"ERROR: Max valid subtitle length = 24 hours\n intervalMs {intervalMs}ms x {MAX_COUNT} = { intervalMs * MAX_COUNT / 1000 / 60 / 60}hours")
    exit(-1)

filePath = './subtitle.srt' # filename and path are hardcoded for now

file = open(filePath, "w")

for i in range(0, MAX_COUNT):
    #CONTENT
    file.write(str(i+1) + "\n")

    ms = offsetMs + (i * intervalMs)
    hrs = int(ms/1000/60/60)
    mins = int ((ms/1000/60) % 60)
    secs = int ((ms/1000) % 60)
    fromStr = f"{hrs:02}:{mins:02}:{secs:02},{(ms%1000):03}"

    if debug:
        print(f"{ms} ms = {hrs}:{mins}:{secs}")

    ms = int(offsetMs + (i * intervalMs) + displayTimeMs)
    hrs = int(ms/1000/60/60)
    mins = int ((ms/1000/60) % 60)
    secs = int((ms/1000) % 60)
    toStr = f"{hrs:02}:{mins:02}:{secs:02},{(ms%1000):03}"

    file.write(f"{fromStr} --> {toStr}\n")

    file.write(f"{(i%8)+1}\n\n")

file.close()
