import subprocess, sys, os, glob
import yaml

from dirs_lib import *

def run_cmd(program, args, accept_no_output=False, env=None, verbose=False):
    cmd = [program] + args
    #print ' '.join("'%s'" % e if ' ' in e else e for e in cmd)
    process = subprocess.Popen(cmd, env=env,
                               stdout=None if verbose else subprocess.PIPE,
                               stderr=None if verbose else subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        if (accept_no_output
            and ("pdflatex: failed to create output file" in stderr
                 or "Latexmk: Log file says no output from latex" in stderr)
            and "! " not in stderr):
            # Exited successfully, but no output.
            return False
        else:
            if stderr is not None:
                sys.stderr.write("Running command: %s\n\n" % ' '.join(cmd))
                sys.stderr.write(stderr)
            sys.stderr.write("`%s` exited with status %d.\n" % (
                    ' '.join(cmd), process.returncode))
            sys.exit(1)
    if accept_no_output:
        return True
    else:
        return stdout

# Not all versions of latexmk support the -lualatex flag directly, so spell it
# out.
LATEX_MAP = dict(lualatex="-pdflatex=lualatex %O %S",
                 xelatex="-xelatex",
                 pdflatex=None)
default_latex = 'pdflatex'
try:
    config = yaml.safe_load(open(GAMEKI_DIR + 'config.yaml'))
except IOError:
    pass
else:
    if 'latex' in config:
        default_latex = config['latex']

def prod(target, jobname=None, single_sided=False, color_sheets=False,
         run=None, text=False, latex=None, outdir=None,
         accept_no_output=False, verbose=False):
    reldir = ""
    updir = ""
    if not os.path.exists("LaTeX"):
        updir = os.path.basename(os.getcwd())
        reldir = ".."
        while not os.path.exists(os.path.join(reldir, "LaTeX")):
            updir = os.path.join(os.path.basename(os.path.abspath(reldir)),
                                 updir)
            reldir = os.path.join("..", reldir)
            if os.path.abspath(reldir) == "/":
                print >>sys.stderr, "No LaTeX directiory found; are you in a GameTeX directory?"
                sys.exit(1)
    dir = os.path.abspath(reldir)
    if not outdir:
        outdir = "Out"
        if reldir:
            outdir = os.path.join(reldir, outdir)

    clses = glob.glob(os.path.join(dir, 'LaTeX', '*.cls'))
    assert len(clses) == 1, clses
    gameclassname = os.path.basename(clses[0]).split('.', 1)[0]
    env = {
        "TEXINPUTS": "%s/LaTeX/:%s/Gameki/lib/:" % (dir, dir),
        "gameclassname": gameclassname,
        gameclassname: dir,
        "PATH": os.environ["PATH"],
        "USER": os.environ["USER"],
        }

    tex = "prod"
    if single_sided:
        tex = "single"
    if color_sheets:
        tex = "color"

    if '-' in target and '.' not in target:
        # If the arg has a dash and no dot, then it's a jobname to pass to
        # Gameki/LaTeX/prod.tex.
        texfile = os.path.join(dir, 'Gameki', 'lib', tex + '.tex')
        jobname = target
    else:
        texfile = target

    flags = ["-halt-on-error", "-interaction=nonstopmode", "-pdf"]
    if text:
        flags.append(LATEX_MAP['lualatex'])
    else:
        if latex is None:
            latex = default_latex
        if LATEX_MAP[latex]:
            flags.append(LATEX_MAP[latex])

    if run:
        jn = run + ":" + texfile.split('.', 1)[0]
	if jobname:
	    jn += ":" + jobname
	flags.append("-jobname=" + jn)
        texfile = os.path.join(dir, "Gameki", "lib", "file.tex")
	od = os.path.join(outdir, os.path.basename(f.split('.', 1)[0]))
        os.makedirs(os.path.dirname(os.path.join(od, jn)))
    elif jobname:
	flags.append("-jobname=" + jobname)
	jn = jobname
        # If we reimplement in python, we could use os.path.relpath()
	od = os.path.join(outdir, os.path.basename(texfile.split('.', 1)[0]))
    else:
	jn = os.path.basename(texfile.split('.', 1)[0])
	od = os.path.join(outdir, updir, os.path.dirname(texfile))

    try:
        os.makedirs(od)
    except OSError:
        pass
    flags = ["-outdir=" + od] + flags

    product = os.path.join(od, jn + ".pdf")
    try:
        if not run_cmd('latexmk', flags + [texfile],
                       accept_no_output=accept_no_output, env=env,
                       verbose=verbose):
            return None
    except:
        if os.path.exists(product):
            os.remove(product)
        raise
    return product

def get_pdf_path(target, jobname=None, single_sided=False, color_sheets=False,
                 run=None, verbose=False, **kw):
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

    return prod(target, jobname=jobname, single_sided=single_sided,
                color_sheets=color_sheets, run=run,
                accept_no_output=not verbose, verbose=verbose,
                **kw)

def get_pdf(target):
    pdf = get_pdf_path(target)
    with open(pdf) as fil:
        return fil.read()

def get_text(tex, jobname=None, run=None):
    assert tex.endswith('.tex'), tex
    product = prod(tex, text=True, jobname=jobname, run=run)
    return open(product[:-len('.pdf')] + ".txt").read()
