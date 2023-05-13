@echo off

REM Set the number of times to run the scripts
set /a num_times=5

REM Loop through the specified number of times
for /l %%i in (1,1,%num_times%) do (
    REM Execute the Python script with the client_text.txt file as an argument
    python client_single.py client_text.txt
)
python plot_graph.py

