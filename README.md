# Instructions

Use `git clone` to save a local copy of this repository. Here are the instructions about how to contribute to this repository.

## Making changes in the local repository

1. Create your own branch in your local repository. For example:

```
git branch mybranch
```

2. Push your branch to the remote repository (Skip this if you do not want to push your branch). For example:

```
git push -u origin mybranch
```

3. Switch to your branch, and do anything you want. You may want to commit and push your branch periodically.

```
git checkout mybranch

# do something...

git add .
git commit
git push
```

## Committing your changes to the master branch

1. Check if all your changes have been committed to your branch.

```
git status
```

2. Switch to the `master` branch.

```
git checkout master
```
3. Make sure your `master` branch is up-to-date.

```
git pull
```

4. Merge your branch to the `master` branch.

```
git merge mybranch
```

5. Push the `master` branch to the remote repository.

```
git push
```

6. Now `mybranch` is useless. You can delete it.

```
git branch -d mybranch
```

7. If you want to make further changes, create `mybranch` again and repeat the steps above.

## Why not directly commit to `master` branch?

Suppose that you make two commits `E` and `F` to the `master` branch of your local repository. In the mean time, someone else makes two commits `E'` and `F'` to the `master` branch of the remote repository, as shown below:

![branch-graph](/github-instructions-1.svg)

In this case, you cannot push your commits to the remote `master` branch. `git` will insist you run `git pull` on your local `master` branch first, before you can push it. 

This is more complicated. You have to manually resolve the conflicts, at the risk of losing your own commits if not done properly.

# Contents

## Homework Assignment 1
Dining Concierge Chatbot. See the README.md in `hw1` for more details

