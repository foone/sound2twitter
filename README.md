# Sound2Twitter

This tool converts audio files into mp4 files, for easy posting onto twitter. 

![Screenshot of @3dmmsfx](https://github.com/foone/sound2twitter/raw/master/docs/sample.png "Screenshot of @3dmmsfx")

It generates a waveform of the video in greyscale, then has it turn red as the video plays

It was created for the [@3dmmsfx bot](https://twitter.com/3dmmSFX).

## Prerequisites

Needs python 2.7, Pillow(or PIL), and ImageMagick.

## Example use:

In a virtualenv (on unix):

```
$ virtualenv venv
$ venv/bin/pip install -r requirements.txt
$ venv/bin/python sound2twitter.py foo.wav
```


In a virtualenv (on windows):

```
C:\sound2twitter> virtualenv venv
C:\sound2twitter> venv\Scripts\pip install -r requirements.txt
C:\sound2twitter> venv\Scripts\python sound2twitter.py foo.wav
```

System-wide pillow:

```
$ python sound2twitter.py foo.wav
```

## Limitations/Bugs

* The tool doesn't yet check for over-long soundfiles! Twitter will not let you post a 5 minute movie unless you're some kind of advertiser
* There's no command options. You have to edit the MINLENGTH/PADDING/W/H constants at the top of sound2twitter.py to change options
* This has barely been tested!
* It generates tons of temp files while running, in the current directory. They're automatically cleaned up on successful exit, but they should be avoided. 
* This is probably not as good at making twitterable mp4s as [twitmovie](https://github.com/foone/twitmovie). Combine the two or at least copy-paste the Good Bits? 


## Similar software:

* [NY Public Radio's audiogram](https://github.com/nypublicradio/audiogram)
