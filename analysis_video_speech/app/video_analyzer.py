# Python code to convert video to audio
# code original source : https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
import moviepy.editor as mp
import speech_recognition as sr

import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

from threading import Timer

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 7,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    r = sr.Recognizer()
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="fr-FR")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

        #delete the chunk
        os.remove(chunk_filename)
    # return the text for all chunks detected
    return whole_text

def shortwav(audio_path):
    # initialize the recognizermoviepy ffmp
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(audio_path) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="fr-FR")
        return text


def extract_audio(video_file):
    # Insert Local Video File Path
    clip = mp.VideoFileClip(video_file)
    # Insert Local Audio File Path
    temp_file_path = "/tmp/data/test.wav"

    # https://github.com/Zulko/moviepy/issues/803

    def timeout_trigger():
        print("killing process")
        try:

            clip.close()
        except Exception as e:
            print("too late")

    #must monitor progress instead of killing after 30 seconds...
    timer = Timer(30, timeout_trigger)
    timer.start()
    try:
        clip.audio.write_audiofile(temp_file_path, codec='pcm_s16le', write_logfile=True)
    except Exception as e:
        print("Wav bug")

    timer.cancel()
    print(temp_file_path)
    return temp_file_path


def get_text(video_path):
    audio_path = extract_audio(video_path)
    #shortwav(audio_path)
    return get_large_audio_transcription(audio_path)

if __name__ == '__main__':
    #audio_path = extract_audio("/tmp/data/test.mov")
    audio_path="C:/tmp/test/R20240109-100027.WAV"
    text = get_large_audio_transcription(audio_path)
    print(text)
    #shortwav(audio_path)