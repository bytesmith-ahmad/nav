:: Runs launcher in interactive mode

setlocal

git pull

python ".\nav_ninja.py"

:: Create a temporary file with the message
echo DON'T FORGET TO COMMIT > message.txt

:: Open Notepad with the message
start notepad.exe message.txt

:: Exit the batch script without closing Notepad
exit /b
