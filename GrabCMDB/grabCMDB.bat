::############################################################################################################
::# This script use for grab owner from CMBD.xml files (C:\CMDB.xml) under all karmalab/Lab Windows servers. #
::# Run this under a karmalab/Lab Windows server, need a file save all the servers' name. (E:\windows.txt)   #
::# Execute it under E:\ here, if you want to run on other path, just update the path E:\ on this script     #
::############################################################################################################

:: an example of CMDB.xml as below
::# <CmdbOwner>
::#  <Owner id="6e93c86b4017f000f1cb11369ea67b85" name="Platform Infrastructure Services: End to End Integration Environments" /> 
::#  <Application id="e4dc608b60e74588a73845e3fd845ae7" name="E2E" /> 
::#  <Modified date="10-09-2013" person="SEA\becole" /> 
::# </CmdbOwner>

@echo off
:: print output
echo Grab the Owner from CMDB files.
::E:\windows.txt save all the kamalab Windows servers, %%i is single server name
for /f %%i in (E:\windows.txt) do (
  :: copy a CMDB.xml from a single server to local E:\
  xcopy /v /y /q /z \\%%i\C$\CMDB.xml E:\
  :: rename it to servername.xml
  rename E:\CMDB.xml %%i.xml
  :: split by =, and grab the 4th item when the line include keyword "<Owner", then write it into E:\windows_list.txt
  :: should be Platform Infrastructure Services: End to End Integration Environments on above CMDB.xml
  for /f tokens^=4^ delims^=^" %%a in ('find "<Owner" E:\%%i.xml') do echo %%i -- %%a >> E:\windows_list.txt
  :: split by =, and grab the 4th item when the line include keyword "person", then write it into E:\windows_list.txt
  :: should be SEA\becole on above CMBD.xml
  for /f tokens^=4^ delims^=^" %%a in ('find "person" E:\%%i.xml') do echo                 -- %%a >> E:\windows_list.txt
  :: delete E:\server.xml
  del E:\%%i.xml
  )
cmd /k echo
