#!/bin/bash

#######################################################################
# This shell script use for group servers by keyword                  #
# Please execute it under the same path with (windows/linux_list.txt) #
# the files -- group_*.txt are what you need after execute            #
#######################################################################

# windows_list.txt and linux_list.txt save the servers name && owner/person #

echo -e "\n############# Begin #############"
echo -e "\n\tGroupping..."
# deal with windows_list.txt #
# insert "Windows:\n" into the first line of group_bfs.txt, group_bfs.txt will be created automatically under current path #
echo -e "Windows:\n" >> group_bfs.txt
# grab the line with keyword "bfs" and the next line on file -- windows_list.txt, then write into group_bfs.txt #
# "-A 1" -- one line after, "-v" -- not, "^--" -- begin with "--" #
cat windows_list.txt | grep -A 1 bfs | grep -v ^-- >> group_bfs.txt
# create group_str.txt #
echo -e "Windows:\n" >> group_str.txt
# grab with keyword "str" or "st" [0-9] means following with number. use egrep to grap two situation at the same time #
cat windows_list.txt | egrep -A 1 "str[0-9]|st[0-9]" | grep -v ^-- >> group_str.txt
# create group_air.txt, grab with keyword "air" #
echo -e "Windows:\n" >> group_air.txt
cat windows_list.txt | grep -A 1 air | grep -v ^-- >> group_air.txt
# create group_car.txt, grab with keyword "air" #
echo -e "Windows:\n" >> group_car.txt
cat windows_list.txt | grep -A 1 car | grep -v ^-- >> group_car.txt
# copy windows_list.txt to group_others.txt #
cp windows_list.txt group_others.txt
# insert Windows: into the first line of group_others.txt, 1i means insert at the first line #
sed -i '1i Windows:\n' group_others.txt
# -e -- use when one than one action in need, it will execute one by one for the same file (group_others.txt) #
# N; -- next line, s///g use to replace, N;s/\n/::/g -- join every two line into one line via replace \n to :: #
# /st[0-9]/d -- delete the line with keyword st[0-9], s/::/\n/g -- replace :: to \n, roll back the format for the file #
sed -i -e 'N;s/\n/::/g' -e '/st[0-9]/d' -e '/str[0-9]/d' -e '/bfs/d' -e '/air/d' -e '/car/d' -e 's/::/\n/g' group_others.txt

#deal with linxu_list.txt #
# insert "Linux:\n" into the last line of group_bfs.txt #
echo -e "Linux:\n" >> group_bfs.txt
# grab with keyword "bfs" on file -- linux_list.txt, and write into group_bfs.txt #
cat linux_list.txt | grep -A 1 bfs | grep -v ^-- >> group_bfs.txt
# insert "Linux:\n", and grab with keyword "str[0-9]&&st[0-9]" #
echo -e "Linux:\n" >> group_str.txt
cat linux_list.txt | egrep -A 1 "str[0-9]|st[0-9]" | grep -v ^-- >> group_str.txt
# insert "Linux:\n", and grab with keyword "air" #
echo -e "Linux:\n" >> group_air.txt
cat linux_list.txt | grep -A 1 air | grep -v ^-- >> group_air.txt
# insert "Linux:\n", and grab with keyword "car" #
echo -e "Linux:\n" >> group_car.txt
cat linux_list.txt | grep -A 1 car | grep -v ^-- >> group_car.txt
# copy linux_list.txt to group_others.txt.linux #
cp linux_list.txt group_others.txt.linux
# refer to line 36 #
sed -i -e 'N;s/\n/::/g' -e '/st[0-9]/d' -e '/str[0-9]/d' -e '/bfs/d' -e '/air/d' -e '/car/d' -e 's/::/\n/g' group_others.txt.linux
# insert "Linux:\n" into the last line of group_others.txt #
echo -e "Linux:\n" >> group_others.txt
# print out the content of group_others.txt.linux, and write into group_others.txt #
cat group_others.txt.linux >> group_others.txt
# remove group_others.txt.linux #
rm group_others.txt.linux

echo -e "\n\tGrouped!"
echo -e "\n############## End ##############"
