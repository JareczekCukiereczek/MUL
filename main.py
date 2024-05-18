from pydub import AudioSegment
from playsound import playsound
import os
import unidecode
import re

def normalize_phrase(phrase):
    phrase = re.sub(r'[^\w\s]', '', phrase)  # Remove punctuation
    return unidecode.unidecode(phrase).lower()  # Remove Polish characters and convert to lowercase

def find_audio_file(directory, phrase):
    normalized_phrase = normalize_phrase(phrase)
    for filename in os.listdir(directory):
        normalized_filename = normalize_phrase(filename)
        if normalized_phrase in normalized_filename:
            return os.path.join(directory, filename)
    return None

def process_phrases(phrases, directories):
    audio_segments = []
    i = 0
    while i < len(phrases):
        phrase = phrases[i]
        audio_file = None

        if "stacji" in phrase or "przez" in phrase:
            if i + 1 < len(phrases):
                combined_phrase = f"{phrase} {phrases[i + 1]}"
                audio_file = find_audio_file(directories['stacje'], combined_phrase)
                if audio_file:
                    audio_segments.append(AudioSegment.from_file(audio_file))
                    i += 2
                    continue
            audio_file = find_audio_file(directories['stacje'], phrase)
        elif "peronie" in phrase or "toru" in phrase:
            audio_file = find_audio_file(directories['perony_i_tory'], phrase)
        else:
            audio_file = find_audio_file(directories['do_z_stacji'], phrase)

        if audio_file:
            audio_segments.append(AudioSegment.from_file(audio_file))
        i += 1

    return audio_segments

def synthesize_speech(text):
    base_dir = "/Users/kuba/PycharmProjects/MUL"
    directories = {
        'stacje': os.path.join(base_dir, "stacje"),
        'perony_i_tory': os.path.join(base_dir, "perony_i_tory"),
        'do_z_stacji': os.path.join(base_dir, "do_z_stacji")
    }
    phrases = re.split(r',|\s', text)
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    audio_segments = process_phrases(phrases, directories)

    if audio_segments:
        combined = sum(audio_segments[1:], audio_segments[0])
        output_file = os.path.join(base_dir, "final.wav")
        combined.export(output_file, format="wav")
        playsound(output_file)
    else:
        print("No matching audio files found for synthesis.")

if __name__ == "__main__":
    text = input("Enter text: ")
    synthesize_speech(text)
