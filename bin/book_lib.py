import yaml

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

    cover = 'Gameki/Templates/cover.tex'
    booklet = ['listchar', 'listblue', 'listgreen']
    back = 'abilstats'
    try:
        config = yaml.safe_load(open(GAMEKI_DIR + 'config.yaml'))
    except IOError:
        pass
    else:
        if 'cover' in configL
            cover = config['cover']
        if 'booklet' in config:
            booklet = config['booklet']
        if 'back' in config:
            back = config['back']

    run_infix = ''
    if not pdfdir:
        pdfdir = 'Out/book/'
        if run is not None:
            run_infix = '%s-' % run

    rules = get_pdf_path('Handouts/rules-scenario.tex')
    for i in xrange(len(macros)):
        m = macros[i]

        def get_page_path(p):
            if '/' in p:
                return get_pdf_path(p, m, run=run)
            else:
                return get_pdf_path('%s-%s%s' % (p, run_infix, m),
                                    color_sheets=True)

        sheets = [cover, rules]
        for p in booklet:
            sheet = get_page_path(p)
            if sheet:
                sheets.append(sheet)
        back_page = get_page_path(back)

        try:
            os.makedirs(pdfdir)
        except OSError:
            pass
        if use_names:
            name = names[i].replace('/', '-').encode('utf-8')
        else:
            name = m[1:]
        joined = '%s/%s%s-packet.pdf' % (pdfdir, run_infix, name)
        run_cmd('pdfjoin', ['-o', joined] + sheets)
        yield joined
        statcard_out = '%s/%s%s-statcard.pdf' % (pdfdir, run_infix, name)
        run_cmd('cp', [back_page, statcard_out])
        yield statcard_out
        book = '%s/%s%s-booklet.pdf' % (pdfdir, run_infix, name)
        run_cmd(GAMEKI_DIR + 'bin/backbook.sh', [joined, back_page, book])
        yield book
