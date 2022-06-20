from enum import Flag, auto
from PyQt5.QtCore import Qt


class EventType(Flag):
    OPEN_PATH = auto()
    LOAD_IMAGE = auto()
    NEW_SHAPE = auto()
    MODE_CHANGED = auto()
    CVS_DOUBLE_CLICK = auto()


class LabelImgPlugin(object):
    """Documentation for LabelImgPlugins

    """
    def __init__(self, app):
        "docstring"
        self.app = app
        self.canvas = app.canvas

    @property
    def latest_shape(self):
        if not self.canvas.shapes:
            return None
        return self.canvas.shapes[-1]

    @property
    def latest_marked_label(self):
        if self.latest_shape is not None:
            return self.latest_shape.label
        return None

    def add_shapes(self, shapes):
        if not isinstance(shapes, list):
            shapes = [shapes]
        for shape in shapes:
            # self.canvas.shapes.append(shape)
            # self.canvas.repaint()
            self.app.add_label(shape)
        shapes.extend(self.canvas.shapes)
        self.canvas.load_shapes(shapes)
        self.app.set_dirty()

    def label(self, index):
        if self.app.label_hist is None or len(self.app.label_hist) < index:
            return index
        return self.app.label_hist[index]

    def hide_shape_by_label(self, label):
        for item in self.app.label_list.findItems(label, Qt.MatchExactly):
            item.setCheckState(False)

    @property
    def sub(self):
        return None

    def on_event(self):
        pass

