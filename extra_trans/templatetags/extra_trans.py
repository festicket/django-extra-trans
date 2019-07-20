from django import template
from django.template import TemplateSyntaxError
from django.templatetags.i18n import LanguageNode
from django.conf import settings
from django.utils import translation

register = template.Library()

@register.tag
def if_not_default_language(parser, token):
    """Tag to include the content enclosed only if the current language is not default."""
    bits = token.split_contents()

    if len(bits) > 2:
        raise TemplateSyntaxError("'%s' too many arguments" % bits[0])
    
    language = template.Variable('current_language') 
    nodelist = parser.parse(('end',))
    parser.delete_first_token()
    return IfNotDefaultLanguageNode(nodelist, language)


class IfNotDefaultLanguageNode(LanguageNode):
    def render(self, context):
        """Render the node only if the current language is not the default one."""
        language_code = self.language.resolve(context)
        if language_code is None or language_code == settings.LANGUAGE_CODE:
            return ''
        else:
            return super().render(context)