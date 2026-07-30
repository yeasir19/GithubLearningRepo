# GitHub and GitLab CLI Commands

> Command-line field guide - a practical reference for `gh` and `glab`.

Installation | authentication | repositories | collaboration | releases | CI/CD | APIs | scripting

Updated 30 July 2026

Use gh help <command> or glab <command> --help to confirm flags in your installed version.

# Contents

- 1. Quick orientation and conventions

- 2. Install, authenticate, and configure

- 3. Repository and project work

- 4. Issues and pull requests / merge requests

- 5. Releases, snippets, and packages

- 6. CI/CD, pipelines, and automation

- 7. API calls, JSON output, aliases, and extensions

- 8. GitHub gh command reference

- 9. GitLab glab command reference

- 10. Cross-platform workflow recipes

- 11. Security, scripting, and troubleshooting

- 12. Official references

# 1. Quick orientation and conventions

GitHub CLI uses the executable gh. GitLab CLI uses glab. Both complement Git: Git handles local history, branches, commits, remotes, and pushes; the platform CLI handles hosted collaboration and platform APIs.

| Concept | GitHub | GitLab |
| --- | --- | --- |
| Repository | gh repo | glab repo |
| Code review | gh pr | glab mr |
| Work item | gh issue | glab issue |
| Automation | gh workflow / gh run | glab ci / glab pipeline |
| Release | gh release | glab release |
| API | gh api | glab api |
| Global help | gh help <command> | glab <command> --help |

## Universal patterns

- Run commands inside a cloned repository when possible; both CLIs infer the current project from the Git remote.

- Use -R OWNER/REPO with gh or -R GROUP/PROJECT with glab to target a repository explicitly.

- Use --web or -w for many commands to open the matching page in a browser.

- Use --json plus --jq (or --template where supported) for machine-readable output; never parse human-formatted output in scripts.

# 2. Install, authenticate, and configure

Install gh from cli.github.com or your OS package manager, and glab from docs.gitlab.com/cli or your package manager. Confirm installation before using either tool.

| Task | GitHub CLI (gh) | GitLab CLI (glab) |
| --- | --- | --- |
| Check version | gh --version | glab --version |
| Interactive sign-in | gh auth login | glab auth login |
| Token sign-in | TOKEN \| gh auth login --with-token | GITLAB_TOKEN=TOKEN glab auth login --token $env:GITLAB_TOKEN |
| Check account | gh auth status | glab auth status |
| Sign out | gh auth logout | glab auth logout |
| Set editor | gh config set editor code --wait | glab config set editor code --wait |
| Set host | gh auth login --hostname github.example.com | glab auth login --hostname gitlab.example.com |

## Authentication notes

- Prefer browser/device login for a workstation. For CI, inject short-lived tokens through the CI secret store, never source control.

- GitHub recognizes GITHUB_TOKEN; GitHub Enterprise automation commonly uses GH_ENTERPRISE_TOKEN. GitLab accepts GITLAB_TOKEN for non-interactive API authentication.

- Choose HTTPS or SSH intentionally during gh auth login. SSH needs an available key and access on the target host.

```shell
gh auth login --web --git-protocol ssh
glab auth login --hostname gitlab.example.com
```

# 3. Repository and project work

Use repository commands to create, clone, fork, inspect, and open projects. Native Git commands still own local branch and commit operations.

| Goal | GitHub | GitLab |
| --- | --- | --- |
| Create repository | gh repo create my-app --private --source=. --push | glab repo create my-app --private --source=. --push |
| Clone | gh repo clone OWNER/REPO | glab repo clone GROUP/PROJECT |
| Fork | gh repo fork OWNER/REPO --clone | glab repo fork GROUP/PROJECT --clone |
| View project | gh repo view --web | glab repo view --web |
| List own repos | gh repo list USER --limit 100 | glab repo list |
| Create branch + push | git switch -c feature/x; git push -u origin HEAD | git switch -c feature/x; git push -u origin HEAD |

## Useful repository commands

```shell
gh repo create my-org/demo --public --add-readme --license mit --clone
gh repo edit --enable-issues --enable-wiki=false --description "Example service"
glab repo create group/demo --private --defaultBranch main
glab repo view group/demo --web
```

# 4. Issues and pull requests / merge requests

Issues track work. GitHub calls code-review requests pull requests (PRs); GitLab calls them merge requests (MRs). Both tools can create, list, view, comment on, and merge them.

| Goal | GitHub gh | GitLab glab |
| --- | --- | --- |
| Create issue | gh issue create --title "Bug" --body "Details" --label bug | glab issue create --title "Bug" --description "Details" --label bug |
| List open issues | gh issue list --state open --limit 100 | glab issue list --state opened --per-page 100 |
| View issue | gh issue view 42 --comments | glab issue view 42 --comments |
| Close issue | gh issue close 42 | glab issue close 42 |
| Create review request | gh pr create --fill --base main | glab mr create --fill --target-branch main |
| List review requests | gh pr list --state open | glab mr list --state opened |
| Check out review branch | gh pr checkout 42 | glab mr checkout 42 |
| Review / comment | gh pr review 42 --approve --body "LGTM" | glab mr approve 42; glab mr note 42 --message "LGTM" |
| Merge | gh pr merge 42 --squash --delete-branch | glab mr merge 42 --squash --remove-source-branch |

## Review workflow

1. Create a branch and commit your changes with Git.

1. Push the branch: git push -u origin HEAD.

1. Open a PR or MR using --fill when commit metadata is sufficient, otherwise specify title/body.

1. Inspect CI status before merge; request review and respond to feedback.

1. Merge using the team-approved strategy (merge, squash, or rebase) and delete the source branch if policy permits.

```shell
gh pr create --title "Add health endpoint" --body "Closes #42" --base main
glab mr create --title "Add health endpoint" --description "Closes #42" --target-branch main
```

# 5. Releases, snippets, and packages

Release commands publish tagged software versions and attach build artifacts. A GitHub gist is a lightweight code/text share; GitLab snippets serve a similar purpose.

| Task | GitHub | GitLab |
| --- | --- | --- |
| Create release | gh release create v1.2.0 dist/app.zip --generate-notes | glab release create v1.2.0 dist/app.zip#app.zip --notes "Release notes" |
| List releases | gh release list | glab release list |
| View release | gh release view v1.2.0 | glab release view v1.2.0 |
| Download assets | gh release download v1.2.0 --pattern "*.zip" | glab release download v1.2.0 |
| Create snippet/gist | gh gist create script.sh --desc "Helper" | glab snippet create --title "Helper" --file script.sh |
| List snippets/gists | gh gist list | glab snippet list |

- Create and push the tag before or during release creation according to your release process. Validate artifacts and release notes before publishing.

# 6. CI/CD, pipelines, and automation

GitHub Actions uses workflow definitions and workflow runs. GitLab CI/CD uses .gitlab-ci.yml, pipelines, jobs, variables, and artifacts.

| Task | GitHub Actions via gh | GitLab CI/CD via glab |
| --- | --- | --- |
| List definitions | gh workflow list | glab ci list |
| Run manually | gh workflow run build.yml -f environment=staging | glab ci run --branch main |
| List executions | gh run list --workflow build.yml | glab pipeline list |
| Watch execution | gh run watch --exit-status | glab pipeline view <id> |
| View logs | gh run view <id> --log-failed | glab job trace <job-id> |
| Rerun | gh run rerun <id> --failed | glab pipeline retry <id> |
| Cancel | gh run cancel <id> | glab pipeline cancel <id> |
| Download artifacts | gh run download <id> --dir artifacts | glab job artifact <job-id> |

## Automation safety

- Use --exit-status with gh run watch when a script must fail if the workflow fails.

- Treat artifact downloads and reruns as stateful operations. Confirm the target run/pipeline ID, branch, and environment.

- Keep secrets in Actions secrets/variables or GitLab CI/CD variables. Never pass secrets through command-line flags when process listings or logs could expose them.

# 7. API calls, JSON output, aliases, and extensions

API commands fill gaps where a first-class CLI command is unavailable. Start by inspecting the documented REST/GraphQL endpoint, then make the smallest read-only call that proves the request.

| Pattern | GitHub gh | GitLab glab |
| --- | --- | --- |
| GET API | gh api repos/OWNER/REPO | glab api projects/:id |
| POST API | gh api -X POST repos/OWNER/REPO/labels -f name=bug | glab api -X POST projects/:id/labels -f name=bug |
| JSON projection | gh pr list --json number,title,url --jq .[] \| "#\\(.number) \\(.title)" | glab issue list --output json |
| Alias | gh alias set pv pr view | glab alias set pv mr view |
| Extensions/plugins | gh extension search; gh extension install OWNER/EXT | glab extension list; glab extension install <name> |

## Scripting patterns

```shell
gh issue list --state open --json number,title,url --jq .[] | {number,title,url}
glab api projects/:id/merge_requests?state=opened
```

- Quote shell metacharacters carefully. On PowerShell, prefer single quotes around literal JSON/JQ expressions; validate locally before adding to CI.

- Use pagination options (--paginate in gh api, per-page/page APIs in glab) when result sets can exceed defaults.

# 8. GitHub gh command reference

This section groups the most used gh command families. Run gh help <family> and gh <family> <subcommand> --help for the authoritative syntax installed on your machine.

| Family | What it does | Representative commands |
| --- | --- | --- |
| auth | Sign in, verify, refresh, log out | gh auth login \| status \| refresh \| logout |
| repo | Create, clone, fork, edit, view repositories | gh repo create \| clone \| fork \| view \| edit \| list |
| issue | Create and manage issues | gh issue create \| list \| view \| edit \| comment \| close \| reopen \| pin |
| pr | Manage pull requests and reviews | gh pr create \| list \| view \| checkout \| diff \| review \| merge \| checks |
| workflow / run | Manage Actions definitions and executions | gh workflow list \| run \| view; gh run list \| view \| watch \| rerun \| cancel |
| release | Publish releases and assets | gh release create \| list \| view \| upload \| download \| delete |
| project | Manage Projects | gh project list \| create \| item-list \| item-add \| item-edit |
| search | Search code, issues, PRs, repos | gh search code \| issues \| prs \| repos |
| secret / variable | Manage Actions and environment configuration | gh secret set \| list \| delete; gh variable set \| list \| get |
| api | Call GitHub REST or GraphQL APIs | gh api /repos/OWNER/REPO; gh api graphql |
| extension / alias | Customize CLI behavior | gh extension install; gh alias set |
| status / browse | Inspect status or open web context | gh status; gh browse |

## High-value gh examples

```shell
gh pr checks 42 --watch
gh issue develop 42 --name feature/issue-42 --checkout
gh release create v2.0.0 --generate-notes --latest
gh search code "TODO" --repo OWNER/REPO --language TypeScript
gh api graphql -f query=query { viewer { login } }
```

# 9. GitLab glab command reference

glab command coverage can vary with the installed version and GitLab edition. Consult glab <family> --help and the GitLab CLI documentation for current flags and availability.

| Family | What it does | Representative commands |
| --- | --- | --- |
| auth / config | Authenticate and set local/global behavior | glab auth login \| status \| logout; glab config get \| set \| edit |
| repo | Create, clone, fork, view repositories | glab repo create \| clone \| fork \| view \| list |
| issue | Create and manage issues | glab issue create \| list \| view \| update \| note \| close \| reopen |
| mr | Manage merge requests | glab mr create \| list \| view \| checkout \| diff \| approve \| note \| merge |
| pipeline / ci / job | Operate CI/CD pipelines and jobs | glab pipeline list \| view \| retry \| cancel; glab ci run; glab job trace |
| release | Publish and consume releases | glab release create \| list \| view \| download \| delete |
| api | Call GitLab API | glab api projects/:id; glab api groups/:id |
| snippet | Create and manage snippets | glab snippet create \| list \| view \| update \| delete |
| variable | Manage CI/CD variables | glab variable set \| list \| get \| delete |
| label / milestone | Organize work | glab label create \| list; glab milestone create \| list |
| schedule | Manage pipeline schedules | glab schedule create \| list \| run \| delete |
| alias / extension | Customize CLI behavior | glab alias set; glab extension install |

## High-value glab examples

```shell
glab mr create --fill --target-branch main --remove-source-branch
glab issue list --assignee @me --state opened
glab pipeline list --source push --per-page 20
glab job trace 123456
glab api projects/:id/variables
```

# 10. Cross-platform workflow recipes

The pairs below make migration and multi-host work easier. Substitute placeholders such as OWNER/REPO, GROUP/PROJECT, IDs, and branch names.

## Create a review request from the current branch

```shell
git push -u origin HEAD
gh pr create --fill --base main
glab mr create --fill --target-branch main
```

## Check review status and merge after CI

```shell
gh pr checks --watch; gh pr merge --squash --delete-branch
glab mr view 42; glab mr merge 42 --squash --remove-source-branch
```

## Triage assigned work

```shell
gh issue list --assignee @me --state open; gh pr list --author @me --state open
glab issue list --assignee @me --state opened; glab mr list --author @me --state opened
```

## Release a version

```shell
gh release create v1.0.0 dist/* --generate-notes
glab release create v1.0.0 dist/app.zip#app.zip --notes-file RELEASE_NOTES.md
```

# 11. Security, scripting, and troubleshooting

Most CLI failures come from authentication, a missing Git remote, insufficient permissions, an incorrect project selector, or an unsupported flag in the installed version.

## Security checklist

- Use least-privilege tokens and only the scopes required by the operation.

- Store tokens in OS credential storage or CI secret variables. Rotate and revoke tokens promptly when exposure is suspected.

- Avoid putting tokens, passwords, or production data in shell history, CLI arguments, pasted issue text, or logs.

- Use explicit repositories/projects in automation. Include a dry read (view/list) before destructive operations such as delete, close, merge, or release delete.

## Troubleshooting map

| Symptom | Checks | Likely fix |
| --- | --- | --- |
| Not authenticated | gh auth status / glab auth status | Log in again; check selected hostname and token scope. |
| Wrong project | git remote -v | Use -R OWNER/REPO or -R GROUP/PROJECT; confirm remote host. |
| 403 / forbidden | Account role and token scopes | Request required project/org role or a correctly scoped token. |
| Command/flag unknown | gh --version / glab --version | Run help; upgrade CLI or use the API documented for your version. |
| CI command fails | Run/pipeline ID, branch, logs | Use gh run view --log-failed or glab job trace <id>. |
| Script output fragile | Human-formatted output | Switch to --json/--jq or API JSON; assert exit codes. |

# 12. Official references

CLI features evolve frequently. Treat the local --help output and these official pages as the source of truth for exact flags, preview features, editions, and version-specific behavior.

GitHub CLI manual: https://cli.github.com/manual/index

GitHub CLI command reference: https://cli.github.com/manual/gh_help_reference

GitHub CLI authentication: https://cli.github.com/manual/gh_auth_login

GitLab CLI documentation: https://docs.gitlab.com/cli/

GitLab CLI command reference: https://docs.gitlab.com/cli/commands/

GitLab CLI authentication: https://docs.gitlab.com/cli/auth/login/

Document scope: a practical command reference, not a replacement for each platform’s version-specific manual. Commands marked as examples should be adapted to your organization, permissions, policies, and shell.
