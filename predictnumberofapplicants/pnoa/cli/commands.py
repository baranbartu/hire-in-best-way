from pnoa.cli import core 


@core.command
def train(args):
    print 'success'


def load_commands():
    import commands

    attrs = set(dir(commands))
    return filter(
        lambda f: isinstance(f, core.Command), map(
            lambda attr: getattr(commands, attr), attrs))
