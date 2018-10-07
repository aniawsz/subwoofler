# Inspired by: https://www.jonwitts.co.uk/archives/896
# and http://code.activestate.com/recipes/134892/

def getch():
    # Are we running Windows?
    try:
        import msvcrt
        return msvcrt.getch()
    except ModuleNotFoundError:
        # Ah, we're on a UNIX machine then
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
