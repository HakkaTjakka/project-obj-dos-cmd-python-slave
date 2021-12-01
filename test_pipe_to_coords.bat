@echo off
del result.txt
make_holland.bat | python pipe_to_coords.py
pause