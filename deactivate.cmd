@rem
@rem DEACTIVATE THE PROJECTS CONDA ENVIRONMENT
@rem
@echo Resetting PATH env variable
@set PATH=%OLD_PATH%
@set CONDA_ENVS=%HOMEDRIVE%%HOMEPATH%\AppData\Local\conda\conda
@echo Deactivating conda env
@%CONDA_ENVS%\envs\api\Scripts\deactivate.bat