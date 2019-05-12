import os
import time
#from tqdm import tqdm
from pathlib import Path

def importGithubFiles():
    print("Enter the file which has all the github id's")
    file_present=False
    p = Path('..')

    while(1): # This will take the input file with github id's 
        #ids = input()
        ids="github_list"
        for files in os.walk("{}".format(p)):
            if ids in files[-1]:
                file_present = True
                break
        if file_present:
            break
        # print("Please enter the filename present in autograder folder directory")
        print("File not present, please enter the filename present in autograder folder directory")

    #class_name=input("\nEnter the class name for github repository... For example, bu-cs540-2019s \n") 
    class_name="bu-cs540-20191s"
    #project_name=input("\nInput the project name... For example, container_in_c \n")
    project_name="map-container"

    print("\nNow creating folder for project... \n ")
    os.chdir("{}".format(p))
    parent_path=os.getcwd()
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    project_path=os.path.join(os.getcwd(),project_name)

    print("Cloning github repositories ... \n ")
    
    with open("{}".format(ids)) as f:
        githubids=f.read().splitlines()
    
    #for ids,i in zip(githubids,tqdm(range(len(githubids)))):
    for ids in githubids:
        web_address=os.path.join("https://github.com","{}/{}-{}".format(class_name,project_name,ids))
        print(web_address)
        os.chdir("{}".format(project_path))
        os.system("git clone {} > garbage 2>&1".format(web_address))
        os.chdir("{}".format(parent_path))


    os.chdir("{}".format(project_path))
    os.system("rm garbage")
    os.chdir("{}".format(parent_path))
    print("\n\n-------------DONE-------------------\n")

    
def main():
    importGithubFiles()
main()
