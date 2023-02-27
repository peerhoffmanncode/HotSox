from django.forms.widgets import Input, NumberInput, CheckboxInput


class RangeInput(NumberInput):
    input_type = "range"
    template_name = "widgets/range.html"


class SwitchCheckboxInput(Input):
    input_type = "range"
    template_name = "widgets/switch.html"
