# GithubLearningRepo

This repository contains a simple static HTML project that showcases a location with an embedded Google Map.

## Project Overview

- `index.html` contains the full page structure, styling, and JavaScript.
- The page includes a hero section, a map section, an about section, and a contact section.
- This project does not require a build tool or package installation.

## Get Started

Clone the repository:

```bash
git clone https://github.com/<your-username>/GithubLearningRepo.git
cd GithubLearningRepo
```

Open the project locally:

```bash
# Option 1: open the HTML file directly
start index.html

# Option 2: open the project in VS Code
code .
```

If you use VS Code with Live Server, you can also run the page in a local browser from the editor.

## GitHub Full Instructions

### 1. Create a new repository on GitHub

1. Sign in to [GitHub](https://github.com/).
2. Click `New repository`.
3. Set the repository name to `GithubLearningRepo`.
4. Create the repository without adding a README if this local project already has one.

### 2. Connect your local project to GitHub

Run these commands inside the project folder:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/GithubLearningRepo.git
git push -u origin main
```

If the repository is already initialized, skip `git init`.

### 3. Daily GitHub workflow

Use these commands when making updates:

```bash
git status
git add .
git commit -m "Describe your change"
git push
```

### 4. Pull the latest changes

If you are working from multiple devices or with collaborators:

```bash
git pull origin main
```

### 5. Create a new branch for changes

This is useful for feature work or experiments:

```bash
git checkout -b feature/update-homepage
git add .
git commit -m "Update homepage"
git push -u origin feature/update-homepage
```

### 6. Open a pull request on GitHub

1. Push your branch to GitHub.
2. Open the repository in your browser.
3. Click `Compare & pull request`.
4. Review the changes and create the pull request.

## Useful Commands

```bash
git status
git log --oneline
git remote -v
git branch
```

## Notes

- Replace `<your-username>` with your real GitHub username.
- Because this is a static site, you can test it by simply opening `index.html` in a browser.
