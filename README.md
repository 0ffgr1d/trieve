# trieve
A python script to search through AD Users attributes from a file using regex


## Purpose
This tool was designed for searching for specific Active Directory user attributes within an AD users file. Within an Active Directory environment typically the operator would query and write the AD Users information to a file, then download the file to your local machine. Using the script the operator can begin searching through the file for specific accounts or account attributes.

## How to use
trieve.py -f inputfile + parameters

## Parameters
- -f = input the adusers.txt file
- -a = the Active Directory attribute you want to look at
- -r = regex expression in each Active Directory object
- -o = output file
- -v = View of the returned objects
- -e = echo back all results found objects.
  ##### *Note: if you specify -v and -e this gives you the option to hit enter after each object to view slower*
  
 ### Example: 
 python trieve.py -f users.txt -a samaccountname,pwdlastset,useraccountcontrol -r ^useraccountcontrol.DONT_EXPIRE  -v -e
  
  
  
  
### Example: 
python trieve.py -f users.txt -a samaccountname,description,pwdlastset -r . -e

  
  
### Example: 
python trieve.py -f users.txt -a samaccountname,description,pwdlastset,useraccountcontrol,cn,accountexpires -r pwdlastset.20* -o expires.txt
