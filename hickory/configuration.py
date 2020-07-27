try:
    import IPython
    _name = IPython.get_ipython().__class__.__name__
except ImportError:
    _name = None

config = {
    # by default plot, plot_hist etc. convenience functions show
    # on the screen, except in jupyter
    'show': False if _name == 'ZMQInteractiveShell' else True,

    # if set, the convenience functions put the plot into
    # the background by default
    'fork_window': True if _name == 'TerminalInteractiveShell' else False,
}
