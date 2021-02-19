from django import template
register = template.Library()


@register.filter
def addclass(field, css):
    if field.label == 'Tags':
        return field.as_widget(attrs={"class": css, "data-role": "tagsinput"})
    return field.as_widget(attrs={"class": css})