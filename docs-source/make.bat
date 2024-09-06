@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

REM You can set these variables from the command line, and also
REM from the environment for the first two.
SET SPHINXOPTS=
SET SPHINXBUILD=sphinx-build
SET SOURCEDIR=source
SET LOCALBUILDDIR=build
SET GITHUBBUILDDIR=..\docs

%SPHINXBUILD% --version >NUL 2>&1
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

REM Put it first so that "make" without argument is like "make help".
if "%1"=="" goto help

if "%1"=="help" goto help
if "%1"=="html" goto html
if "%1"=="github" goto github
if "%1"=="githubclean" goto githubclean

goto all

:help
    %SPHINXBUILD% -M help "%SOURCEDIR%" "%LOCALBUILDDIR%" %SPHINXOPTS%
    goto end

:github
    echo. > "%GITHUBBUILDDIR%\.nojekyll"
    %SPHINXBUILD% -b html "%SOURCEDIR%" "%GITHUBBUILDDIR%" %SPHINXOPTS%
    goto end

:githubclean
    %SPHINXBUILD% -M clean "%SOURCEDIR%" "%GITHUBBUILDDIR%" %SPHINXOPTS%
    goto end

:html
    %SPHINXBUILD% -b html "%SOURCEDIR%" "%LOCALBUILDDIR%" %SPHINXOPTS%
    goto end

REM Catch-all target: route all unknown targets to Sphinx using the new
REM "make mode" option.
:all
    %SPHINXBUILD% -M %1 "%SOURCEDIR%" "%LOCALBUILDDIR%" %SPHINXOPTS%

:end
popd
