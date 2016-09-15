from prod_lib import *

def get_book_paths(run=None, use_names=False, pdfdir=None):
    macros = [
        unicode(m.strip(), 'utf-8')
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
        cover = get_pdf_path('Handouts/cover.tex', m[1:], run=run)
        body = get_pdf_path('Charsheets/%s.tex' % m[2:], run=run)
        statcard = get_pdf_path('statcards-%s%s' % (run_infix, m[1:]))

        try:
            os.makedirs(pdfdir)
        except OSError:
            pass
        if use_names:
            name = names[i].replace('/', '-').encode('utf-8')
        else:
            name = m[1:]
        joined = '%s/%s%s-packet.pdf' % (pdfdir, run_infix, name)
        run_cmd('pdfjoin', ['-o', joined, cover, rules, body])
        yield joined
        statcard_out = '%s/%s%s-statcard.pdf' % (pdfdir, run_infix, name)
        run_cmd('cp', [statcard, statcard_out])
        yield statcard_out
        book = '%s/%s%s-booklet.pdf' % (pdfdir, run_infix, name)
        run_cmd('Gameki/bin/backbook.sh', [joined, statcard, book])
        yield book
