class Annots:
    def __init__(self, begin, end, obj):
        self.begin = begin
        self.end = end
        self.obj = obj


BEGIN_PATTERN = '''%PDF-1.2
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
    /Type /Pages
    /Kids [{}]
    /Count {}
>>
endobj\n'''


PAGE_PATTERN = '''{} 0 obj
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
    /Contents {} 0 R
>>
endobj\n'''


CONTENT_PATTERN = '''{} 0 obj
<<
/Length {}
>>
stream
  BT
  {}ET
endstream
endobj\n'''


TRAILER_PATTERN = '''trailer
<<
    /Root 1 0 R
    /Size {}
>>
startxref
{}
%%EOF'''

ANNONTS_PATTERN = '''{} 0 obj
<<	/Type /Annot
    /Subtype /Link
    /Rect [40 {} 560 {}]
    /Border [16 16 1]
    /Dest [{} 0 R /FitBH 680.75]
>>
endobj\n'''

ANNOTS_PAGE_PATTERN = '''{} 0 obj
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
    /Contents {} 0 R
    /Annots [{}]
>>
endobj\n'''


def get_screening_string(string):
    return string.replace('(', '\\(').replace(')', '\\)').replace("'", "\\'")


def get_title():
    return "/FBold 16 Tf\n 40 9960 Td\n (Docstrings to PDF_Doc:) Tj\n"


def get_pages_references(pages_count, shift=0):
    return ' '.join(str(i + 3) + ' 0 R' for i in range(shift,
                                                       pages_count + shift))


def make_pages_part(pages_count, annots):
    annots_count = int(len(annots) / 35) + 1 if len(annots) % 35 else 0
    pages_part = []
    for i in range(annots_count):
        pages_part.append(ANNOTS_PAGE_PATTERN.format(
            3 + i,
            3 + i + pages_count,
            get_pages_references(len(annots), pages_count * 2)))
    for i in range(annots_count,
                   pages_count):
        page_number = 3 + i
        pages_part.append(PAGE_PATTERN.format(page_number,
                                              page_number + pages_count))
    return pages_part


def make_content_part(pages_count, list_of_strings):
    content_part = []
    first_line_pattern = '''/FBase 10 Tf\n
    295 752 Td\n
    ({}) Tj\n
    /FBase 12 Tf\n
    -255 -1 Td\n
    () Tj\n'''
    for i, page in enumerate(list_of_strings):
        length = len(CONTENT_PATTERN)
        current_text = first_line_pattern.format(i + 1)
        for string in page:
            length += len(string)
            current_text += string
        content_part.append(CONTENT_PATTERN.format(i + 3 + pages_count,
                                                   length + 10,
                                                   current_text))
    return content_part


def make_annots_part(pages_count, annots_list):
    annots_part = []
    for i, annot in enumerate(annots_list):
        annots_part.append(ANNONTS_PATTERN.format(i + 3 + pages_count * 2,
                                                  annot.begin,
                                                  annot.end,
                                                  annot.obj + 2))
    return annots_part


def make_xref_table(pages, content):
    objects = pages + content
    objects_count = len(pages) * 2 + 2
    xref_table = '''xref\n0 {}\n0000000000 65535 f\n'''.format(
        objects_count + 1)
    xref_table += "0000000015 00000 n\n" + "0000000064 00000 n\n"
    xref_string_pattern = '''{} 00000 n\n'''
    current_shift = 64
    for i, obj in enumerate(objects):
        current_shift += len(obj)
        length = '0000000000' + str(current_shift)
        xref_table += xref_string_pattern.format(length[-10:])
    return xref_table


def get_text_in_pdf_format(pdf_modules, annots=[]):
    pages_count = len(pdf_modules)
    result_string = BEGIN_PATTERN.format(
        get_pages_references(pages_count), pages_count)
    pages = make_pages_part(pages_count, annots)
    content = make_content_part(pages_count, pdf_modules)
    annots_part = make_annots_part(pages_count, annots)
    xref_table = make_xref_table(pages, content)
    for obj in pages + content + annots_part:
        result_string += obj
    result_string += xref_table
    result_string += TRAILER_PATTERN.format(pages_count * 2 + 2,
                                            len(result_string) + 100)
    return result_string


def get_module_pdf(string, shift):
    string = get_screening_string(string)
    string = "Module: " + string
    return "/FBold 16 Tf\n {} -20 Td\n({}) Tj\n".format(shift, string)


def get_class_pdf(string, shift):
    string = get_screening_string(string)
    string = "Class: " + string
    return "/FBase 14 Tf\n {} -20 Td\n({}) Tj\n".format(shift, string)


def get_func_pdf(string, shift):
    string = get_screening_string(string)
    return "/FBase 12 Tf\n {} -20 Td\n({}) Tj\n".format(shift, string)


def get_docstring_pdf(string, shift):
    string = get_screening_string(string)
    return "/FItalic 10 Tf\n {} -20 Td\n({}) Tj\n".format(shift, string)


def get_uni_string_pdf(string, shift):
    string = get_screening_string(string)
    return "/FStand 12 Tf\n {} -20 Td\n({}) Tj\n".format(shift, string)
