Engeto-pa-3-project

The third project on Python Academy by Engeto

Project description
This project is used to extract the results of the parliamentary elections in 2017. 
View link: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Installing libraries
The libraries used in the program are stored in the requirements.txt file. For installation, I recommend using a new virtual environment and with the manager installed, run as follows:
pip --version   # this will verify the manager version
pip install -r requirements.txt   # installation of libraries

Launching the project
Launching the main.py file from the command line requires two mandatory arguments:
python <district-link> <output-filename>
Then the results will be downloaded and stored as csv file.

Project example
Voting results for the Frýdek-Místek district
1st argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102
2nd argument: frydek-mistek
Executing the program from the command line:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102" frydek-mistek

Download progress:
DOWNLOADING DATA FROM THE SELECTED URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102
SAVING TO FILE: frydek-mistek.csv
TERMINATING PROGRAM

Example of partial output:
code,location,registered,envelopes,valid,Občanská..
598011,Baška,3 093,2,065,2,053,175,1,1,124,1,49,192,21,12,21,1,0,216,0,0,44,665,2,9,194,1,16,7,3,293,5
598020,White,285,178,178,19,0,0,14,0,10,21,3,1,0,1,0 ,12,1,0,3,52,0,0,15,0,3,0,0,23,0
511633,Bocanovice,358,197,197,20,0,0,32,0,3,13,3,1,0,0,0,18,0,1,1,45,0,0,43,0,0,0,0,17,0
598038,Brušperk,3 199,2 173,2 158,211,3,0,183,0,53,204,25,17,30,3,1,171,0,2,61,767,3,3,145,0,22,5,0,241,8
...
