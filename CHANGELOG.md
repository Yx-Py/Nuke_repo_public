# ChangeKnob Panel - Changelog

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