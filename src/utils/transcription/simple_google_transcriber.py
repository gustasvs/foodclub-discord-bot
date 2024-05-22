import speech_recognition as sr
from pydub import AudioSegment
import os

def convert_to_wav(audio_file_path):
    """Convert audio file to .wav format if it's not already."""
    file_name, file_extension = os.path.splitext(audio_file_path)
    if file_extension.lower() != '.wav':
        audio = AudioSegment.from_file(audio_file_path)
        wav_file_path = f"{file_name}.wav"
        audio.export(wav_file_path, format="wav")
        return wav_file_path
    return audio_file_path

def google_lv_transcriber(audio_file_path):
    recognizer = sr.Recognizer()
    wav_file_path = convert_to_wav(audio_file_path)
    with sr.AudioFile(wav_file_path) as source:
        audio = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio, language="lv-LV")
        print(f"Transcript: {transcript}")
        return transcript, True
    except sr.UnknownValueError:
        return "Failed to recognize speech", False
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}", False
    
# transcribe_speech('path_to_your_audio_file.wav')

if __name__ == "__main__":
    transcribe_speech('sample.wav')