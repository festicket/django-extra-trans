"""Tests for `extra_trans` module."""
import pytest
from django.template import TemplateSyntaxError, engines
from django.utils import translation

class TestWithDefaultLanguage:
    """Tests for `language.templatetags.language_tags#with_default_language` tag."""

    @pytest.mark.parametrize(
        'args, language, expected_output',
        [
            ('', 'en-gb', 'Order'),
            ('', 'fr', 'Ordre&nbsp;|&nbsp;Order'),
            ('<br>', 'fr', 'Ordre<br>Order'),
            ('"<p class=\"foo\">" </p>', 'fr', 'Ordre<p class="foo">Order</p>'),
        ],
    )
    def test_okay(self, args, language, expected_output):
        """
        Check valid cases.
         :param args: a string with optional paramaters to include into the template
        :param language: a string with the code of the currently active language
        :param expected_ouput: a string with the expected output
        """
        output = self.render(args, language)
        assert output == expected_output

    def test_arguments_error(self):
        """Check the case when the number of arguments is incorrect."""
        with pytest.raises(TemplateSyntaxError):
            self.render('a b c', {})

    @staticmethod
    def render(args, language):
        """Helper to render a template from string."""
        engine = engines['django']
        template = (
            "{% load i18n extra_trans %}" f"{{% with_default_language {args} %}}" "{% trans 'Order' %}" "{% end %}"
        )

        with translation.override(language):
            return engine.from_string(template).render({})
