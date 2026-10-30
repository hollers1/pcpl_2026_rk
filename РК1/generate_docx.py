import os
import subprocess
import sys
import docx
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    """Установить цвет фона ячейки таблицы"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Установить внутренние отступы ячейки (в dxa, 20 dxa = 1 pt)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def create_report_docx():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(script_dir, "main.py")

    with open(main_py_path, "r", encoding="utf-8") as f:
        code_text = f.read()

    # Запускаем main.py для получения актуального вывода
    result = subprocess.run(
        [sys.executable, "-X", "utf8", main_py_path],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    output_text = result.stdout.strip()

    doc = docx.Document()

    # Настройка полей страницы А4 (ГОСТ: левое 25 мм, правое 15 мм, верх/низ 20 мм)
    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.left_margin = Mm(25)
        section.right_margin = Mm(15)

    # Базовые стили: шрифт Times New Roman, цвет строго черный
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Заголовок документа (без титульника)
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    r_title = title_p.add_run("Рубежный контроль №1 по курсу «ПиК ЯП»")
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(12)
    r_sub = sub_p.add_run("Вариант предметной области: 9 («Операционная система» — «Компьютер») | Вариант запросов: Б")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # ------------------ Раздел 1 ------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True
    r_h1 = h1.add_run("1. Описание классов данных предметной области")
    r_h1.font.size = Pt(13)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p1 = doc.add_paragraph()
    p1.paragraph_format.first_line_indent = Mm(12.5)
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(6)
    p1.paragraph_format.line_spacing = 1.15
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_p1 = p1.add_run(
        "В соответствии с вариантом №9 предметной области определены три класса данных, "
        "моделирующие сущности «Операционная система» (сторона отношения «многие») и «Компьютер» "
        "(сторона отношения «один»), а также ассоциативную связку для отношения «многие-ко-многим»."
    )
    r_p1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Таблица классов
    classes_table = doc.add_table(rows=4, cols=3)
    classes_table.style = 'Table Grid'
    classes_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_widths = [Mm(42), Mm(48), Mm(80)]

    headers = ["Класс", "Поля класса", "Назначение и сторона связи"]
    for i, h_text in enumerate(headers):
        cell = classes_table.rows[0].cells[i]
        cell.width = t_widths[i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    rows_data = [
        (
            "OS\n(Операционная система)",
            "• id: int\n• name: str\n• price: int/float\n• comp_id: int",
            "Сущность на стороне связи «многие» (аналог «Сотрудник»). Содержит количественный признак price (стоимость лицензии) и внешний ключ comp_id для связи один-ко-многим с компьютером."
        ),
        (
            "Comp\n(Компьютер)",
            "• id: int\n• name: str",
            "Сущность на стороне связи «один» (аналог «Отдел»). Моделирует физический или виртуальный компьютер/сервер."
        ),
        (
            "OSComp\n(Связь ОС и Компьютеров)",
            "• comp_id: int\n• os_id: int",
            "Ассоциативный класс для реализации связи «многие-ко-многим». Отражает установку нескольких ОС на различных компьютерах."
        )
    ]

    for row_idx, (c_name, fields, desc) in enumerate(rows_data, start=1):
        row = classes_table.rows[row_idx]
        for col_idx, text_val in enumerate([c_name, fields, desc]):
            cell = row.cells[col_idx]
            cell.width = t_widths[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text_val)
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if col_idx == 0:
                r.font.bold = True

    # ------------------ Раздел 2 ------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    r_h2 = h2.add_run("2. Постановка и адаптация запросов (Вариант Б)")
    r_h2.font.size = Pt(13)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p2 = doc.add_paragraph()
    p2.paragraph_format.first_line_indent = Mm(12.5)
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.line_spacing = 1.15
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_p2 = p2.add_run("Формулировки запросов варианта Б перенесены в предметную область №9 следующим образом:")
    r_p2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    tasks = [
        (
            "Запрос Б1 (один-ко-многим):",
            " «Компьютер» и «Операционная система» связаны соотношением один-ко-многим. Выведите список всех связанных операционных систем и компьютеров, отсортированный по операционным системам (по наименованию ОС), сортировка по компьютерам произвольная."
        ),
        (
            "Запрос Б2 (один-ко-многим):",
            " «Компьютер» и «Операционная система» связаны соотношением один-ко-многим. Выведите список компьютеров с количеством операционных систем на каждом компьютере, отсортированный по количеству операционных систем (по убыванию)."
        ),
        (
            "Запрос Б3 (многие-ко-многим):",
            " «Компьютер» и «Операционная система» связаны соотношением многие-ко-многим. Выведите список всех операционных систем, у которых название заканчивается на «Linux» (адаптация условия варианта Б «фамилия заканчивается на «ов»» для предметной области с использованием метода str.endswith), и названия их компьютеров."
        )
    ]

    for title, text in tasks:
        p_task = doc.add_paragraph()
        p_task.paragraph_format.first_line_indent = Mm(12.5)
        p_task.paragraph_format.space_before = Pt(2)
        p_task.paragraph_format.space_after = Pt(4)
        p_task.paragraph_format.line_spacing = 1.15
        p_task.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_t = p_task.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11.5)
        r_t.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        r_d = p_task.add_run(text)
        r_d.font.size = Pt(11.5)
        r_d.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # ------------------ Раздел 3 ------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True
    r_h3 = h3.add_run("3. Исходный код программы (main.py)")
    r_h3.font.size = Pt(13)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Таблица-бокс для моноширинного кода
    code_table = doc.add_table(rows=1, cols=1)
    code_table.style = 'Table Grid'
    code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_code = code_table.rows[0].cells[0]
    cell_code.width = Mm(170)
    set_cell_background(cell_code, "FAFAFA")
    set_cell_margins(cell_code, top=120, bottom=120, left=140, right=140)

    p_code = cell_code.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.15
    run_code = p_code.add_run(code_text)
    run_code.font.name = 'Consolas'
    run_code.font.size = Pt(8.5)
    run_code.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # ------------------ Раздел 4 ------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)
    h4.paragraph_format.keep_with_next = True
    r_h4 = h4.add_run("4. Результаты выполнения программы")
    r_h4.font.size = Pt(13)
    r_h4.font.bold = True
    r_h4.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_out_desc = doc.add_paragraph()
    p_out_desc.paragraph_format.first_line_indent = Mm(12.5)
    p_out_desc.paragraph_format.space_before = Pt(2)
    p_out_desc.paragraph_format.space_after = Pt(4)
    r_out_desc = p_out_desc.add_run("Результаты выполнения программы при запуске интерпретатором Python:")
    r_out_desc.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Таблица-бокс для консольного вывода (светлый фон, чисто черный моноширинный шрифт)
    out_table = doc.add_table(rows=1, cols=1)
    out_table.style = 'Table Grid'
    out_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_out = out_table.rows[0].cells[0]
    cell_out.width = Mm(170)
    set_cell_background(cell_out, "F4F4F4")
    set_cell_margins(cell_out, top=120, bottom=120, left=140, right=140)

    p_out = cell_out.paragraphs[0]
    p_out.paragraph_format.space_before = Pt(0)
    p_out.paragraph_format.space_after = Pt(0)
    p_out.paragraph_format.line_spacing = 1.15
    run_out = p_out.add_run(output_text)
    run_out.font.name = 'Consolas'
    run_out.font.size = Pt(9)
    run_out.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # ------------------ Раздел 5 ------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)
    h5.paragraph_format.keep_with_next = True
    r_h5 = h5.add_run("5. Анализ и пояснения к решению")
    r_h5.font.size = Pt(13)
    r_h5.font.bold = True
    r_h5.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p5 = doc.add_paragraph()
    p5.paragraph_format.first_line_indent = Mm(12.5)
    p5.paragraph_format.space_before = Pt(2)
    p5.paragraph_format.space_after = Pt(4)
    p5.paragraph_format.line_spacing = 1.15
    p5.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_p5 = p5.add_run("В ходе разработки программы были использованы следующие возможности Python:")
    r_p5.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    points = [
        ("Генераторы списков (List Comprehensions): ", "использованы для моделирования реляционных операций соединения сущностей по ключам (one_to_many и many_to_many)."),
        ("Функция высшего порядка sorted и operator.itemgetter: ", "в запросе Б1 сортировка выполнена по наименованию ОС (индекс 0 кортежа), в запросе Б2 — по количеству ОС на компьютере (индекс 1) в порядке убывания (reverse=True)."),
        ("Функция высшего порядка filter и lambda-выражения: ", "применены для фильтрации связанных записей по компьютеру (Б2) и по операционной системе (Б3)."),
        ("Метод str.endswith(): ", "в запросе Б3 осуществлена фильтрация по окончанию наименования ОС, что семантически эквивалентно фильтрации фамилий на «ов».")
    ]

    for b_title, b_text in points:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.first_line_indent = Mm(12.5)
        p_pt.paragraph_format.space_before = Pt(2)
        p_pt.paragraph_format.space_after = Pt(2)
        p_pt.paragraph_format.line_spacing = 1.15
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_bullet = p_pt.add_run("• ")
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        r_bt = p_pt.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.size = Pt(11)
        r_bt.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        r_bdesc = p_pt.add_run(b_text)
        r_bdesc.font.size = Pt(11)
        r_bdesc.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    docx_path = os.path.join(script_dir, "РК1_Отчет_Вариант9_Б.docx")
    docx_latin_path = os.path.join(script_dir, "RK1_Report_Var9_B.docx")

    saved_files = []

    # Сохраняем файл с латинским именем
    doc.save(docx_latin_path)
    saved_files.append(docx_latin_path)

    # Пробуем сохранить основной файл, если он не заблокирован открытым Word
    try:
        doc.save(docx_path)
        saved_files.append(docx_path)
    except PermissionError:
        # Если открыт в Word, сохраняем рядом с суффиксом _new
        alt_path = os.path.join(script_dir, "РК1_Отчет_Вариант9_Б_обновленный.docx")
        doc.save(alt_path)
        saved_files.append(alt_path)

    print("DOCX успешно обновлен (черный текст, без титульника):")
    for f in saved_files:
        print(f" - {f} ({os.path.getsize(f)} байт)")

if __name__ == "__main__":
    create_report_docx()
