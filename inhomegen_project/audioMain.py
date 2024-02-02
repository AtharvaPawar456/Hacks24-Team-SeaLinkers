import sounddevice as sd
import speech_recognition as sr

def record_audio(duration=5, sample_rate=44100):
    print("Recording...")

    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()

    print("Recording finished.")
    return audio_data, sample_rate

def audio_to_text(audio_data, sample_rate):
    recognizer = sr.Recognizer()

    # Convert audio to text
    audio = sr.AudioData(audio_data.tobytes(), sample_rate=sample_rate, sample_width=2)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    # Record audio
    audio_data, sample_rate = record_audio()

    # Convert audio to text
    text_result = audio_to_text(audio_data, sample_rate)

    # Print the result
    print("Text from audio: ", text_result)

# python aud
    
'''
create a minimalistic kitchen interior with one dinnaying table and chair
'''