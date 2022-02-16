import sys 
import getopt
import re

class main():
    def __init__(self):
        self.attributes = {} # Initilized here, populated by self.intake + self.setattributes
        self.outputfile = None # None by default unless declared from intake
        self.inputecho = None # None by default unless declared from intake
        self.echo = None  # None by default unless declared from intake
        self.copylist = []  # Holds objects for copying to self.outputfile 
        self.inputfile_arg = self.intake()[0] # REQUIRED -i
        self.attr_args = self.intake()[1] # REQUIRED -a
        self.regexargs = self.intake()[2] # REQUIRED -r
        self.setflags() # Sets attributes and marks them for regex if passed 
        self.setattributes()
# DEBUG print(self.attributes) 
# DEBUG input()
        self.parse()
        if self.outputfile:
            self.copyout()
    def setattributes(self):
        for attribute in self.attr_args:
            if attribute in self.attributes.keys():
                continue
            else:
                self.attributes.update({attribute:[False,None,None]})
    def intake(self):
        try:
            regex = False
            opts, args = getopt.getopt(sys.argv[1:],"f:a:r:o:veh")
        except getopt.GetoptError:
            print("unknown operator value")
            print("trieve.py -f <inputfile> -a <attributes to be returned, seperated by commas> -r <regex expression in each AD object> -o <output file> -v <view each returned object> -e <echo back found objects>")
            sys.exit(2)
        for opt, arg in opts:
            if opt in ['-f']:
                inputfile = arg
            elif opt in ['-a']:
                ad_attributes = arg.split(",")
            elif opt in ['-r']:
                regex = arg
            elif opt in ['-o']:
                self.outputfile = arg
            elif opt in ['-e']:
                self.echo = True
            elif opt in ["-v"]:
                self.inputecho = True
            elif opt in ["-h"]:
                print("trieve.py -f <inputfile> -a <attributes to be returned, seperated by commas> -r <regex expression in each AD object> -o <output file> -v <view each returned object> -e <echo back found objects>")
                sys.exit()
        return inputfile,ad_attributes,regex
    def setflags(self):
        if len(self.regexargs) == 1 and self.regexargs == ".":
# DEBUG            print("This is a period. We will return everything on ",self.regexargs," for ",self.attr_args)
            for attribute in self.attr_args:
                self.attributes.update({attribute:[False,None,None]}) # Found,RegexFound,RegexMatchValue
# DEBUG           print(self.attributes)
        elif "," in self.regexargs:
            templist = self.regexargs.split(",")
            self.validate(templist)
        elif "." in self.regexargs:
            templist = self.regexargs.split(".",1)
# DEBUG           print("Single attribute for parsing",templist[0]," ",templist[1])
            self.attributes.update({templist[0]:[False,False,templist[1]]})
    def validate(self,regexargs):
# DEBUG       print("Validating multiple args")
        for arg in regexargs:
# DEBUG        print(arg)
            if arg == "":
                print("Cannot have a blank argument, please do not use a comma at "+self.regexargs)
                sys.exit()
            elif "." in arg:
                templist = arg.split(".",1)
                self.attributes.update({templist[0]:[False,False,templist[1]]})
    def parse(self):
        fhand = open(self.inputfile_arg,encoding='utf-8') # Might not need this encoding
        mylist = [] 
        counter = 0 # Use counter to determine if we have a complete object 
        for line in fhand:
            line = line.strip()
            for attribute in self.attributes.keys():             
                if re.search("^"+attribute,line): # If we find our attribute in the line:
                    if self.attributes[attribute][0] == True and counter != len(self.attributes.keys()): # checks if this is a service account or given object is missing attributes
                        self.reset()
                        mylist = []
                        counter = 0
                    elif self.attributes[attribute][0] == True and counter == len(self.attributes.keys()): 
                        self.reset()
                        mylist.sort()
                        if len(mylist) == len(self.attributes.keys()):
                            mylist.insert(0,"==============================================================")
                            self.copylist.append(mylist)
                            if self.echo == True:
                                for object in mylist:
                                    print(object)
                                if self.inputecho == True:
                                    input("Press enter to continue...")
                            elif self.echo == None and self.inputecho == True:
                                for object in mylist:
                                    print(object)
                                input("Press enter to continue...")
                        mylist = []
                        counter = 0
                    if self.attributes[attribute][0] == False:
                        self.attributes[attribute][0] = True
                        counter = counter + 1
                        if self.attributes[attribute][1] != None:
                            if self.checkregex(attribute,self.attributes[attribute][2],line):
                                mylist.append(line)
                        elif self.attributes[attribute][1] == None:
                            mylist.append(line)
    def copyout(self): 
        fhand = open(self.outputfile,"a")
        fhand.write(str(len(self.copylist))+" Objects matched criteria\n")
        for list in self.copylist:
            for line in list:
                fhand.write(line +"\n")
        fhand.close()
            
    def reset(self): # Resets dictionary and cycles to next object
        for key in self.attributes:
            self.attributes[key][0] = False
            if self.attributes[key][1] != None:
                self.attributes[key][1] = False
            
    def checkregex(self,attribute,regex,line):
        if re.search("."+regex,line):
            self.attributes[attribute][1] = True 
            return True



# attribtue : {[Found? Regex Found? Regextocheck to validate Regex Found?]}        
main()