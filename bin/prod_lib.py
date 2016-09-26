import subprocess, sys, os

from dirs_lib import *

def run_cmd(program, args, accept_no_output=False):
    cmd = [program] + args
    #print ' '.join("'%s'" % e if ' ' in e else e for e in cmd)
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        if (accept_no_output
            and ("pdflatex: failed to create output file" in stderr
                 or "Latexmk: Log file says no output from latex" in stderr)
            and "! " not in stderr):
            # Exited successfully, but no output.
            return False
        else:
            sys.stderr.write("Running command: %s\n\n" % ' '.join(cmd))
            sys.stderr.write(stderr)
            sys.stderr.write("`%s` exited with status %d.\n" % (
                    ' '.join(cmd), process.returncode))
            sys.exit(1)
    if accept_no_output:
        return True
    else:
        return stdout

def prod(target, extra_args=[], **kw):
    return run_cmd(GAMEKI_DIR + 'bin/prod', extra_args + [target], **kw)

def get_pdf_path(target, jobname=None, single_sided=False, color_sheets=False,
                 run=None):
    if target.startswith('joined-'):
        m = target[len('joined-'):]
        # TODO(xavid); this should come from config.yaml
        in_paths = [
            get_pdf_path('listchar-%s' % m),
            get_pdf_path('listblue-%s' % m),
            get_pdf_path('listgreen-%s' % m),
            get_pdf_path('abils-%s' % m),
            ]
        out_path = TOP_DIR + 'Out/prod/%s.pdf' % target
        run_cmd('pdfjoin', ['-o', out_path] + in_paths)
        return out_path

    args = []
    if jobname:
        args += ['-j', jobname]
    if single_sided:
        args.append('-s')
    elif color_sheets:
        args.append('-c')
    if run is not None:
        args += ['-r', run]

    if jobname:
        if run is not None:
            outfile = TOP_DIR + 'Out/file/%s:%s:%s.pdf' % (
                run, target[:-len('.tex')], jobname)
        else:
            outfile = TOP_DIR + 'Out/%s/%s.pdf' % (
                os.path.basename(target)[:-len('.tex')], jobname)
        if '/' in target:
            target = TOP_DIR + target
    elif '/' in target:
        assert target.endswith('.tex')
        if run is not None:
            outfile = TOP_DIR + 'Out/file/%s:%s.pdf' % (
                run, target[:-len('.tex')])
        else:
            outfile = TOP_DIR + 'Out/' + target[:-len('.tex')] + '.pdf'
        target = TOP_DIR + target
    elif single_sided:
        outfile = TOP_DIR + 'Out/single/%s.pdf' % target
    elif color_sheets:
        outfile = TOP_DIR + 'Out/color/%s.pdf' % target
    else:
        outfile = TOP_DIR + 'Out/prod/%s.pdf' % target

    if not prod(target, args, accept_no_output=True):
        return None
    return outfile

def get_pdf(target):
    pdf = get_pdf_path(target)
    with open(pdf) as fil:
        return fil.read()

def get_text(tex, jobname=None, run=None):
    assert tex.endswith('.tex'), tex
    args = ['-t']
    if jobname:
        args.append('-j')
        args.append(jobname)
    if run is not None:
        args += ['-r', run]
    return prod(tex, args)
