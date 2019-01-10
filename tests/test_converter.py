import unittest
import sys
import os
from modules import converter
from modules import code_parser
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))


class ConverterTest(unittest.TestCase):
    def test_split_func1(self):
        expected = ["def __init__(self, r, x=7, y=[])"]
        actual = converter.make_lines(expected[0])
        self.assertEqual(expected, actual)

    def test_split_func2(self):
        func = ("__init__(self, loop, protocol, args, shell, stdin, stdout,"
                + " stderr, bufsize, waiter=None, extra=None, **kwargs)")
        expected = ["__init__(self, loop, protocol, args, shell, stdin, "
                    + "stdout, stderr, bufsize, waiter=None, extra=None,",
                    "**kwargs)"]
        actual = converter.make_lines(func)
        self.assertEqual(expected, actual)

    def test_get_items_list1(self):
        file_path = """\dir\python_file.py"""
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "test2.py")) as f:
            code_example = f.read()
        module_ex = code_parser.Module(file_path, code_example)
        expected = [code_parser.TextItem(code_parser.ItemsType.MODULE,
                                         "python_file.py",
                                         "Module's docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Point",
                                         "docstring for point class"),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        "__init__(self, r, x=7, y=[])", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "__eq__(self, other)", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "find_dist_sq(self, other)", ""),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Game", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "__init__(self)", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "_update_game_state(self)", "")]
        actual = converter.get_items_list(module_ex, True, False, False, False)
        self.assertEqual(actual, expected)

    def test_get_items_list2(self):
        file_path = """\dir\python_file.py"""
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "test2.py")) as f:
            code_example = f.read()
        module_ex = code_parser.Module(file_path, code_example)
        expected = [code_parser.TextItem(code_parser.ItemsType.MODULE,
                                         "python_file.py",
                                         "Module's docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Point",
                                         "docstring for point class"),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "find_dist_sq(self, other)", ""),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Monster", ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        """make_step(self, field, width, height)""",
                        "two\nlines docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Game", "")]
        actual = converter.get_items_list(module_ex, False, True, False, False)
        self.assertEqual(actual, expected)

    def test_get_items_list3(self):
        file_path = """\dir\python_file.py"""
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "test2.py")) as f:
            code_example = f.read()
        module_ex = code_parser.Module(file_path, code_example)
        expected = [code_parser.TextItem(code_parser.ItemsType.MODULE,
                                         "python_file.py",
                                         "Module's docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Point",
                                         "docstring for point class"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Monster", ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        """make_step(self, field, width, height)""",
                        "two\nlines docstring")]
        actual = converter.get_items_list(module_ex, False, False, True, False)
        self.assertEqual(actual, expected)

    def test_split_docstring1(self):
        docstring = "one line"
        expected = [docstring]
        actual = converter.split_docstring(docstring)
        self.assertEqual(actual, expected)

    def test_split_docstring2(self):
        docstring = "first line\nsecond line"
        expected = ["first line second line"]
        actual = converter.split_docstring(docstring)
        self.assertEqual(actual, expected)

    def test_split_docstring3(self):
        docstring = "first line\n\nsecond line"
        expected = ["first line", "second line"]
        actual = converter.split_docstring(docstring)
        self.assertEqual(actual, expected)

    def test_whole_work(self):
        expected = '''%PDF-1.2
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
    /Type /Pages
    /Kids [3 0 R 4 0 R]
    /Count 2
>>
endobj
3 0 obj
<<
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
            /FStand
            <<
                /Type /Font
                /Subtype /Type1
                /BaseFont /Courier
            >>
        >>
    >>
    /MediaBox [0 0 612 792]
    /Contents 5 0 R
    /Annots [7 0 R]
>>
endobj
4 0 obj
<<
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
    /Contents 6 0 R
>>
endobj
5 0 obj
<<
/Length 210
>>
stream
  BT
  /FBase 10 Tf

    295 752 Td

    (1) Tj

    /FBase 12 Tf

    -255 -1 Td

    () Tj
/FStand 12 Tf
 0 -20 Td
(MODULES:) Tj
/FStand 12 Tf
 0 -20 Td
(test2.py.............................................................2) Tj
ET
endstream
endobj
6 0 obj
<<
/Length 818
>>
stream
  BT
  /FBase 10 Tf

    295 752 Td

    (2) Tj

    /FBase 12 Tf

    -255 -1 Td

    () Tj
/FBold 16 Tf
 0 -20 Td
(Module: test2.py) Tj
/FItalic 10 Tf
 0 -20 Td
(Module\\'s docstring) Tj
/FBase 14 Tf
 30 -20 Td
(Class: Point) Tj
/FItalic 10 Tf
 0 -20 Td
(docstring for point class) Tj
/FBase 12 Tf
 20 -20 Td
(__init__\(self, r, x=7, y=[]\)) Tj
/FBase 12 Tf
 0 -20 Td
(__eq__\(self, other\)) Tj
/FBase 12 Tf
 0 -20 Td
(find_dist_sq\(self, other\)) Tj
/FBase 14 Tf
 -20 -20 Td
(Class: Monster) Tj
/FBase 12 Tf
 20 -20 Td
(__init__\(self, current_pos, image, scatter_point\)) Tj
/FBase 12 Tf
 0 -20 Td
(make_step\(self, field, width, height\)) Tj
/FItalic 10 Tf
 0 -20 Td
(two lines docstring) Tj
/FBase 14 Tf
 -20 -20 Td
(Class: Game) Tj
/FBase 12 Tf
 20 -20 Td
(__init__\(self\)) Tj
/FBase 12 Tf
 0 -20 Td
(_update_game_state\(self\)) Tj
ET
endstream
endobj
7 0 obj
<<	/Type /Annot
    /Subtype /Link
    /Rect [40 712 560 717]
    /Border [16 16 1]
    /Dest [4 0 R /FitBH 680.75]
>>
endobj
xref
0 7
0000000000 65535 f
0000000015 00000 n
0000000064 00000 n
0000000843 00000 n
0000001457 00000 n
0000001741 00000 n
0000002633 00000 n
trailer
<<
    /Root 1 0 R
    /Size 6
>>
startxref
3078
%%EOF'''
        actual = converter.convert([os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test2.py")], False, False, False, True, False)
        self.assertEqual(actual, expected)
