import nukescripts
import changeknob_panel

menubar=nuke.menu("Nuke")
m=menubar.addMenu("&ToolBox", icon="changeknob_icon.png")
m.addCommand("change knobs value", changeknob_panel.show_change_knob_panel)

nukescripts.panels.registerWidgetAsPanel(
    "changeknob_panel.create_change_knob_panel",
    "Change Knob Value",
    "co.uk.changeknobPanel"
)