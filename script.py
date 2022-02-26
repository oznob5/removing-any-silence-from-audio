from moviepy.editor import *
import sys

arguments = sys.argv[1:]  # terminal input list

clip = VideoFileClip("testclip.mp4")
audio = clip.audio  # convert video into audio

silence_volume_threshold = float(arguments[0])
silence_length_threshold = float(arguments[1])

def get_silences(clip, silence_volume_threshold=silence_volume_threshold):
    silences = []  # (time) list of lists when silence is detected
    silent = False  # silence detector
    marked_in = False  # bool magnitude of start or end silence
    silence = []  # moments of silences
    for frame in audio.iter_frames(fps=100, with_times=True):  # 0 - time; 1 - sound level
        current_level = abs(sum(frame[1]))  # sum left and right
        silent = current_level < silence_volume_threshold  # is it silence? (sound border)
        if silent:  # begin of silence interval
            if not marked_in:
                silence.append(frame[0])
                marked_in = True
        else:  # end of silence interval
            if marked_in:
                silence.append(frame[0])
                marked_in = False
                silences.append(silence)
                silence = list()
        if frame[0] == clip.duration and marked_in:  # if the end of audio clip silence
            silence.append(frame[0])
            marked_in = False
            silences.append(silence)
            silence = []
    return silences

def remove_silences(silences, silence_length_threshold=silence_length_threshold):
    list_of_silences = []
    for silence in silences:
        if silence[1] - silence[0] > silence_length_threshold:
            list_of_silences.append(silence)
    return list_of_silences

silences = get_silences(clip)
actual_silences = remove_silences(silences)

print(actual_silences)
clip.close()
audio.close()
