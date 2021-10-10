from django import template

register = template.Library()


@register.inclusion_tag("includes/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    return {"breadcrumbs": context["breadcrumbs"]}
