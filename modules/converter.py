import modules.code_parser as code_parser
import modules.formatter as formatter


def get_items_list(module, all_format, public, only_docstrings,
                   empty):
    if all_format:
        return module.get_according_to_all()
    if public:
        return module.get_public_items()
    if only_docstrings:
        return module.get_items_with_docstrings()
    if empty:
        return module.items
    return module.get_items_without_empty()


def make_lines(line, line_len=100):
    current_line = ""
    words = line.split(' ')
    lines = []
    for word in words:
        if len(current_line) + len(word) > line_len:
            lines.append(current_line)
            current_line = word
        else:
            current_line += (" " + word
                             if current_line else word)
    lines.append(current_line)
    return lines


def split_docstring(docstring, line_len=100):
    paragraphs = docstring.split('\n\n')
    lines = []
    for line in paragraphs:
        line = line.replace('\n', ' ')
        lines += make_lines(line, line_len)
    return lines


CLASS_SHIFT = 30
FUNC_SHIFT = 20
METHOD_SHIFT = 50
STRINGS_COUNT = 35
PAGE_LEN = 717


def create_pages(text_items):
    pages = []
    page = []
    for item in text_items:
        if item.type == code_parser.ItemsType.METHOD:
            for i, line in enumerate(make_lines(item.name)):
                page.append(code_parser.TextItem(
                    code_parser.ItemsType.METHOD,
                    line, ""))
        else:
            page.append(item)
        if item.docstring:
            for line in split_docstring(item.docstring):
                current_page = code_parser.TextItem(
                    code_parser.ItemsType.DOCSTRING,
                    line, "")
                if len(page) == STRINGS_COUNT:
                    pages.append(page)
                    page = []
                page.append(current_page)
        if len(page) == STRINGS_COUNT:
            pages.append(page)
            page = []
    pages.append(page)
    return pages


def get_pdf_pages(pages):
    pdf_pages = []
    page_shift = 0
    last_class = False
    for page in pages:
        page_content = []
        shift = 0
        for item in page:
            if item.type == code_parser.ItemsType.MODULE:
                page_content.append(formatter.get_module_pdf(item.name, shift))
                last_class = False
            if item.type == code_parser.ItemsType.CLASS:
                page_content.append(
                    formatter.get_class_pdf(item.name, shift + CLASS_SHIFT))
                shift = -CLASS_SHIFT
                last_class = True
            if item.type == code_parser.ItemsType.METHOD:
                curr_shift = METHOD_SHIFT if last_class else FUNC_SHIFT
                page_content.append(formatter.get_func_pdf(item.name,
                                                           curr_shift + shift))
                shift = -curr_shift
            if item.type == code_parser.ItemsType.DOCSTRING:
                if not page_content:
                    page_content.append(
                        formatter.get_docstring_pdf(item.name, page_shift))
                    shift = -page_shift
                else:
                    page_content.append(formatter.get_docstring_pdf(item.name,
                                                                    0))
            page_shift = -shift
        if page_content:
            pdf_pages.append(page_content)
    return pdf_pages


def make_content_table(pages):
    class Chapter:
        def __init__(self, name, page_number):
            self.name = name
            self.page_number = page_number

    def make_chapters():
        content_pages = []
        chapters = []
        num = 0
        for i, page in enumerate(pages):
            if not page:
                num += 1
            if page and page[0].type == code_parser.ItemsType.MODULE:
                chapters.append(Chapter(page[0].name, i - num))
            if len(chapters) == STRINGS_COUNT:
                content_pages.append(chapters)
                chapters = []
        if chapters:
            content_pages.append(chapters)
        return content_pages

    def make_pdf_pages(content_pages):
        pdf_pages = []
        for i, page in enumerate(content_pages):
            current_page = []
            if i == 0:
                current_page.append(
                    formatter.get_uni_string_pdf("MODULES:", 0))
            for chapter in page:
                num = str(chapter.page_number + len(content_pages) + 1)
                points_len = len(chapter.name) + len(num)
                current_page.append(
                    formatter.get_uni_string_pdf(
                        chapter.name + ('.' * 70)[: -points_len] + num,
                        0))
            pdf_pages.append(current_page)
        return pdf_pages

    def make_annots(content_pages):
        annots = []
        for page in content_pages:
            for i, line in enumerate(page):
                end = PAGE_LEN - i * 20
                begin = end - 5
                annots.append(formatter.Annots(
                    begin, end,
                    line.page_number + len(content_pages) + 1))
        return annots

    content_pages = make_chapters()
    return make_pdf_pages(content_pages), make_annots(content_pages)


def convert(files_list, all_format, public, only_docstrings,
            content_table, empty):
    pdf_string_modules = []
    pages = []
    for file in files_list:
        with open(file) as f:
            code = f.read()
        module = code_parser.Module(file, code)
        text_items = get_items_list(module, all_format,
                                    public, only_docstrings,
                                    empty)
        curr_pages = create_pages(text_items)
        pdf_string_modules += get_pdf_pages(curr_pages)
        pages += curr_pages
    if content_table:
        content = make_content_table(pages)
        pdf_string_modules = content[0] + pdf_string_modules
        return formatter.get_text_in_pdf_format(pdf_string_modules, content[1])
    return formatter.get_text_in_pdf_format(pdf_string_modules)
