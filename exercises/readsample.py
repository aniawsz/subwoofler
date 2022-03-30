if __name__ == "__main__":
    import wave
    import sys

    if len(sys.argv) > 1:
        sample_name = sys.argv[1]

        with wave.open(sample_name, "rb") as f:
            fs = f.getframerate()
            channels_no = f.getnchannels()
            data = f.readframes(-1)
            sample_width = f.getsampwidth()
    else:
        print("Please provide a sample name")
