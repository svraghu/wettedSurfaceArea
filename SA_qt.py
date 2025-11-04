"""
To run this program you need to install the PyQt6 library:

    pip install PyQt6 sympy
"""

import sys
import math
from sympy import sympify, SympifyError

try:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QApplication,
        QComboBox,
        QFormLayout,
        QGridLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QPushButton,
        QVBoxLayout,
        QWidget,
        QMessageBox,
    )
except ImportError as e:
    raise ImportError(
        "PyQt6 is required to run this application. "
        "Install it with `pip install PyQt6`."
    ) from e


class Shape:

    def __init__(self, name, dimensions):
        self.name = name
        self.dimensions = dimensions

    def surface_area(self, *args):  # pragma: no cover
        raise NotImplementedError

    def volume(self, *args):  # pragma: no cover
        raise NotImplementedError


class ConicalFrustrum(Shape):
    def __init__(self):
        super().__init__("Conical Frustrum", ["Small Diameter", "Large Diameter", "Length"])

    def surface_area(self, sdiameter, ldiameter, length):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        sa = math.pi * ((r1 + r2) * (((r1 - r2) ** 2 + length**2) ** 0.5))
        return sa

    def volume(self, sdiameter, ldiameter, length):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        vol = ((r1**2 + r2**2 + (r1 * r2)) * math.pi * length) / 3
        return vol


class Tube(Shape):
    def __init__(self):
        super().__init__("Tube", ["Diameter", "Length"])

    def surface_area(self, diameter, length):
        return math.pi * diameter * length

    def volume(self, diameter, length):
        return math.pi * (diameter / 2) ** 2 * length


class TwoDBag(Shape):
    def __init__(self):
        super().__init__("2D Bag", ["Length", "Height"])

    def surface_area(self, length, width):
        return 2 * length * width

    def volume(self, length, width):
        return math.pi * (width / 2) ** 2 * length


class ThreeDBiocontainer(Shape):
    def __init__(self):
        super().__init__("3D Rectangular Biocontainer", ["Length", "Width", "Height"])

    def surface_area(self, length, width, height):
        return 2 * (length * width + width * height + length * height)

    def volume(self, length, width, height):
        return length * width * height


class Tee(Shape):
    def __init__(self):
        super().__init__("Tee", ["Horizontal ID", "Vertical ID", "Length", "Height", "Flange OD"])

    def surface_area(self, id_1, id_2, length, height, flange):
        trunk_height = height - ((flange - id_1) / 2) - id_1
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * trunk_height
        return area_tube_1 + area_tube_2

    def volume(self, id_1, id_2, length, height, flange):
        r1 = id_1 / 2
        r2 = id_2 / 2
        trunk_height = height - ((flange - id_1) / 2) - id_1
        vol = (math.pi * length * r1**2) + (math.pi * trunk_height * r2**2)
        return vol


class Elbow(Shape):
    def __init__(self):
        super().__init__("Elbow", ["Horizontal ID", "Vertical ID", "Length", "Height"])

    def surface_area(self, id_1, id_2, length, height):
        arc_length = math.radians(90)
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * height
        area_curve = math.pi * id_2 * arc_length
        return area_tube_1 + area_tube_2 + area_curve

    def volume(self, id_1, id_2, length, height):
        r1 = id_1 / 2
        r2 = id_2 / 2
        arc_length = math.radians(90)
        vol = (math.pi * length * r1**2) + (math.pi * height * r2**2) + (math.pi * arc_length * r2**2)
        return vol


class Cross(Shape):
    def __init__(self):
        super().__init__("Cross", ["Horizontal ID", "Vertical ID", "Length", "Height"])

    def surface_area(self, id_1, id_2, length, height):
        area_tube_1 = math.pi * id_1 * length
        area_tube_2 = math.pi * id_2 * height
        intersection_area = math.pi * (id_2 / 2) ** 2
        return area_tube_1 + area_tube_2 - intersection_area

    def volume(self, id_1, id_2, length, height):
        r1 = id_1 / 2
        r2 = id_2 / 2
        return (math.pi * length * r1**2) + (math.pi * height * r2**2) - (math.pi * r2**2)


class Wye(Shape):
    def __init__(self):
        super().__init__("Wye", ["Tusk ID", "Trunk ID", "Length", "Height"])

    def surface_area(self, id_1, id_2, length, height):
        tusk_height = (height - (2 * math.cos(math.radians(30)) * (id_1 / 2))) / 2
        tusk_length = tusk_height / math.sin(math.radians(30))
        tusk_area = 2 * math.pi * id_1 * tusk_length
        trunk_length = (length - (math.cos(math.radians(30)) * tusk_length)) - ((id_1 / 2) * math.sin(math.radians(30)))
        trunk_area = math.pi * id_2 * trunk_length
        sa_curve = math.radians(30) * id_2
        intersection_area = math.pi * (id_2 / 2) ** 2
        return tusk_area + trunk_area + sa_curve - intersection_area

    def volume(self, id_1, id_2, length, height):
        tusk_height = (height - (2 * math.cos(math.radians(30)) * (id_1 / 2))) / 2
        tusk_length = tusk_height / math.sin(math.radians(30))
        trunk_length = (length - (math.cos(math.radians(30)) * tusk_length)) - ((id_1 / 2) * math.sin(math.radians(30)))
        vol_tusk = 2 * (math.pi * tusk_length * (id_1 / 2) ** 2)
        vol_trunk = (math.pi * trunk_length * (id_2 / 2) ** 2)
        arc_length = math.radians(30) * id_2
        vol_curve = (arc_length * (id_2 / 2) ** 2 * math.pi) / 3
        return vol_tusk + vol_trunk + vol_curve


class ThreeDRdBottle(Shape):
    def __init__(self):
        super().__init__("3D Round Bottle", ["ID", "Height"])

    def surface_area(self, id_1, height):
        return (math.pi * ((id_1 / 2) ** 2)) + (math.pi * id_1 * height)

    def volume(self, id_1, height):
        return math.pi * height * (id_1 / 2) ** 2


class ThreeDRdBiocontainer(Shape):
    def __init__(self):
        super().__init__("3D Round Biocontainer", ["Fold Length", "Width", "Height"])

    def surface_area(self, flength, width, height):
        flatgap = width - (2 * flength)
        id_1 = ((flength + (flatgap / 2)) / math.cos(math.radians(45))) * 2
        return (2 * math.pi * ((id_1 / 2) ** 2)) + (math.pi * id_1 * height)

    def volume(self, flength, width, height):
        flatgap = width - (2 * flength)
        id_1 = ((flength + (flatgap / 2)) / math.cos(math.radians(45))) * 2
        return math.pi * height * (id_1 / 2) ** 2


class Cap(Shape):
    def __init__(self):
        super().__init__("Cap", ["ID"])

    def surface_area(self, id_1):
        return math.pi * ((id_1 / 2) ** 2)

    def volume(self, id_1):
        return 0.0


class Flask(Shape):
    def __init__(self):
        super().__init__("Flask", ["Small Diameter", "Large Diameter", "Height"])

    def surface_area(self, sdiameter, ldiameter, height):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        return math.pi * ((r1 + r2) * (((r1 - r2) ** 2 + height**2) ** 0.5)) + (r2**2)

    def volume(self, sdiameter, ldiameter, height):
        r1 = sdiameter / 2
        r2 = ldiameter / 2
        return ((r1**2 + r2**2 + (r1 * r2)) * math.pi * height) / 3


class Plug(Shape):
    def __init__(self):
        super().__init__("Plug", ["Diameter", "Length"])

    def surface_area(self, diameter, length):
        return (math.pi * (diameter / 2) ** 2) + (math.pi * diameter * length)

    def volume(self, diameter, length):
        return 0.0


# List of available shape instances
SHAPES = [
    Tube(),
    TwoDBag(),
    ThreeDBiocontainer(),
    ThreeDRdBiocontainer(),
    ThreeDRdBottle(),
    Flask(),
    ConicalFrustrum(),
    Tee(),
    Elbow(),
    Cross(),
    Wye(),
    Cap(),
    Plug(),
]


class MainWindow(QWidget):
    """Main application window for the Qt shape calculator."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shape Calculator")
        self.shape_classes = {shape.name: type(shape) for shape in SHAPES}
        self.entry_widgets: list[QLineEdit] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        """Create and arrange widgets for the GUI."""
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Choose a shape:"))
        self.shape_combo = QComboBox()
        self.shape_combo.addItem("Select a shape…")
        self.shape_combo.addItems([shape.name for shape in SHAPES])
        self.shape_combo.currentTextChanged.connect(self.on_shape_change)
        top_layout.addWidget(self.shape_combo)

        self.form_layout = QFormLayout()

        self.sa_label = QLabel("")
        self.sa_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_label = QLabel("")
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        self.compute_btn = QPushButton("Compute")
        self.compute_btn.clicked.connect(self.compute_values)
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(QApplication.instance().quit)
        button_layout.addWidget(self.compute_btn)
        button_layout.addWidget(self.quit_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.sa_label)
        main_layout.addWidget(self.volume_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.on_shape_change("")

    def on_shape_change(self, shape_name: str) -> None:
        while self.form_layout.rowCount():
            self.form_layout.removeRow(0)
        self.entry_widgets.clear()
        self.sa_label.clear()
        self.volume_label.clear()
        if not shape_name or shape_name == "Select a shape…":
            self.adjustSize()
            return
        shape_instance = self.shape_classes[shape_name]()
        for dim in shape_instance.dimensions:
            label = QLabel(f"{dim}:")
            entry = QLineEdit()
            entry.setPlaceholderText("Enter value or expression")
            self.form_layout.addRow(label, entry)
            self.entry_widgets.append(entry)
        self.adjustSize()

    def compute_values(self) -> None:
        shape_name = self.shape_combo.currentText()
        if not shape_name or shape_name == "Select a shape…":
            QMessageBox.information(self, "Select a Shape", "Please choose a shape before computing.")
            return
        shape_class = self.shape_classes[shape_name]
        shape_instance = shape_class()
        try:
            values: list[float] = []
            for entry in self.entry_widgets:
                text = entry.text().strip()
                if not text:
                    values.append(0.0)
                else:
                    values.append(float(sympify(text)))
            sa = shape_instance.surface_area(*values)
            vol = shape_instance.volume(*values)
            self.sa_label.setText(f"Surface Area: {sa:,.2f} cm\u00B2")
            self.volume_label.setText(f"Volume: {vol:,.2f} cm\u00B3")
        except (ValueError, SympifyError):
            QMessageBox.critical(self, "Invalid Input", "Please enter valid numbers or expressions for dimensions.")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()