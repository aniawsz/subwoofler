from getch import getch


def run():
    while True:
        char = getch()
        if (char == 'q'):
            print("quitting")
            exit(0)
        else:
            print("pressed: ", char)


if __name__ == '__main__':
    run()
