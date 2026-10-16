# -*- coding: utf-8 -*-
# مُولِّد كتلِ «شرحِ المصفوفةِ» — يُستعمَل من جلسات التحرير فقط
def emit(sid,label,rows):
    out=['\n  <h3>الدرسُ %s</h3>'%label,
         '  <p class="small">تفصيلُ هذا البابِ في <a href="#%s">درسِه</a>، وهذا شرحُ بوّاباتِه الستِّ على نحوٍ مستقلٍّ.</p>'%sid]
    for bab,qaid,sharh,exs,has in rows:
        out.append('  <h4>البابُ: %s</h4>'%bab)
        out.append('  <div class="box"><span class="tag">القاعدةُ</span> %s</div>'%qaid)
        out.append('  <div class="box note"><span class="tag">الشرحُ المفصَّلُ</span> %s</div>'%sharh)
        for stmt,items in exs:
            lis=''.join('<li>%s</li>'%i for i in items)
            out.append('  <div class="irab"><span class="stmt">%s</span><ul>%s</ul></div>'%(stmt,lis))
        out.append('  <div class="box ex"><span class="tag">المحصَّلَةُ</span> %s</div>'%has)
    return '\n'.join(out)+'\n'
