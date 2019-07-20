from django import template
from django.template import TemplateSyntaxError, Node
from django.templatetags.i18n import LanguageNode
from django.conf import settings
from django.utils import translation
from django.utils.text import unescape_string_literal
from django.utils.html import mark_safe


register = template.Library()

@register.tag
def with_default_language(parser, token):
    """
    Template tag to render two versions of the text both in local and default languages.

    Accepts two optional paramaters:
        * prefix - a string to put before the text in the default language
        * suffix - a string to put after the text in the default language

    This tag allows translated static content be listed in templates i.e. discoverable by
    `makemessages` command and at the same time reduce the boilerplate if you need to display
    two versions of the text.

    Example of usage:

        {% with_default_language <span> </span> %}
            <p>{% trans "Hello" %}</p>
        {% end %}

        Will produce next HTML:

             <p>Bonjour</p><span><p>Hello</p></span>

        Given that the current active language is French.
    """
    bits = token.split_contents()
    name, args = bits[0], bits[1:]

    if len(args) > 2:
        raise TemplateSyntaxError(f'{name}: too many arguments: {args}')

    try:
        prefix = args[0]
    except IndexError:
        prefix = '&nbsp;|&nbsp;'

    try:
        suffix = args[1]
    except IndexError:
        suffix = ''

    nodelist = parser.parse(('end',))
    parser.delete_first_token()
    return WithDefaultLanguageNode(nodelist, prefix=prefix, suffix=suffix)


class WithDefaultLanguageNode(Node):
    """Node class to use with `with_default_language` template tag."""

    def __init__(self, nodelist, prefix, suffix):
        self.nodelist = nodelist
        self.prefix = safe_unescape_string_literal(prefix)
        self.suffix = safe_unescape_string_literal(suffix)

    def render(self, context):
        """Render content in default language if the current one is not it."""
        original_output = self.nodelist.render(context)

        if translation.get_language() == settings.LANGUAGE_CODE:
            return original_output

        with translation.override(settings.LANGUAGE_CODE):
            in_default_language_output = self.nodelist.render(context)        
        
        return mark_safe(f'{original_output}{self.prefix}{in_default_language_output}{self.suffix}')


def safe_unescape_string_literal(value):
    """Safe version of the `django.utils.text#unescape_string_literal` function."""
    try:
        return unescape_string_literal(value)
    except (ValueError, IndexError):
        return value
