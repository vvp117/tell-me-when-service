from django import template
from django.forms.boundfield import BoundField

register = template.Library()


class AriaDescribedby:
    tag_attr = 'aria-describedby'
    field_attr = 'aria_describedby'

    @register.filter(name='set_aria_describedby')
    def set_id(bound_field: BoundField) -> BoundField:
        field = bound_field.field
        aria_describedby =f'{bound_field.id_for_label}_description'

        setattr(field, AriaDescribedby.field_attr, aria_describedby)
        field.widget.attrs[AriaDescribedby.tag_attr] = aria_describedby

        return bound_field


    @register.filter(name='get_aria_describedby')
    def get_id(bound_field: BoundField) -> str:
        return getattr(bound_field.field, AriaDescribedby.field_attr, '')


@register.filter
def render_label(field, classes):
    return field.label_tag(attrs={'class': classes})
