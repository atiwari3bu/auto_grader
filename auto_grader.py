import os
import time
import sys
import getopt
from pathlib import Path

class Inputdata:
    def __init__(self,arg):
        self.usernames_file=arg[1]
        self.class_name=arg[2]
        self.project_name=arg[3]
        self.project_path=None
        self.parent_path=None

def importGithubFiles(data):
    file_present=False
    files=[x for x in os.listdir(os.getcwd())]

    if(data.usernames_file not in files):
        print("Please keep the usernames file in auto_grader directory")
        exit()

    with open("{}".format(data.usernames_file)) as f:
        github_ids=f.read().splitlines()

    print("\nNow creating folder for project... \n ")
    parent_path=os.getcwd()
    data.parent_path=parent_path
    p=Path('..')
    os.chdir("{}".format(p))
    if not os.path.exists(data.project_name):
        os.makedirs(data.project_name)
    project_path=os.path.join(os.getcwd(),data.project_name)
    data.project_path=project_path
    os.chdir("{}".format(project_path))

    print("Cloning github repositories ... \n")
    os.system("git config --global credential.helper {}".format('cache --timeout=3600'))
   
    toolbar_width = len(github_ids)
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

      
    for ids,i in zip(github_ids,range(0,toolbar_width)):
        web_address=os.path.join("https://github.com","{}/{}-{}".format(data.class_name,data.project_name,ids))
        #print(web_address)
        os.system("git clone {} > garbage 2>&1".format(web_address))

        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()
    
    
    sys.stdout.write("\n") 
    os.system("rm garbage")
    os.chdir("{}".format(parent_path))
    print("\nSuccesfully cloned projects in {} folder\n".format(data.project_name))
    

def runningMossOnSubmissions(data):
    print("Coping moss from parent directory to project directory and changing its permissions\n")
    os.system("cp moss.pl {}".format(data.project_path))
    os.chdir("{}".format(data.project_path))
    submissions=[x for x in os.listdir(os.getcwd())]
    os.system("chmod ug+x moss.pl")
    command="./moss.pl -l cc -d "
    
    for project_name in submissions:
        if(project_name=="moss.pl" or project_name=="report.txt"):
            continue
        
        project_dir=os.path.join(os.getcwd(),project_name)
        files=[x for x in os.listdir(project_dir)]
        if (len(files)==1):
            continue
                    
        path_exists=False
        for file_name in files:
            if(file_name==".git" or file_name==".DS_Store"):
                continue
            file_path=os.path.join(project_dir,file_name)
            
            if(os.path.isdir("{}".format(file_path))):
                print(file_path)
                command+=file_path
                command+="/* "
                path_exists=True
                
            else:
                command+=file_path
                command+=" "
            
        #if(path_exists==False):
            #command+=project_dir
            #command+="/* "
         #   command+=project_dir
          #  command+=" "

         
    print(command)
    os.system("touch report.txt")
    os.system("{} 2>&1 report.txt".format(command))
    print("Result for the moss is written into report.txt file in your project folder")

def compilingAndRunning(data):
    os.chdir("{}".format(data.parent_path))
    files=[x for x in os.listdir(os.getcwd())]
    
    if("test_cases" not in files):
        print("\nNo folder like test_cases present in auto_grader directory\n")
        return

    os.chdir(os.path.join(data.parent_path,"test_cases"))
    
    for test_file in os.listdir(os.getcwd()):
        print(test_file)
        print("\ncopying {} into target files\n".format(test_file))
        os.system("cp {} {}".format(test_file,data.project_path))
        os.chdir(data.project_path)

        for submission in os.listdir(os.getcwd()):
            if(submission=="report.txt" or submission=="moss.pl"): 
                continue
            print(submission)
            
            pt=os.path.join(os.getcwd(),submission)
            os.system("cp {} {} ".format(test_file,pt))
            fl=open("report.txt","a")
            fl.write("Compiling {} for {}\n ".format(test_file,submission))

        os.system("rm {}".format(test_file))


def main(arg):
    if(len(arg)!=4):
        print("\nNumber of arguments incorrect\n")
        return

    data=Inputdata(arg)
    importGithubFiles(data)
    #runningMossOnSubmissions(data)
    compilingAndRunning(data)

main(sys.argv)
