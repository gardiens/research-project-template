

# Monkeytype

Download it with

pip install monkeytype

do monkeytype myscript.py

then if you want to get the annotation
monkeytype  --list.module
and apply on  every module if you want

## +
Quite accurate typing ( it runs the code haha )
## -
-Import are explicit and no string are used so beware of circular import
- It is slow
- custom configs seems bugged.  ( needs to put () in a monkeytype file .)
- Idk how I should rewrite or not import of file by myself.

# Autotyping

A promising autotyper with a pre-commit ( it bugged when I use it ). It doesn't run actual code so it's quite fast
To run it :
pip install autotyping
python -m autotyping MYCODE.PY  --safe
python -m autotyping MYCODE.py --aggressive #may produce wrong code
## +
it's really fast
## -
bro pre-commit doesn't works


# infer-types
The old one I was using, don't do magic but works haha
to run it :
python3 -m pip install infer-types
python3 -m infer_types myscript.py

## +
it is fast
## -
a bit dumb ( but it doesn't break or import code so it should be fine )


# Pyre

Bro it's meta don't expect any docs

# +
it's meta
# -
i couldn't make it work on windoss ( neither on a workstation)

# Further

see here https://github.com/typeddjango/awesome-python-typing
