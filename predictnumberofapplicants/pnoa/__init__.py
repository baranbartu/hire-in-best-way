from core import CommandParser


__version__ = '0.0.1'


def init():
    from commands import load_commands
    
    parser = CommandParser(fromfile_prefix_chars='@')
    for command in load_commands():
        parser.add_command(command)

    parser.run()


if __name__ == "__main__":
    init()
