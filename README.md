# stock_screener

# Governance and Administration 
[Git Workflow and Project](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

### Branch
- main = contain abridged version -- commit when having new release
- develop = contain complete history of the project -- **keep origin/develop updated** by committing development progress
- feature/xxx = contain feature development -- commit when development finish 
- release = contain snapshot of develop branch

### Procedure
1. create feature branch
   1. without git-flow: 

Note: always start from develop branch

> git checkout develop` 
> 
> git checkout -b feature_xx

   2. with git-flow: 

> git flow `feature start` feature_xx

2. -- develop, add, and commit on feature branch -- 
3. finish feature branch 
   1. without git-flow: 

Note: always start from develop branch

> git checkout develop
>
> git merge feature_xx

   2. with git-flow:
> git flow `feature finish` feature_xx

4. release branch
   1. without git-flow 

> git checkout develop
> git checkout -b release/0.1.0
> git checkout main
> git merge release/0.1.0
   
   2. with git-flow
 
> git flow `release start` 0.1.0
> git flow `release finish` '0.1.0

  