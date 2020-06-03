py -m pip install coverage
py -m coverage run UnittestProject.py
py -m coverage html --omit=escapejson/*,galaxy/*,galaxyutils/*,parameterized/*
