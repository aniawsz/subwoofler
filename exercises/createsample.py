import numpy as np


def create_silent_data():
    values = np.zeros(44100*2, dtype=np.int8)
    return values.tobytes()


def create_noise_data():
    int_info = np.iinfo(np.int8)
    values = np.random.randint(int_info.min, int_info.max, size=44100*2, dtype=np.int8)
    return values.tobytes()


def create_tone(frequency):
    time = np.arange(0, 1, 1/44100)
    sinewave = 100 * np.sin(2 * np.pi * frequency * time)
    sinewave = sinewave.astype(np.int8)
    return sinewave.tobytes()


if __name__ == "__main__":
    import wave
    import sys

    if len(sys.argv) > 1:
        sample_name = sys.argv[1]

        with wave.open(sample_name, "wb") as f:
            f.setframerate(44100.0)
            f.setnchannels(1)
            f.setsampwidth(1)

            data = create_tone(50)
            f.writeframes(data)
    else:
        print("Please provide a sample name")
