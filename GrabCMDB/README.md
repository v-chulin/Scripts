Goal
----

The scripts under this folder are used to grab the owner from CMDB.xml 
for the servers list on a file -- servers.txt.
You can edit this file with input the servers name line by line.

How to excute?
----

#### Execute sequence as below:

1. determineOS.sh             
    input  -- servers.txt                      
    output -- windows.txt/linux.txt
2. grabCMDB.bat/grabCMDB.sh   
    input  -- windows.txt/linux.txt            
    output -- windows_list.txt/linux_list.txt
3. group.sh                   
    iuput  -- windows_list.txt/linux_list.txt  
    output -- group_*.txt

Read the scripts for more detail!
