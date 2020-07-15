class Legend(object):
    """
    plot legend

    Parameters
    ----------
    loc: str
        E.g. 'upper right'.  Default 'upper left'
    frame: bool
        If True draw a frame around the legend.  Default False
    borderaxespad: float
        Padding between the legend and the axes, in units of the font size.
    framealpha: float
        When frame is true, this is the alpha for the frame background.
        Default None which means it will use the value from the rc params
        (which itself defaults to 0.8)
    """
    def __init__(
        self,
        loc='upper right',
        frame=False,
        borderaxespad=2,
        framealpha=None,
    ):
        self.loc = loc
        self.frame = frame
        self.borderaxespad = borderaxespad
        self.framealpha = framealpha
