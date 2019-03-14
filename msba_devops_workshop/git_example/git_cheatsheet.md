# *1) Git setup*
### System level configuration
	/etc/gitconfig
	git config --system

### User level
	$HOME\.gitconfig
	git config --global 
	git config --global user.name "Your name"
	git config --global user.email "Your email"

### Project level
	myproject/.git/config
	git config

# *2) Git basics*
## Difference in different way
	git diff --color-words <file_name>
	git diff --staged ## to check things different from staging area

## Commit logs
	git log
	git log -n

## Current status
	git status

## Adding files to staging area
	git add <filename>
	git add .

## Commiting to repository
	git commit -m "comment"
	git commit -am "comment"

# *3) Undoing Changes*
## Undo changes from working directory (puts it in working directory)
	git checkout -- <file_name>

## To revert a change to a previous commit (puts it in staging area)
	git  checkout <SHA value of older commit> -- <filename>

## Unstaging a change 
    git rm --cached <filename> ->> Put the file changes from staging to working directory
	git reset head <filename> ->> reset the file to a previous commit version

	
## Put changes in staging index
	git commit --amend -m "Comment"

## Changing the last commit message
	git commit --amend -m "New comment"

## Revert to a previous commit 
	git revert  <SHA value>

## Revert to multiple earlier commits(moves the head pointer)
	-- soft
		Move the pointer but doesn't change staging index and working directory
	-- mixed(default)
		changes the staging index to match repository
		doesn't change working directory
	-- hard
		changes staging, working directory back to previous repo
		
	git reset --<option> <SHA value>

## Deleting all untracked files
	git clean -<option>
		-n (just tester)
		-f (removes files from working directory)
	
# *4) Ignoring files*
## Ignoring some files(from root directory)
	.gitignore

	Guidelines -
	compiled source code
	packages /compressed
	logs/databases
	operating system generated files
	user-uploaded assets(images/PDFs,videos)

## Global ignoring files
	- ignore files in all repository
	- settings not tracked in repository
	- user-specific instead of repository-specific

	Typically kept in Users/<Username>/<.filename>
	git config --global core.excludesfile <path>/<.filename>

## Ignoring tracked files
	git rm --cached temfile2.txt (Remove it from staging index)

	## Tracking empty directories (git keep tracks of file not directory)
	Put a file in it. Standard convention is a file name ".gitkeep"
	
## Navigating the commit trees
	Tree-ish -> references the part of tree
		- Full SHA1 Hash
		- Short SHA1 Hash
			-- atleast 4 characters (Typically 8-10 characters)
		- HEAD pointer
		- Branch reference, tag reference
		- ancestry 
			- parent commit
				-- HEAD^, acadfae^, master^
				-- HEAD~1, HEAD~
			- grandparent commit
				-- HEAD^^, acadfae^^, master^^
				-- HEAD~2
	
	git ls-tree <tree-ish>-> For help documentation
	git ls-tree master^ assets/
	
## Git log
		git log --oneline / git log --format=oneline (other formats -> short/medium/full/fuller/raw)
		git log --oneline --graph --all --decorate
		git log --oneline -5
		git log --since="2012-06-20" / git log --after="2012-06-20"
		git log --since="2 weeks ago" --until="3 days ago"
		git log --since=2.weeks --until=3.days
		git log --until="2012-06-20"
		git log --author="Aayush"
		git log --grep="temp"
		git log 6c63bea..dbc47d5 --oneline
		git log <sha1>.. <filename> (any commits which effect the file from the commit mentioned)
		git log -p (tell changes)
		git log --stat --summary (tell number of lines added/removed plus commits with comments and date)
		
## Examining a commit	
		git show <tree-ish>
		git show <SHA1 value>
		git show --format=oneline HEAD~3
		
	## Comparing commits(comparing two directories)
	git diff <SHA1 value> (what's changed from this SHA with current)
	git diff <SHA1 value> <filename>
	git diff <SHA1 values>..<SHA1 values> <filename>
	git diff <tree-ish>..<tree-ish> <filename>
	git diff --stat --summary <SHA1 value>..HEAD
	git diff (-b/--ignore-space-change) <SHA1 value>..HEAD
	git diff (-w/--ignore-all-space) <SHA1 value>..HEAD
	
cat .git/HEAD (shows file location of HEAD)

# *5) Branching*
	git branch ->> shows list of all branches
	git branch <branch_name> ->> creates a new branch, will still be in master
	git checkout <branch_name> ->> switching to a different branch
	git checkout -b <branch_name> ->> creates a new branch & switch to new branch
	git diff <branch_name>..<branch_name> ->> Shows difference b/w two branches tip
	git branch --merged ->> shows us which branches all the commits the current branch contains
	git branch -m <branch_name> <new_branch_name> ->> changes the name of the branch
	git branch -d <branch_name> ->> Deletes the branch (does a check for stupidity)
	git branch -D <branch_name> ->> Force deleting the branch without any checks
	git push origin --delete <branch Name> ->> Deletes branch on remote repository
	
## Merging branches
	git merge <branch_name> --> merges the branch into current branch
	git merge --no-ff <branch_name> ->> Dos not let git do fast forward merge and forces to make a new commit
	git merge --ff-only <branch_name> ->> Only do a fast forward merge if not abort
	
	## Resolve Conflicts
		- Abort Merge
			git merge --abort
		- resolve the conflicts manually
		- use a merge tool
			git mergetool --tool=<tool_name>
			
	## Strategy to reduce merge conflicts	
		- keep lines short
		- keep commits small and focused
		- beware stray edits to whitespace
			- spaces, tabs, line returns
		- merge often
		- track changes to master (merge master in the branch)

## Stashing Changes
	- stash is not part of any repository, staging index or working directory
	- untracked files can also be stashed by using include untracked option
	
	git stash save "<message>" ->> stashing uncommited files which are changed 
	git stash list ->> will show us what's there in stash
	"stash@{0}" ->> reference to stash
	git stash show <stash reference> ->> shows diff stat
	git stash show -p <stash reference> ->> shows edits
	
	git stash pop <stash reference> ->> Pull into working directory and delete stashed item from stash
	git stash apply <stash reference> ->> Pull into working directory and keep a copy in stash
	git stash drop <stash reference> ->> Delete stash by the stash reference
	git stash clear ->> Clears the entire stash in once
	
# *6) Remotes*
	git remote ->> Let us know about all the remort it knows about
	git remote -v ->> give url for fetch and push
	git remote add <alias> <url> ->> adds a remote repository
	git remote rm <alias> ->> removes the remote
	git push -u origin master ->> pushes changes to origin 
	git branch -r ->> Shows all the remote branches
	git branch -a ->> Show all branches local or remote
	git clone <url> <folder name>
	git branch --set-upstream <branch_name> origing/<branch_name> ->> To start tracking non tracked branch
	git fetch origin ->> Sync up local origin repo with remote repo, didn't effect master in local repo
	git pull = git fetch + git merge
	git push origin :<branch_name> ->> delete a remote branch
	git push origin --delete <branch_name> ->> delete a remote branch
	
	
	Guidelines -
	- fetch before you work
	- fetch before you push
	- fetch often
	- fetch then merge
	
# *7) Aliases*
    git config --global alias.st "status" ->> Shortcut git st for git status
    git config --global alias.co "checkout" ->> Shortcut git co for git checkout
    git config --global alias.ci "commit" 
    git config --global alias.br "branch"
    git config --global alias.df "diff" 
    git config --global alias.dfs "diff --staged"
    git config --global alias.logg "log --graph --decorate --oneline --abbrev-commit --all"
		
	

