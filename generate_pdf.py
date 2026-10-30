import subprocess
import os
import sys

def build_pdf():
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

    # Заменяем спецсимволы HTML для безопасного отображения кода
    def escape_html(text):
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    escaped_code = escape_html(code_text)
    escaped_output = escape_html(output_text)

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Отчет по рубежному контролю №1 — Вариант 9-Б</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
        @bottom-right {{
            content: "Стр. " counter(page);
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
        }}
    }}
    body {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 12pt;
        line-height: 1.35;
        color: #111;
        margin: 0;
        padding: 0;
    }}
    .header-box {{
        text-align: center;
        font-size: 11pt;
        line-height: 1.25;
        margin-bottom: 18px;
        border-bottom: 2px solid #2b4c7e;
        padding-bottom: 10px;
    }}
    .header-box .univ {{
        font-weight: bold;
        text-transform: uppercase;
        font-size: 11pt;
    }}
    h1 {{
        font-size: 15pt;
        text-align: center;
        margin-top: 14px;
        margin-bottom: 12px;
        text-transform: uppercase;
        color: #2b4c7e;
    }}
    h2 {{
        font-size: 13pt;
        color: #2b4c7e;
        margin-top: 16px;
        margin-bottom: 8px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 3px;
        page-break-after: avoid;
        break-after: avoid;
    }}
    h3 {{
        font-size: 12pt;
        margin-top: 10px;
        margin-bottom: 4px;
        page-break-after: avoid;
        break-after: avoid;
    }}
    p {{
        margin-top: 5px;
        margin-bottom: 5px;
        text-indent: 1.25cm;
        text-align: justify;
    }}
    p.no-indent {{
        text-indent: 0;
    }}
    .meta-table {{
        width: 100%;
        margin: 12px 0 16px 0;
        border-collapse: collapse;
        font-size: 11.5pt;
    }}
    .meta-table td {{
        border: none;
        padding: 4px 8px;
    }}
    .meta-table td.label {{
        width: 32%;
        font-weight: bold;
        color: #333;
    }}
    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 14px 0;
        font-size: 10.5pt;
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    table.data-table th, table.data-table td {{
        border: 1px solid #777;
        padding: 5px 8px;
        text-align: left;
    }}
    table.data-table th {{
        background-color: #eaeff5;
        font-weight: bold;
        color: #2b4c7e;
    }}
    pre {{
        background-color: #f7f9fb;
        border: 1px solid #d0d7de;
        border-left: 3px solid #2b4c7e;
        border-radius: 4px;
        padding: 10px 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.22;
        white-space: pre-wrap;
        word-wrap: break-word;
        page-break-inside: auto;
    }}
    .output-box {{
        background-color: #1e242c;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.28;
        white-space: pre-wrap;
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    ul, ol {{
        margin-top: 4px;
        margin-bottom: 6px;
        padding-left: 2cm;
    }}
    li {{
        margin-bottom: 2px;
    }}
    .highlight-task {{
        background-color: #f3f6f9;
        border-left: 4px solid #2b4c7e;
        padding: 6px 12px;
        margin: 8px 0;
        font-size: 11pt;
    }}
    .code-comment {{
        color: #57606a;
    }}
</style>
</head>
<body>

<div class="header-box">
    <div class="univ">Московский государственный технический университет имени Н.Э. Баумана</div>
    <div>(национальный исследовательский университет)</div>
    <div style="margin-top: 4px;">Факультет «Информатика и системы управления» | Кафедра «Программная инженерия» (ИУ7)</div>
    <div>Дисциплина: «Программирование и конструирование языков программирования» (ПиК ЯП)</div>
</div>

<h1>Отчет по рубежному контролю №1</h1>
<p style="text-align: center; text-indent: 0; font-size: 12.5pt; font-weight: bold; margin-bottom: 14px;">
    Разработка программ на языке Python с использованием функционального стиля
</p>

<table class="meta-table">
    <tr>
        <td class="label">Студент:</td>
        <td>___________________________________</td>
    </tr>
    <tr>
        <td class="label">Учебная группа:</td>
        <td>___________________________________</td>
    </tr>
    <tr>
        <td class="label">Вариант предметной области:</td>
        <td><strong>№ 9 («Операционная система» — «Компьютер»)</strong></td>
    </tr>
    <tr>
        <td class="label">Вариант запросов:</td>
        <td><strong>Вариант Б</strong></td>
    </tr>
</table>

<h2>1. Описание классов данных предметной области</h2>
<p>
В соответствии с условиями рубежного контроля (вариант предметной области №9) разработаны классы данных, представляющие сущности «Операционная система» (сторона отношения «многие») и «Компьютер» (сторона отношения «один»), а также ассоциативный класс для отношения «многие-ко-многим».
</p>

<table class="data-table">
    <thead>
        <tr>
            <th style="width: 20%;">Класс</th>
            <th style="width: 32%;">Поля класса</th>
            <th style="width: 48%;">Назначение и связь</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>OS</strong><br>(Операционная система)</td>
            <td>
                <code>id</code> (int)<br>
                <code>name</code> (str)<br>
                <code>price</code> (int/float)<br>
                <code>comp_id</code> (int)
            </td>
            <td>
                Сущность на стороне связи «многие» (аналог «Сотрудник»). Содержит количественный признак <code>price</code> (стоимость лицензии) и внешний ключ <code>comp_id</code> для связи один-ко-многим с компьютером.
            </td>
        </tr>
        <tr>
            <td><strong>Comp</strong><br>(Компьютер)</td>
            <td>
                <code>id</code> (int)<br>
                <code>name</code> (str)
            </td>
            <td>
                Сущность на стороне связи «один» (аналог «Отдел»). Представляет собой рабочий компьютер или сервер организации.
            </td>
        </tr>
        <tr>
            <td><strong>OSComp</strong><br>(Связь ОС и Компьютеров)</td>
            <td>
                <code>comp_id</code> (int)<br>
                <code>os_id</code> (int)
            </td>
            <td>
                Таблица/класс связки для реализации отношения «многие-ко-многим». Отражает установку нескольких ОС на различных компьютерах.
            </td>
        </tr>
    </tbody>
</table>

<h2>2. Постановка и адаптация запросов (Вариант Б)</h2>
<p>
Запросы из варианта Б перенесены в предметную область №9 с сохранением логических критериев и функциональных требований:
</p>

<div class="highlight-task">
    <strong>Запрос Б1 (один-ко-многим):</strong> «Компьютер» и «Операционная система» связаны соотношением один-ко-многим. Выведите список всех связанных операционных систем и компьютеров, отсортированный по операционным системам (по названию ОС), сортировка по компьютерам произвольная.
</div>

<div class="highlight-task">
    <strong>Запрос Б2 (один-ко-многим):</strong> «Компьютер» и «Операционная система» связаны соотношением один-ко-многим. Выведите список компьютеров с количеством операционных систем на каждом компьютере, отсортированный по количеству операционных систем (по убыванию).
</div>

<div class="highlight-task">
    <strong>Запрос Б3 (многие-ко-многим):</strong> «Компьютер» и «Операционная система» связаны соотношением многие-ко-многим. Выведите список всех операционных систем, у которых название заканчивается на «Linux» (адаптация критерия варианта Б <em>«фамилия заканчивается на «ов»»</em> для предметной области с использованием метода <code>str.endswith</code>), и названия их компьютеров.
</div>

<h2>3. Исходный код программы (main.py)</h2>
<pre><code>{escaped_code}</code></pre>

<h2>4. Результаты выполнения программы</h2>
<p class="no-indent">
Результаты выполнения программы, полученные при запуске интерпретатором Python:
</p>

<div class="output-box">{escaped_output}</div>

<h2>5. Краткие выводы и пояснения</h2>
<p>
При выполнении рубежного контроля решены все поставленные задачи:
</p>
<ol>
    <li>Созданы классы данных <code>OS</code>, <code>Comp</code> и <code>OSComp</code> в строгом соответствии с предметной областью №9 («Операционная система» — «Компьютер»). В класс <code>OS</code> включен количественный признак <code>price</code> (стоимость лицензии), а также внешний ключ <code>comp_id</code>.</li>
    <li>Сформированы тестовые наборы данных, содержащие 5 компьютеров, 6 операционных систем и 10 связей многие-ко-многим, гарантирующие полноту и корректность проверки всех трех запросов.</li>
    <li>Для формирования связей один-ко-многим и многие-ко-многим применены списковые включения (<em>list comprehensions</em>), моделирующие реляционные операции соединения таблиц.</li>
    <li>В запросах активно использованы функциональные возможности Python:
        <ul>
            <li>встроенная функция <code>sorted()</code> с извлечением ключа через <code>operator.itemgetter</code>;</li>
            <li>функция высшего порядка <code>filter()</code> в связке с анонимными функциями <code>lambda</code>;</li>
            <li>метод <code>str.endswith()</code> для эффективной строковой фильтрации.</li>
        </ul>
    </li>
</ol>

</body>
</html>
"""

    html_path = os.path.join(script_dir, "report.html")
    pdf_path = os.path.join(script_dir, "РК1_Отчет_Вариант9_Б.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)

    print(f"PDF успешно сгенерирован: {pdf_path}")
    print(f"Размер: {os.path.getsize(pdf_path)} байт")

if __name__ == "__main__":
    build_pdf()
