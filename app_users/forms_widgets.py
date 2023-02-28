from django.forms.widgets import TextInput, NumberInput, CheckboxInput


class RangeInput(NumberInput):
    input_type = "range"
    template_name = "widgets/range.html"


class SwitchCheckboxInput(CheckboxInput):
    input_type = "checkbox"
    template_name = "widgets/switch.html"
