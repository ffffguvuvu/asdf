# -*- coding: utf-8 -*-
"""قسم اللغة الإنجليزية: قواعد ومفردات بأسلوب المسابقات، مع شرح عربي لكل إجابة."""

from qkit import mk, SRC_HOT, SRC_CUR

E = "eng"

# (الجملة بها فراغ ____، الإجابة، البدائل، الشرح بالعربية، التكرار)
GRAMMAR = [
    ("He ____ to school every day.", "goes", ["go", "going", "gone"],
     "المضارع البسيط مع الفاعل المفرد الغائب يأخذ s/es، والدليل every day.", 2),
    ("They ____ playing football now.", "are", ["is", "am", "be"],
     "المضارع المستمر: فاعل جمع They ⇐ are + v-ing، والدليل now.", 2),
    ("I ____ my homework yesterday.", "did", ["do", "done", "doing"],
     "الدليل yesterday ⇐ الماضي البسيط، وتصريف do الثاني did.", 2),
    ("She has ____ her book.", "lost", ["lose", "loses", "losing"],
     "المضارع التام: has + التصريف الثالث (lost).", 2),
    ("We ____ travel to Cairo next week.", "will", ["did", "have", "are"],
     "الدليل next week ⇐ المستقبل البسيط will + مصدر.", 2),
    ("He has been teaching ____ ten years.", "for", ["since", "ago", "from"],
     "for تُستعمل مع المدة (ten years)، وsince مع نقطة زمنية محددة.", 2),
    ("I have known him ____ 2010.", "since", ["for", "during", "while"],
     "since مع نقطة البداية الزمنية (2010).", 2),
    ("If it rains, we ____ at home.", "will stay", ["stayed", "would stay", "stay"],
     "الشرط من النوع الأول: If + مضارع بسيط، والجواب will + مصدر.", 2),
    ("If I ____ rich, I would travel the world.", "were", ["am", "will be", "have been"],
     "الشرط من النوع الثاني: If + ماضي بسيط (were لكل الضمائر) + would + مصدر.", 2),
    ("The letter ____ by the teacher yesterday.", "was written", ["wrote", "is writing", "has written"],
     "المبني للمجهول في الماضي البسيط: was/were + التصريف الثالث.", 2),
    ("English ____ all over the world.", "is spoken", ["speaks", "is speaking", "spoke"],
     "المبني للمجهول في المضارع البسيط: is/are + التصريف الثالث.", 2),
    ("You are a teacher, ____ ?", "aren't you", ["don't you", "isn't it", "are you"],
     "السؤال الذيلي: الجملة مثبتة ⇐ الذيل منفي، ونستعمل نفس الفعل المساعد are.", 2),
    ("She can't swim, ____ ?", "can she", ["can't she", "does she", "is she"],
     "الجملة منفية ⇐ الذيل مثبت بنفس الفعل المساعد can.", 2),
    ("This is ____ interesting book.", "an", ["a", "the", "some"],
     "an قبل الكلمة التي تبدأ بصوت متحرك (interesting).", 2),
    ("He is ____ university student.", "a", ["an", "the", "any"],
     "university تبدأ بصوت ساكن /ju/ فتأخذ a لا an.", 2),
    ("Cairo is ____ city in Egypt.", "the biggest", ["bigger", "big", "more big"],
     "التفضيل المطلق (superlative) يسبقه the ويُقارن بمجموعة.", 2),
    ("This book is ____ than that one.", "more useful", ["usefuler", "most useful", "the most useful"],
     "الصفة الطويلة تُقارن بـ more + الصفة + than.", 2),
    ("You ____ wear a helmet when you ride a bike.", "must", ["can", "may", "might"],
     "must للضرورة والإلزام.", 1),
    ("He said that he ____ tired.", "was", ["is", "will be", "has been"],
     "في الكلام المنقول يتحول المضارع البسيط إلى ماضٍ بسيط.", 2),
    ("She asked me where I ____.", "lived", ["live", "do live", "living"],
     "في السؤال المنقول نستعمل ترتيب الجملة الخبرية مع تغيير الزمن.", 1),
    ("Neither Ali nor his brothers ____ present.", "were", ["was", "is", "has been"],
     "مع neither...nor يتبع الفعل أقرب فاعل (his brothers).", 1),
    ("The number of students ____ increasing.", "is", ["are", "were", "have"],
     "the number of + جمع يأخذ فعلًا مفردًا.", 1),
    ("Each of the boys ____ a book.", "has", ["have", "are having", "having"],
     "each of + جمع يأخذ فعلًا مفردًا.", 1),
    ("I enjoy ____ novels.", "reading", ["read", "to read", "reads"],
     "بعد enjoy يأتي الفعل بصيغة v-ing.", 2),
    ("He decided ____ abroad.", "to travel", ["travel", "traveling", "travels"],
     "بعد decide يأتي المصدر مسبوقًا بـ to.", 2),
    ("She is good ____ English.", "at", ["in", "on", "for"],
     "التعبير الثابت: good at = ماهر في.", 2),
    ("He is interested ____ history.", "in", ["at", "on", "with"],
     "التعبير الثابت: interested in.", 2),
    ("I am afraid ____ snakes.", "of", ["from", "at", "about"],
     "التعبير الثابت: afraid of.", 2),
    ("We arrived ____ the airport at six.", "at", ["to", "in", "on"],
     "arrive at مع الأماكن المحددة، وarrive in مع المدن والدول.", 1),
    ("The meeting will be held ____ Monday.", "on", ["in", "at", "since"],
     "on مع أيام الأسبوع، in مع الشهور والسنوات، at مع الساعات.", 2),
    ("I have ____ money to buy this car.", "enough", ["much", "many", "a few"],
     "enough بمعنى (كافٍ) وتأتي قبل الاسم.", 1),
    ("There isn't ____ sugar in the cup.", "much", ["many", "a lot", "few"],
     "much مع المعدود غير القابل للعد في النفي والسؤال.", 2),
    ("How ____ students are there in the class?", "many", ["much", "long", "far"],
     "many مع المعدود (students).", 2),
    ("He works hard ____ he can succeed.", "so that", ["because", "although", "unless"],
     "so that تفيد الغرض (لكي).", 1),
    ("____ he was tired, he finished the work.", "Although", ["Because", "So", "Unless"],
     "Although تفيد التضاد (على الرغم من).", 2),
    ("I will not go ____ you come with me.", "unless", ["if", "when", "because"],
     "unless = if not (ما لم).", 1),
    ("The man ____ helped me is my teacher.", "who", ["which", "whose", "whom"],
     "who ضمير وصل للعاقل في محل فاعل.", 2),
    ("This is the book ____ I bought yesterday.", "which", ["who", "whose", "where"],
     "which ضمير وصل لغير العاقل.", 2),
    ("He used ____ in Alexandria.", "to live", ["live", "living", "lived"],
     "used to + مصدر للتعبير عن عادة في الماضي.", 1),
    ("I would rather ____ at home tonight.", "stay", ["to stay", "staying", "stayed"],
     "would rather + مصدر بدون to.", 1),
    ("By the time we arrived, the match ____.", "had started", ["started", "starts", "has started"],
     "الماضي التام للحدث الأسبق بين حدثين ماضيين.", 1),
    ("While I ____ TV, the phone rang.", "was watching", ["watched", "watch", "have watched"],
     "الماضي المستمر للحدث الطويل المقطوع بحدث قصير في الماضي البسيط.", 2),
    ("Look! The baby ____.", "is crying", ["cries", "cried", "has cried"],
     "Look! دليل على المضارع المستمر.", 2),
    ("Water ____ at 100 degrees.", "boils", ["is boiling", "boiled", "has boiled"],
     "الحقائق العلمية الثابتة تُصاغ بالمضارع البسيط.", 2),
    ("She has lived here ____ five years.", "for", ["since", "ago", "during"],
     "for مع المدد الزمنية.", 2),
    ("My father ____ in this school since 2005.", "has worked", ["works", "worked", "is working"],
     "since دليل على المضارع التام.", 2),
    ("It is the ____ film I have ever seen.", "best", ["better", "good", "well"],
     "بعد the ومع ever نستخدم صيغة التفضيل المطلق best.", 1),
    ("He speaks English ____.", "fluently", ["fluent", "fluency", "more fluent"],
     "نحتاج حالًا (adverb) لوصف الفعل speaks.", 2),
    ("The teacher made the students ____ the poem.", "memorize", ["to memorize", "memorizing",
                                                                   "memorized"],
     "بعد make + مفعول يأتي المصدر بدون to.", 1),
    ("I am looking forward to ____ from you.", "hearing", ["hear", "heard", "be hear"],
     "look forward to تتبعها v-ing لأن to هنا حرف جر.", 1),
    ("Hardly ____ entered the room when the bell rang.", "had I", ["I had", "did I", "I have"],
     "بعد Hardly في بداية الجملة يحدث قلب (inversion).", 0),
]

VERBS = [
    ("go", "went", "gone"), ("write", "wrote", "written"), ("take", "took", "taken"),
    ("see", "saw", "seen"), ("eat", "ate", "eaten"), ("give", "gave", "given"),
    ("come", "came", "come"), ("do", "did", "done"), ("drink", "drank", "drunk"),
    ("speak", "spoke", "spoken"), ("break", "broke", "broken"), ("choose", "chose", "chosen"),
    ("begin", "began", "begun"), ("buy", "bought", "bought"), ("bring", "brought", "brought"),
    ("teach", "taught", "taught"), ("think", "thought", "thought"), ("catch", "caught", "caught"),
    ("find", "found", "found"), ("feel", "felt", "felt"), ("keep", "kept", "kept"),
    ("leave", "left", "left"), ("lose", "lost", "lost"), ("make", "made", "made"),
    ("meet", "met", "met"), ("pay", "paid", "paid"), ("read", "read", "read"),
    ("run", "ran", "run"), ("say", "said", "said"), ("sell", "sold", "sold"),
    ("send", "sent", "sent"), ("sing", "sang", "sung"), ("sit", "sat", "sat"),
    ("sleep", "slept", "slept"), ("swim", "swam", "swum"), ("teach", "taught", "taught"),
    ("tell", "told", "told"), ("wear", "wore", "worn"), ("win", "won", "won"),
    ("know", "knew", "known"), ("grow", "grew", "grown"), ("fly", "flew", "flown"),
]

VOCAB = [
    ("The opposite of 'difficult' is ____.", "easy", ["hard", "tough", "complex"], "ضد difficult هو easy."),
    ("The opposite of 'ancient' is ____.", "modern", ["old", "antique", "past"], "ضد ancient هو modern."),
    ("The opposite of 'increase' is ____.", "decrease", ["grow", "rise", "expand"], "ضد increase هو decrease."),
    ("The opposite of 'success' is ____.", "failure", ["victory", "win", "triumph"], "ضد success هو failure."),
    ("A person who teaches at a school is a ____.", "teacher", ["student", "doctor", "farmer"],
     "من يعلّم في المدرسة هو teacher."),
    ("A place where books are kept is a ____.", "library", ["laboratory", "museum", "garage"],
     "مكان حفظ الكتب هو library."),
    ("The synonym of 'clever' is ____.", "intelligent", ["lazy", "weak", "slow"],
     "مرادف clever هو intelligent."),
    ("The synonym of 'begin' is ____.", "start", ["finish", "stop", "end"], "مرادف begin هو start."),
    ("The synonym of 'famous' is ____.", "well-known", ["unknown", "strange", "silent"],
     "مرادف famous هو well-known."),
    ("A person who writes books is an ____.", "author", ["actor", "artist", "engineer"],
     "من يؤلف الكتب هو author."),
    ("The opposite of 'cheap' is ____.", "expensive", ["low", "free", "small"], "ضد cheap هو expensive."),
    ("The synonym of 'quickly' is ____.", "rapidly", ["slowly", "calmly", "lately"],
     "مرادف quickly هو rapidly."),
    ("Students study in a ____.", "classroom", ["kitchen", "garden", "station"],
     "الطلاب يدرسون في classroom."),
    ("The opposite of 'absent' is ____.", "present", ["away", "late", "missing"], "ضد absent هو present."),
    ("A test taken at the end of the year is a ____ exam.", "final", ["first", "early", "middle"],
     "امتحان نهاية العام هو final exam."),
]


def bank():
    out = []
    for sent, ans, wrongs, why, r in GRAMMAR:
        q = mk(f"Choose the correct answer:  {sent}", ans, wrongs, why, E, "الإنجليزي — القواعد",
               SRC_HOT if r == 2 else SRC_CUR, r)
        if q:
            out.append(q)

    seen = set()
    for i, (v1, v2, v3) in enumerate(VERBS):
        if v1 in seen:
            continue
        seen.add(v1)
        others2 = [x[1] for x in VERBS if x[0] != v1]
        others3 = [x[2] for x in VERBS if x[0] != v1]
        q = mk(f"What is the past simple of «{v1}»?", v2, others2[i % 20:i % 20 + 3],
               f"التصريف الثاني (الماضي البسيط) للفعل {v1} هو {v2}، والثالث {v3}.",
               E, "الإنجليزي — تصريف الأفعال", SRC_CUR, 1)
        if q:
            out.append(q)
        q = mk(f"What is the past participle of «{v1}»?", v3, others3[(i + 5) % 20:(i + 5) % 20 + 3],
               f"التصريف الثالث للفعل {v1} هو {v3} ويُستعمل مع have/has/had وفي المبني للمجهول.",
               E, "الإنجليزي — تصريف الأفعال", SRC_CUR, 1)
        if q:
            out.append(q)
        q = mk(f"He has already ____ the letter.  (verb: {v1})", v3, [v1, v2, v1 + "ing"],
               f"بعد has نستعمل التصريف الثالث: {v3}.",
               E, "الإنجليزي — القواعد", SRC_CUR, 0)
        if q:
            out.append(q)
        q = mk(f"Yesterday he ____ to the market.  (verb: {v1})", v2, [v1, v3, v1 + "s"],
               f"yesterday دليل الماضي البسيط: {v2}.",
               E, "الإنجليزي — القواعد", SRC_CUR, 0)
        if q:
            out.append(q)

    for sent, ans, wrongs, why in VOCAB:
        q = mk(f"Choose the correct answer:  {sent}", ans, wrongs, why, E, "الإنجليزي — المفردات",
               SRC_CUR, 1)
        if q:
            out.append(q)
    return out
