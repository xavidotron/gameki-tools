from prod_lib import *

def get_book_paths(run=None, use_names=False, pdfdir=None, macros=None):
    if not macros:
        macros = [
            unicode(m[1:].strip(), 'utf-8')
            for m in
            get_text(GAMEKI_DIR + 'lib/charmacros.tex').strip().split('\n')]

    if use_names:
        names = [
            unicode(m.strip(), 'utf-8')
            for m in
            get_text(GAMEKI_DIR + 'lib/charnames.tex',
                     run=run).strip().split('\n')]

    run_infix = ''
    if not pdfdir:
        pdfdir = 'Out/book/'
        if run is not None:
            run_infix = '%s-' % run

    rules = get_pdf_path('Handouts/rules-scenario.tex')
    for i in xrange(len(macros)):
        m = macros[i]
        cover = get_pdf_path('Gameki/Templates/cover.tex', m, run=run)
        image = get_pdf_path('image-%s%s' % (run_infix, m))
        body = get_pdf_path('listchar-%s%s' % (run_infix, m), color_sheets=True)
        blues = get_pdf_path('listblue-%s%s' % (run_infix, m),
                             color_sheets=True)
        #body = get_pdf_path('Charsheets/%s.tex' % m[2:], run=run)
        #statcard = get_pdf_path('statcards-%s%s' % (run_infix, m))
        statcard = get_pdf_path('abilstats-%s%s' % (run_infix, m))

        try:
            os.makedirs(pdfdir)
        except OSError:
            pass
        if use_names:
            name = names[i].replace('/', '-').encode('utf-8')
        else:
            name = m[1:]
        joined = '%s/%s%s-packet.pdf' % (pdfdir, run_infix, name)
        sheets = [cover, rules, image, body]
        if blues:
            sheets.append(blues)
        run_cmd('pdfjoin', ['-o', joined] + sheets)
        yield joined
        statcard_out = '%s/%s%s-statcard.pdf' % (pdfdir, run_infix, name)
        run_cmd('cp', [statcard, statcard_out])
        yield statcard_out
        book = '%s/%s%s-booklet.pdf' % (pdfdir, run_infix, name)
        run_cmd(GAMEKI_DIR + 'bin/backbook.sh', [joined, statcard, book])
        yield book
