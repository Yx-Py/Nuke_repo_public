# 🧩 ChangeKnob Panel – Nuke Toolbox Module

![Status](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Nuke](https://img.shields.io/badge/Nuke-13+-orange)

A lightweight and powerful Nuke panel to quickly apply knob changes across multiple nodes.  
Designed to improve speed, consistency, and flexibility in artist workflows.

---

## 📚 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [UI Overview](#ui-overview)
- [Integration](#integration)
- [Roadmap](#roadmap)
- [License](#license)

---

## 🚀 Features

- Target nodes by selection, class, or name fragment
- Multi-knob changes with undo support (`Ctrl+Z`)
- Auto-load common knobs across selected nodes
- Clean and intuitive floating UI
- Smart filtering to ignore internal/unusable knobs

---

## 💾 Installation

1. Clone or download this repository.
2. Add the module to your Nuke plugin path:

```python
# In your menu.py
import change_knob_panel
change_knob_panel.create_change_knob_panel()
```

3. (Optional) Register the panel in the Nuke Pane menu:

```python
nukescripts.registerWidgetAsPanel("create_change_knob_panel", "Change Knob Panel", "yalux.changeknob")
```

---

## 🧰 Usage

Open the panel and:

1. Choose the node selection mode (Selection, Class, Name)
2. Add knobs and their new values in the table
3. Click **Apply** to commit the changes
4. Use **Load Common Knobs** to auto-detect shared knobs
5. **Undo** with `Ctrl+Z` to revert

---

## 🎛️ UI Overview

| Element              | Description                                              |
|----------------------|----------------------------------------------------------|
| Apply to             | Selection mode                                           |
| Node Class / Name    | Class or name fragment (if needed)                       |
| Table (Knob/Value)   | List of knob/value pairs                                 |
| + / –                | Add or remove table rows                                 |
| Clear Table          | Clears the entire knob table                             |
| Load Common Knobs    | Auto-detects knobs common to all targeted nodes          |
| Apply                | Applies changes                                           |

---

## 🛠 Integration

Works out of the box with custom Nuke scripts.  
Easily embeddable in larger pipeline toolkits or studio environments.

---

## 📌 Roadmap

- Preset saving and loading
- Knob name auto-completion
- Edit history
- Multi-shot pipeline integration

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Yx and Dot] – feel free to contribute or reach out!