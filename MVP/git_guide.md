# Git & GitHub Collaboration Guide (Team Project)

This guide contains the basic Git and GitHub commands needed for a small team (e.g., 3 developers) to work on the same project while developing different modules.

---

## 1. One-Time Setup

Install Git and configure your identity.

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Verify configuration:

```bash
git config --list
```

---

## 2. Clone the Repository

Each team member clones the repository to their local machine.

```bash
git clone https://github.com/username/repository-name.git
```

Enter the project directory:

```bash
cd repository-name
```

---

## 3. Check Repository Status

Check which files are modified or staged.

```bash
git status
```

---

## 4. Pull Latest Changes (Do This First)

Before starting work, update your local repository.

```bash
git pull origin main
```

---

## 5. Create a New Branch for Your Feature

Each developer should work in a separate branch.

```bash
git checkout -b branch-name
```

Example:

```bash
git checkout -b login-module
```

---

## 6. Make Changes to the Code

Edit the project files as needed.

Check modified files:

```bash
git status
```

---

## 7. Stage Changes

Add files to the staging area.

Add a specific file:

```bash
git add filename
```

Add all changed files:

```bash
git add .
```

---

## 8. Commit Changes

Save staged changes with a clear commit message.

```bash
git commit -m "Add login validation logic"
```

---

## 9. Push Branch to GitHub

Upload your branch to GitHub.

```bash
git push origin branch-name
```

Example:

```bash
git push origin login-module
```

---

## 10. Create a Pull Request (PR)

1. Go to the repository on GitHub.
2. Click **Compare & Pull Request**.
3. Add a description of your changes.
4. Request teammates to review.
5. Merge after approval.

---

## 11. Update Local Main Branch After Merge

```bash
git checkout main
git pull origin main
```

---

## 12. Delete Finished Branch (Optional)

Delete local branch:

```bash
git branch -d branch-name
```

Delete remote branch:

```bash
git push origin --delete branch-name
```

---

## 13. List Branches

Local branches:

```bash
git branch
```

Remote branches:

```bash
git branch -r
```

---

## 14. Switch Branches

```bash
git checkout branch-name
```

Example:

```bash
git checkout main
```

---

## 15. Resolving Merge Conflicts

When Git reports a conflict, the file may contain markers like this:

```
<<<<<<< HEAD
your code
=======
incoming code
>>>>>>> branch-name
```

Steps to resolve:

1. Edit the file and keep the correct code.
2. Remove the conflict markers.
3. Stage and commit the fix.

```bash
git add .
git commit -m "Resolve merge conflict"
```

---

## Recommended Team Workflow

1. Pull latest `main`
2. Create a feature branch
3. Implement your module
4. Stage and commit changes
5. Push the branch
6. Create a Pull Request
7. Team reviews the code
8. Merge into `main`
9. Pull updated `main`

---

## Example Workflow

```bash
git pull origin main
git checkout -b payment-module

# edit project files

git add .
git commit -m "Implement payment module"
git push origin payment-module
```

Create a Pull Request on GitHub to merge the branch.

---

## Good Commit Message Examples

```
Add login authentication
Fix navbar alignment bug
Implement database connection
Refactor API request logic
```

Avoid vague messages like:

```
update
fix
changes
```

---

## Quick Command Cheat Sheet

| Task             | Command                       |
| ---------------- | ----------------------------- |
| Clone repository | `git clone repo-url`          |
| Check status     | `git status`                  |
| Pull updates     | `git pull origin main`        |
| Create branch    | `git checkout -b branch-name` |
| Stage files      | `git add .`                   |
| Commit changes   | `git commit -m "message"`     |
| Push branch      | `git push origin branch-name` |
| Switch branch    | `git checkout branch-name`    |

---
