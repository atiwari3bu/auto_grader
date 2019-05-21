filename=auto_grader.py 

all:
	python3 $(filename) github_list bu-cs540-20191s smart-pointer 
  
open:
	vim $(filename) 
