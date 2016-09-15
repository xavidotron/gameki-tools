\ProvidesClass{gameki}

% We allow information to be passed into Gameki LaTeX files through the jobname.
% This can take several different formats:
% 2 (numeric): set GAMERUN to 2
% cJamesBond (second letter capitalized): set \parsedmacros to \cJamesBond{}
% whatever (jobname possibly not specified): set \parsedmacros to every PC
% 2-cJamesBond: set GAMERUN to 2; set \parsedmacros to \cJamesBond{}
% listchar-cJamesBond: uses listchar as the game option; set \parsedmacros
%                      to \cJamesBond{}
% listchar-2-cJamesBond
%
% (\GAMERUN must be set early (before gametex.sty) to have an effect.)

% Defaults.
\def\gameoption{sheet}
\def\parsedmacros{\production}

% Helpers
\def\stripdashb#1-\endstrip{%
  \gdef\parsedmacros{\csname#1\endcsname{}}%
}
\def\stripdasha#1-#2\endstrip{%
  \def\tmp{#2}%
  \ifx\tmp\empty\relax% no second dash
    \gdef\parsedmacros{\csname#1\endcsname{}}%
  \else% second dash
    \gdef\GAMERUN{#1}%
    \stripdashb#2\endstrip
  \fi
}
\def\secondcharswitch#1#2#3\endswitch{%
  %\typeout{#1:#2:#3}%
  \ifnum`#2=\uccode`#2\relax% If the second char is uppercase (cJamesBond)
    \gdef\parsedmacros{\csname#1#2#3\endcsname{}}%
  \else% Keep defaults, jobname not overridden (whatever)
  \fi
}

\def\parsejobname#1-#2\endparse{%
  \def\tmp{#2}%
  \ifx\tmp\empty\relax% No dash in jobname
    \ifnum0<0#1\relax% If it's a number (2)
      \gdef\GAMERUN{#1}%
    \else
      \secondcharswitch#1\endswitch%
    \fi
  \else% Dash in jobname
    \stripdasha#2\endstrip
    \ifnum0<0#1\relax% If predash is a number (2-cJamesBond)
      \gdef\GAMERUN{#1}%
    \else% Not number (listchar-cJamesBond)
      \gdef\gameoption{#1}
    \fi
  \fi
}

% We need an empty and a dash at the end so that the macro parses if there's
% no dash in \jobname. If there is one, the extra dash will get stripped off.
\csname gamekihook\endcsname{\expandafter\parsejobname\jobname-\endparse}

% Load the gameki class based on the gameclassname environment variable
% (set by Gameki/bin/prod).
\edef\gameclassenvvar{\string${gameclassname}} % $
\LoadClass[\gameoption]{\gameclassenvvar}

\def\gamekilib{\gamepath/Gameki/lib}
