import subprocess, sys, os

def prod(target, extra_args=[]):
    cmd = [os.path.dirname(__file__) + '/prod'] + extra_args + [target]
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

def get_pdf(target):
    prod(target)
    if '/' in target:
        assert target.endswith('.tex')
        pdf = 'Out/' + target[:-len('.tex')] + '.pdf'
    else:
        pdf = 'Out/prod/%s.pdf' % target
    with open(pdf) as fil:
        return fil.read()

def get_text(tex, jobname=None):
    assert tex.endswith('.tex'), tex
    args = ['-t']
    if jobname:
        args.append('-j')
        args.append(jobname)
    return prod(tex, args)
