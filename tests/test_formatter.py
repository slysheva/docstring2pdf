import os
import sys
import unittest
from modules import formatter

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))


class FormatterTest(unittest.TestCase):
    def test_get_screening_string1(self):
        string = "def sum(a, b)"
        expected = "def sum\\(a, b\\)"
        actual = formatter.get_screening_string(string)
        self.assertEqual(actual, expected)

    def test_get_screening_string2(self):
        string = "I'm cool"
        expected = "I\\'m cool"
        actual = formatter.get_screening_string(string)
        self.assertEqual(actual, expected)

    def test_get_pages_references(self):
        expected = "3 0 R 4 0 R 5 0 R"
        actual = formatter.get_pages_references(3)
        self.assertEqual(actual, expected)

    def test_make_pages_part(self):
        one_page = '''3 0 obj\n<<
    /Type /Page
    /Parent 2 0 R
    /Resources
    <<
        /Font
        <<
            /FBase
            <<
                /Type /Font
                /Subtype /Type1
                /BaseFont /Times-Roman
            >>
            /FBold
            <<
                /Type /Font
                /Subtype /Type1
                /BaseFont /Times-Bold
            >>
            /FItalic
            <<
                /Type /Font
                /Subtype /Type1
                /BaseFont /Times-Italic
            >>
        >>
    >>
    /MediaBox [0 0 612 792]
    /Contents 4 0 R
>>
endobj\n'''
        expected = [one_page]
        actual = formatter.make_pages_part(1, [])
        self.assertEqual(actual, expected)

    def test_make_content_part(self):
        expected = ['''4 0 obj
<<
/Length 74
>>
stream
  BT
  /FBase 10 Tf

    295 752 Td

    (1) Tj

    /FBase 12 Tf

    -255 -1 Td

    () Tj
HIET
endstream
endobj\n''']
        actual = formatter.make_content_part(1, ["HI"])
        self.assertEqual(actual, expected)

    def test_make_xref_table(self):
        pages = formatter.make_pages_part(1, [])
        content = formatter.make_content_part(1, ["HI"])
        expected = '''xref
0 5
0000000000 65535 f
0000000015 00000 n
0000000064 00000 n
0000000678 00000 n
0000000825 00000 n\n'''
        actual = formatter.make_xref_table(pages, content)
        self.assertEqual(actual, expected)

    def test_get_module_pdf_string(self):
        string = "example"
        shift = 0
        expected = "/FBold 16 Tf\n 0 -20 Td\n(Module: example) Tj\n"
        actual = formatter.get_module_pdf(string, shift)
        self.assertEqual(actual, expected)

    def test_get_function_pdf_string(self):
        string = "example"
        shift = 0
        expected = "/FBase 12 Tf\n 0 -20 Td\n(example) Tj\n"
        actual = formatter.get_func_pdf(string, shift)

        self.assertEqual(actual, expected)

    def test_get_docstring_pdf_string(self):
        string = "example"
        shift = 0
        expected = "/FItalic 10 Tf\n 0 -20 Td\n(example) Tj\n"
        actual = formatter.get_docstring_pdf(string, shift)
        self.assertEqual(actual, expected)
