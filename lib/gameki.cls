\ProvidesClass{gameki}

% We allow information to be passed into Gameki LaTeX files through the jobname.
% This can take several different formats:
% listchar-cJamesBond: uses listchar as the game option; set \parsedmacros
%                      to \cJamesBond{}
% 2-cJamesBond: set GAMERUN to 2; set \parsedmacros to \cJamesBond{}
% 2: set GAMERUN to 2
% cJamesBond (second letter capitalized): set \parsedmacros to \cJamesBond{}
% whatever (jobname possibly not specified): set \parsedmacros to every PC
%
% (\GAMERUN must be set early (before gametex.sty) to have an effect.)

% Defaults.
\def\gameoption{sheet}
\def\parsedmacros{EVERY{PC}{\ME{}\par}}

% Helper
\def\stripdashset#1-\endstrip{\def\parsedmacros{\csname#1\endcsname{}}}

% #1 and #2 are the first two characters of the pre-dash part. #2 and #3 might
% be empty.
\def\parsejobname#1#2#3-#4\endparse{%
  \def\tmp{#4}%
  \ifx\tmp\empty\relax% No dash in jobname
    \ifnum0<0#1#2#3\relax% If it's a number (2)
      \def\GAMERUN{#1#2#3}%
    \else
      \ifnum`#2=\uccode`#2\relax% If the second char is uppercase (cJamesBond)
        \def\parsedmacros{\csname#1#2#3\endcsname{}}%
      \else% Keep defaults, jobname not overridden (whatever)
      \fi
    \fi
  \else% Dash in jobname
    \stripdashset#4\endstrip
    \ifnum0<0#1#2#3\relax% If predash is a number (2-cJamesBond)
      \def\GAMERUN{#1#2#3}%
    \else% Not number (listchar-cJamesBond)
      \def\gameoption{#1#2#3}
    \fi
  \fi
}

% We need an empty and a dash at the end so that the macro parses if there's
% no dash in \jobname. If there is one, the extra dash will get stripped off.
\expandafter\parsejobname\jobname-\endparse

% Load the gameki class based on the gameclassname environment variable
% (set by Gameki/bin/prod).
\edef\gameclassenvvar{\string${gameclassname}} % $
\LoadClass[\gameoption]{\gameclassenvvar}

\def\gamekilib{\gamepath/Gameki/lib}
