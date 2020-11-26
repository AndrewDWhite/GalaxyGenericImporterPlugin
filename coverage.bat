py  -3.7-32 -m pip install coverage
py  -3.7-32 -m coverage run UnittestProject.py
py  -3.7-32 -m coverage html --omit=escapejson/*,galaxy/*,galaxyutils/*,parameterized/*,win32/*,wrapt/*,aiounittest/*,syncasync.py

for /f %%i in ('dir /b TestDirectory*') do rd /s /q %%i
