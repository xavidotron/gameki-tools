import subprocess, sys, os

GAMEKI_DIR = os.path.relpath(os.path.dirname(os.path.dirname(__file__)))

def run(program, args):
    cmd = [program] + args
    print cmd
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        sys.stderr.write("Running command: %s\n\n" % ' '.join(cmd))
        sys.stderr.write(stderr)
        sys.stderr.write("`%s` exited with status %d.\n" % (
                ' '.join(cmd), process.returncode))
        sys.exit(1)
    return stdout

def prod(target, extra_args=[]):
    return run(GAMEKI_DIR + '/bin/prod', extra_args + [target])

def get_pdf_path(target, jobname=None):
    if target.startswith('joined-'):
        m = target[len('joined-'):]
        # TODO(xavid); this should come from config.yaml
        in_paths = [get_pdf_path('Handouts/cover.tex', m),
                    get_pdf_path('Handouts/rules-scenario.tex'),
                    get_pdf_path('Gen/Charsheets/%s.tex' % m[1:])]
        out_path = 'Out/prod/%s.pdf' % target
        run('pdfjoin', ['-o', out_path] + in_paths)
        return out_path

    args = []
    if jobname:
        args += ['-j', jobname]
    prod(target, args)
    if jobname:
        return 'Out/%s/%s.pdf' % (os.path.basename(target)[:-len('.tex')],
                                  jobname)
    elif '/' in target:
        assert target.endswith('.tex')
        return 'Out/' + target[:-len('.tex')] + '.pdf'
    else:
        return 'Out/prod/%s.pdf' % target

def get_pdf(target):
    pdf = get_pdf_path(target)
    with open(pdf) as fil:
        return fil.read()

def get_text(tex, jobname=None):
    assert tex.endswith('.tex'), tex
    args = ['-t']
    if jobname:
        args.append('-j')
        args.append(jobname)
    return prod(tex, args)
