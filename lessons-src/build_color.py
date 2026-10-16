#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بناء «شرحُ الدروسِ — نسخةٌ ملوَّنةٌ»: ملفٌّ جديدٌ قائمٌ بنفسه، ملوَّنٌ ومنسَّقٌ ومفهرَسٌ،
يُغطِّي الدروسَ الأربعةَ عشر والملاحقَ الأربعةَ، ويضيفُ لكلِّ درسٍ: شريطَ معلوماتٍ، وخريطةَ درسٍ،
وخلاصةً في سطورٍ؛ ولِكُلِّ وحدةٍ: فاصلاً ملوَّناً وتمهيداً.
التقطيعُ والترقيمُ محفورٌ وقتَ البناءِ كما في الملفِّ الأصليِّ (تقطيعٌ واحدٌ لا يقيسُ الشاشةَ).
شغِّلْه من جذرِ المستودع:  python3 lessons-src/build_color.py
"""
import re, os, glob, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import paginate as PG

OUT = os.path.join(ROOT, 'arabic-lessons-color.html')
REF = os.path.join(ROOT, 'arabic-grammar.html')
BUILD = os.path.join(HERE, 'build.py')

AR = '٠١٢٣٤٥٦٧٨٩'


def ar(n):
    return ''.join(AR[int(c)] for c in str(n))


# ————— سبعُ وحداتَ ملوَّنةٍ —————
UNITS = [
    dict(key='u1', name='جملةُ الابتداءِ: المبتدأُ والخبرُ',
         pal=('#0d5c52', '#178a76', '#c9e6de', '#f1fbf7', '#0b4b43'),
         idx=[0, 1],
         intro='هنا يُوضَعُ الأساسُ كلُّه: اسمٌ يُبتَدَأُ به واسمٌ يُخبَرُ عنه. من أحكمَ هاتينِ '
               'الركنَينِ أدركَ أكثرَ إعرابِ الجُملِ الاسميّةِ، وعَرَفَ متى يُحذَفُ أحدُ الركنَينِ '
               'وجوبًا، ومتى يتقدَّمَ الخبرُ أو يتأخَّرُ، وما الذي يَمنَعُ الابتداءَ بالنكرةِ.'),
    dict(key='u2', name='الجملةُ الفعليّةُ: الفعلُ ومَن يَفعلُ',
         pal=('#1b3f7a', '#2f63b0', '#cfdcf2', '#f2f7fd', '#16335f'),
         idx=[2, 3],
         intro='الجملةُ الفعليّةُ تُبنى على ثلاثةِ أركانٍ: فعلٌ، فاعلٌ، ومفعولٌ به. في هاتينِ '
               'الوحدتَينِ تُراجِعُ أزمنةَ الفعلِ وإسنادَه، ثمَّ صورَ الفاعلِ ومواضعَ وجوبِ '
               'تأخيرِه، ونائبَ الفاعلِ وما يُرفَعُ مَعَها.'),
    dict(key='u3', name='المفعولاتُ الخمسُ وسائرُ المنصوباتِ',
         pal=('#8a5a12', '#c08a24', '#f0e0bf', '#fdf7ea', '#6b4f12'),
         idx=[4],
         intro='بابُ المنصوباتِ هو أوسعُ الأبوابِ وأكثرُها اشتباكًا. يُفتَحُ بميزانٍ واحدٍ '
               'يُوازِنُ بين المفعولِ به والمُطلَقِ والظرفِ والمُلهِ والمَعيّةِ، ثمَّ يُتبَعُ '
               'بسائرِ المنصوباتِ من حالٍ وتمييزٍ ومستثنًى ومنادى.'),
    dict(key='u4', name='أسماءٌ تُعرَفُ بما بعدها: الإشارةُ والموصولُ',
         pal=('#5a2a7a', '#7c46a6', '#e2d4ef', '#f9f4fd', '#482161'),
         idx=[5, 6],
         intro='أسماءُ الإشارةِ والأسماءُ الموصولةُ أبوابٌ مبنِيّةٌ في جملتها، لكنَّ لكلِّ واحدٍ '
               'منها فروعًا: المُثنَّى المُعرَبُ، والجمعُ بين «ذا» و«أل»، وصلةُ الموصولِ '
               'والعائدُ وحذفُ حرفِها، وأحكامُ «ما» و«الذي» الفرعيّةُ.'),
    dict(key='u5', name='التوابعُ الأربعةُ: العطفُ والتوكيدُ والبدلُ والنعتُ',
         pal=('#8e2440', '#bb3a5c', '#f2d5de', '#fdf2f5', '#6f1c32'),
         idx=[7, 8, 9, 10],
         intro='التوابعُ أربعةٌ في المذهبِ الجُمهوريّ، يَعمَلُ فيها أصلٌ واحدٌ: تابعٌ يَتبَعُ '
               'متبوعَه في الحكمِ. ويُفرِّقُ بينَها المعنى: نَسقٌ، أو تكريرٌ، أو إبدالٌ '
               'يَسْتَغرِقُ المُبدَلَ منهُ أو بعضَهُ، أو وَصفٌ. في هذه الوحدةِ فروعُ كلِّ تابعٍ '
               'وأحكامُه وشروطُه.'),
    dict(key='u6', name='المنصوباتُ الزائدةُ والإضافةُ',
         pal=('#0e6274', '#1a8aa3', '#cfe8ef', '#f1fbfd', '#0b4e5c'),
         idx=[11, 12, 13],
         intro='الحالُ والتمييزُ إجابةٌ عن «كيفَ؟» و«في أيِّ شيءٍ؟»، والإضافةُ نسبةٌ تُجرِّدُ المضافَ من «ألْ» والتنوينِ، وتُفيدُ تعريفًا أو تخصيصًا.'
               'المجرَّدِ من «ألْ» والتنوينِ. الفصلُ بين الحالِ والتمييزِ والنعتِ هو ما '
               'يَظهَرُ في الاختبارِ، ولهذا جُمِعَ الثلاثُ في ميزانٍ واحدٍ.'),
    dict(key='u7', name='الملاحقُ الجامعةُ: الثوابتُ والبوّاباتُ والمصفوفةُ والمصادرُ',
         pal=('#4a4238', '#6f6558', '#e4ddd2', '#faf7f2', '#3a342c'),
         idx=[14, 15, 16, 17],
         intro='أربعةُ ملاحقَ تُجمِعُ ما تفرَّقَ في الدروسِ: ثوابتُ المرفوعاتِ والمنصوباتِ '
               'والمجروراتِ والتوابعِ والنواسخِ والأعدادِ والحروفِ مُصنَّفةً، وبوّاباتُ '
               'إعرابٍ تُعرَفُ بها المواضعُ، ومصفوفةُ كلِّ درسٍ في كلِّ بابٍ، والمصادرُ '
               'ومنهجيّةُ الإعرابِ في سبعِ خطواتٍ.'),
]

# ————— خريطةُ كلِّ درسٍ وخلاصتُه —————
EXTRA = {
    'l01': ('يُحدَّدُ أوّلًا حدُّ المبتدأِ والصورةُ التي يأتي عليها: اسمٌ ظاهرٌ، أو ضميرٌ منفصلٌ، '
            'أو مصدرٌ مؤوَّلٌ، أو اسمٌ مُشتقٌّ في موضعِ الاسمِ. ثمَّ تُعرَضُ مسوِّغاتُ الابتداءِ '
            'بالنكرةِ واحدًا واحدًا، ثمَّ الأحكامُ الثابتةُ، ثمَّ مواضعُ حذفِه جوازًا ووجوبًا. '
            'ويُختَمُ بجدولِ «مواضعُ الدرسِ» في الأساليبِ والتقديمِ والحذفِ والنواصبِ والنواسخِ '
            'والتراكيبِ الخاصّةِ.',
            ['المبتدأُ اسمٌ مجرَّدٌ من العواملِ اللفظيّةِ، مرفوعٌ أو في محلِّ رفعٍ.',
             'النكرةُ لا يُبتدَأُ بها إلّا بمسوِّغٍ: خصوصيةٍ، أو عمومٍ، أو شرطٍ، أو نفيٍ.',
             'يُحذَفُ المبتدأُ وجوبًا في قَسَمِ «لعمْرُ اللهِ» وفي الجوابِ المُقصَرِ: «مَن عندَكَ؟ — زيدٌ».']),
    'l02': ('الخبرُ ركنُ الجملةِ الاسميّةِ الثاني، ويُقسَّمُ أولًا إلى مفردٍ وغيرِ مفردٍ، ثمَّ إلى '
            'جملةٍ فعليّةٍ واسميّةٍ وشبهِ جملةٍ. ويُبيَّنُ أحكامُه الثابتةُ في المطابقةِ '
            'والتقديمِ، ومواضعُ تقدُّمِه على المبتدأِ وجوبًا وجوازًا، مع أمثلةٍ مُعرَبةٍ '
            'سَطرًا سطرًا وجدولِ مواضعَ جامعٍ.',
             ['الخبرُ أصلًا غيرُ محذوفٍ؛ فإن حُذِفَ فبدليلٍ: «أيُّهم أفقَهُ؟ — زيدٌ»، أي: زيدٌ أفقَهُم.',
              'الجملةُ بعدَ المضمرِ المُبتدَأِ به خبرٌ لا نعتٌ: «هو الذي جاءَ».',
              'تقديمُ الخبرِ وجوبًا إذا كانَ المبتدأُ نكرةً محضةً: «في الدارِ رجلٌ».']),
    'l03': ('الفعلُ قسيمٌ ثلاثيّ الأزمنةِ، ويُلتمَسُ له أولًا علامةُ كلِّ زمنٍ، ثمَّ تُعرَضُ '
            'تقسيماتُه الأخرى: لازمٌ ومتعدٍّ، مبنيٌّ للمعلومِ والمجهولِ، صحيحٌ ومعتلٌّ، تامٌّ '
            'وناقصٌ، وأوامرُ التصريفِ المتكرِّرةِ. ثمَّ مواضعُه في البابِ الستّةِ.',
             ['الماضي مبنيٌّ دائمًا، والمضارعُ مبنيٌّ في موضعَينِ: مع نونِ النسوةِ، ومع نونِ التوكيدِ خفيفةً أو ثقيلةً.',
              'المضارعُ المعتلُّ الآخرِ يُجزمُ بحذفِ حرفِ العلّةِ: «لم يخشَ»، والأجوفُ يُجزمُ بحذفِ عينِهِ: «لم يَعِدْ».',
              'الأفعالُ الناقصةُ ترفعُ الاسمَ وتنصبُ الخبرَ، وحدُّها أن تُفيءَ معنى من معاني الصيرورةِ أو الانتفاءِ أو الزمنِ.']),
    'l04': ('الفاعلُ اسمٌ مرفوعٌ ذكرَ بعدَه فعلٌ فأسنِدَ إليه الفعلُ، وهو إمّا اسمٌ ظاهرٌ، أو '
            'ضميرٌ مستترٌ، أو مؤوَّلٌ، أو «ما» و«من» الموصوليّتانِ. ثمَّ أحكامُه الثابتةُ في '
            'التأخيرِ والتقدُّمِ والتذكيرِ والتأنيثِ، ثمَّ نائبُ الفاعلِ وحدَه وأمورُه.',
             ['إذا كانَ الفاعلُ ضميرًا متَّصلًا وجَبَ تأخيرُهُ: «كرمتُ»؛ ولا يَصِحُّ «أنا كرمْتُ» بمعنى الإسنادِ، بل هي مبتدأٌ والجملةُ خبرٌ.',
              '«نِعمَ» و«بِئسَ» يخُصُّهُما الفاعلُ: معرفةٌ مُفسَّرةٌ بنكرةٍ أو ضميرِ مُخاطَبٍ.',
              'نائبُ الفاعلِ ما أُسنِدَ الفعلُ إليهِ بعدَ حذفِ الفاعلِ: «ضُرِبَ زيدٌ»؛ والأصلُ أن ينوبَ المفعولُ بهِ، ثمَّ الظرفُ والمجرورُ عندَ من يُجيزُها.']),
    'l05': ('أوسعُ درسٍ في الملفِّ: المفاعيلُ الخمسةُ تُعرَضُ في ميزانٍ واحدٍ يُبيِّنُ سؤالَ كلِّ '
            'واحدٍ منها، ثمَّ لكلِّ مفعولٍ حدُّه وصورُه وأحكامُه وما ينوبُ عنْه. ويُختَمُ '
            'بسائرِ المنصوباتِ: الحالُ، والتمييزُ، والمستثنى، والمنادى، والنادي، و«ما» الحرفيّةَ.',
             ['المفعولُ المطلقُ مصدرٌ يَذكُرُهُ فاعِلُهُ لتوكيدِ فعلِهِ أو بيانِ نوعِهِ أو بيانِ فعلِهِ.',
              'المفعولُ لأجلِهِ مصدرٌ قَلبيٌّ وقعَ جوابًا «لِمَ؟»، وفعلُهُ فاعلُ فاعلِهِ، ولا يُقدَّمُ على فعلِهِ إلّا ما يُقدَّمُ من ظرفٍ ومجرورٍ.',
              'المفعولُ معهُ اسمٌ بعدَ واوِ المعيّةِ لا يَصلُحُ أن يكونَ معطوفًا: «جئتُ والمطرَ».']),
    'l06': ('ألفاظُ الإشارةِ تُستَوعَبُ كاملةً بحسب المُشارِ إليهِ: مُفردًا ومُثنًّى وجمعًا، '
            'مُذكَّرًا ومؤنَّثًا، وقُربًا وبُعدًا وقُربًا متوسطًا. ثمَّ أحكامُها الثابتةُ: البناءُ '
            'إلّا المُثنَّى، ودخولُ «ألْ» عليها، و«ذا» مع ظرفيَّتي «هنَّ» و«ثمَّ».',
             ['أسماءُ الإشارةِ كلُّها مبنيّةٌ إلّا المُثنَّى منها: «ذانِكَ» و«تانِكَ» فيُعرَبانِ.',
              '«هذا» للمُذكَّرِ القريبِ، و«هذه» تُستعمَلُ للمؤنَّثِ وللجمعِ غيرِ العاقلِ.',
              'إذا جاءَ بعدَ اسمِ الإشارةِ اسمٌ معرَّفٌ بـ«ألْ» كانَ بدلًا أو عطفَ بيانٍ عندَ الجمهورِ، ولا يكونُ نعتًا: «هذا الرجلُ مُكرَمٌ».']),
    'l07': ('الموصولُ اسمٌ مُغلَقٌ لا يستقلُّ بمعنًى إلّا بصلةٍ. تُعرَضُ ألفاظُه كاملةً، ثمَّ '
            'أحكامُ الصلةِ والعائدِ: متى يَجِبُ ذكرُ العائدِ، ومتى يُمكِنُ حذفُه، ومتى تُحذَفُ '
            'الألفُ واللامُ من الصلةِ، و«ما» المصدريةُ الموصولةُ.',
             ['صلةُ الموصولِ جملةٌ، وقد تكونُ شبهَ جملةٍ أو مفردًا على مذهبٍ في التقديرِ.',
              'العائدُ إن كانَ منصوبًا أو مجرورًا بحرفِ جرٍّ أصيلٍ جازَ حذفُهُ: «هذا الذي رأيْتُهُ»؛ وإذا كانَ مرفوعًا لَزِمَ ذكرُهُ في الأكثرِ.',
              '«أيٌّ» من الأسماءِ الموصولةِ — وهو المُعرَبُ وحدَهُ بينَها — ويُضافُ غالبًا إلى نكرةٍ فيُعربُ المضافُ وحدَهُ: «أيُّ رجلٍ يأتيني أكرِمْهُ».']),
    'l08': ('العطفُ نَسقٌ بين كلمتينِ بحرفٍ يُفيدُ معنى. تُستَوعَبُ حروفُ العطفِ العشرةُ '
            'بمعانيها وشروطِها، ثمَّ عطفُ البيانِ — وهو أخصُّ من البدلِ عندَ كثيرٍ من النحاةِ — '
            'ثمَّ أحكامٌ ثابتةٌ في تقدُّمِ المعطوفِ عليهِ وحكمِ «إلّا» و«حتى».',
             ['المعطوفُ تابعٌ للمعطوفِ عليهِ في حكمِ عامِلِهِ لا في لفظِه.',
              '«حتّى» الأصلُ فيها أن تكونَ حرفَ جرٍّ وغايةً، وتكونُ عاطفةً بشروطٍ ذَكَرَها النحاةُ؛ فإذا اشتَبَهَت فالجرُّ هو الأصلُ.',
              'عطفُ البيانِ يُشْبِهُ النعتَ في أنَّهُ لا يُقصَدُ بهِ الوصفُ، والبدلَ في أنَّهُ يُبَيِّنُ المُبْهَمَ؛ ومن هنا خرجَ الخلافُ في «جاءَني زيدٌ أبوهُ»: بدلٌ أو عطفُ بيانٍ؟.']),
    'l09': ('التوكيدُ تابعٌ يَرفَعُ احتمالَ المجازِ والتقديرِ. ويُقسَمُ أوّلًا إلى لفظيٍّ '
            'و معنويٍّ، ثمَّ تُعرَضُ ألفاظُ المعنويِّ الخمسةُ وشروطُها، وما يعملُ في كلِّ نوعٍ.',
             ['التوكيدُ اللفظيُّ تكريرُ اللفظِ بعينِهِ — بحرفِهِ أو بمعناهُ — وحُكمُهُ حُكمُ المُؤكَّدِ.',
              '«أجمعُ» يُثنَّى ويُجمَعُ ويُؤنَّثُ كما يُشَاءُ، ولا بُدَّ من تقدُّمِ «كلٍّ» أو «أل» على المؤكَّدِ عندَ أكثرِهم.',
              'توكيدُ الضميرِ المُتَّصلِ لا يكونُ إلّا بالضميرِ المُنفصلِ: «جاءَني هُوَ».']),
    'l10': ('البدلُ أربعةُ أقسامٍ: كلٌّ من كلٍّ، وبعضٌ من كلٍّ، واشتقاقٌ من اسمِ فعلٍ، وبدلُ '
            'الغلطِ والنسيانِ. ثمَّ أنواعٌ تابعةٌ وأسماءٌ أُخَرُ في البابِ وأحكامٌ ثابتةٌ '
            'تُميِّزُهُ من عطفِ البيانِ والصفةِ.',
             ['بدلُ كلٍّ من كلٍّ يَأخُذُ إعرابَ المُبدَّلِ منهُ، وهو الذي يَعمَلُ فيهِ العاملُ وحدَهُ.',
              'بدلُ بعضٍ من كلٍّ يَشترِطُ ضميرًا مُطابِقًا مُتَّصلًا بالمُبدَلِ منهُ.',
              'بدلُ الاشتمالِ ليسَ مُتبادرًا كغيرِهِ: المُبدَّلُ منهُ ليسَ كُلَّهُ ولا بعضَهُ، بل هو مُشتَمَلٌ عليهِ: «أعجبَني زيدٌ علمُهُ».']),
    'l11': ('النعتُ صفةٌ تابعةٌ، ويُقسَمُ أوّلًا إلى حقيقيٍّ وسببيٍّ، ثمَّ تُشرَحُ شروطُ المطابقةِ '
            'في العلاماتِ الأربعِ، وأربعَ عشرةَ صورةً لـ«ما يُنعَتُ بهِ»، ثمَّ فروقٌ تُدرَكُ في '
            'التطبيقِ والاختبارِ بينَ النعتِ والبدلِ والعطفِ والبيانِ.',
             ['النعتُ السببيُّ يُطابِقُ منعوتَهُ في التعريفِ والتنكيرِ، وصاحبَهُ في التثنيةِ والجمعِ والتذكيرِ والتأنيثِ.',
              'النعتُ المُقطَّعُ عن منعوتهِ بالفاصلِ الأجنبيِّ يَجوزُ رفعُه على الابتداءِ.',
              '«أفعلُ» في التفضيلِ والتعجُّبِ لا يُنعَتُ بهِ إلّا مُضافًا أو مُجرَّدًا من «ألْ» مُجَرَّرًا بـ«من»: «مررتُ برجلٍ أفضلَ منكَ».']),
    'l12': ('الحالُ وصفٌ مُنتصِبٌ يُجيبُ عن «كيفَ؟»، وتُعرَضُ صورُها، وشروطُ صاحبِ الحالِ، '
            'وأحكامُها الثابتةُ، ثمَّ ميزانٌ يَجمَعُ الحالَ والتمييزَ والنعتَ في صفحةٍ واحدةٍ '
            'لأجلِ ما يَشترِكُ فيهِ الثلاثُ من الانتصابِ والاشتقاقِ.',
             ['صاحبُ الحالِ معرفةٌ في الأكثرِ، وتأتي الحالُ من النكرةِ في مواضعَ معدودةٍ.',
              'لا يَجوزُ تقديمُ الحالِ الصريحةِ على صاحبِها عندَ أكثرِ النحاةِ، ويجوزُ تقديمُ الجُملةِ وشبهَ الجُملةِ.',
              'الحالُ مُنتصِبٌ يُبيِّنُ هيأةَ صاحبِهِ: «جاءَ زيدٌ راكبًا»، والتمييزُ يُبيِّنُ المُنبَهِمَ من ذاتٍ أو نسبةٍ؛ والفرقُ في السؤالِ: «كيفَ؟» لا «كم؟».']),
    'l13': ('التمييزُ نوعانِ: تمييزُ الذّاتِ — وهو ما بعدَ العددِ والمقدارِ — وتمييزُ النّسبةِ، '
            'وهو ما يُرفَعُ من مُلبِسِ النسبةِ. ثمَّ أحكامٌ ثابتةٌ، ثمَّ تصنيفٌ جامعٌ '
            'لألفاظٍ تُميَّزُ بعدَها، مع جدولِ مواضعَ وأمثلةٍ مُعرَبةٍ.',
             ['تمييزُ ما بينَ ثلاثةَ عشرَ إلى تسعةٍ وتسعينَ مفردٌ منصوبٌ، وما بينَ ثلاثةٍ إلى عشرةٍ جمعُ قولٍ مجرورٌ.',
              'المساحةُ والكيلُ والوزنُ: تمييزُها مفردٌ دائمًا، وتذكيرُ تمييزِ العددِ وتأنيثُهُ تابعٌ لمُميَّزِه.',
              '«ما» و«كم» تُبهِمانِ فيحتاجانِ إلى تمييزٍ؛ فإذا دَخَلَت عليهما «ألْ» استَغنَتا عنهُ: «ما أحسنَ زيدًا» و«الكيلُ عِشرونَ صاعًا».']),
    'l14': ('الإضافةُ نسبتانِ: معنويّةٌ تُنيبُ عن عاملٍ، ولفظيّةٌ لا تُنيبُ. ثمَّ أحكامُ '
            'المضافِ: ما يُلزَمُ الإضافةَ، وما تُحذَفُ نونُه، وما لا يُضافُ إلّا لفظًا؛ ثمَّ '
            'أحكامُ المُضافِ إليهِ، والمُضافُ إلى ياءِ المتكلِّمِ.',
             ['الإضافةُ المعنويّةُ تُنيبُ عن عاملِها: «ضاربُ زيدٍ» أي يَضربُ زيدًا؛ واللفظيّةُ لا تُنيبُ عن شيءٍ.',
              'المُضافُ إلى ياءِ المتكلِّمِ: ما كانَ ما قبلَهُ مفتوحًا فُتِحَت ياؤُهُ في الأكثرِ: «هذا فتايَ»، وما كانَ مكسورًا كُسِرَت: «هذا غلامي».']),
    'thawat':  ('ثوابتُ الإعرابِ مُصنَّفةٌ في اثني عشرَ بابًا: المرفوعاتُ، المنصوباتُ، '
                'المجروراتُ، التوابعُ الخمسةُ، النواسخُ، النواصبُ والجوازمُ، الأسماءُ الخاصّةُ، '
                'الجُمَلُ، العددُ والمعدودُ، الحروفُ المشتركةُ، الحذفُ والإضمارُ، والبوّاباتُ. '
                'وهي جدولٌ بعدَ جدولٍ تُرجَعُ إليهِ عندَ كلِّ إشكالٍ.',
                ['الثوابتُ منقولةٌ بحُكمِها، فما كانَ فيهِ خلافٌ فمُنَبَّهٌ عليهِ لئلّا يُنسَبَ إلى الإجماعِ.',
                 'أبوابُها مرتَّبةٌ على حركاتِ الإعرابِ أولًا: المرفوعاتُ، فالمنصوباتُ، فالمجروراتُ، ثمَّ التوابعُ والنواسخُ والخاصُّ.',
                 'إذا تعارَضَ ثابتانِ فالمُعتَمَدُ نصُّ البابِ المختَصِّ في أصلِ الدرسِ لا جدولُ الثوابتِ.']),
    'thawat2': ('بوّاباتٌ إعرابيّةٌ — جوامعُ تُعرَفُ بها الإعراباتُ من مواضعِها — في سبعةِ '
                'فصولٍ: للمبتدأِ والخبرِ، وللفعلِ والفاعلِ ونائبِهِ، وللمفاعيلِ والتوابعِ '
                'والفضلاتِ، وللنواسخِ والنواصبِ والجوازمِ، وللاسماءِ الخاصّةِ والمبنيّاتِ، '
                'وللحذفِ والتقديرِ، وللأساليبِ.',
                ['البوّابةُ عَلامةٌ يُمكِنُ أن تُطبَّقَ على كلامٍ لم يَرِدْ في الكتابِ.',
                 'كلُّ بوّابةٍ معَها مثالٌ مُعرَبٌ يُبيِّنُ كيفَ تُستَعمَلُ، لا مجرَّدَ حُكمٍ.',
                 'ما يُناسِبُ البابَ من بوّاباتِ الأساليبِ مُدرَجٌ مع درسِه أيضًا.']),
    'matrix':  ('مصفوفةُ المواضعِ: كلُّ درسٍ من الدروسِ الأربعةَ عشرَ في مقابلِ الأبوابِ الستّةِ '
                '— الأساليبُ، التقديمُ والتأخيرُ، الحذفُ، النواصبُ، النواسخُ، التراكيبُ '
                'الخاصّةُ. فتُعرَضُ القاعدةُ نصًّا، ثمَّ أمثلتُها، ثمَّ وجوهُ الإعرابِ، ثمَّ '
                'الفروقُ والأخطاءُ الشائعةُ.',
                ['ثمانيةٌ وثمانونَ بابًا مفصَّلًا، ومئتانِ واثنانِ وخمسونَ ركنَ شرحٍ، ومئةٌ وسبعةٌ وستُّونَ مثالًا.',
                 'لا يُكتَفى في المصفوفةِ بجدولٍ مُختصَرٍ؛ لكلِّ بابٍ نصُّ قاعدةٍ وأمثلةٌ ووجوهُ إعرابٍ.',
                 'هذه المصفوفةُ مرجِعُ ترتيبِ المواضعِ؛ فإذا اشتبَهَ موضعٌ فارجِعْ إلى بابِه منها.']),
    'sources': ('المصادرُ والطبقاتُ، ثمَّ المنهجيّةُ، ثمَّ خطواتُ الإعرابِ السبعُ، ثمَّ مسائلُ '
                'أُثبِتَ فيهِ الخلافُ فلا تُنسَبُ إلى اليقينِ. وهو خاتمةُ الملفِّ ودليلُ استعمالِه.',
                ['الطبقةُ الأولى أمَّهاتُ الكتبِ: سيبويه، والمبرّدُ، وابنُ عقيلٍ، والأزهريُّ، وابنُ هشامٍ.',
                 'خُطُواتُ الإعرابِ السبعُ مُطبَّقةٌ على أمثلةٍ: من تحديدِ موضعِ الكلمةِ إلى تقديرِ المحذوفِ والتعليلِ.',
                 'كلُّ مسألةٍ خِلافيّةٍ مُنبَّهٌ عليهِ في بابِه، ولا يُنسَبُ خلافٌ إلى إجماعٍ.']),
}

# نصُّ كلِّ درسٍ في الشريطِ الجانبيِّ والفهرسِ مُشتَقٌّ من العنوانِ، ولا يُكتَبُ يدويًّا.

COLOR_CSS = """

/* ————— نسخةٌ ملوَّنةٌ: سبعُ وحداتٍ، وشريطُ معلوماتٍ لكلِّ درسٍ، وخريطةٌ وخلاصةٌ ————— */
main section > h2{display:block;background:linear-gradient(135deg,var(--h1),var(--h2));color:#fbf8f0;
  border:none;border-radius:13px;padding:.55em .9em;margin:.2em 0 .7em;text-align:center;
  font-size:1.62em;line-height:1.55;box-shadow:0 2px 0 rgba(0,0,0,.08)}
main section > h2 .num{color:#fff;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);
  border-radius:9px;padding:.02em .42em;font-size:.72em;margin-inline-end:.45em;vertical-align:.06em}
main h3{color:var(--ht);border-bottom:2px solid var(--hb);padding-bottom:.16em;border-radius:0}
main h4{color:var(--h1)}
main h4:before{content:"◆ ";color:var(--h2)}
main .lede{border-inline-start:5px solid var(--h2);background:var(--hm)}
.lbar{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:.15em 0 .8em}
.lbar .lb-t{background:linear-gradient(135deg,var(--h1),var(--h2));color:#fbf8f0;border-radius:99px;
  padding:.16em .8em;font-weight:800;font-size:.88em}
.lbar .lb-c{border:1px solid var(--hb);background:var(--hm);color:var(--ht);border-radius:99px;
  padding:.12em .7em;font-size:.84em;font-weight:700}
.lbar .lb-u{margin-inline-start:auto;font-size:.82em;color:var(--muted)}
.lmap{background:var(--hm);border:1px solid var(--hb);border-inline-start:5px solid var(--h2);
  border-radius:11px;padding:.65em .9em;margin:.2em 0 1em}
.lmap .lcap{display:block;color:var(--h1);font-weight:800;font-size:.92em;margin-bottom:.25em}
.lmap p{margin:0;font-size:.95em;line-height:1.9}
.lrecap{background:linear-gradient(135deg,var(--hm),#fff);border:1px dashed var(--h2);
  border-radius:11px;padding:.6em .9em .5em;margin:1.1em 0 .2em}
.lrecap .lcap{display:block;color:var(--h1);font-weight:800;font-size:.92em;margin-bottom:.3em}
.lrecap ul{margin:0;padding-inline-start:1.35em}
.lrecap li{margin:.18em 0;font-size:.93em;line-height:1.85}
.lrecap li:before{content:"◂ ";color:var(--h2)}
.unitmark{border-radius:14px;background:linear-gradient(135deg,var(--h1),var(--h2));color:#fbf8f0;
  padding:.85em 1.1em;margin:22px 0 14px;box-shadow:0 3px 14px rgba(0,0,0,.10)}
.unitmark .uk{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.38);
  border-radius:99px;padding:.05em .7em;font-size:.8em;font-weight:700;margin-bottom:.35em}
.unitmark .uh{display:block;font-size:1.3em;font-weight:800;line-height:1.5}
.unitmark p{margin:.35em 0 0;font-size:.92em;line-height:1.85;color:#f2eee4}
.unitmark .ul{display:flex;flex-wrap:wrap;gap:6px;margin-top:.55em}
.unitmark .ul a{background:#fffdfa;color:var(--h1);border-radius:8px;padding:.14em .6em;font-size:.84em;
  font-weight:700;text-decoration:none;border:1px solid rgba(255,255,255,.6)}
.legend{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:.9em 0 0;padding:.7em .9em;
  background:var(--paper,#fffdfa);border:1px solid var(--line);border-radius:12px}
.legend .lg{display:inline-flex;align-items:center;gap:.35em;border:1px solid var(--line);
  border-radius:99px;padding:.1em .7em;font-size:.86em;font-weight:700;color:var(--ink2);background:#fff}
.legend .lg i{width:.75em;height:.75em;border-radius:3px;background:var(--c);display:inline-block}
.unitcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin:1em 0}
.uc{border:1px solid var(--line);border-top:5px solid var(--h2);border-radius:13px;padding:.7em .85em;
  background:linear-gradient(180deg,var(--hm),#fff 60%)}
.uc b{display:block;color:var(--h1);font-size:1.02em;line-height:1.6}
.uc .uc-k{display:block;font-size:.8em;color:var(--muted);font-weight:700;letter-spacing:.4px}
.uc ul{list-style:none;margin:.4em 0 0;padding:0}
.uc li{margin:.2em 0;font-size:.9em}
.uc li:before{content:"● ";color:var(--h2);font-size:.7em;vertical-align:.15em}
body.sheets .unitmark,body.sheets .lmap,body.sheets .lrecap,body.sheets .lbar,
body.sheets .uc,body.sheets .legend{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body.sheets .sheet .lmap p,body.sheets .sheet .lrecap li{font-size:1em;line-height:inherit}
body.sheets .sheet main section > h2,body.sheets .sheet h2{font-size:1.45em;line-height:1.6}
body.sheets .sheet .lrecap{background:var(--hm)}
body.sheets .sheet .unitmark p,body.sheets .sheet .unitmark .ul a{font-size:1em}
@media print{
  .unitmark{-webkit-print-color-adjust:exact;print-color-adjust:exact;border-radius:0;box-shadow:none}
  main section > h2{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .legend{display:none}
}
nav.toc a.grp{padding-inline-start:.45em;border-inline-start:3px solid var(--uc,var(--line))}
.idxsub a{border-radius:6px;padding:0 .18em}
.idxsub a:hover{background:var(--green-soft)}
"""

# ————— أنماطُ الغلافِ الجديدِ —————
HERO_CSS = """
.hero{background:
  radial-gradient(120% 140% at 88% 8%, #12776a 0%, rgba(18,119,106,0) 55%),
  linear-gradient(120deg,#0d5c52 0%,#1b3f7a 34%,#5a2a7a 66%,#8e2440 100%)!important}
.hero-inner .badge{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.34)}
.hero-nav{display:flex;flex-wrap:wrap;gap:6px;margin:1.1em 0 0}
.hero-nav a{display:inline-flex;align-items:center;gap:.4em;background:rgba(255,255,255,.10);
  border:1px solid rgba(255,255,255,.28);border-radius:99px;padding:.2em .7em;font-size:.86em;
  font-weight:700;color:#f6f2e8;text-decoration:none}
.hero-nav a:hover{background:#fffdfa;color:#0d5c52}
.hero-nav a i{width:.7em;height:.7em;border-radius:2px;background:var(--c);display:inline-block}
.hero-how{margin:1em 0 0;padding:.7em .9em;border:1px dashed rgba(255,255,255,.4);border-radius:12px;
  font-size:.92em;line-height:1.85;color:#eee8dc}
.hero-how b{color:#ffe6ab}
"""


def slug_titles(html, sid):
    idx = {'h3': 0, 'h4': 0}
    items = []

    def repl(m):
        tag, attrs, txt = m.group(1), m.group(2), m.group(3)
        idx[tag] += 1
        new_id = "%s-%s%d" % (sid, tag[1], idx[tag])
        if 'id=' not in attrs:
            label = re.sub(r'<[^>]+>', '', txt).strip()
            items.append((tag, new_id, label))
            return '<%s%s id="%s">%s</%s>' % (tag, attrs, new_id, txt, tag)
        return m.group(0)

    out = re.sub(r'<(h3|h4)((?:[^>]|\n)*?)>((?:(?!</h3>|</h4>)[\s\S])*)</h[34]>', repl, html)
    return out, items


def counts_of(html):
    """عِدّادٌ صادقةٌ من نصِّ الدرسِ نفسِه."""
    rules = 0
    for ol in re.findall(r'(?is)<ol class="rules">.*?</ol>', html):
        rules += len(re.findall(r'(?is)<li\b', ol))
    return {
        'قواعدُ': rules,
        'أركانُ شرحٍ': len(re.findall(r'class="card"', html)),
        'أمثلةٌ': len(re.findall(r'class="box ex"', html)) + len(re.findall(r'class="stmt"', html)),
        'وجوهُ إعرابٍ': len(re.findall(r'class="irab"', html)),
        'جداولُ': len(re.findall(r'<table', html)),
    }


def main():
    parts = sorted(glob.glob(os.path.join(HERE, 'p*.html')))
    if not parts:
        sys.exit('لا توجد أجزاء في lessons-src/')
    style = ''
    if os.path.exists(REF):
        style = re.search(r'<style>.*?</style>', open(REF, encoding='utf-8').read(), re.S).group(0)
    paper = ''
    if os.path.exists(BUILD):
        pm = re.search(r'EXTRA_CSS = """(.*?)\n"""', open(BUILD, encoding='utf-8').read(), re.S)
        if pm:
            paper = pm.group(1)
    style = style.replace('</style>', paper + COLOR_CSS + HERO_CSS + '\n</style>')

    metas = []
    for path in parts:
        raw = open(path, encoding='utf-8').read().strip()
        m = re.search(r'<section id="([^"]+)"', raw)
        sid = m.group(1) if m else os.path.basename(path)[1:-5]
        raw, items = slug_titles(raw, sid)
        h2 = re.search(r'<h2>((?:(?!</h2>)[\s\S])*)</h2>', raw)
        title = re.sub(r'<[^>]+>', '', h2.group(1)).strip() if h2 else sid
        num = ''
        if h2:
            nn = re.search(r'<span class="num">(.*?)</span>', h2.group(1))
            num = nn.group(1) if nn else ''
            if nn:
                title = re.sub(r'^\s*' + re.escape(num) + r'\s*', '', title).strip()
        metas.append({'sid': sid, 'num': num, 'title': title, 'raw': raw, 'items': items})

    # ربطُ كلِّ درسٍ بوحدتِهِ
    unit_of = {}
    for ui, u in enumerate(UNITS):
        for k in u['idx']:
            if k < len(metas):
                unit_of[metas[k]['sid']] = ui
    for i, mt in enumerate(metas):
        mt['ui'] = unit_of.get(mt['sid'], len(UNITS) - 1)
        mt['hue'] = UNITS[mt['ui']]['pal']

    # ————— إضافةُ الشريطِ والخريطةِ والخلاصةِ، وتلوينُ العناوينِ —————
    for mt in metas:
        h1, h2c, hb, hm, ht = mt['hue']
        hue = '--h1:%s;--h2:%s;--hb:%s;--hm:%s;--ht:%s' % (h1, h2c, hb, hm, ht)
        raw = mt['raw']
        raw = raw.replace('<h2>', '<h2 style="%s">' % hue, 1)
        raw = re.sub(r'<(h[34])([^>]*?)>',
                     lambda m: '<%s%s style="--h1:%s;--h2:%s;--hb:%s;--ht:%s">' % (m.group(1), m.group(2), h1, h2c, hb, ht),
                     raw)
        cnt = counts_of(raw)
        c = [k for k, v in cnt.items() if v]
        chips = ''.join('<span class="lb-c">%s: %s</span>' % (k, ar(cnt[k])) for k in c)
        bar = ('\n  <div class="lbar" style="%s"><span class="lb-t">الدرسُ %s — %s</span>%s'
               '<span class="lb-u">الوحدةُ %s من %s</span></div>') % (
            hue, mt['num'], UNITS[mt['ui']]['name'], chips,
            ar(mt['ui'] + 1), ar(len(UNITS)))
        extra = EXTRA.get(mt['sid'])
        inject = bar
        if extra:
            inject += ('\n  <div class="lmap" style="%s"><b class="lcap">خريطةُ هذا الدرسِ</b><p>%s</p></div>'
                       % (hue, extra[0]))
        mt['raw'] = raw.replace('</h2>', '</h2>' + inject, 1) if '</h2>' in raw else raw + inject
        if extra and extra[1]:
            recap = ('\n  <div class="lrecap" style="%s"><b class="lcap">خلاصةٌ في ثلاثِ سطورٍ</b><ul>%s</ul></div>'
                     % (hue, ''.join('<li>%s</li>' % x for x in extra[1])))
            pos = mt['raw'].rfind('</section>')
            if pos > -1:
                mt['raw'] = mt['raw'][:pos] + recap + mt['raw'][pos:]
            else:
                mt['raw'] += recap

    # ————— روابطُ سبقٍ ولحوقٍ ملوَّنةٌ —————
    n_all = len(metas)
    for i, mt in enumerate(metas):
        cells = []
        if i > 0:
            p_ = metas[i - 1]
            cells.append('<a href="#%s"><span class="small">الدرسُ السابق</span> <b>%s</b>%s</a>'
                         % (p_['sid'], p_['num'], p_['title']))
        if i + 1 < n_all:
            n_ = metas[i + 1]
            cells.append('<a href="#%s"><span class="small">الدرسُ التالي</span> <b>%s</b>%s</a>'
                         % (n_['sid'], n_['num'], n_['title']))
        if cells:
            pos = mt['raw'].rfind('</section>')
            mt['raw'] = mt['raw'][:pos] + '\n  <div class="pager">' + ''.join(cells) + '</div>' + mt['raw'][pos:]

    # ————— فواصلُ الوحداتِ —————
    for ui, u in enumerate(UNITS):
        h1, h2c, hb, hm, ht = u['pal']
        hue = '--h1:%s;--h2:%s;--hb:%s;--hm:%s;--ht:%s' % (h1, h2c, hb, hm, ht)
        lessons = [metas[k] for k in u['idx'] if k < len(metas)]
        links = ''.join('<a href="#%s">%s %s</a>' % (mt['sid'], mt['num'], mt['title']) for mt in lessons)
        mark = ('<div class="unitmark" style="%s"><span class="uk">الوحدةُ %s</span>'
                '<b class="uh">%s</b><p>%s</p><div class="ul">%s</div></div>') % (
            hue, ar(ui + 1), u['name'], u['intro'], links)
        first = lessons[0]['raw']
        lessons[0]['raw'] = mark + '\n' + first

    # ————— الفهرسُ الملوَّنُ —————
    idx = []
    for ui, u in enumerate(UNITS):
        h1, h2c, hb, hm, ht = u['pal']
        hue = '--h1:%s;--h2:%s;--hb:%s;--hm:%s;--ht:%s' % (h1, h2c, hb, hm, ht)
        subs = []
        for k in u['idx']:
            mt = metas[k]
            sub = ' '.join('<a href="#%s" class="%s">%s</a>' % (i2, ('subsub' if t == 'h4' else ''), l)
                           for t, i2, l in mt['items'])
            subs.append('<li><a href="#%s"><b>%s</b>%s</a>%s</li>' % (
                mt['sid'], mt['num'], mt['title'],
                ('\n      <div class="idxsub">%s</div>' % sub) if sub else ''))
        idx.append('<li class="uc-i" style="%s"><a href="#toc-u%s"><b>الوحدةُ %s</b> — %s</a>'
                   '<div class="idxsub">%s</div></li>'
                   % (hue, ar(ui + 1), ar(ui + 1), u['name'], ''.join(subs)))

    cards = []
    for ui, u in enumerate(UNITS):
        h1, h2c, hb, hm, ht = u['pal']
        hue = '--h1:%s;--h2:%s;--hb:%s;--hm:%s;--ht:%s' % (h1, h2c, hb, hm, ht)
        lessons = [metas[k] for k in u['idx'] if k < len(metas)]
        lis = ''.join('<li><a href="#%s">%s %s</a></li>' % (mt['sid'], mt['num'], mt['title']) for mt in lessons)
        cards.append('<div class="uc" id="toc-u%s" style="%s"><span class="uc-k">الوحدةُ %s</span>'
                     '<b>%s</b><ul>%s</ul></div>'
                     % (ar(ui + 1), hue, ar(ui + 1), u['name'], lis))

    legend = ('<div class="legend">'
              '<b>دليلُ الألوانِ:</b>'
              '<span class="lg" style="--c:#0d5c52"><i></i>جملةُ الابتداءِ</span>'
              '<span class="lg" style="--c:#1b3f7a"><i></i>الجملةُ الفعليّةُ</span>'
              '<span class="lg" style="--c:#8a5a12"><i></i>المفعولاتُ</span>'
              '<span class="lg" style="--c:#5a2a7a"><i></i>الإشارةُ والموصولُ</span>'
              '<span class="lg" style="--c:#8e2440"><i></i>التوابعُ</span>'
              '<span class="lg" style="--c:#0e6274"><i></i>الحالُ والتمييزُ والإضافةُ</span>'
              '<span class="lg" style="--c:#4a4238"><i></i>الملاحقُ</span>'
              '<span class="lg" style="--c:#e7d9b6"><i></i>مثالٌ مشكولٌ</span>'
              '<span class="lg" style="--c:#123a34"><i></i>وجهُ الإعرابِ</span>'
              '<span class="lg" style="--c:#b4432f"><i></i>خطأٌ شائعٌ</span>'
              '</div>')

    toc_html = ('<section id="toc">\n'
                '  <h2 style="--h1:#0d5c52;--h2:#5a2a7a;--hb:#cfe7e0;--hm:#f2fbf8;--ht:#0b4b43">'
                '<span class="num">٭</span>الفهرسُ الملوَّنُ التفصيليُّ</h2>\n'
                '  <p>سبعُ وحداتٍ ملوَّنةٍ، لكلِّ وحدةٍ لونُها: شريطٌ أعلى كلِّ درسٍ يُخبِرُك بعددِ '
                'قواعدِهِ وأمثلةِهِ ووجوهِ إعرابِهِ، و«خريطةُ هذا الدرسِ» تمهيدٌ قبلَ الدخولِ، و'
                '«خلاصةٌ في ثلاثِ سطورٍ» بعدَ الفراغِ. ثمَّ في آخرِ كلِّ درسٍ جدولُ «مواضعُ الدرسِ» '
                'في الأبوابِ الستّةِ: الأساليبِ، والتقديمِ والتأخيرِ، والحذفِ، والنواصبِ، والنواسخِ، '
                'والتراكيبِ الخاصّةِ.\n' + legend + '</p>\n'
                '  <div class="unitcards">' + ''.join(cards) + '</div>\n'
                '  <ol class="idxlist">\n' + '\n'.join(idx) + '\n  </ol>\n</section>')
    foot_html = ('<footer>\n  <p>شرحُ الدروسِ — نسخةٌ ملوَّنةٌ: ملفٌّ قائمٌ بنفسه، يعملُ بلا إنترنت، '
                 'وكلُّ رابطٍ داخليٍّ مُتحقَّقٌ منه. التقطيعُ والصفحاتُ محفورٌ وقتَ البناءِ، فلا يختلفُ '
                 'عرضُ الشاشةِ عن الطباعةِ. راجِعْهُ مع «دروسِ الإعراب الأربعةَ عشرَ» الأصلِيَّةِ '
                 'و«الدليل الشامل في النحو العربي والبلاغة».</p>\n</footer>')

    body = ''.join(mt['raw'] for mt in metas)
    main_src = toc_html + '\n' + body + '\n' + foot_html
    titles = {mt['sid']: (mt['num'] + ' ' + mt['title']).strip() for mt in metas}
    sheets_html, total_pages = PG.paginate(main_src, titles, cover=True)
    pages_html = '<div class="book">\n' + sheets_html + '\n</div>'

    stats = {
        'lessons': sum(1 for mt in metas if re.match(r'^l\d+$', mt['sid'])),
        'appendix': sum(1 for mt in metas if not re.match(r'^l\d+$', mt['sid'])),
        'heads': len(re.findall(r'<h3', body)) + len(re.findall(r'<h4', body)),
        'tables': body.count('<table'),
        'examples': body.count('class="box ex"') + body.count('class="stmt"'),
        'irab': body.count('class="irab"'),
    }

    hero_nav = ''.join('<a href="#%s" style="--c:%s"><i></i>%s %s</a>'
                       % (mt['sid'], mt['hue'][0], mt['num'], mt['title']) for mt in metas)
    unit_links = ''.join('<a href="#toc-u%s" style="--c:%s"><i></i>الوحدةُ %s</a>'
                         % (ar(ui + 1), u['pal'][0], ar(ui + 1)) for ui, u in enumerate(UNITS))

    nav = []
    for mt in metas:
        nav.append('      <a class="grp" href="#%s" style="--uc:%s"><b>%s</b>%s</a>\n'
                   % (mt['sid'], mt['hue'][0], mt['num'], mt['title']))

    doc = '''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>شرحُ الدروسِ — نسخةٌ ملوَّنةٌ ومنظَّمةٌ: أربعةَ عشرَ درسًا وأربعةَ ملاحقِ</title>
<meta name="description" content="ملفٌّ جديدٌ ملوَّنٌ ومنسَّقٌ ومفهرَسٌ لشرحِ دروسِ الإعرابِ: سبعُ وحداتٍ ملوَّنةٍ، لكلِّ درسٍ شريطُ معلوماتٍ وخريطةٌ وخلاصةٌ، وفهرسٌ تفصيليٌّ بكلِّ مبحثٍ، وجدولُ مواضعَ لكلِّ درسٍ، وثوابتٌ وبوّاباتٌ ومصفوفةٌ ومصادرُ. بمقاسِ صفحاتِ Word وترقيمٍ ثابتٍ.">
__STYLE__
</head>
<body class="sheets">
<div class="toolbar no-print">
  <button onclick="document.body.classList.toggle('sheets')">عرضٌ ورقيٌّ (أوراقٌ مثبَّتةٌ) / عرضٌ متَّصلٌ</button>
  <button onclick="document.body.classList.toggle('plain')">بلا تلوينٍ (أبيضُ وأسودَ)</button>
  <button onclick="window.print()">طباعةٌ أو حفظٌ في ملفٍ مستقلٍّ</button>
  <span class="hint">سبعُ وحداتٍ ملوَّنةٍ: اللونُ يُعرِّفُ البابَ لا الجمالَ — كلُّ درسٍ يحملُ لونَ وحدتِهِ في عنوانِهِ وشريطِهِ وخريطتِهِ وخلاصتِهِ. المقاسُ مقاسُ وورد: ٢١ × ٢٩٫٧ سم، وهوامشُ ٢٫٥٤ و٣٫١٨ سم، وخطٌّ ١١٫٥ نقطةً بسطرٍ ١٫٩٥ وتبريرٍ. التقطيعُ محفورٌ وقتَ البناءِ: __TOTAL__ صفحةً.</span>
</div>
<header class="hero">
  <div class="hero-inner">
    <span class="badge">ملوَّنٌ · منظَّمٌ · مفهرَسٌ · بشرحٍ جديدٍ قبلَ كلِّ درسٍ</span>
    <h1>شرحُ الدروسِ الأربعةَ عشرَ</h1>
    <p class="sub">نسخةٌ مُعادُ ترتيبِها للدراسةِ لا للمرجَعِ وحدَهُ: سبْعُ وحداتٍ ملوَّنةٍ يَجري فيها
    المحوَرُ من الأُولى إلى السادسةِ ثمَّ تُختَمُ بالملاحقِ. قبلَ كلِّ درسٍ «خريطةٌ» تُمهِّدُ، 
    وبعدَهُ «خلاصةٌ في ثلاثِ سطورٍ»، وفوقَهُما شريطٌ يُخبِرُ كم في الدرسِ من قاعدةٍ ومثالٍ ووجهِ إعرابٍ.</p>
    <div class="hero-stats">
      <span>🎨 ٧ وحداتٍ ملوَّنةٍ</span>
      <span>📚 __NLESSONS__ درسًا مفصَّلًا</span>
      <span>🧾 __NAPP__ ملاحقَ جامعة</span>
      <span>🗂️ __NHEADS__ مبحثًا فرعيًّا</span>
      <span>📐 __NTABLES__ جدولًا</span>
      <span>🖋️ __NEX__ مثالًا مشكولًا</span>
      <span>🔎 __NIRAB__ وجهًا إعرابيًّا</span>
      <span>📄 __TOTAL__ صفحةً مثبَّتةَ الترقيمِ</span>
    </div>
    <div class="hero-nav">__UNITS__</div>
    <div class="hero-nav">__LESSONS__</div>
    <div class="hero-how"><b>كيفَ تقرأُ هذا الملفَّ؟</b> إن كنتَ تبدأُ من الصفرِ: الوحدةُ <b>الأُولى</b> ثمَّ <b>الثانيةُ</b> ثمَّ <b>الثالثةُ</b>، ولا تَتجاوَزْ درسًا قبلَ أن تقرأَ «خلاصتَهُ»
    وتُصحِّحَ «أخطاءَهُ الشائعةَ». وإن كنتَ راجعًا للاختبارِ: اقرأ «خلاصةٌ في ثلاثِ سطورٍ» لكلِّ 
    درسٍ، ثمَّ ارجِعْ إلى «ملاحقُ» — البوّاباتُ والمصفوفةُ تُغنيانِ عن إعادةِ القراءةِ. وللطباعةِ 
    أو للحفظِ في ملفٍ مستقلٍّ اضغطْ زرَّ الطباعةِ: الأوراقُ والصفحاتُ كما تراها الآنَ.</div>
    <div class="hero-callout">
      <span class="big">﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ﴾</span>
      <span class="small">مثالٌ يُطبَّقُ في الوحدةِ الأُولى: «الحَيُّ القَيُّومُ» خبرٌ لمبتدأٍ محذوفٍ وجوبًا، و«إلّا» أداةُ حصرٍ، و«هُوَ» ضميرٌ منفصلٌ في محلِّ رفعٍ مبتدأٌ.</span>
    </div>
  </div>
  <p class="pnum">صفحةُ ١ من __TOTAL__</p>
</header>
<div class="layout">
  <nav class="toc">
    <h4>الفهرس</h4>
    <a class="grp" href="#toc"><b>٭</b>الفهرسُ الملوَّنُ</a>
__NAV__      <a class="grp" href="#matrix"><b>٭</b>مصفوفةُ المواضعِ</a>
  </nav>
  <main>
__PAGES__
  </main>
</div>
</body>
</html>
'''
    doc = (doc.replace('__STYLE__', style)
              .replace('__TOTAL__', ar(total_pages))
              .replace('__NLESSONS__', ar(stats['lessons']))
              .replace('__NAPP__', ar(stats['appendix']))
              .replace('__NHEADS__', ar(stats['heads']))
              .replace('__NTABLES__', ar(stats['tables']))
              .replace('__NEX__', ar(stats['examples']))
              .replace('__NIRAB__', ar(stats['irab']))
              .replace('__UNITS__', unit_links)
              .replace('__LESSONS__', hero_nav)
              .replace('__NAV__', ''.join(nav))
              .replace('__PAGES__', pages_html))

    plain_css = """
body.plain main section > h2{background:none;color:var(--ink);border:1px solid var(--line);box-shadow:none}
body.plain main h4:before{content:""}
body.plain .lmap,body.plain .lrecap,body.plain .unitmark{background:#fff;color:var(--ink);border:1px solid var(--line)}
body.plain .unitmark .uk,body.plain .lbar .lb-t{background:#fff;color:var(--ink);border:1px solid var(--line)}
body.plain .unitmark p,body.plain .unitmark .uh,body.plain .lbar .lb-c{color:var(--ink)}
body.plain .lbar .lb-c{background:#fff}
body.plain .unitmark .ul a{background:#fff;color:var(--ink)}
"""
    doc = doc.replace('</style>', plain_css + '</style>', 1)
    open(OUT, 'w', encoding='utf-8').write(doc)

    # ————— الفحوصُ —————
    from html.parser import HTMLParser
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
            'param', 'source', 'track', 'wbr'}

    class P(HTMLParser):
        def __init__(s):
            super().__init__(convert_charrefs=True)
            s.st = []
            s.err = []

        def handle_starttag(s, t, a):
            if t not in VOID:
                s.st.append((t, s.getpos()[0]))

        def handle_endtag(s, t):
            if t in VOID:
                return
            if s.st and s.st[-1][0] == t:
                s.st.pop()
            else:
                s.err.append('</%s> سطر %d' % (t, s.getpos()[0]))

    p = P()
    p.feed(doc)
    for t, l in p.st:
        p.err.append('وسمٌ غيرُ مغلق <%s> سطر %d' % (t, l))
    ids = set(re.findall(r'id="([^"]+)"', doc))
    broken = [h for h in set(re.findall(r'href="#([^"]+)"', doc)) if h not in ids]
    mism = []
    for tm in re.finditer(r'<table.*?</table>', doc, re.S):
        blk = tm.group(0)
        head = len(re.findall(r'<th[ >]', blk))
        active = []
        for rm in re.finditer(r'<tr>(.*?)</tr>', blk, re.S):
            row = rm.group(1)
            cells = len(re.findall(r'<t[dh][ >]', row)) + len(active)
            active = [a - 1 for a in active if a > 1]
            active += [int(x) - 1 for x in re.findall(r'rowspan="(\d+)"', row) if int(x) > 1]
            if head and cells and cells != head:
                mism.append((head, cells, re.sub(r'\s+', ' ', row)[:44]))
    vis = re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>|<script.*?</script>', '', doc, flags=re.S))
    print('=== البناءُ تمَّ ===')
    print('KB:', round(len(doc.encode()) / 1024, 1), '| أوراقٌ:', doc.count('<div class="sheet'),
          '| أقسامٌ:', doc.count('<section'), '| جداولٌ:', doc.count('<table'))
    print('أخطاء الوسوم:', len(p.err), p.err[:4])
    print('روابطُ معطوبةٌ:', broken[:6], len(broken))
    print('خلايا جداولَ غيرُ متوافقةٍ:', mism[:3], len(mism))
    print('حروفٌ لاتينيةٌ مرئيّةٌ:', len(re.findall(r'[A-Za-z]', vis)),
          '| أرقامٌ لاتينيةٌ:', len(re.findall(r'[0-9]', vis)),
          '| «»', vis.count('«') - vis.count('»'), '| ﴿﴾', vis.count('﴿'), vis.count('﴾'))
    print('أقواسُ CSSٌ:', re.search(r'<style>(.*?)</style>', doc, re.S).group(1).count('{'),
          re.search(r'<style>(.*?)</style>', doc, re.S).group(1).count('}'))
    print('عددُ الوحداتِ الملوَّنةِ:', doc.count('class="unitmark"'), '| خرائطُ:', doc.count('class="lmap"'),
          '| خلاصاتٌ:', doc.count('class="lrecap"'), '| أشرطةٌ:', doc.count('class="lbar"'))


main()
