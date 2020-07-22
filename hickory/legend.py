class Legend(object):
    """
    plot legend, which just passes on the args/kw to the legend
    method.  See those docs.
    """
    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw
