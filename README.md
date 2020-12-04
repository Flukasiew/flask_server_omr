
# Table of Contents

1.  [Flask backend for OMR](#org313795c)
2.  [Instalation](#orgd4954dc)
3.  [Usage](#org03ae982)
    1.  [Running server](#org59c12d5)
    2.  [Crontab](#org697c6f0)
        1.  [Adding job](#orgbc9a3be)
        2.  [Adding remove](#orgea0680a)
4.  [EndPoints](#org0e7e587)
    1.  [/static/file<sub>name</sub>](#org178e445)
    2.  [/predict<sub>uri</sub>/file<sub>name</sub>](#org1bd08c0)
    3.  [/ping](#org5411e75)



<a id="org313795c"></a>

# Flask backend for OMR

Allows for interaction of mutliple clients with model 

If not specified running commands assumes current working directory to be main directory of the project


<a id="orgd4954dc"></a>

# Instalation

1.  Install prerequisites
    1.  Install Fluidsynth with system package manager
        Advised way as per midi2audio library OSX installtions instruction: [midi2audio](https://github.com/bzamecnik/midi2audio)
    2.  Install Lilypond with system package manager
    3.  Check if both are available in the shell
2.  Clone repo
    $ git clon <https://github.com/Flukasiew/flask_server_omr>
3.  Install conda enviroment
    1.  Download conda env from[ env](https://mega.nz/file/PaYTmAQC#DuVkHPnibDdIEsluH11Hy3Qrl48eU-TToly5KsaVOJU)
    2.  Install conda env with
        $ conda env create -f file<sub>name.yml</sub>
    3.  Install remaining packages with pip after activating conda env
        1.  Activate enviroment with
            $ conda activate env<sub>name</sub>
        2.  install flask<sub>crontab</sub>
            $ pip install flask<sub>crontab</sub>
        3.  install midi2audio
            $ pip install midi2audio
4.  Setting up model
    1.  Download model from[ model](https://mega.nz/file/THRxQYhK#wDgbG21okzXli9Vr6lEyO3wi7_jumD9Otds9pvupNMc)
    2.  Extract model files into &ldquo;app/static&rdquo; directory


<a id="org03ae982"></a>

# Usage


<a id="org59c12d5"></a>

## Running server

$ flask run


<a id="org697c6f0"></a>

## Crontab

File auto remove functionality. 
Assumes crontab present on the system, use only is you are sure it is installed


<a id="orgbc9a3be"></a>

### Adding job

$ flask crontab add


<a id="orgea0680a"></a>

### Adding remove

$ flask crontab remove


<a id="org0e7e587"></a>

# EndPoints


<a id="org178e445"></a>

## /static/file<sub>name</sub>

Gives acces to file on server, streaming is possible from this file


<a id="org1bd08c0"></a>

## /predict<sub>uri</sub>/file<sub>name</sub>

Runs prediciton on the supplied image
Returns uri in form &ldquo;static/file<sub>name</sub>&rdquo; can be used to access file on the server


<a id="org5411e75"></a>

## /ping

Returns &ldquo;sucessful&rdquo;

