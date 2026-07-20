# Git과 GitHub 기본 정리

> 강의 자료: Git & GitHub 기본 이론 (© Elice) — 10개 이론 강의 자료를 학습 순서대로 정리한 문서입니다.

## 목차

1. [코드 변경 관리의 중요성](#1-코드-변경-관리의-중요성)
2. [Git 개념과 환경 설정](#2-git-개념과-환경-설정)
3. [Git 초기 설정과 파일 생성](#3-git-초기-설정과-파일-생성)
4. [Git status — 파일 상태 확인](#4-git-status--파일-상태-확인)
5. [Git commit — 저장소에 반영](#5-git-commit--저장소에-반영)
6. [Git Branch — 브랜치](#6-git-branch--브랜치)
7. [Git Merge — 병합과 충돌 해결](#7-git-merge--병합과-충돌-해결)
8. [원격 저장소(GitHub)와 협업의 기본](#8-원격-저장소github와-협업의-기본)
9. [협업하기 (1) — Collaborator](#9-협업하기-1--collaborator)
10. [협업하기 (2) — Pull Request](#10-협업하기-2--pull-request)
11. [핵심 명령어 요약](#핵심-명령어-요약)

---

## 1. 코드 변경 관리의 중요성

### 왜 버전 관리가 필요한가

- 코드는 계속 바뀐다. 기능 추가, 버그 수정, 되돌리기가 반복된다.
- 변경 이력을 관리하지 않으면:
  - 언제, 누가, 무엇을 바꿨는지 알 수 없다
  - 이전 상태로 되돌리기 어렵다
  - 여러 명이 같은 파일을 수정할 때 충돌·덮어쓰기가 발생한다
- **버전 관리 시스템(VCS)** = 파일의 변경 이력을 체계적으로 기록·관리하는 도구.

### Git이 해결해 주는 것

- 변경 이력(누가/언제/무엇을)을 커밋 단위로 저장
- 원하는 시점으로 되돌리기
- 여러 작업을 브랜치로 분리해 동시에 진행
- 여러 사람이 하나의 프로젝트를 안전하게 협업

---

## 2. Git 개념과 환경 설정

### Git이란?

- **분산 버전 관리 시스템(Distributed VCS)**.
- 각 개발자가 전체 저장소(이력 포함)의 복사본을 로컬에 가진다 → 인터넷 없이도 작업·커밋 가능.

### Git의 3가지 영역

| 영역 | 설명 |
|---|---|
| Working Directory (작업 폴더) | 실제로 파일을 만들고 수정하는 공간 |
| Staging Area (준비 영역) | 커밋할 파일을 골라 담아두는 중간 공간 |
| Git Repository (저장소) | 커밋된 내용(이력)이 영구 저장되는 공간 |

- 기본 흐름: **Working Directory → (git add) → Staging Area → (git commit) → Repository**

### 설치 확인

```bash
$ git --version
```

- Git을 설치한 뒤 위 명령으로 버전이 출력되면 설치 완료.

---

## 3. Git 초기 설정과 파일 생성

### 1) 사용자 정보 설정

```bash
$ git config --global user.name "elice"
$ git config --global user.email gitaccount@elice.com
```

- 저장소에 코드를 반영(commit)할 때 **기록될 작성자 정보**를 설정한다.
- `--global`은 이 컴퓨터의 모든 저장소에 적용. **프로젝트마다 다른 정보를 쓰려면** 저장소 생성 후 `--global`을 빼고 실행.

### 2) 설정 정보 확인

```bash
$ git config --list
credential.helper=osxkeychain
user.name=elice
user.email=gitaccount@elice.com
...
```

### 3) Git 저장소 생성 — git init

```bash
$ git init
Initialized empty Git repository in /Users/elice/git_test/.git/
```

- 기존 디렉토리를 git repository로 설정. Git을 사용할 프로젝트 폴더로 이동 후 실행.

```bash
$ ls -al
drwxr-xr-x   3 elice  staff   96 11 11 21:45 .
drwx------+  5 elice  staff  160 11 11 21:45 ..
drwxr-xr-x  10 elice  staff  320 11 11 21:45 .git
```

- 프로젝트 디렉토리에 `.git` 디렉토리가 생성되면 저장소 생성 완료.

### 4) 파일 영역의 라이프 사이클

- 파일 상태: **Untracked → Unmodified → Modified → Staged**
  - `Untracked`: 한 번도 Git이 추적하지 않은 새 파일
  - Add the file → Staged, Edit → Modified, Stage the file → Staged, Commit → Unmodified

### 5) 파일을 Staging Area로 — git add

```bash
$ git add comment.js      # 특정 파일 하나
$ git add user.js         # 이어서 더 추가 가능
$ git add .               # 현재 폴더 내 전체 파일을 한 번에
```

- 작업한 파일을 **준비 영역(Staging Area)**으로 보낸다. 파일이 많으면 `git add .`로 전체 지정.

### 6) Staging 취소 — git reset

```bash
$ git reset <file_name>
```

- 위 명령으로 `add`(staging)를 취소할 수 있다.

---

## 4. Git status — 파일 상태 확인

```bash
$ git status
```

- 각 파일이 세 영역 중 **어디에 있는지**(Untracked / Staged / Modified 등)를 보여준다.

### Untracked files

- `add` 명령어로 staging되지 않은, **한 번도 commit되지 않은 파일들**.
- `git status`를 실행하면 어떤 파일이 Untracked인지, 어떤 파일이 staging되었는지 확인할 수 있다.
- 작업 중간중간 `git status`로 현재 상태를 점검하는 습관이 중요하다.

---

## 5. Git commit — 저장소에 반영

### commit이란

- Staging Area에 있는 파일들을 **저장소(Repository)에 영구 기록**하는 작업.
- 메시지는 생략 가능하지만, 나중에 이력을 쉽게 파악하도록 **적절한 메시지**를 남기는 것이 좋다.

```bash
$ git commit -m "커밋 메시지"
```

### commit 내용 변경 — amend

```bash
$ git commit --amend
```

- 방금 작성한 메시지에 오타가 있거나 누락된 파일이 있을 때 정정할 수 있다.
- 실행하면 텍스트 편집기가 열리고, 수정 후 저장하면 그대로 반영된다.

### commit 기록 확인 — git log

```bash
$ git log
```

- 지금까지의 커밋 이력(해시, 작성자, 날짜, 메시지)을 확인한다.

---

## 6. Git Branch — 브랜치

### Branch란

- **독립된 작업 공간**. 각 브랜치는 다른 브랜치의 영향을 받지 않으므로 **여러 작업을 동시에** 진행할 수 있다.
- `HEAD`는 현재 내가 위치한(작업 중인) 브랜치를 가리킨다.

### 브랜치 생성·이동

```bash
$ git branch new_branch        # new_branch 생성
$ git checkout new_branch       # new_branch로 이동
# 생성과 동시에 이동: git checkout -b new_branch
```

### 갈라지는 Branch

- 각 브랜치의 working directory에서 **같은 파일을 다르게 수정**할 수 있다.
- 예시: `c1 - c2`에서 시작해 `new_branch`(c3)와 `main`(c4)이 갈라짐.

```bash
$ git log --pretty=oneline --graph --all
* 0dd4b5e... (HEAD -> main) add main
| * a6a6ed1... (new_branch) add new_branch
|/
* aeb7765... Initial Commit
```

- `git log --pretty=oneline --graph --all`로 커밋 그래프를 보기 좋게 확인할 수 있다.

### 병합 후 브랜치 삭제

```bash
$ git branch --merged        # merge된 브랜치 목록 확인
* main
  new_branch

$ git branch -d new_branch   # 사용을 마친 브랜치 삭제
Deleted branch new_branch (was 1454fda).
```

---

## 7. Git Merge — 병합과 충돌 해결

### 기본 병합

```bash
$ git checkout main
switched to branch 'main'
$ git merge new_branch
Merge made by the 'ort' strategy.
 article.js | 1 +
 1 file changed, 1 insertion(+)
```

- `main`으로 checkout한 후 `git merge new_branch`로 병합. 갈라진 두 브랜치가 새 커밋(c5)으로 합쳐진다.

### Merge Conflict (충돌)

- **두 브랜치에서 같은 파일을 변경**했을 때 충돌이 발생한다.

```bash
$ git merge new_branch
Auto-merging article.js
CONFLICT (content): Merge conflict in article.js
Automatic merge failed; fix conflicts and then commit the result.
```

- `git status`로 어느 파일에서 충돌이 났는지 확인(`both modified: article.js`).

### 충돌 해결하기

- 충돌 파일을 열면 다음과 같은 표시가 들어 있다:

```javascript
const i = "article";
<<<<<<< HEAD
const main = "main";
=======
const article = "hello";
>>>>>>> new_branch
```

- 원하는 내용으로 직접 수정하고, `<<<<<<<`, `=======`, `>>>>>>>`가 포함된 행을 삭제한다:

```javascript
const i = "article";
const article = "hello";
```

- 이후 다시 add / commit 해서 병합을 마무리한다:

```bash
$ git add .
$ git commit -m "merged new_branch"
```

### Merge Conflict를 방지하려면?

- **`main` 브랜치의 변화를 지속적으로 가져와서**, 충돌이 발생하는 부분을 최대한 미리 제거한다.

---

## 8. 원격 저장소(GitHub)와 협업의 기본

### 원격 저장소(Remote Repository)란

- 인터넷이나 네트워크 어딘가에 있는 저장소. 대표적으로 **GitHub, GitLab**.
- 여러 사람이 같은 저장소를 공유하며 협업할 수 있다.

### 원격 저장소 받아오기 — git clone

```bash
$ git clone <repository_url>
$ git clone https://github.com/TheAlgorithms/Python.git
```

1. 원격에 있는 git repository를 복사하는 명령어
2. GitHub/GitLab 등에서 원하는 Repository의 `Code`(또는 `Clone`) 버튼을 누른다
3. 여러 옵션 중 **HTTPS** 주소를 복사
4. (이미 만든 로컬 저장소에 원격을 연결하려면 `git remote add` 사용 — 아래)

### 원격 저장소 연결 — git remote add

```bash
$ git remote add origin https://github.com/TheAlgorithms/Python.git
#                └origin┘ └────웹호스트──┘ └───그룹명────┘ └프로젝트명┘
```

- URL 구성: **웹 호스트 서비스 / 그룹(계정)명 / 프로젝트명**

### 연결 확인 — git remote show / -v

```bash
$ git remote show origin
* remote origin
  Fetch URL: https://github.com/.../git_test.git
  Push  URL: https://github.com/.../git_test.git
  HEAD branch: main
  ...

$ git remote -v
origin https://gitlab.com/group/project (fetch)
origin https://gitlab.com/group/project (push)
```

- `-v` 옵션으로 지정한 저장소의 이름과 주소를 함께 볼 수 있다.

### 원격 저장소 동기화 — Pull vs Fetch

| 명령 | 동작 |
|---|---|
| **Pull** | 원격 저장소에서 데이터 가져오기 **+ 병합(Merge)** |
| **Fetch** | 원격 저장소에서 데이터 **가져오기만** (병합은 하지 않음) |

**git pull** — 가져와서 로컬과 병합까지:

```bash
$ git pull
...
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
# git log --all → HEAD와 origin/main이 같은 커밋을 가리킴
```

**git fetch** — 가져오기만, 병합은 별도:

```bash
$ git fetch
...
   c61952d..932dd32  main -> origin/main
# git log --all → HEAD(main)와 origin/main이 서로 다른 위치
```

- fetch는 데이터만 가져오므로, **진행 중인 작업을 마무리하고 직접 병합**해 주어야 한다.

### 원격 저장소에 반영 — git push

```bash
$ git push origin main
```

- 로컬에서 작업한 내용을 원격 저장소에 반영한다.
- **협업 시 주의**: 다른 사람이 먼저 push한 상태에서는 push할 수 없다. **다른 사람 작업을 먼저 merge(pull)한 뒤** push한다.

### origin이란?

- `git remote add origin ...`은 원격 저장소의 **단축 이름을 `origin`으로 지정**한다는 의미.
- `origin`이 아닌 다른 이름(예: `myproject`)으로도 지정할 수 있다.
- 기본적으로 만들어진 원격 저장소 이름은 `origin`이 default. 그래서 `clone`으로 복사한 저장소의 이름은 `origin`으로 통일된다.

### 원격 저장소 작업 요약

1. `git remote add origin` (또는 다른 이름)으로 로컬 저장소와 **연결**
2. `git fetch` 또는 `git pull`로 원격 저장소 내용을 **동기화**
3. fetch를 실행한 경우 `git merge origin/main`으로 **병합**을 완료
4. `git push origin main`으로 변경 사항을 원격 저장소에 **반영**

---

## 9. 협업하기 (1) — Collaborator

### Collaborator란

- 같은 **Remote Repository를 직접 수정**하는 협업 방식.

### 팀원 등록 방법

- Repository → **Settings → Collaborators**에서 타 수강생(팀원)을 초대
- **초대받은 사람이 수락**해야 등록 완료

### 등록 후 할 수 있는 것

- Collaborator로 등록되면 Repository를 직접 수정 가능
- 연필 모양 버튼으로 **웹 상에서 바로 commit, push** 가능

### 협업 시 주의점

- 최신 버전 유지를 위해 **Remote Repository의 변경 사항을 로컬에 적용(Pull) 필수**
- 최신 버전이 유지되지 않으면 충돌이 발생해 원활한 협업이 불가능

---

## 10. 협업하기 (2) — Pull Request

### Collaborator 방식과의 차이

- Collaborator: 같은 저장소를 직접 수정
- Pull Request 방식: **내용은 같으나 따로 존재하는 Remote Repository**(원본 / 복사본)를 각자 수정하고 통합

### Fork

- **Fork = 내용이 동일한 Repository를 내 계정으로 복사**
- GitHub 저장소 우측 상단의 `Fork` 버튼으로 생성
- 포크한 저장소에서 수정을 해도 **원래(원본) 저장소에는 반영되지 않는다** (각자 본인의 Repository를 수정하므로).

### Pull Request (PR)

- **복사본(Fork)에서 원본으로 통합을 요청하는 것 = Pull Request (PR)**.
- 원본과 Fork를 **동기화시켜 주는 것이 Pull Request와 Merge**.
- PR을 **승인(Merge)하면 원본 또한 바뀐다**.

### PR 생성 흐름

1. **Comparing changes**: base repository(원본) ← head repository(내 Fork) 를 비교. `commit`을 기준으로 Pull Request를 생성할 수 있다.
2. **Open a pull request**: 어떤 변경이 있는지 **설명(제목·본문)을 작성**하고, 필요하면 **리뷰어(Reviewer)를 지정**한다.
3. **리뷰 & Merge**: PR이 오면 원작자는 내용을 리뷰한 후 **Commit 내용을 Merge**할 수 있다.
4. **Merge 완료**: Merge되면 커밋 내용들이 원본에 모두 정상 반영된다 (`Merge pull request #1 from ...` 커밋이 생성됨).

- 변경 내용을 시각화하면 커밋 그래프로 확인할 수 있다 (예시 프로그램: **GitKraken**).

---

## 핵심 명령어 요약

### 설정 & 초기화

| 명령어 | 설명 |
|---|---|
| `git --version` | 설치 확인 |
| `git config --global user.name "이름"` | 작성자 이름 설정 |
| `git config --global user.email 메일` | 작성자 이메일 설정 |
| `git config --list` | 설정 확인 |
| `git init` | 현재 폴더를 저장소로 초기화 |

### 기본 작업 흐름

| 명령어 | 설명 |
|---|---|
| `git status` | 파일 상태 확인 |
| `git add <파일>` / `git add .` | Staging Area에 추가 |
| `git reset <파일>` | add(staging) 취소 |
| `git commit -m "메시지"` | 저장소에 반영 |
| `git commit --amend` | 직전 커밋 수정 |
| `git log` | 커밋 이력 확인 |

### 브랜치 & 병합

| 명령어 | 설명 |
|---|---|
| `git branch <이름>` | 브랜치 생성 |
| `git checkout <이름>` | 브랜치 이동 (`-b`로 생성+이동) |
| `git log --pretty=oneline --graph --all` | 커밋 그래프 확인 |
| `git merge <브랜치>` | 현재 브랜치에 병합 |
| `git branch --merged` | 병합된 브랜치 확인 |
| `git branch -d <이름>` | 브랜치 삭제 |

### 원격 저장소

| 명령어 | 설명 |
|---|---|
| `git clone <url>` | 원격 저장소 복제 |
| `git remote add origin <url>` | 원격 저장소 연결 |
| `git remote -v` | 연결된 원격 확인 |
| `git fetch` | 원격 데이터 가져오기 (병합 X) |
| `git pull` | 가져오기 + 병합 |
| `git push origin main` | 로컬 변경을 원격에 반영 |

### 협업 개념

| 개념 | 설명 |
|---|---|
| Collaborator | 같은 저장소를 직접 수정 (Settings → Collaborators 초대) |
| Fork | 원본 저장소를 내 계정으로 복사 |
| Pull Request | 복사본 → 원본으로 통합 요청 (리뷰 후 Merge) |
