import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from modules import code_parser


class CodeParserTest(unittest.TestCase):
    file_path = """\dir\python_file.py"""
    with open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)),
            "test2.py")) as f:
        code_example2 = f.read()
    module_ex2 = code_parser.Module(file_path, code_example2)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "test1.py")) as f:
        code_example1 = f.read()
    module_ex1 = code_parser.Module(file_path, code_example1)

    def test_file_name_defined(self):
        self.assertEqual(self.module_ex1.name, "python_file.py")

    def test_defaults(self):
        expected = [code_parser.TextItem(code_parser.ItemsType.MODULE,
                                         "python_file.py",
                                         "Module's docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "B", ""),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "DifferentDefaults",
                                         "docstring for class "
                                         + "with different default arguments"),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "args_kwargs(self, *args, **kwargs)",
                                         ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         'default_string(self, a="string")',
                                         ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        'default_empty_dict_list(self, a={}, b=[])',
                        ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         'default_own_class(self, a=B())',
                                         ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         'default_dict(self, a={1: 1, 2: 2})',
                                         ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        "default_func(self, search_name, link, "
                        + "_egg_info_re=re(\"([a-z0-9_.]+)-"
                        + "([a-z0-9_.!+-]+)\", re.I))",
                        ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        'default_expr1(self, a=(1 + 3) * (4 - 5))',
                        ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         'default_expr2(self, a=7 % 5)',
                                         "")]

        self.assertEqual(self.module_ex1.items, expected)

    def test_extract_text_items(self):
        expected = [code_parser.TextItem(code_parser.ItemsType.MODULE,
                                         "python_file.py",
                                         "Module's docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Point", "docstring for point class"),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "__init__(self, r, x=7, y=[])",
                                         ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "__eq__(self, other)", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "find_dist_sq(self, other)", ""),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Monster", ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        "__init__(self, current_pos, image, scatter_point)",
                        ""),
                    code_parser.TextItem(
                        code_parser.ItemsType.METHOD,
                        "make_step(self, field, width, height)",
                        "two\nlines docstring"),
                    code_parser.TextItem(code_parser.ItemsType.CLASS,
                                         "Game", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "__init__(self)", ""),
                    code_parser.TextItem(code_parser.ItemsType.METHOD,
                                         "_update_game_state(self)", "")]
        self.assertEqual(self.module_ex2.items, expected)

    def test_get_according_to_all(self):
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
        self.assertEqual(self.module_ex2.get_according_to_all(), expected)

    def test_get_public_items(self):
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
        self.assertEqual(self.module_ex2.get_public_items(), expected)

    def test_get_items_with_docstrings(self):
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
        self.assertEqual(self.module_ex2.get_items_with_docstrings(), expected)
