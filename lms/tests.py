from django.test import TestCase
from django.template import Context, Template
from lms.templatetags.custom_filters import split

class SplitFilterTests(TestCase):
    def test_split_string(self):
        value = "a/b/c"
        result = split(value, "/")
        self.assertEqual(result, ["a", "b", "c"])

    def test_split_string_no_delimiter(self):
        value = "abc"
        result = split(value, "/")
        self.assertEqual(result, ["abc"])

    def test_split_empty_string(self):
        # My filter returns [] if value is falsy
        value = ""
        result = split(value, "/")
        self.assertEqual(result, [])

    def test_template_usage(self):
        template = Template("{% load custom_filters %}{{ 'x-y-z'|split:'-'|join:',' }}")
        rendered = template.render(Context())
        self.assertEqual(rendered, "x,y,z")
