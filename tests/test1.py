"""Module's docstring"""
import re


class B:
    pass


# class Monster:
#     def __init__(self, current_pos, image, scatter_point):
#         pass
#     def make_step(self, field, width, height):
#         """two
#         lines docstring"""
#         pass
# кавычки, метод с одного подч, класс в функции


class DifferentDefaults:
    '''docstring for class with different default arguments'''

    def args_kwargs(self, *args, **kwargs):
        pass

    def default_string(self, a="string"):
        pass

    def default_empty_dict_list(self, a={}, b=[]):
        # '''fake docstring'''
        pass

    def default_own_class(self, a=B()):
        pass

    def default_dict(self, a={1: 1, 2: 2}):
        pass

    def default_func(
            self, search_name, link,
            _egg_info_re=re.compile(r'([a-z0-9_.]+)-([a-z0-9_.!+-]+)', re.I)):
        pass

    def default_expr1(self, a=(1 + 3) * (4 - 5)):
        pass

    def default_expr2(self, a=7 % 5):
        pass
