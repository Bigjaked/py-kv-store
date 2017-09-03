@rem
@rem ACTIVATE THE PROJECTS CONDA ENVIRONMENT
@rem
@rem get the name of the current directory
@for %%* in (.) do @set CurrDirName=%%~nx*
@set CONDA_ENVS=C:%HOMEPATH%\AppData\Local\conda\conda
@echo Setting PATH env variable
@set OLD_PATH=%PATH%
@set PATH=%CONDA_ENVS%\envs\api;^
         %CONDA_ENVS%\envs\api\Scripts\;^
         %PATH%
@echo Activating conda env '%CurrDirName%'
%CONDA_ENVS%\envs\api\Scripts\activate.bat %CurrDirName%