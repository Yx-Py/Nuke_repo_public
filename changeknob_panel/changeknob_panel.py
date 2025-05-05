import nuke
import nukescripts
from PySide2 import QtWidgets, QtCore

# Liste de base des noms de knobs à exclure (modifiable)
IGNORED_KNOBS = [
    'name', 'xpos', 'ypos', 'selected', 'tile_color', 'hide_input',
    'note_font', 'note_font_size', 'label', 'postage', 'dependencies',
    'autolabel', 'bookmark', 'cached', 'crop', 'disable', 'dope_sheet',
    'enable', 'fringe', 'gl_color', 'help', 'icon', 'indicators', 'inject',
    'invert_mask', 'lifetimeEnd', 'lifetimeStart', 'maskFromFlag',
    'note_font_color', 'onCreate', 'onDestroy', 'postage_stamp',
    'postage_stamp_frame', 'process_mask', 'rootNodeUpdated','updateUI',
    'useLifetime', 'mix_luminance', 'enable_mix_luminance', 'invert_unpremult'
]

# Types de knobs non modifiables
EXCLUDED_KNOB_TYPES = (
    nuke.Tab_Knob,
    nuke.Text_Knob,
    nuke.PyScript_Knob,
    nuke.Script_Knob,
    nuke.Obsolete_Knob,
    nuke.Channel_Knob
)

# Fonction de filtrage avancé
def is_ignored_knob(knob_name, knob_obj):
    if knob_name in IGNORED_KNOBS:
        return True
    if any(part in knob_name.lower() for part in ['panel', 'tooltip', 'drop']):
        return True
    if knob_name.endswith('knobChanged'):
        return True
    if isinstance(knob_obj, EXCLUDED_KNOB_TYPES):
        return True
    return False

class ChangeKnobValueWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ChangeKnobValueWidget, self).__init__(parent)

        self.setMinimumHeight(300)
        self.setMaximumHeight(500)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Selection Type
        self.selection_label = QtWidgets.QLabel("Apply to:")
        self.selection_combo = QtWidgets.QComboBox()
        self.selection_combo.setToolTip("Choose how to target the nodes: by selection, class, or name.")
        self.selection_combo.addItems([
            "Selected Nodes", 
            "Class in Selection", 
            "All Nodes by Class", 
            "Name", 
            "Name in Selection"
        ])
        layout.addWidget(self.selection_label)
        layout.addWidget(self.selection_combo)

        # Class or Name Input
        self.class_or_name_label = QtWidgets.QLabel("Node Class / Name (if applicable):")
        self.class_or_name_input = QtWidgets.QLineEdit()
        self.class_or_name_input.setToolTip("Used when targeting by class or name.")
        layout.addWidget(self.class_or_name_label)
        layout.addWidget(self.class_or_name_input)

        # Filter checkbox
        self.ignore_internal_checkbox = QtWidgets.QCheckBox("Ignore Internal Knobs")
        self.ignore_internal_checkbox.setChecked(True)
        self.ignore_internal_checkbox.setToolTip("Uncheck to include all knobs, even internal/system ones.")
        layout.addWidget(self.ignore_internal_checkbox)

        # Table for multiple knob changes
        self.table = QtWidgets.QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Knob Name", "Knob Value"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setToolTip("Enter multiple knob names and values to modify in selected nodes.")
        layout.addWidget(self.table)

        # Buttons to add/remove/clear rows
        button_layout = QtWidgets.QHBoxLayout()
        self.add_row_button = QtWidgets.QPushButton("+")
        self.add_row_button.setToolTip("Add a new knob/value row.")
        self.remove_row_button = QtWidgets.QPushButton("–")
        self.remove_row_button.setToolTip("Remove selected rows.")
        self.clear_table_button = QtWidgets.QPushButton("Clear Table")
        self.clear_table_button.setToolTip("Clear all rows from the table.")

        self.add_row_button.clicked.connect(self.add_table_row)
        self.remove_row_button.clicked.connect(self.remove_table_row)
        self.clear_table_button.clicked.connect(self.clear_table)

        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.remove_row_button)
        button_layout.addWidget(self.clear_table_button)
        layout.addLayout(button_layout)

        # Load Common Knobs button
        self.load_common_button = QtWidgets.QPushButton("Load Common Knobs")
        self.load_common_button.setToolTip("Detect and load knobs shared by all targeted nodes.")
        self.load_common_button.clicked.connect(self.load_common_knobs)
        layout.addWidget(self.load_common_button)

        # Search Knobs Button
        self.search_knob_button = QtWidgets.QPushButton("Search Knobs...")
        self.search_knob_button.setToolTip("Search knob names in the targeted nodes.")
        self.search_knob_button.clicked.connect(self.search_knobs)
        layout.addWidget(self.search_knob_button)

        # Status label for common knobs
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: #66cc66; font-weight: bold;")
        layout.addWidget(self.status_label)

        # Apply Button
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.apply_button.setToolTip("Apply all knob/value changes to the targeted nodes.")
        self.apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(self.apply_button)

        layout.addStretch()
        self.setLayout(layout)

        # Add 3 default rows (first one pre-filled)
        self.add_table_row()
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("size"))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem("25"))
        self.add_table_row()
        self.add_table_row()

    def add_table_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def remove_table_row(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)

    def clear_table(self):
        self.table.setRowCount(0)
        self.status_label.setText("")

    def get_target_nodes(self):
        selection_type = self.selection_combo.currentText()
        search_value = self.class_or_name_input.text().strip()

        if selection_type == "Selected Nodes":
            return nuke.selectedNodes()
        elif selection_type == "Class in Selection":
            return [n for n in nuke.selectedNodes() if n.Class() == search_value]
        elif selection_type == "All Nodes by Class":
            return [n for n in nuke.allNodes() if n.Class() == search_value]
        elif selection_type == "Name":
            return [n for n in nuke.allNodes() if search_value in n.name()]
        elif selection_type == "Name in Selection":
            return [n for n in nuke.selectedNodes() if search_value in n.name()]
        return []

    def load_common_knobs(self):
        nodes = self.get_target_nodes()
        if not nodes:
            nuke.message("No nodes found for analysis.")
            return

        def valid_knobs(node):
            if not self.ignore_internal_checkbox.isChecked():
                return set(node.knobs().keys())
            return set(
                k for k in node.knobs()
                if not is_ignored_knob(k, node[k])
            )

        common = valid_knobs(nodes[0])
        for node in nodes[1:]:
            common.intersection_update(valid_knobs(node))

        if not common:
            self.status_label.setText("No common editable knobs found.")
            return

        self.table.setRowCount(0)
        reference_node = nodes[0]
        for knob_name in reference_node.knobs():
            if knob_name in common:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(knob_name))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))


        self.status_label.setText(f"{len(common)} common knobs loaded.")
        nuke.tprint(f"Loaded {len(common)} common editable knobs into the table.")

    def apply_changes(self):
        nodes = self.get_target_nodes()
        if not nodes:
            nuke.message("No matching nodes found.")
            return

        changes = []
        for row in range(self.table.rowCount()):
            knob_name_item = self.table.item(row, 0)
            knob_value_item = self.table.item(row, 1)
            if knob_name_item and knob_value_item:
                knob_name = knob_name_item.text().strip()
                knob_value = knob_value_item.text().strip()
                if knob_name:
                    changes.append((knob_name, knob_value))

        if not changes:
            nuke.message("Please add at least one knob/value pair.")
            return

        nuke.Undo().begin("Multi-Knob Change")
        try:
            for node in nodes:
                for knob_name, knob_value in changes:
                    # Support multiple knobs: split by comma or space
                    knob_names = [k.strip() for k in knob_name.replace(",", " ").split()]
                    for kname in knob_names:
                        if kname in node.knobs():
                            old_val = node[kname].toScript()
                            node[kname].fromScript(knob_value)
                            new_val = node[kname].toScript()
                            nuke.tprint(f"[{node.name()}] {kname}: {old_val} to {new_val}")
                        else:
                            nuke.tprint(f"[{node.name()}] Knob '{kname}' not found.")

        except Exception as e:
            nuke.message(f"Error modifying nodes: {str(e)}")
        finally:
            nuke.Undo().end()

        nuke.tprint(f"\nChangeKnob Applied {len(changes)} knob(s) to {len(nodes)} node(s).\n")


    def search_knobs(self):
        search_text, ok = QtWidgets.QInputDialog.getText(
            self, "Search Knobs", "Enter part of a knob name to search:"
        )
        if not ok or not search_text.strip():
            return

        nodes = self.get_target_nodes()
        if not nodes:
            nuke.message("No matching nodes to search.")
            return

        results = []
        knob_names_found = set()
        search_lower = search_text.strip().lower()
        for node in nodes:
            for k, knob in node.knobs().items():
                if search_lower in k.lower():
                    results.append(f"{node.name()} → {k} ({knob.Class()})")
                    knob_names_found.add(k)

        if not results:
            QtWidgets.QMessageBox.information(self, "Search Knobs", "No matching knobs found.")
            return

        # Show results
        result_text = "\n".join(results)
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Matching Knobs")
        msg.setText(f"{len(knob_names_found)} unique knobs found:\n\n{result_text}")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msg.setInformativeText("Do you want to add these knobs to the table?")
        result = msg.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            # Collect existing names in the table
            existing_knobs = set()
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item:
                    existing_knobs.add(item.text().strip())

            # Add only new names
            for knob_name in sorted(knob_names_found):
                if knob_name not in existing_knobs:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(knob_name))
                    self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(""))


# Fonction utilisée par registerWidgetAsPanel
def create_change_knob_panel():
    return ChangeKnobValueWidget()

# Show Panel
def show_change_knob_panel():
    global change_knob_panel
    change_knob_panel = ChangeKnobValueWidget()
    flags = change_knob_panel.windowFlags() | QtCore.Qt.WindowStaysOnTopHint
    change_knob_panel.setWindowFlags(flags)
    change_knob_panel.show()
