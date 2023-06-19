# FTP_Socket_SRI
A networking Summer project, implement FTP and use multithreading to send multiple packet on the same time. 

## Setup the project
### First run the server file using
```
pyhton server.py
or
.\server.py
```

### Now in new terminal run the client file using
```
pyhton client.py
or
.\client.py
```
## Upload
### You need to copy file (which you want to upload) in to main folder. THe uploaded file will be in sever_side folder.
```
UPLOAD <filename>
```
## Download
### You have to select a file from the all the files.
### Type below command to see all files on server
```
LIST
```
### To download file from server
```
DOWNLOAD <filename>
```
