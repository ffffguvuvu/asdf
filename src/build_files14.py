# -*- coding: utf-8 -*-
"""يبني ملفًّا واحدًا يجمع أسئلة ملفّات مجلّد «تخصص عربي» الأربعة عشر على منصّة اجتاز."""
import html, importlib, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(os.path.dirname(HERE), "egtaz-14-files-questions.html")
FOLDER = "1YvqHviSNCHqECMZ0aslM0tJ5_1oKYnn3"

def esc(t): return html.escape(str(t), quote=True)

AD = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
def ad(n): return str(n).translate(AD)

# ───────────────────────── الملفّات الأربعة عشر كما هي في المجلّد ─────────────────────────
# st: ok | part | no    —    mods: وحدات الأسئلة المنسوبة لهذا الملفّ
FILES = [
 dict(n="٣٦٠ سؤال في اللغة العربية", i="15dEHc1YLM7Bq96LdyuySg_8ikaIkN5d6",
      st="part", mods=["egtaz.data_f360"],
      how="رفض خمس عشرة صيغة رابط نصّيّ، ثم فُتح أخيرًا بتحويل صفحاته إلى صور.",
      note="اختيار من متعدّد بأربعة بدائل، نحوٌ وإملاءٌ وبلاغةٌ وأدب. بلغ السحب الصفحة الثانية والعشرين من نحو ثلاثين. ومن الحادية عشرة يتغيّر طابع الملفّ إلى قطع فهمٍ طويلة."),

 dict(n="أحدث أسئلة الحاسب الآلي — الجزء الثاني", i="1WXhwsTz_HawAXCwNIwhG50i0j3Sc3Typ",
      st="no", mods=[],
      how="لم يُفتح بعد.",
      note="ليس من تخصّص اللغة العربية أصلًا — حاسبٌ آليّ، وُضع في المجلّد سهوًا على ما يبدو."),

 dict(n="أسئلة تخصص لغة عربية لمسابقة وزارة التربية والتعليم — ١", i="1tg6bYgQwUfNqwbCWZWNQdypV_RGK5zl4",
      st="ok", mods=[],
      how="قُرئ نصًّا.", shared=True,
      note="مادّته داخلة في البنك المجمَّع أدناه (نحو وصرف وبلاغة)."),

 dict(n="أسئلة معلم فصل", i="1nP8OhffpeTur5QW3zkPjh4TBlfA7wGQL",
      st="no", mods=[],
      how="لم يُفتح بعد.",
      note="تخصّص معلم فصل لا لغة عربية، ومادّته تربويّة في الأغلب."),

 dict(n="أساسيات في قواعد الإملاء", i="1E5f9rmWstEZvsLPcXW9T06DVATqiqMas",
      st="ok", mods=["egtaz.data_imla"],
      how="قُرئ نصًّا بالكامل.",
      note="هو الأصل الذي بُني عليه باب الإملاء والرسم."),

 dict(n="الأسئلة التي وردت لتخصص اللغة العربية — نهائي، مراجعة ما قبل الامتحان",
      i="1xzABhOKXn_d-3Et4Q_2uRY2bBd5yKeU8",
      st="ok", mods=["egtaz.data_ex2"],
      how="قُرئ نصًّا بالكامل.",
      note="غالبه شواهد ونصوص يُسأل عن وجه الاستشهاد فيها."),

 dict(n="اللغة العربية تخصص للجميع", i="1W4laM6dZ6iAde1gDU1jU2EWRXkb0lxFi",
      st="ok", mods=[], shared=True,
      how="قُرئ نصًّا.",
      note="مادّته داخلة في البنك المجمَّع أدناه (بلاغة وأدب ودلالة)."),

 dict(n="تسريبات الحسام في العربية (خاص بتخصص اللغة العربية)", i="1bVTEI5MthfwqOfmRPHO9Axtkv3nixq7i",
      st="part", mods=[],
      how="خطُّه مكسور الترميز؛ فُكّ بتصوير الصفحات بعد أن ثبت استحالة فكّ الشفرة.",
      note="هو الملفّ التالي نفسه حرفًا بحرف — نسختان لمستندٍ واحد. أسئلته في البطاقة التالية."),

 dict(n="تسريبات الحسام في اللغة العربية (خاص بتخصص اللغة العربية)", i="1q5gtVzy-OH_HwOAkHGaqI8HzAKWuIpwG",
      st="part", mods=["egtaz.data_hsam"],
      how="فُكّ بتصوير الصفحات. قُرئت ثلاث صفحات من نحو مئة.",
      note="بطاقات قصيرة: مسألة ← سهم ← جوابها بلا شرح. والتعليل هنا مضافٌ من كتب الفنّ."),

 dict(n="تسريبات الحسام في اللغة العربية (عربي عام — جميع التخصصات)", i="1_WddWQE9PHILx0uTG8bS82_Zp2S5Tihm",
      st="ok", mods=["egtaz.data_ex3"],
      how="قُرئ نصًّا بالكامل — تسعٌ وعشرون صفحة.",
      note="المفاعيل والحال والتمييز، جمعا السلامة والمثنّى، النواسخ، الهمزات، علامات الترقيم."),

 dict(n="تسريبات الحسام — أحدث الأسئلة التي وردت في تخصص اللغة العربية ٣",
      i="1H-UcQJVnUwi99rLqYdkslart2SiCnVU4",
      st="ok", mods=["egtaz.data_ex1"],
      how="قُرئ نصًّا بالكامل.",
      note="أجود ملفّات المجلّد وأكثرها تركيزًا على المتكرِّر في الامتحانات."),

 dict(n="طرق تدريس اللغة العربية — ١", i="1mdA95NQHaND5OWk7idNx2HJD0pGdK1mN",
      st="ok", mods=[], shared=True,
      how="نسخة مكرّرة من الملفّ التالي.",
      note="لا مادّة زائدة فيه؛ أسئلته هي أسئلة «طرق تدريس اللغة العربية» نفسها."),

 dict(n="طرق تدريس اللغة العربية", i="1LYDW8xOVjcOmEmRYUUWhsoJi4DLLJ2hq",
      st="ok", mods=["egtaz.data_turuq"],
      how="قُرئ نصًّا بالكامل.",
      note="الطرائق والكفايات والتقويم وأساليب تدريس الفروع."),

 dict(n="مراجعة ما قبل الامتحان — أحدث أسئلة وردت بالفعل في اختبارات تخصص اللغة",
      i="1sj1Z16W6qT74AyrUHyh03Nj_wRy3mvDi",
      st="ok", mods=["egtaz.data_ex4"],
      how="قُرئ نصًّا.",
      note="مراجعة سريعة مركّزة، وفيها نصيبٌ وافر من آيات القرآن وتوجيهها."),
]

# البنك المجمَّع: مادّةٌ تواترت في عدّة ملفّات فلم يصحّ نسبتها إلى ملفٍّ بعينه
SHARED = [
 ("egtaz.data_nahw",  "النحو"),
 ("egtaz.data_sarf",  "الصرف والاشتقاق"),
 ("egtaz.data_bala",  "البلاغة"),
 ("egtaz.data_arud",  "العروض والقافية"),
 ("egtaz.data_adab",  "الأدب والنقد"),
 ("egtaz.data_lugha", "الأصوات والمعاجم والدلالة"),
 ("egtaz.data_mansa", "من دروس المنصّة نفسها (لا من الملفّات)"),
]

def load(mod):
    M = importlib.import_module(mod)
    out = []
    for t in M.QS:
        q, a, e = t[0], t[1], t[2]
        opts = list(t[3]) if len(t) > 3 else []
        out.append(dict(q=q, a=a, e=e, o=opts))
    return out

# ───────────────────────── التجميع ─────────────────────────
groups = []          # [(عنوان, وصف, [أسئلة])]
n_files_q = 0
for f in FILES:
    qs = []
    for m in f["mods"]:
        qs += load(m)
    f["_qs"] = qs
    n_files_q += len(qs)

shared_groups = []
for mod, title in SHARED:
    shared_groups.append((title, load(mod)))
n_shared_q = sum(len(q) for _, q in shared_groups)

TOTAL = n_files_q + n_shared_q
ST_LBL = {"ok": "مقروء", "part": "مقروء جزئيًّا", "no": "لم يُفتح"}

# ───────────────────────── البناء ─────────────────────────
def q_html(idx, it):
    o = ""
    if it["o"]:
        alls = [it["a"]] + it["o"]
        o = '<ul class="opts">' + "".join(
            f'<li class="{"c" if x == it["a"] else ""}">{esc(x)}</li>' for x in alls) + "</ul>"
    return (f'<li class="q"><div class="qt">{esc(it["q"])}</div>{o}'
            f'<div class="ans"><b>الإجابة:</b> {esc(it["a"])}</div>'
            f'<div class="exp">{esc(it["e"])}</div></li>')

rows = []
for k, f in enumerate(FILES, 1):
    cnt = len(f["_qs"])
    badge = f'<span class="st {f["st"]}">{ST_LBL[f["st"]]}</span>'
    num = f'{ad(cnt)} سؤال' if cnt else ("ضمن المجمَّع" if f.get("shared") else "—")
    rows.append(f'<tr><td class="k">{ad(k)}</td><td class="nm">{esc(f["n"])}</td>'
                f'<td>{badge}</td><td class="c">{num}</td></tr>')

secs = []
for k, f in enumerate(FILES, 1):
    if not f["_qs"]:
        secs.append(
            f'<section class="file empty" id="f{k}"><h2>{ad(k)}· {esc(f["n"])}</h2>'
            f'<p class="meta"><span class="st {f["st"]}">{ST_LBL[f["st"]]}</span> '
            f'{esc(f["how"])}</p><p class="note">{esc(f["note"])}</p></section>')
        continue
    items = "".join(q_html(i, it) for i, it in enumerate(f["_qs"], 1))
    secs.append(
        f'<section class="file" id="f{k}"><h2>{ad(k)}· {esc(f["n"])}</h2>'
        f'<p class="meta"><span class="st {f["st"]}">{ST_LBL[f["st"]]}</span> '
        f'{esc(f["how"])} &nbsp;·&nbsp; <b>{ad(len(f["_qs"]))}</b> سؤالًا</p>'
        f'<p class="note">{esc(f["note"])}</p><ol class="qs">{items}</ol></section>')

shared_secs = []
for title, qs in shared_groups:
    items = "".join(q_html(i, it) for i, it in enumerate(qs, 1))
    shared_secs.append(
        f'<section class="file"><h2>{esc(title)}</h2>'
        f'<p class="meta"><b>{ad(len(qs))}</b> سؤالًا</p><ol class="qs">{items}</ol></section>')

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f6f7f9;color:#17202a;font:16px/1.85 "Noto Naskh Arabic","Amiri",
 "Times New Roman",serif;direction:rtl}
.wrap{max-width:1000px;margin:0 auto;padding:26px 18px 90px}
header{background:#0f2d3f;color:#fff;padding:30px 18px;text-align:center}
header h1{margin:0 0 6px;font-size:28px}
header p{margin:0;opacity:.85;font-size:15px}
.kpis{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:16px}
.kpi{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);
 border-radius:10px;padding:7px 14px;font-size:14px}
.kpi b{font-size:19px;display:block}
.card{background:#fff;border:1px solid #dfe4ea;border-radius:12px;padding:18px 20px;margin:18px 0}
h2{font-size:21px;margin:0 0 8px;color:#0f2d3f;border-bottom:2px solid #e6eaef;padding-bottom:8px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th,td{padding:8px 10px;border-bottom:1px solid #eceff3;text-align:right;vertical-align:top}
th{background:#f0f3f6;font-size:13.5px}
td.k{color:#8795a4;width:34px}
td.c{white-space:nowrap;color:#4a5a69}
.nm{font-weight:600}
.st{display:inline-block;border-radius:20px;padding:2px 11px;font-size:12.5px;white-space:nowrap}
.st.ok{background:#e3f5e9;color:#1a7a43;border:1px solid #bfe6cf}
.st.part{background:#fff6e0;color:#9a6b00;border:1px solid #f0dfae}
.st.no{background:#fdeaea;color:#a32222;border:1px solid #f3c9c9}
.toolbar{position:sticky;top:0;z-index:5;background:#f6f7f9;padding:12px 0;margin-bottom:4px}
#search{width:100%;padding:11px 14px;border:1px solid #cfd6de;border-radius:10px;
 font:inherit;font-size:15px;background:#fff}
section.file{background:#fff;border:1px solid #dfe4ea;border-radius:12px;
 padding:18px 20px;margin:16px 0}
section.file.empty{opacity:.82;background:#fbfcfd}
.meta{margin:0 0 4px;font-size:14px;color:#4a5a69}
.note{margin:0 0 12px;font-size:14px;color:#6b7a89;border-right:3px solid #e6eaef;padding-right:10px}
ol.qs{margin:0;padding:0 22px 0 0}
li.q{margin:0 0 15px;padding:0 0 13px;border-bottom:1px dashed #e8ecf1}
li.q:last-child{border-bottom:0;margin-bottom:0}
.qt{font-weight:600;color:#14212c}
ul.opts{list-style:none;margin:7px 0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
ul.opts li{border:1px solid #dfe4ea;border-radius:8px;padding:3px 11px;font-size:14.5px;background:#fafbfc}
ul.opts li.c{background:#e3f5e9;border-color:#bfe6cf;color:#1a7a43;font-weight:600}
.ans{margin-top:5px;color:#1a7a43;font-size:15px}
.exp{margin-top:3px;color:#53616f;font-size:14.5px}
.hide{display:none!important}
.lead{font-size:15px;color:#3d4c5a;margin:0 0 10px}
footer{text-align:center;color:#8795a4;font-size:13px;padding:26px 14px 40px}
@media print{body{background:#fff}.toolbar{display:none}
 section.file,.card{break-inside:auto;border-color:#ccc}header{background:#fff;color:#000}}
"""

JS = """
var box=document.getElementById('search');
var secs=[].slice.call(document.querySelectorAll('section.file'));
var hint=document.getElementById('hint');
function nrm(s){return s.replace(/[\\u064B-\\u0652\\u0670]/g,'')
 .replace(/[\\u0622\\u0623\\u0625\\u0671]/g,'\\u0627')
 .replace(/\\u0649/g,'\\u064A').replace(/\\u0629/g,'\\u0647')
 .replace(/\\s+/g,' ').trim();}
box.addEventListener('input',function(){
  var t=nrm(box.value); var shown=0,total=0;
  secs.forEach(function(s){
    var any=false;
    [].slice.call(s.querySelectorAll('li.q')).forEach(function(q){
      total++;
      var hit = !t || nrm(q.textContent).indexOf(t)>-1;
      q.classList.toggle('hide',!hit); if(hit){any=true;shown++;}
    });
    if(!s.querySelector('li.q')) any = !t;
    s.classList.toggle('hide',!any);
  });
  hint.textContent = t ? ('ظهر '+shown+' من '+total+' سؤالًا') : '';
});
"""

doc = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>بنك أسئلة ملفّات «تخصص عربي» الأربعة عشر — منصّة اجتاز</title>
<style>{CSS}</style></head><body>
<header>
<h1>بنك أسئلة ملفّات «تخصص عربي» الأربعة عشر</h1>
<p>مجمَّعٌ من مجلّد «تخصص عربي» على منصّة اجتاز — في ملفٍّ واحد</p>
<div class="kpis">
 <div class="kpi"><b>{ad(14)}</b>ملفًّا في المجلّد</div>
 <div class="kpi"><b>{ad(TOTAL)}</b>سؤالًا مجمَّعًا</div>
 <div class="kpi"><b>{ad(sum(1 for f in FILES if f['st']=='ok'))}</b>ملفًّا مقروءًا</div>
 <div class="kpi"><b>{ad(sum(1 for f in FILES if f['st']=='part'))}</b>مقروءًا جزئيًّا</div>
 <div class="kpi"><b>{ad(sum(1 for f in FILES if f['st']=='no'))}</b>لم يُفتح</div>
</div></header>
<div class="wrap">

<div class="toolbar"><input id="search" type="search"
 placeholder="ابحث في كلّ الأسئلة… (الحركات والهمزات لا تُشترط)">
 <div id="hint" style="font-size:13px;color:#6b7a89;padding:4px 2px"></div></div>

<div class="card">
<h2>جرد المجلّد</h2>
<p class="lead">هذه الملفّات الأربعة عشر كما هي مرتَّبة في المجلّد، وحال كلٍّ منها عندي.
الأسئلة بعد الجدول مرتَّبةٌ على الترتيب نفسه.</p>
<table><thead><tr><th>#</th><th>اسم الملفّ</th><th>الحال</th><th>المستخرَج</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<p class="note">ملحوظة مهمّة: هذه الملفّات يُعيد بعضها بعضًا إعادةً كثيرة — والسؤال الواحد
يَرِد في ثلاثة ملفّات أو أربعة. فما تواتر منها ولم يصحّ ردُّه إلى ملفٍّ بعينه جمعتُه في
«البنك المجمَّع» آخر هذا الملفّ مرتَّبًا على الأبواب، ولم أنسبه زورًا إلى ملفٍّ واحد.</p>
</div>

<div class="card">
<h2>كيف جُمعت هذه الأسئلة</h2>
<p class="lead">المجلّد عامٌّ لا يحتاج دخولًا ولا اشتراكًا، وهذه الملفّات تُفتح بروابط
المشاركة نفسها. وقد سلكتُ إليها طريقين:</p>
<ul>
<li><b>طريق النصّ</b> — استخراج طبقة النصّ من الـPDF مباشرة. نجح مع تسعة ملفّات.</li>
<li><b>طريق الصور</b> — تحويل الصفحات إلى صور وقراءتها بالنظر. وهو الذي أنقذ ملفَّي
«تسريبات الحسام» المكسورَي الترميز، وأنقذ «٣٦٠ سؤال» الذي رفض خمس عشرة صيغة رابط نصّيّ.</li>
</ul>
<p class="note">والأسئلة هنا <b>معادة الصياغة</b>، والتعليل تحت كلّ جواب <b>أصليٌّ</b> مستمدٌّ
من كتب الفنّ لا منقولٌ من الملفّات. ولم يُنسخ من أيّ ملفٍّ نصٌّ حرفيّ ولا صورةُ صفحة.</p>
</div>

<h2 style="margin:28px 0 2px;border:0;font-size:23px">أوّلًا: الأسئلة منسوبةً إلى ملفّاتها</h2>
{''.join(secs)}

<h2 style="margin:34px 0 2px;border:0;font-size:23px">ثانيًا: البنك المجمَّع
<span style="font-size:15px;font-weight:400;color:#6b7a89">— مادّةٌ تواترت في عدّة ملفّات</span></h2>
{''.join(shared_secs)}

<div class="card">
<h2>ما بقي، وكيف يُستكمل</h2>
<ul>
<li><b>«٣٦٠ سؤال»</b> — فُتح، والسحب جارٍ: بلغ الصفحة الثانية والعشرين. وبقيّته تحتاج مرورًا صفحةً صفحة؛
وهو أغزر ما في المجلّد لأنه اختيارٌ من متعدّد بإجاباتٍ مؤشَّرة.</li>
<li><b>«تسريبات الحسام» المشفَّران</b> — ثلاث صفحات من نحو مئة.</li>
<li><b>«أسئلة معلم فصل»</b> و<b>«الحاسب الآلي ج٢»</b> — خارج تخصّص اللغة العربية،
ولم أفتحهما بعدُ لأن نفعهما لطالب العربية قليل.</li>
</ul>
<p class="note">والعدد الظاهر أعلاه هو ما تحقّقتُ منه فعلًا، لا ما يدّعيه مجموع عناوين
الملفّات. وأنا أُفضّل أن أُسلِّمك رقمًا صادقًا على رقمٍ منفوخ.</p>
</div>

<footer>بنك أسئلة ملفّات «تخصص عربي» الأربعة عشر · {ad(TOTAL)} سؤالًا ·
 مجلّد المصدر: <span dir="ltr">{FOLDER}</span></footer>
</div>
<script>{JS}</script></body></html>"""

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(doc)

print(f"WROTE {OUT} {os.path.getsize(OUT)} bytes")
print(f"files 14 | attributed {n_files_q} | shared {n_shared_q} | TOTAL {TOTAL}")
for k, f in enumerate(FILES, 1):
    print(f"  {k:2d}. {ST_LBL[f['st']]:14s} {len(f['_qs']):4d}  {f['n'][:52]}")
