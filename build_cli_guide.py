from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE

OUT = 'GitHub_and_GitLab_CLI_Command_Guide.docx'
BLUE = '2E74B5'; NAVY = '1F4D78'; PALE = 'E8EEF5'; LIGHT = 'F4F6F9'; MUTED = '5B6573'

def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), fill); tcPr.append(shd)

def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tcPr = cell._tc.get_or_add_tcPr(); mar = tcPr.first_child_found_in('w:tcMar')
    if mar is None: mar = OxmlElement('w:tcMar'); tcPr.append(mar)
    for side, value in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node = mar.find(qn('w:' + side))
        if node is None: node = OxmlElement('w:' + side); mar.append(node)
        node.set(qn('w:w'), str(value)); node.set(qn('w:type'), 'dxa')

def set_table_geometry(table, widths):
    table.autofit = False
    tblPr = table._tbl.tblPr
    for tag, attrs in [('w:tblW', {'w:w':'9360','w:type':'dxa'}), ('w:tblInd', {'w:w':'120','w:type':'dxa'}), ('w:tblLayout', {'w:type':'fixed'})]:
        e = tblPr.find(qn(tag))
        if e is None: e = OxmlElement(tag); tblPr.append(e)
        for k,v in attrs.items(): e.set(qn(k), v)
    grid = table._tbl.tblGrid
    for col, w in zip(grid.gridCol_lst, widths): col.set(qn('w:w'), str(w))
    for row in table.rows:
        for cell,w in zip(row.cells,widths):
            cell.width = Inches(w/1440)
            tcPr = cell._tc.get_or_add_tcPr(); tcW = tcPr.find(qn('w:tcW'))
            if tcW is None: tcW = OxmlElement('w:tcW'); tcPr.append(tcW)
            tcW.set(qn('w:w'), str(w)); tcW.set(qn('w:type'), 'dxa')
            set_cell_margins(cell); cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr(); node = OxmlElement('w:tblHeader'); node.set(qn('w:val'), 'true'); trPr.append(node)

def font(run, size=11, bold=False, color='000000', italic=False):
    run.font.name='Calibri'; run._element.rPr.rFonts.set(qn('w:ascii'),'Calibri'); run._element.rPr.rFonts.set(qn('w:hAnsi'),'Calibri')
    run.font.size=Pt(size); run.bold=bold; run.italic=italic; run.font.color.rgb=RGBColor.from_string(color)

def add_page_field(p):
    r=p.add_run('Page '); font(r,9,color=MUTED)
    fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); p._p.append(fld)

def add_p(doc, text='', style=None, before=None, after=None, align=None):
    p=doc.add_paragraph(style=style)
    if text: font(p.add_run(text))
    if before is not None: p.paragraph_format.space_before=Pt(before)
    if after is not None: p.paragraph_format.space_after=Pt(after)
    if align is not None: p.alignment=align
    return p

def code(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(2); p.paragraph_format.space_after=Pt(4)
    p.paragraph_format.left_indent=Inches(.22); p.paragraph_format.right_indent=Inches(.12)
    r=p.add_run(text); r.font.name='Consolas'; r._element.rPr.rFonts.set(qn('w:ascii'),'Consolas'); r._element.rPr.rFonts.set(qn('w:hAnsi'),'Consolas'); r.font.size=Pt(9.2); r.font.color.rgb=RGBColor.from_string('183B56')
    pPr=p._p.get_or_add_pPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'F4F6F9'); pPr.append(shd)
    return p

def bullet(doc, text):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1.25; font(p.add_run(text)); return p

def numbered(doc, text):
    p=doc.add_paragraph(style='List Number'); p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1.25; font(p.add_run(text)); return p

def table(doc, headers, rows, widths):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.LEFT; t.style='Table Grid'
    set_table_geometry(t, widths); hdr=t.rows[0]
    for i,h in enumerate(headers):
        c=hdr.cells[i]; set_cell_shading(c, PALE); p=c.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.LEFT; font(p.add_run(h),9.5,True,NAVY)
    set_repeat_table_header(hdr)
    for row in rows:
        cells=t.add_row().cells
        for i,val in enumerate(row):
            p=cells[i].paragraphs[0]; p.paragraph_format.space_after=Pt(0); font(p.add_run(val),9.2)
    return t

def h(doc, text, level=1): doc.add_heading(text, level=level)

def section_intro(doc, title, text):
    h(doc,title,1); add_p(doc,text,after=6)

doc=Document()
sec=doc.sections[0]; sec.top_margin=Inches(1); sec.bottom_margin=Inches(1); sec.left_margin=Inches(1); sec.right_margin=Inches(1); sec.header_distance=Inches(.492); sec.footer_distance=Inches(.492)

# Styles: compact_reference_guide tokens.
normal=doc.styles['Normal']; normal.font.name='Calibri'; normal._element.rPr.rFonts.set(qn('w:ascii'),'Calibri'); normal._element.rPr.rFonts.set(qn('w:hAnsi'),'Calibri'); normal.font.size=Pt(11); normal.paragraph_format.space_after=Pt(6); normal.paragraph_format.line_spacing=1.25
for name,size,color,before,after in [('Heading 1',16,BLUE,18,10),('Heading 2',13,BLUE,14,7),('Heading 3',12,NAVY,10,5)]:
    s=doc.styles[name]; s.font.name='Calibri'; s._element.rPr.rFonts.set(qn('w:ascii'),'Calibri'); s._element.rPr.rFonts.set(qn('w:hAnsi'),'Calibri'); s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=RGBColor.from_string(color); s.paragraph_format.space_before=Pt(before); s.paragraph_format.space_after=Pt(after); s.paragraph_format.keep_with_next=True

# Header/footer (editorial_cover pattern, restrained).
header=sec.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.LEFT; r=header.add_run('CLI REFERENCE GUIDE  |  GitHub gh + GitLab glab'); font(r,9,True,MUTED)
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT; add_page_field(footer)

# Cover
add_p(doc,'COMMAND-LINE FIELD GUIDE',after=18,align=WD_ALIGN_PARAGRAPH.CENTER)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(8); font(p.add_run('GitHub and GitLab CLI Commands'),30,True,'0B2545')
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(28); font(p.add_run('A practical reference for gh and glab'),15,False,MUTED)
add_p(doc,'Installation | authentication | repositories | collaboration | releases | CI/CD | APIs | scripting',after=80,align=WD_ALIGN_PARAGRAPH.CENTER)
add_p(doc,'Updated 30 July 2026',after=4,align=WD_ALIGN_PARAGRAPH.CENTER)
add_p(doc,'Use gh help <command> or glab <command> --help to confirm flags in your installed version.',after=0,align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

h(doc,'Contents',1)
for item in ['1. Quick orientation and conventions','2. Install, authenticate, and configure','3. Repository and project work','4. Issues and pull requests / merge requests','5. Releases, snippets, and packages','6. CI/CD, pipelines, and automation','7. API calls, JSON output, aliases, and extensions','8. GitHub gh command reference','9. GitLab glab command reference','10. Cross-platform workflow recipes','11. Security, scripting, and troubleshooting','12. Official references']:
    bullet(doc,item)

section_intro(doc,'1. Quick orientation and conventions','GitHub CLI uses the executable gh. GitLab CLI uses glab. Both complement Git: Git handles local history, branches, commits, remotes, and pushes; the platform CLI handles hosted collaboration and platform APIs.')
table(doc,['Concept','GitHub','GitLab'],[
    ['Repository','gh repo','glab repo'],['Code review','gh pr','glab mr'],['Work item','gh issue','glab issue'],['Automation','gh workflow / gh run','glab ci / glab pipeline'],['Release','gh release','glab release'],['API','gh api','glab api'],['Global help','gh help <command>','glab <command> --help']], [1800,3780,3780])
h(doc,'Universal patterns',2)
bullet(doc,'Run commands inside a cloned repository when possible; both CLIs infer the current project from the Git remote.')
bullet(doc,'Use -R OWNER/REPO with gh or -R GROUP/PROJECT with glab to target a repository explicitly.')
bullet(doc,'Use --web or -w for many commands to open the matching page in a browser.')
bullet(doc,'Use --json plus --jq (or --template where supported) for machine-readable output; never parse human-formatted output in scripts.')

section_intro(doc,'2. Install, authenticate, and configure','Install gh from cli.github.com or your OS package manager, and glab from docs.gitlab.com/cli or your package manager. Confirm installation before using either tool.')
table(doc,['Task','GitHub CLI (gh)','GitLab CLI (glab)'],[
    ['Check version','gh --version','glab --version'],['Interactive sign-in','gh auth login','glab auth login'],['Token sign-in','TOKEN | gh auth login --with-token','GITLAB_TOKEN=TOKEN glab auth login --token $env:GITLAB_TOKEN'],['Check account','gh auth status','glab auth status'],['Sign out','gh auth logout','glab auth logout'],['Set editor','gh config set editor code --wait','glab config set editor code --wait'],['Set host','gh auth login --hostname github.example.com','glab auth login --hostname gitlab.example.com']], [1850,3755,3755])
h(doc,'Authentication notes',2)
bullet(doc,'Prefer browser/device login for a workstation. For CI, inject short-lived tokens through the CI secret store, never source control.')
bullet(doc,'GitHub recognizes GITHUB_TOKEN; GitHub Enterprise automation commonly uses GH_ENTERPRISE_TOKEN. GitLab accepts GITLAB_TOKEN for non-interactive API authentication.')
bullet(doc,'Choose HTTPS or SSH intentionally during gh auth login. SSH needs an available key and access on the target host.')
code(doc,'gh auth login --web --git-protocol ssh')
code(doc,'glab auth login --hostname gitlab.example.com')

section_intro(doc,'3. Repository and project work','Use repository commands to create, clone, fork, inspect, and open projects. Native Git commands still own local branch and commit operations.')
table(doc,['Goal','GitHub','GitLab'],[
 ['Create repository','gh repo create my-app --private --source=. --push','glab repo create my-app --private --source=. --push'],
 ['Clone','gh repo clone OWNER/REPO','glab repo clone GROUP/PROJECT'],
 ['Fork','gh repo fork OWNER/REPO --clone','glab repo fork GROUP/PROJECT --clone'],
 ['View project','gh repo view --web','glab repo view --web'],
 ['List own repos','gh repo list USER --limit 100','glab repo list'],
 ['Create branch + push','git switch -c feature/x; git push -u origin HEAD','git switch -c feature/x; git push -u origin HEAD']], [1850,3755,3755])
h(doc,'Useful repository commands',2)
code(doc,'gh repo create my-org/demo --public --add-readme --license mit --clone')
code(doc,'gh repo edit --enable-issues --enable-wiki=false --description "Example service"')
code(doc,'glab repo create group/demo --private --defaultBranch main')
code(doc,'glab repo view group/demo --web')

section_intro(doc,'4. Issues and pull requests / merge requests','Issues track work. GitHub calls code-review requests pull requests (PRs); GitLab calls them merge requests (MRs). Both tools can create, list, view, comment on, and merge them.')
table(doc,['Goal','GitHub gh','GitLab glab'],[
 ['Create issue','gh issue create --title "Bug" --body "Details" --label bug','glab issue create --title "Bug" --description "Details" --label bug'],
 ['List open issues','gh issue list --state open --limit 100','glab issue list --state opened --per-page 100'],
 ['View issue','gh issue view 42 --comments','glab issue view 42 --comments'],
 ['Close issue','gh issue close 42','glab issue close 42'],
 ['Create review request','gh pr create --fill --base main','glab mr create --fill --target-branch main'],
 ['List review requests','gh pr list --state open','glab mr list --state opened'],
 ['Check out review branch','gh pr checkout 42','glab mr checkout 42'],
 ['Review / comment','gh pr review 42 --approve --body "LGTM"','glab mr approve 42; glab mr note 42 --message "LGTM"'],
 ['Merge','gh pr merge 42 --squash --delete-branch','glab mr merge 42 --squash --remove-source-branch']], [1900,3730,3730])
h(doc,'Review workflow',2)
for step in ['Create a branch and commit your changes with Git.','Push the branch: git push -u origin HEAD.','Open a PR or MR using --fill when commit metadata is sufficient, otherwise specify title/body.','Inspect CI status before merge; request review and respond to feedback.','Merge using the team-approved strategy (merge, squash, or rebase) and delete the source branch if policy permits.']:
    numbered(doc,step)
code(doc,'gh pr create --title "Add health endpoint" --body "Closes #42" --base main')
code(doc,'glab mr create --title "Add health endpoint" --description "Closes #42" --target-branch main')

section_intro(doc,'5. Releases, snippets, and packages','Release commands publish tagged software versions and attach build artifacts. A GitHub gist is a lightweight code/text share; GitLab snippets serve a similar purpose.')
table(doc,['Task','GitHub','GitLab'],[
 ['Create release','gh release create v1.2.0 dist/app.zip --generate-notes','glab release create v1.2.0 dist/app.zip#app.zip --notes "Release notes"'],
 ['List releases','gh release list','glab release list'],
 ['View release','gh release view v1.2.0','glab release view v1.2.0'],
 ['Download assets','gh release download v1.2.0 --pattern "*.zip"','glab release download v1.2.0'],
 ['Create snippet/gist','gh gist create script.sh --desc "Helper"','glab snippet create --title "Helper" --file script.sh'],
 ['List snippets/gists','gh gist list','glab snippet list']], [1900,3730,3730])
bullet(doc,'Create and push the tag before or during release creation according to your release process. Validate artifacts and release notes before publishing.')

section_intro(doc,'6. CI/CD, pipelines, and automation','GitHub Actions uses workflow definitions and workflow runs. GitLab CI/CD uses .gitlab-ci.yml, pipelines, jobs, variables, and artifacts.')
table(doc,['Task','GitHub Actions via gh','GitLab CI/CD via glab'],[
 ['List definitions','gh workflow list','glab ci list'],
 ['Run manually','gh workflow run build.yml -f environment=staging','glab ci run --branch main'],
 ['List executions','gh run list --workflow build.yml','glab pipeline list'],
 ['Watch execution','gh run watch --exit-status','glab pipeline view <id>'],
 ['View logs','gh run view <id> --log-failed','glab job trace <job-id>'],
 ['Rerun','gh run rerun <id> --failed','glab pipeline retry <id>'],
 ['Cancel','gh run cancel <id>','glab pipeline cancel <id>'],
 ['Download artifacts','gh run download <id> --dir artifacts','glab job artifact <job-id>']], [1900,3730,3730])
h(doc,'Automation safety',2)
bullet(doc,'Use --exit-status with gh run watch when a script must fail if the workflow fails.')
bullet(doc,'Treat artifact downloads and reruns as stateful operations. Confirm the target run/pipeline ID, branch, and environment.')
bullet(doc,'Keep secrets in Actions secrets/variables or GitLab CI/CD variables. Never pass secrets through command-line flags when process listings or logs could expose them.')

section_intro(doc,'7. API calls, JSON output, aliases, and extensions','API commands fill gaps where a first-class CLI command is unavailable. Start by inspecting the documented REST/GraphQL endpoint, then make the smallest read-only call that proves the request.')
table(doc,['Pattern','GitHub gh','GitLab glab'],[
 ['GET API','gh api repos/OWNER/REPO','glab api projects/:id'],
 ['POST API','gh api -X POST repos/OWNER/REPO/labels -f name=bug','glab api -X POST projects/:id/labels -f name=bug'],
 ['JSON projection','gh pr list --json number,title,url --jq ''.[] | "#\\(.number) \\(.title)"''','glab issue list --output json'],
 ['Alias','gh alias set pv ''pr view''','glab alias set pv ''mr view'''],
 ['Extensions/plugins','gh extension search; gh extension install OWNER/EXT','glab extension list; glab extension install <name>']], [1900,3730,3730])
h(doc,'Scripting patterns',2)
code(doc,'gh issue list --state open --json number,title,url --jq ''.[] | {number,title,url}''')
code(doc,'glab api projects/:id/merge_requests?state=opened')
bullet(doc,'Quote shell metacharacters carefully. On PowerShell, prefer single quotes around literal JSON/JQ expressions; validate locally before adding to CI.')
bullet(doc,'Use pagination options (--paginate in gh api, per-page/page APIs in glab) when result sets can exceed defaults.')

section_intro(doc,'8. GitHub gh command reference','This section groups the most used gh command families. Run gh help <family> and gh <family> <subcommand> --help for the authoritative syntax installed on your machine.')
table(doc,['Family','What it does','Representative commands'],[
 ['auth','Sign in, verify, refresh, log out','gh auth login | status | refresh | logout'],
 ['repo','Create, clone, fork, edit, view repositories','gh repo create | clone | fork | view | edit | list'],
 ['issue','Create and manage issues','gh issue create | list | view | edit | comment | close | reopen | pin'],
 ['pr','Manage pull requests and reviews','gh pr create | list | view | checkout | diff | review | merge | checks'],
 ['workflow / run','Manage Actions definitions and executions','gh workflow list | run | view; gh run list | view | watch | rerun | cancel'],
 ['release','Publish releases and assets','gh release create | list | view | upload | download | delete'],
 ['project','Manage Projects','gh project list | create | item-list | item-add | item-edit'],
 ['search','Search code, issues, PRs, repos','gh search code | issues | prs | repos'],
 ['secret / variable','Manage Actions and environment configuration','gh secret set | list | delete; gh variable set | list | get'],
 ['api','Call GitHub REST or GraphQL APIs','gh api /repos/OWNER/REPO; gh api graphql'],
 ['extension / alias','Customize CLI behavior','gh extension install; gh alias set'],
 ['status / browse','Inspect status or open web context','gh status; gh browse']], [1600,2600,5160])
h(doc,'High-value gh examples',2)
code(doc,'gh pr checks 42 --watch')
code(doc,'gh issue develop 42 --name feature/issue-42 --checkout')
code(doc,'gh release create v2.0.0 --generate-notes --latest')
code(doc,'gh search code "TODO" --repo OWNER/REPO --language TypeScript')
code(doc,'gh api graphql -f query=''query { viewer { login } }''')

section_intro(doc,'9. GitLab glab command reference','glab command coverage can vary with the installed version and GitLab edition. Consult glab <family> --help and the GitLab CLI documentation for current flags and availability.')
table(doc,['Family','What it does','Representative commands'],[
 ['auth / config','Authenticate and set local/global behavior','glab auth login | status | logout; glab config get | set | edit'],
 ['repo','Create, clone, fork, view repositories','glab repo create | clone | fork | view | list'],
 ['issue','Create and manage issues','glab issue create | list | view | update | note | close | reopen'],
 ['mr','Manage merge requests','glab mr create | list | view | checkout | diff | approve | note | merge'],
 ['pipeline / ci / job','Operate CI/CD pipelines and jobs','glab pipeline list | view | retry | cancel; glab ci run; glab job trace'],
 ['release','Publish and consume releases','glab release create | list | view | download | delete'],
 ['api','Call GitLab API','glab api projects/:id; glab api groups/:id'],
 ['snippet','Create and manage snippets','glab snippet create | list | view | update | delete'],
 ['variable','Manage CI/CD variables','glab variable set | list | get | delete'],
 ['label / milestone','Organize work','glab label create | list; glab milestone create | list'],
 ['schedule','Manage pipeline schedules','glab schedule create | list | run | delete'],
 ['alias / extension','Customize CLI behavior','glab alias set; glab extension install']], [1600,2600,5160])
h(doc,'High-value glab examples',2)
code(doc,'glab mr create --fill --target-branch main --remove-source-branch')
code(doc,'glab issue list --assignee @me --state opened')
code(doc,'glab pipeline list --source push --per-page 20')
code(doc,'glab job trace 123456')
code(doc,'glab api projects/:id/variables')

section_intro(doc,'10. Cross-platform workflow recipes','The pairs below make migration and multi-host work easier. Substitute placeholders such as OWNER/REPO, GROUP/PROJECT, IDs, and branch names.')
h(doc,'Create a review request from the current branch',2)
code(doc,'git push -u origin HEAD')
code(doc,'gh pr create --fill --base main')
code(doc,'glab mr create --fill --target-branch main')
h(doc,'Check review status and merge after CI',2)
code(doc,'gh pr checks --watch; gh pr merge --squash --delete-branch')
code(doc,'glab mr view 42; glab mr merge 42 --squash --remove-source-branch')
h(doc,'Triage assigned work',2)
code(doc,'gh issue list --assignee @me --state open; gh pr list --author @me --state open')
code(doc,'glab issue list --assignee @me --state opened; glab mr list --author @me --state opened')
h(doc,'Release a version',2)
code(doc,'gh release create v1.0.0 dist/* --generate-notes')
code(doc,'glab release create v1.0.0 dist/app.zip#app.zip --notes-file RELEASE_NOTES.md')

section_intro(doc,'11. Security, scripting, and troubleshooting','Most CLI failures come from authentication, a missing Git remote, insufficient permissions, an incorrect project selector, or an unsupported flag in the installed version.')
h(doc,'Security checklist',2)
bullet(doc,'Use least-privilege tokens and only the scopes required by the operation.')
bullet(doc,'Store tokens in OS credential storage or CI secret variables. Rotate and revoke tokens promptly when exposure is suspected.')
bullet(doc,'Avoid putting tokens, passwords, or production data in shell history, CLI arguments, pasted issue text, or logs.')
bullet(doc,'Use explicit repositories/projects in automation. Include a dry read (view/list) before destructive operations such as delete, close, merge, or release delete.')
h(doc,'Troubleshooting map',2)
table(doc,['Symptom','Checks','Likely fix'],[
 ['Not authenticated','gh auth status / glab auth status','Log in again; check selected hostname and token scope.'],
 ['Wrong project','git remote -v','Use -R OWNER/REPO or -R GROUP/PROJECT; confirm remote host.'],
 ['403 / forbidden','Account role and token scopes','Request required project/org role or a correctly scoped token.'],
 ['Command/flag unknown','gh --version / glab --version','Run help; upgrade CLI or use the API documented for your version.'],
 ['CI command fails','Run/pipeline ID, branch, logs','Use gh run view --log-failed or glab job trace <id>.'],
 ['Script output fragile','Human-formatted output','Switch to --json/--jq or API JSON; assert exit codes.']], [1900,3400,4060])

section_intro(doc,'12. Official references','CLI features evolve frequently. Treat the local --help output and these official pages as the source of truth for exact flags, preview features, editions, and version-specific behavior.')
refs=[
 ('GitHub CLI manual','https://cli.github.com/manual/index'),
 ('GitHub CLI command reference','https://cli.github.com/manual/gh_help_reference'),
 ('GitHub CLI authentication','https://cli.github.com/manual/gh_auth_login'),
 ('GitLab CLI documentation','https://docs.gitlab.com/cli/'),
 ('GitLab CLI command reference','https://docs.gitlab.com/cli/commands/'),
 ('GitLab CLI authentication','https://docs.gitlab.com/cli/auth/login/'),
]
for label,url in refs:
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(4); r=p.add_run(label + ': '); font(r,11,True,NAVY); r=p.add_run(url); font(r,10.5,False,'0563C1')
add_p(doc,'Document scope: a practical command reference, not a replacement for each platform’s version-specific manual. Commands marked as examples should be adapted to your organization, permissions, policies, and shell.',before=14,after=0)

doc.core_properties.title='GitHub and GitLab CLI Command Guide'
doc.core_properties.subject='Practical reference for gh and glab'
doc.core_properties.author='Codex'
doc.save(OUT)
print(OUT)
