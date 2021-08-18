set my_error=0

py  -3.7-32 -m pip install -r ./requirements/requirements_dev.txt --target ./src/
py  -3.7-32 -m pytest src/UnittestProject.py --cov --junit-xml pytest.xml
IF %ERRORLEVEL% NEQ 0 ( 
   set my_error=%ERRORLEVEL%
)
py  -3.7-32 -m coverage html --omit=escapejson/*,galaxy/*,galaxyutils/*,parameterized/*,win32/*,wrapt/*,aiounittest/*,syncasync.py


for /f %%i in ('dir /b TestDirectory*') do rd /s /q %%i

EXIT /B %my_error% 