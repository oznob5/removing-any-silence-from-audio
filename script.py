from moviepy.editor import *
import sys
from app_class import *

def get_silences(clip, silence_volume_threshold):
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

def remove_silences(silences, silence_length_threshold):
    arr_of_silences = []
    for silence in silences:
        if silence[1] - silence[0] > silence_length_threshold:
            arr_of_silences.append(silence)
    return arr_of_silences

def remove_buffer_from_silence(silences, buffer):
    new_silences = []
    for silence in silences:
        s = []
        s.append(silence[0])
        s.append(silence[1])
        s[0] += buffer / 2
        s[1] += buffer / 2
        if s[1]- s[0] > 0:
            new_silences.append(silence)
    return new_silences

def remove_silences_from_clip(clip, vol_threshold, length_threshold, length_buffer):
    silences = get_silences(clip, silence_volume_threshold)
    actual_silences = remove_silences(silences, silence_length_threshold)
    final_silences = remove_buffer_from_silence(actual_silences, silence_length_buffer)
    final_silences.reverse()
    for silence in final_silences:
        clip = clip.cutout(silence[0], silence[1])
    clip.write_videofile(arguments[0].split('.')[0] + "_silences_removed.mp4")
    clip.close()

arguments = sys.argv[1:]  # terminal input list
silence_volume_threshold = float(arguments[1])
silence_length_threshold = float(arguments[2])
silence_length_buffer = float(arguments[3])

clip = VideoFileClip(arguments[0])
audio = clip.audio  # convert video into audio

remove_silences_from_clip(clip, silence_volume_threshold, silence_length_threshold, silence_length_buffer)

clip.close()
audio.close()
