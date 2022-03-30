class Sample(object):
    def __init__(self, framerate, channels_no, sample_width, data):
        self.framerate = framerate
        self.channels_no = channels_no
        self.sample_width = sample_width
        self.data = data


def read_sample(sample_name):
    with wave.open(sample_name, "rb") as f:
        fs = f.getframerate()
        channels_no = f.getnchannels()
        sample_width = f.getsampwidth()
        data = f.readframes(-1)

    return fs, channels_no, sample_width, data


def write_sample(sample_name, sample, speed):
    with wave.open(sample_name, "wb") as f:
        framerate = sample.framerate
        f.setframerate(framerate*speed)
        f.setnchannels(sample.channels_no)
        f.setsampwidth(sample.sample_width)
        f.writeframes(sample.data)


if __name__ == "__main__":
    import wave
    import sys

    if len(sys.argv) > 1:
        sample_name = sys.argv[1]

        framerate, channels_no, sample_width, data = read_sample(sample_name)
        sample = Sample(framerate, channels_no, sample_width, data)

        speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
        name = sample_name.rstrip(".wav")
        modified_name = "{}{}.wav".format(name, speed)
        write_sample(modified_name, sample, speed)
    else:
        print("Please provide a sample name")
