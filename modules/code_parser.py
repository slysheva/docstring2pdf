import ast
import os
from enum import Enum


class ItemsType(Enum):
    MODULE = 0
    CLASS = 1
    METHOD = 2
    DOCSTRING = 3


class TextItem:
    def __init__(self, type_, name, docstring):
        self.type = type_
        self.name = name
        self.docstring = docstring

    def __eq__(self, other):
        return ((self.type, self.name, self.docstring)
                == (other.type, other.name, other.docstring))


class DfsNode:
    def __init__(self, node, index):
        self.node = node
        self.index = index


def quote(string, l, r):
    return l + string + r


class Module:
    def __init__(self, file, code):
        self.path = file
        self.name = self.path.split(os.sep)[-1]
        self.public = set()
        self.modules = []
        self._operations = {ast.Add: "+",
                            ast.Mult: "*",
                            ast.Div: "/",
                            ast.Mod: "%",
                            ast.Sub: "-",
                            ast.Pow: "**",
                            ast.LShift: "<<",
                            ast.RShift: ">>"
                            }
        self.root = ast.parse(code)
        self.items = self._extract_text_items()
        self.all = self._get__all__methods()

    def _get__all__methods(self):
        res = set()
        for next_node in ast.iter_child_nodes(self.root):
            if (isinstance(next_node, ast.Assign)
                    and not isinstance(next_node.value, ast.BinOp)):
                for item in next_node.targets:
                    if "id" in vars(item) and item.id == "__all__":
                        for element in next_node.value.elts:
                            res.add(element.s)
        return res

    def _extract_docstring(self, ast_node):
        description = ast.get_docstring(ast_node)
        if description is not None:
            return str(description)
        return ""

    def _get_defaults(self, node):
        def add_parentheses(expr):
            return quote(expr, '(', ')') if len(expr) > 1 else expr

        def _get_expr(item):
            if (isinstance(item, ast.BinOp)):
                left = add_parentheses(_get_expr(item.left))
                right = add_parentheses(_get_expr(item.right))
                operation = self._operations[type(item.op)]
                return ' '.join((left, operation, right))
            return str(list(item.__dict__.values())[0])

        def get_funs_elems(item):
            res = ', '.join(_get_elems(a) for a in item.args)
            if (isinstance(item.func, ast.Attribute)
                    and "value" in vars(item.func)
                    and "id" in vars(item.func.value)):
                return str(item.func.value.id) + quote(res, '(', ')')
            if ("func" in vars(item)
                    and "id" in vars(item.func)):
                return str(item.func.id) + quote(res, '(', ')')

        def get_dict_elems(item):
            keys = [_get_elems(a) for a in item.keys]
            vals = [_get_elems(a) for a in item.values]
            res = ""
            for i, k in enumerate(keys):
                res += k + ': ' + vals[i] + ', '
            if res:
                res = res[:-2]
            return quote(res, '{', '}')

        def _get_elems(item):
            elem = list(item.__dict__.values())[0]
            if isinstance(item, ast.Call):
                return get_funs_elems(item)
            elif (isinstance(item, ast.Attribute)
                    and "id" in vars(item.value)):
                return item.value.id + "." + item.attr
            elif isinstance(item, ast.List):
                res = ', '.join([_get_elems(a) for a in item.elts])
                return quote(res, '[', ']')
            elif isinstance(item, ast.Dict):
                return get_dict_elems(item)
            elif isinstance(item, ast.Str):
                return '"' + str(elem) + '"'
            elif isinstance(item, ast.BinOp):
                return _get_expr(item)
            else:
                return str(elem)

        return list(map(lambda item: _get_elems(item), node.defaults))

    def _extract_text_items(self):
        dfs_stack = [DfsNode(self.root, 0)]
        items = [TextItem(type_=ItemsType.MODULE,
                          name=self.name,
                          docstring=self._extract_docstring(self.root))]
        while dfs_stack:
            tmp = dfs_stack.pop()
            node = tmp.node
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                name = node.name
                if isinstance(node, ast.ClassDef):
                    if name[0] != '_':
                        self.public.add(name)
                    type_of_item = ItemsType.CLASS
                else:
                    type_of_item = ItemsType.METHOD
                docstring = self._extract_docstring(node)
                items.append(TextItem(type_of_item, name, docstring))
            elif isinstance(node, ast.arguments):
                arguments_list = [x.arg for x in node.args]
                defaults = self._get_defaults(node)
                for i, default in enumerate(defaults):
                    index = -len(defaults) + i
                    arguments_list[index] += "=" + str(default)
                if node.vararg is not None:
                    arguments_list.append('*' + str(node.vararg.arg))
                if node.kwarg is not None:
                    arguments_list.append('**' + str(node.kwarg.arg))
                items[tmp.index].name += quote(", ".join(arguments_list),
                                               '(', ')')
                if items[tmp.index].name[0] != "_":
                    self.public.add(items[tmp.index].name)
                continue
            for next_node in reversed(list(ast.iter_child_nodes(node))):
                if isinstance(next_node, (
                        ast.arguments,
                        ast.ClassDef,
                        ast.FunctionDef)):
                    dfs_stack.append(DfsNode(next_node, len(items) - 1))
        return items

    def get_public_items(self):
        res = [self.items[0]]
        for item in self.items:
            if item.name in self.public:
                res.append(item)
        return res

    def get_according_to_all(self):
        res = [self.items[0]]
        in_all = False
        for item in self.items:
            if item.type == ItemsType.CLASS:
                if item.name in self.all:
                    in_all = True
                    res.append(item)
                else:
                    in_all = False
            elif in_all:
                res.append(item)
        return res

    def get_items_without_empty(self):
        res = []
        for i, item in enumerate(self.items):
            if i == len(self.items) - 1:
                break
            if ((item.type == ItemsType.MODULE
                    and self.items[i + 1].type != ItemsType.MODULE)
                    or item.type != ItemsType.MODULE):
                res.append(item)
        if self.items[-1].type != ItemsType.MODULE:
            res.append(self.items[-1])
        return res


    def get_items_with_docstrings(self):
        reversed_items = reversed(self.items)
        result = []
        current_methods = []
        current_class_has_docstring = False
        for item in reversed_items:
            if item.type == ItemsType.METHOD and item.docstring:
                current_methods.append(item)
                current_class_has_docstring = True
            elif (item.type == ItemsType.CLASS
                  and (current_class_has_docstring or item.docstring)):
                current_methods.append(item)
                result += current_methods
                current_methods = []
                current_class_has_docstring = False
            elif item.type == ItemsType.MODULE:
                if result:
                    result.append(item)
        return list(reversed(result))
