from moviepy.editor import *
import sys

arguments = sys.argv[1:]

clip = VideoFileClip("testclip.mp4")
audio = clip.audio  # convert video into audio

silence_volume_threshold = float(arguments[0])
silences = list()  # (time) list when silence is detected

count = 0  # silence detector
for frame in audio.iter_frames(fps=1000, with_times=True):
    # print(frame[0])
    current_level = abs(sum(frame[1]))
    if current_level < silence_volume_threshold:
        silences.append(frame[0])

print(*silences)

clip.close()
audio.close()
