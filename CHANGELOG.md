# 📦 CHANGELOG

## ✅ Version v1.1 – Refinements & Power Features
Date: 2024-05-XX

### ✨ New Features
- Multi-knob support per row (e.g. `size, center` or `size center`)
- Limit of 5 knobs per row
- Knob search tool: keyword + auto-fill
- Preserve knob order from Nuke property panel
- Toggle to ignore internal/system knobs
- Tooltips and Clear Table button

### 🧠 Improvements
- Undo grouped correctly
- Duplicate knobs ignored in auto-fill
- Lightweight: no callbacks or slowdowns

## 🛠 Version v1.0 – Initial Release
- Modify knobs by selection/class/name
- Table interface
- Load common knobs
- Undo support

## v1.0 – 2024-05-02

### 🚀 Initial Release (Stable)

* Intuitive multi-knob table interface
* Support for applying changes via:

  * node selection
  * class (globally or within selection)
  * partial name (globally or within selection)
* Multi-knob application with global undo support (`Ctrl+Z`)
* Buttons: `+`, `–`, `Clear Table`, `Load Common Knobs`
* Detection of knobs common to all targeted nodes
* Dynamic display of the number of detected knobs
* Added tooltips and UX improvements
* Smart filtering system (`is_ignored_knob`) based on:

  * explicit names
  * generic patterns (`panel`, `tooltip`, `drop`, etc.)
  * non-editable knob types (`Tab_Knob`, `Text_Knob`, etc.)

---

This changelog accompanies the initial stable release of the panel. Future versions may include:

* preset export/import
* knob name auto-completion
* change log or history
* integration with studio pipeline workflows
