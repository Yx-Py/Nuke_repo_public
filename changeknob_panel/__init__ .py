# __init__.py – pour nuke_toolbox.modules.change_knob

from .changeknob_panel import ChangeKnobValueWidget, show_change_knob_panel, create_change_knob_panel

# Enregistrement auto dans le Pane menu (optionnel mais pratique)
import nukescripts
nukescripts.registerWidgetAsPanel("create_change_knob_panel", "Change Knob Panel", "yanoo.changeknob")
