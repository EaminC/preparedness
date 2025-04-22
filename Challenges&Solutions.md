Challenge1:Outside Resources Recursive Dependencies (solved in current repo)
When it needs outside resources which makes it a recursion problem(build a environment needs another environment built)
Solution1:Give the agent a scaffold json file which include all the necessary 3rd party download link not included in the main repo


Challenge2:illusion about version
Agents comes up with a jdk version which does not even exsist
Solution2.1:Provided possible version table json before running
Solution2.2:Give Err msg (sometimes include correct version but not all the times so 2.1 is better)


Challenge3:Missing important files and fail to Interoperate between files
need to change a yaml file and use command line accordingly
need some important config written in yaml not readme
Solution3.1: No good solution yet
Solution3.2:Provide a spotlight json include important files to be noticed 


Challenge4:can not understand file structure
put file in wrong path or with wrong name
Solution : To be figured out

Challenge 5: Tries to read multiple irrelevant files (or reads relevant files, but the task can be completed without reading the content). In my case this happened with the Metis project I am trying to reproduce. It then tried to 
Solution 5.1: Emphasize "Closely follow README step by step", etc, which decreased the rate of irrelevant file reads.
Solution 5.2: To be honest, this problem didn't really effect performance visibly, so maybe doesn't need to be solved.
