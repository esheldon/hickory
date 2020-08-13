def get_marker(marker_name):
    """
    get the single character marker given a full name

    Parameters
    ----------
    marker_name: str
        The name of the marker.  See hickory.markers.MARKERS for
        the available name/character mapping

    Returns
    -------
    marker chracter value
    """

    m = MARKERS.get(marker_name, None)
    if m is None:
        return marker_name
    else:
        return m
        # raise ValueError("no marker '%s' found" % marker_name)

    return m


# name access to some of the markers
MARKERS = {
    "point": ".",
    "dot": ",",
    "circle": "o",
    "triangle_down": "v",
    "triangle_up": "^",
    "triangle": "^",
    "triangle_left": "<",
    "triangle_right": ">",
    "tri_down": "1",
    "tri_up": "2",
    "tri_left": "3",
    "tri_right": "4",
    "octagon": "8",
    "square": "s",
    "pentagon": "p",
    "filled_plus": "P",
    "star": "*",
    "hexagon": "h",
    "hexagon1": "h",
    "hexagon2": "H",
    "plus": "+",
    "x": "x",
    "filled_x": "X",
    "thick_diamond": "D",
    "thin_diamond": "d",
    "diamond": "d",
    # identity mapping
    # ".": ".",
    # ",": ",",
    # "o": "o",
    # "v": "v",
    # "^": "^",
    # "<": "<",
    # ">": ">",
    # "1": "1",
    # "2": "2",
    # "3": "3",
    # "4": "4",
    # "8": "8",
    # "s": "s",
    # "p": "p",
    # "P": "P",
    # "*": "*",
    # "h": "h",
    # "H": "H",
    # "+": "+",
    # "x": "x",
    # "X": "X",
    # "D": "D",
    # "d": "d",
}
