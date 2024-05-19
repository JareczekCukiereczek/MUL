from pydub import AudioSegment
from playsound import playsound
import os
import unidecode
import re

def normalize(phrase):
    phrase = re.sub(r'[^\w\s]', '', phrase)
    return unidecode.unidecode(phrase).lower()

def find_audio(directory, phrase):
    normalized_phrase = normalize(phrase)
    for filename in os.listdir(directory):
        normalized_filename = normalize(filename)
        if normalized_phrase in normalized_filename:
            return os.path.join(directory, filename)
    return None

def processingPhrase(phrases, directories):
    audio_segments = []
    i = 0

    def add_audio_segment(audio_file):
        if audio_file:
            audio_segments.append(AudioSegment.from_file(audio_file))

    while i < len(phrases):
        phrase = phrases[i]
        combined_phrase = None
        audio_file = None

        if "stacji" in phrase or "przez" in phrase:
            if i + 1 < len(phrases):
                combined_phrase = f"{phrase} {phrases[i + 1]}"
                audio_file = find_audio(directories['stacje'], combined_phrase)
                if audio_file:
                    add_audio_segment(audio_file)
                    i += 2
                    continue
            audio_file = find_audio(directories['stacje'], phrase)
        elif "peronie" in phrase or "toru" in phrase:
            audio_file = find_audio(directories['perony_i_tory'], phrase)
        else:
            audio_file = find_audio(directories['do_z_stacji'], phrase)

        add_audio_segment(audio_file)
        i += 1

    return audio_segments

def speech(text):
    base_dir = "/Users/kuba/PycharmProjects/MUL"
    directories = {
        'stacje': os.path.join(base_dir, "stacje"),
        'perony_i_tory': os.path.join(base_dir, "perony_i_tory"),
        'do_z_stacji': os.path.join(base_dir, "do_z_stacji")
    }

    def process_text(text):
        return [phrase.strip() for phrase in re.split(r',|\s', text) if phrase.strip()]

    def combine_audio_segments(audio_segments):
        if audio_segments:
            combined = sum(audio_segments[1:], audio_segments[0])
            output_file = os.path.join(base_dir, "final.wav")
            combined.export(output_file, format="wav")
            playsound(output_file)
        else:
            print("No matching audio files found for synthesis.")

    phrases = process_text(text)
    audio_segments = processingPhrase(phrases, directories)
    combine_audio_segments(audio_segments)

if __name__ == "__main__":
    text = input("Enter text: ")
    speech(text)
