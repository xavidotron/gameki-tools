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

    packet = 'Gameki/Templates/packet.tex'
    epacket = 'Gameki/Templates/epacket.tex'

    run_infix = ''
    if not pdfdir:
        pdfdir = 'Out/book/'
        if run is not None:
            run_infix = '%s-' % run

    for i in xrange(len(macros)):
        m = macros[i]

        def get_page_path(p):
            if '/' in p:
                return get_pdf_path(p, m, run=run)
            else:
                return get_pdf_path('%s-%s%s' % (p, run_infix, m),
                                    color_sheets=True)

        epages = None
        if '/' in m:
            pages = get_pdf_path(m, run=run)
            name = m.rsplit('/', 1)[-1].split('.', 1)[0]
        else:
            pages = get_page_path(packet)
            epages = get_page_path(epacket)
            if use_names:
                name = names[i].replace('/', '-').encode('utf-8')
            else:
                name = m
        yield pages
        if epages:
            yield epages

        try:
            os.makedirs(pdfdir)
        except OSError:
            pass
        book = '%s%s%s-booklet.pdf' % (pdfdir, run_infix, name)
        run_cmd('pdfbook', ['--short-edge', '--paper', 'letter',
                            '-o', book, pages])
        yield book
