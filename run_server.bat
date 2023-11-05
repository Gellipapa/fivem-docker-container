
python start_server.py

@REM setlocal EnableDelayedExpansion

@REM REM specify the path to the .env file
@REM set "env_file=.test.env"

@REM REM read the .env file line by line
@REM for /f "tokens=1,2 delims==" %%G in ('type "%env_file%"') do (
@REM   REM assign the value to a variable
@REM   set "%%G=%%H"
@REM )

@REM REM print the value of the SERVER_NAME variable
@REM echo %SERVER_NAME%

@REM docker-compose --project-name "%SERVER_NAME%" --env-file ".test.env" up
pause
