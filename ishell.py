#!/usr/bin/env python

import os
import sys
from cto_tree.settings import DEBUG as DEVELOP_MODE

# The place to store your command history between sessions
histfile = os.environ["HOME"] + "/.cto_tree_shell_history"
try:
    # Try to set up command history completion/saving/reloading
    import readline
    import atexit
    readline.parse_and_bind('tab: complete')
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass  # It doesn't exist yet.

    def savehist():
        try:
            global histfile
            readline.write_history_file(histfile)
        except:
            print 'Unable to save Python command history'
    atexit.register(savehist)
    del atexit
except ImportError:
    pass


try:
    from IPython.terminal.ipapp import TerminalIPythonApp
    from IPython.terminal.interactiveshell import TerminalInteractiveShell

    class UmengIPythonApp(TerminalIPythonApp):
        def init_shell(self):
            banner1 = 'Umeng development shell, do whatever you want.\n' if DEVELOP_MODE else \
                'Umeng production shell, use it carefully!\n'
            self.shell = TerminalInteractiveShell.instance(config=self.config,
                                                           display_banner=False, profile_dir=self.profile_dir,
                                                           ipython_dir=self.ipython_dir, banner1=banner1, banner2='')

            self.shell.configurables.append(self)

    has_ushell = True

except ImportError:
    has_ushell = False

# Pretty-print at the command prompt for more readable dicts and lists.
from pprint import pprint
import __builtin__


def myhook(value, show=pprint, bltin=__builtin__):
    if value is not None:
        bltin._ = value
        show(value)
sys.displayhook = myhook
del __builtin__

# Colorize the prompts if possible (This is probably non-portable muck)
if os.environ['TERM'] in ['xterm', 'vt100']:
    pre = chr(1) + "\033[1;32m" + chr(2)  # Turn the text green
    suf = chr(1) + "\033[0m" + chr(2)  # Reset to normal
    sys.ps1 = pre + ">>>" + suf + " "
    sys.ps2 = pre + "..." + suf + " "
    del pre, suf


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cto_tree.settings")
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == '--plain':
            raise ImportError
        user_ns = locals()
        if has_ushell:
            app = UmengIPythonApp.instance()
            app.initialize()
            app.shell.user_ns.update(user_ns)
            sys.exit(app.start())
        else:
            from IPython.terminal.interactiveshell import TerminalInteractiveShell
            shell = TerminalInteractiveShell(user_ns=user_ns)
            shell.mainloop()
    except ImportError:
        import code
        shell = code.InteractiveConsole(locals=locals())
        shell.interact()

if __name__ == '__main__':
    main()
