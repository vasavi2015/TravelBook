from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={**field.field.widget.attrs, "class": f'{field.field.widget.attrs.get("class", "")} {css}'.strip()})
@register.filter
def mul(a, b):
    try:
        return float(a) * float(b)
    except Exception:
        return ""