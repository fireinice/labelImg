from enum import Flag, auto
from PyQt5.QtCore import Qt


class EventType(Flag):
    OPEN_DIR = auto()
    LOAD_IMAGE = auto()
    NEW_SHAPE = auto()
    MODE_CHANGED = auto()
    CVS_DOUBLE_CLICK = auto()
    APP_CLOSE = auto()
    SAVE_FILE = auto()


class _PluginsGlobal(object):
    def __init__(self, app, ns):
        "docstring"
        assert isinstance(ns, str)
        self.__dict__["__ns"] = ns

    def __key(self, name):
        return self.__dict__["__ns"] + "__" + name

    def __getattr__(self, name):
        "try self first then canvas then app"
        print("get")
        print(self.__key(name))
        return self.__dict__[self.__key(name)]

    def __setattr__(self, name, value):
        "try self first then canvas then app"
        print("set")
        print(self.__key(name))
        self.__dict__[self.__key(name)] = value

    

class LabelImgPlugin(object):
    """Documentation for LabelImgPlugins

    """
    def __init__(self, app):
        "docstring"
        self.__dict__['app'] = app
        self.__ns = None

    def __getattr__(self, name):
        "try self first then canvas then app"
        if hasattr(self.app, name):
            return getattr(self.app, name)

    def __setattr__(self, name, value):
        "try self first then canvas then app"
        if hasattr(self.app, name):
            setattr(self.app, name, value)
        else:
            if name == "namespace":
                self.set_namespace(value)
            else:
                self.__dict__[name] = value

    @property
    def globals(self):
        if self.__ns is None:
            raise RuntimeError("Need register plugin namespace before use globals")
        return self.app.plugin_globals

    @property
    def namespace(self):
        return self.__ns

    def set_namespace(self, ns):
        self.__ns = ns
        if self.app.plugin_globals is None:
            self.app.plugin_globals = _PluginsGlobal(self.app, self.__ns)

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

    def add_shapes(self, shapes, paint_label=False):
        if not isinstance(shapes, list):
            shapes = [shapes]
        for shape in shapes:
            # self.canvas.shapes.append(shape)
            # self.canvas.repaint()
            self.app.add_label(shape)
            if paint_label:
                shape.paint_label = True
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

