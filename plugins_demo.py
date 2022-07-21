from pathlib import Path
from PyQt5.QtWidgets import QListWidgetItem
from libs.labelFile import LabelFileFormat
from libs.plugins import LabelImgPlugin, EventType


class MarkFilesHaveLabeled(LabelImgPlugin):

    @property
    def sub(self):
        return EventType.OPEN_DIR | EventType.MODE_CHANGED

    def _get_suffix(self):
        format = self.app.label_file_format
        if format == LabelFileFormat.PASCAL_VOC:
            return ".xml"
        elif format == LabelFileFormat.YOLO:
            return '.txt'
        elif format == LabelFileFormat.CREATE_ML:
            return '.json'

    def _mode_changed(self, suffix):
        if not suffix.startswith("."):
            return
        self._gen_file_list()

    def _dir_opened(self, path):
        path = Path(path)
        if not path.is_dir():
            return
        self._gen_file_list()

    def _gen_file_list(self):
        self.app.file_list_widget.clear()
        for img_path in self.app.m_img_list:
            img_path = Path(img_path)
            marked_path = img_path.with_suffix(self._get_suffix())
            img_path = marked_path.as_posix()
            if marked_path.is_file():
                img_path += " (*)"
            item = QListWidgetItem(img_path)
            self.app.file_list_widget.addItem(item)

    def on_event(self, path):
        self._dir_opened(path)
        self._mode_changed(path)


class OpenDirWithLabelPredefined(LabelImgPlugin):

    @property
    def sub(self):
        return EventType.OPEN_DIR

    def _update_default_labels(self):
        self.app.default_label_combo_box.cb.addItems(self._new_labels)

    def on_event(self, path):
        path = Path(path)
        if not path.is_dir():
            return
        predefined_labels_file = path.joinpath("classes.txt")
        self._new_labels = []
        if predefined_labels_file.is_file():
            lines = predefined_labels_file.read_text()
            self._new_labels = [l.strip() for l in lines.split("\n") if l.strip()]
            print(self._new_labels)
            self.app.load_predefined_classes(predefined_labels_file.as_posix())
        self._update_default_labels()


class DoubleClickShapeToDel(LabelImgPlugin):

    @property
    def sub(self):
        return EventType.CVS_DOUBLE_CLICK

    def on_event(self):
        self.app.delete_selected_shape()


class FixSquareShortcut(LabelImgPlugin):

    @property
    def sub(self):
        return EventType.OPEN_DIR

    def on_event(self):
        self.app.toggle_draw_square()


class AutoEnableCreateMode(LabelImgPlugin):

    @property
    def sub(self):
        return EventType.LOAD_IMAGE

    def on_event(self):
        self.app.toggle_advanced_mode(True)
        self.app.set_create_mode()
