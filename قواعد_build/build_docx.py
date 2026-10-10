# -*- coding: utf-8 -*-
"""
يحوّل أجزاء الـMarkdown (part*.md) إلى ملف واحد .md وملف Word .docx باتجاه RTL كامل.
يدعم: # / ## / ### عناوين، - نقاط، 1. ترقيم، | جداول، **غامق**، فهرس يدوي، ترقيم صفحات.
"""
import re
import glob
import os
import datetime

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)
OUT_MD = os.path.join(ROOT, "قواعد_اسئلة_تخصص_اللغة_العربية.md")
OUT_DOCX = os.path.join(ROOT, "قواعد_اسئلة_تخصص_اللغة_العربية.docx")

PARTS = [
    "part00_intro.md", "part01_imla.md", "part02_aswat.md",
    "part03a_nahw.md", "part03b_nahw.md", "part04_sarf.md",
    "part05_balagha.md", "part06_arud.md", "part07_adab.md",
    "part08_moajam.md", "part09_tadrees.md", "part09b_shawahid.md", "part10_appendix.md",
]

BODY_FONT = "Arial"
HEAD_FONT = "Arial"
BODY_SIZE = 12
TABLE_SIZE = 10.5

H_COLORS = {1: RGBColor(0x7B, 0x1E, 0x1E), 2: RGBColor(0x1F, 0x3A, 0x6E), 3: RGBColor(0x2E, 0x5E, 0x2E)}
H_SIZES = {1: 20, 2: 16, 3: 13.5}


# ترتيب العناصر حسب مخطط OOXML حتى لا يعترض Word على الملف
RPR_AFTER_BCS = ("w:i", "w:iCs", "w:caps", "w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow",
                 "w:emboss", "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish", "w:webHidden", "w:color",
                 "w:spacing", "w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect",
                 "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang",
                 "w:eastAsianLayout", "w:specVanish", "w:oMath")
RPR_AFTER_SZCS = ("w:highlight", "w:u", "w:effect", "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl",
                  "w:cs", "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath")
RPR_AFTER_RTL = ("w:cs", "w:em", "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath")
PPR_AFTER_BIDI = ("w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing",
                  "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
                  "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
PPR_AFTER_NUMPR = ("w:suppressLineNumbers", "w:pBdr", "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
                   "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
                   "w:bidi") + PPR_AFTER_BIDI
TBLPR_AFTER_BIDIVISUAL = ("w:tblStyleRowBandSize", "w:tblStyleColBandSize", "w:tblW", "w:jc", "w:tblCellSpacing",
                          "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
                          "w:tblCaption", "w:tblDescription", "w:tblPrChange")


# ---------- helpers: RTL / fonts ----------
def set_run_font(run, name=BODY_FONT, size=BODY_SIZE, bold=None, color=None, italic=None):
    run.font.name = name
    run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), name)
    # complex-script size + rtl + bold
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs")
        rPr.insert_element_before(szCs, *RPR_AFTER_SZCS)
    szCs.set(qn("w:val"), str(int(size * 2)))
    if bold:
        bCs = rPr.find(qn("w:bCs"))
        if bCs is None:
            bCs = OxmlElement("w:bCs")
            rPr.insert_element_before(bCs, *RPR_AFTER_BCS)
    rtl = rPr.find(qn("w:rtl"))
    if rtl is None:
        rtl = OxmlElement("w:rtl")
        rPr.insert_element_before(rtl, *RPR_AFTER_RTL)
    lang = rPr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rPr.insert_element_before(lang, "w:eastAsianLayout", "w:specVanish", "w:oMath")
    lang.set(qn("w:bidi"), "ar-EG")


def set_paragraph_rtl(p, align=WD_ALIGN_PARAGRAPH.RIGHT):
    pPr = p._p.get_or_add_pPr()
    bidi = pPr.find(qn("w:bidi"))
    if bidi is None:
        bidi = OxmlElement("w:bidi")
        pPr.insert_element_before(bidi, *PPR_AFTER_BIDI)
    bidi.set(qn("w:val"), "1")
    # في الفقرات ذات الاتجاه RTL تكون المحاذاة الافتراضية (start) هي اليمين؛
    # لذا لا نكتب jc=right صراحةً (لأن Word يفسّر left/right في فقرات bidi على أنها start/end)
    if align == WD_ALIGN_PARAGRAPH.RIGHT:
        jc = pPr.find(qn("w:jc"))
        if jc is not None:
            pPr.remove(jc)
    else:
        p.alignment = align


INLINE_RE = re.compile(r"(\*\*.+?\*\*)")


def add_inline(p, text, size=BODY_SIZE, base_bold=False, color=None):
    """يضيف النص مع دعم **غامق**."""
    parts = INLINE_RE.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            run = p.add_run(part[2:-2])
            set_run_font(run, size=size, bold=True, color=color)
        else:
            run = p.add_run(part)
            set_run_font(run, size=size, bold=True if base_bold else None, color=color)


def add_body_paragraph(doc, text, style=None, space_after=6, first_indent=None):
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.JUSTIFY if len(text) > 80 else WD_ALIGN_PARAGRAPH.RIGHT)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    add_inline(p, text)
    return p


def add_heading(doc, text, level, page_break=False):
    style = {1: "Heading 1", 2: "Heading 2", 3: "Heading 3"}[level]
    p = doc.add_paragraph(style=style)
    if page_break:
        p.paragraph_format.page_break_before = True
    set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.RIGHT)
    p.paragraph_format.space_before = Pt(18 if level == 1 else 12)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    clean = text.replace("**", "")
    run = p.add_run(clean)
    set_run_font(run, name=HEAD_FONT, size=H_SIZES[level], bold=True, color=H_COLORS[level])
    return p


# ---------- numbering (restartable numbered lists) ----------
class Numbering:
    def __init__(self, doc):
        self.doc = doc
        self.numbering = doc.part.numbering_part.element
        style = doc.styles["List Number"]
        numId = style.element.pPr.numPr.numId.val
        self.abstract_id = None
        for num in self.numbering.findall(qn("w:num")):
            if num.get(qn("w:numId")) == str(numId):
                self.abstract_id = num.find(qn("w:abstractNumId")).get(qn("w:val"))
                break
        # make the abstract numbering RTL-friendly: ensure level 0 uses "%1." format
        self.current = None

    def new_list(self):
        ids = [int(n.get(qn("w:numId"))) for n in self.numbering.findall(qn("w:num"))]
        new_id = max(ids) + 1 if ids else 1
        num = OxmlElement("w:num")
        num.set(qn("w:numId"), str(new_id))
        an = OxmlElement("w:abstractNumId")
        an.set(qn("w:val"), str(self.abstract_id))
        num.append(an)
        ov = OxmlElement("w:lvlOverride")
        ov.set(qn("w:ilvl"), "0")
        so = OxmlElement("w:startOverride")
        so.set(qn("w:val"), "1")
        ov.append(so)
        num.append(ov)
        self.numbering.insert_element_before(num, "w:numIdMacAtCleanup")
        self.current = new_id
        return new_id

    def apply(self, p, num_id):
        pPr = p._p.get_or_add_pPr()
        numPr = pPr.find(qn("w:numPr"))
        if numPr is None:
            numPr = OxmlElement("w:numPr")
            pPr.insert_element_before(numPr, *PPR_AFTER_NUMPR)
        for child in list(numPr):
            numPr.remove(child)
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        nid = OxmlElement("w:numId")
        nid.set(qn("w:val"), str(num_id))
        numPr.append(ilvl)
        numPr.append(nid)


# ---------- tables ----------
def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def set_table_rtl(table):
    tblPr = table._tbl.tblPr
    bidi = OxmlElement("w:bidiVisual")
    tblPr.insert_element_before(bidi, *TBLPR_AFTER_BIDIVISUAL)
    # full width
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), "5000")
    tblW.set(qn("w:type"), "pct")


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip() != "") and any(cells)


def add_table(doc, rows):
    rows = [split_row(r) for r in rows]
    rows = [r for r in rows if not is_separator_row(r)]
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_rtl(table)
    for i, r in enumerate(rows):
        for j in range(ncols):
            text = r[j] if j < len(r) else ""
            cell = table.cell(i, j)
            p = cell.paragraphs[0]
            set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.RIGHT)
            p.paragraph_format.space_after = Pt(2)
            add_inline(p, text, size=TABLE_SIZE, base_bold=(i == 0))
            if i == 0:
                shade_cell(cell, "D9E2F3")
            elif i % 2 == 0:
                shade_cell(cell, "F5F7FA")
    # repeat header row
    trPr = table.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    spacer = doc.add_paragraph()
    set_paragraph_rtl(spacer, WD_ALIGN_PARAGRAPH.RIGHT)
    spacer.paragraph_format.space_after = Pt(2)


# ---------- footer page numbers ----------
def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.CENTER)
    run = p.add_run("صفحة ")
    set_run_font(run, size=10)
    r = p.add_run()
    set_run_font(r, size=10)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t")
    t.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr, fld_sep, t, fld_end):
        r._r.append(el)


# ---------- document defaults ----------
def setup_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = section.right_margin = Cm(2.2)
    section.top_margin = section.bottom_margin = Cm(2.0)
    # default rtl for the section
    sectPr = section._sectPr
    bidi = OxmlElement("w:bidi")
    sectPr.insert_element_before(bidi, "w:rtlGutter", "w:docGrid", "w:printerSettings", "w:sectPrChange")

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(BODY_SIZE)
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), BODY_FONT)
    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), str(BODY_SIZE * 2))
    rPr.insert_element_before(szCs, *RPR_AFTER_SZCS)
    pPr = normal.element.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    pPr.insert_element_before(b, *PPR_AFTER_BIDI)

    for lvl in (1, 2, 3):
        st = doc.styles["Heading %d" % lvl]
        st.font.name = HEAD_FONT
        st.font.bold = True
        st.font.color.rgb = H_COLORS[lvl]
        st.font.size = Pt(H_SIZES[lvl])
        rPr = st.element.get_or_add_rPr()
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.insert(0, rFonts)
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rFonts.set(qn(attr), HEAD_FONT)
        # remove theme font attributes that override explicit fonts
        for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rFonts.get(qn(attr)) is not None:
                del rFonts.attrib[qn(attr)]
    for stname in ("List Bullet", "List Number"):
        st = doc.styles[stname]
        st.font.name = BODY_FONT
        st.font.size = Pt(BODY_SIZE)
    add_page_number_footer(section)


# ---------- markdown parsing ----------
def read_all_parts():
    chunks = []
    for name in PARTS:
        path = os.path.join(BUILD_DIR, name)
        with open(path, encoding="utf-8") as f:
            chunks.append(f.read().strip("\n"))
    return "\n\n".join(chunks) + "\n"


def collect_headings(md_text):
    heads = []
    for line in md_text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            heads.append((len(m.group(1)), m.group(2).replace("**", "").strip()))
    return heads


def build_docx(md_text):
    doc = Document()
    setup_document(doc)
    numbering = Numbering(doc)

    lines = md_text.splitlines()
    headings = collect_headings(md_text)

    # ----- title page -----
    first_title = headings[0][1] if headings else "القواعد"
    tp = doc.add_paragraph()
    set_paragraph_rtl(tp, WD_ALIGN_PARAGRAPH.CENTER)
    tp.paragraph_format.space_before = Pt(120)
    tp.paragraph_format.space_after = Pt(24)
    r = tp.add_run(first_title)
    set_run_font(r, name=HEAD_FONT, size=26, bold=True, color=H_COLORS[1])

    sp = doc.add_paragraph()
    set_paragraph_rtl(sp, WD_ALIGN_PARAGRAPH.CENTER)
    sp.paragraph_format.space_after = Pt(12)
    r = sp.add_run("مستخرج من: تجميعة كافة أسئلة تخصص اللغة العربية (بنك الـ360 سؤالًا + تسريبات + نهائي المراجعة + أسئلة الوزارة)")
    set_run_font(r, size=13, bold=False, color=RGBColor(0x40, 0x40, 0x40))

    sp2 = doc.add_paragraph()
    set_paragraph_rtl(sp2, WD_ALIGN_PARAGRAPH.CENTER)
    r = sp2.add_run("إملاء ـ أصوات ـ نحو ـ صرف ـ بلاغة ـ عروض ـ أدب ونقد ـ معاجم ومفردات ـ طرق تدريس")
    set_run_font(r, size=12, color=RGBColor(0x40, 0x40, 0x40))

    sp3 = doc.add_paragraph()
    set_paragraph_rtl(sp3, WD_ALIGN_PARAGRAPH.CENTER)
    sp3.paragraph_format.space_before = Pt(36)
    r = sp3.add_run(datetime.date.today().strftime("%Y/%m/%d"))
    set_run_font(r, size=11, color=RGBColor(0x60, 0x60, 0x60))

    # ----- TOC -----
    toc_h = doc.add_paragraph()
    toc_h.paragraph_format.page_break_before = True
    set_paragraph_rtl(toc_h, WD_ALIGN_PARAGRAPH.RIGHT)
    r = toc_h.add_run("فهرس المحتويات")
    set_run_font(r, name=HEAD_FONT, size=20, bold=True, color=H_COLORS[1])
    toc_h.paragraph_format.space_after = Pt(12)
    for lvl, text in headings[1:]:
        if lvl > 2:
            continue
        p = doc.add_paragraph()
        set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.RIGHT)
        p.paragraph_format.space_after = Pt(2 if lvl == 2 else 6)
        p.paragraph_format.space_before = Pt(8 if lvl == 1 else 0)
        if lvl == 2:
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.right_indent = Cm(1.0)
        r = p.add_run(text)
        set_run_font(r, size=12 if lvl == 1 else 11, bold=(lvl == 1),
                     color=H_COLORS[1] if lvl == 1 else RGBColor(0x20, 0x20, 0x20))

    # ----- body -----
    i = 0
    n = len(lines)
    seen_h1 = 0
    para_buf = []
    in_numbered = False
    current_num = None

    def flush_para():
        nonlocal para_buf
        if para_buf:
            text = " ".join(s.strip() for s in para_buf)
            add_body_paragraph(doc, text)
            para_buf = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            in_numbered = False
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if m:
            flush_para()
            in_numbered = False
            lvl = len(m.group(1))
            text = m.group(2)
            if lvl == 1:
                seen_h1 += 1
                if seen_h1 == 1:
                    # the document title: already on the title page; skip as heading
                    i += 1
                    continue
                add_heading(doc, text, 1, page_break=True)
            else:
                add_heading(doc, text, lvl)
            i += 1
            continue

        if stripped.startswith("|"):
            flush_para()
            in_numbered = False
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            add_table(doc, rows)
            continue

        mb = re.match(r"^[-•]\s+(.*)$", stripped)
        if mb:
            flush_para()
            in_numbered = False
            p = doc.add_paragraph(style="List Bullet")
            set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.JUSTIFY if len(mb.group(1)) > 80 else WD_ALIGN_PARAGRAPH.RIGHT)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, mb.group(1))
            i += 1
            continue

        mn = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if mn:
            flush_para()
            if not in_numbered:
                current_num = numbering.new_list()
                in_numbered = True
            p = doc.add_paragraph(style="List Number")
            numbering.apply(p, current_num)
            set_paragraph_rtl(p, WD_ALIGN_PARAGRAPH.JUSTIFY if len(mn.group(2)) > 80 else WD_ALIGN_PARAGRAPH.RIGHT)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, mn.group(2))
            i += 1
            continue

        if stripped.startswith("---"):
            flush_para()
            i += 1
            continue

        # ordinary text (accumulate consecutive lines into one paragraph)
        in_numbered = False
        para_buf.append(stripped)
        i += 1

    flush_para()
    return doc


def main():
    md_text = read_all_parts()
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md_text)
    doc = build_docx(md_text)
    doc.save(OUT_DOCX)
    print("written:", OUT_MD, len(md_text), "chars")
    print("written:", OUT_DOCX, os.path.getsize(OUT_DOCX), "bytes")


if __name__ == "__main__":
    main()
