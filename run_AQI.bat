ECHO OFF
REM A batch script to execute a Python script
REM ECHO.%PATH%| FIND /I "python">Nul && ( 
REM 	Echo.Found "Python"
REM ) || (
REM 	FOR /f %%p in ('where python.exe') do SET PYTHONPATH=%%p
REM 	SET PATH=%PATH%;%PYTHONPATH%
REM )
python AQI_not.py -nc
PAUSE