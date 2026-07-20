# GitHub에서 프로젝트 관리하기 정리

> 강의 자료: GitHub에서 프로젝트 관리하기 (© Elice) — 4개 이론 자료(저장소 생성 / Branch 생성과 Pull Request / Issue 생성하기 / Wiki 작성하기)를 실습 순서대로 정리한 문서입니다.
> 모든 실습은 **GitHub 웹 화면에서** 진행합니다 (터미널 명령 없이).

## 목차

1. [GitHub 저장소 생성](#1-github-저장소-생성)
2. [Branch 생성과 Pull Request](#2-branch-생성과-pull-request)
3. [Issue 생성하기](#3-issue-생성하기)
4. [Wiki 작성하기](#4-wiki-작성하기)
5. [핵심 요약](#5-핵심-요약)

---

## 1. GitHub 저장소 생성

### GitHub 접속하기

1. [GitHub](https://github.com) 접속
2. 우측 상단 **Sign in** 클릭 (계정이 없으면 Sign up)

### 레포지토리(Repository)란?

- **하나의 코드 저장소** — 로컬 파일 기준으로 하나의 폴더
- **프로젝트 하나 = Repository 하나**
- 기술 스택 등에 따라 같은 프로젝트 안에서 여러 개의 Repository를 만들기도 함
- 줄여서 **'레포(repo)'** 라고도 표현

### Create repository — 생성 절차

1. 로그인 후 대시보드에서 **Create repository** 클릭
2. **Repository name** 입력 (Owner는 본인 계정)
3. 아래 설정 항목을 지정하고 **Create repository** 클릭

**Repository 생성 시 설정 항목**

| 항목 | 설명 |
|---|---|
| Template | 템플릿 저장소에서 시작할지 여부 |
| Owner | 저장소 소유자 (계정/조직) |
| Repository name | 저장소 이름 (필수) |
| Description | 저장소 설명 (선택) |
| 공개 범위 | Public / Private |
| Add README | README 파일 자동 생성 여부 |
| Add .gitignore | 언어/프레임워크별 .gitignore 템플릿 |
| Add license | 라이선스 지정 |

### 공개 범위 — Public vs Private

| Public | Private |
|---|---|
| Repository를 누구나 조회 가능 | 특정 사용자만 조회 가능 |
| 하나의 포트폴리오가 되기도 함 | 외부 노출이 안 되어 비공개 프로젝트 가능 |
| 외부 서비스 연동 시 비교적 간편 | 무료 사용자에게는 기능이 일부 제한 |
| **민감 정보는 절대 업로드 X (패스워드 등)** | 주로 사내 업무는 Private |

### README란?

- Repository에 대해 **설명하는 글**
- 설치 및 실행 방법, 사용법, 기여하는 방법, License 및 저작권 정보 제공
- 사용자·개발자가 프로젝트를 이해하기 쉬워짐 → **프로젝트 신뢰도와 완성도가 올라가는 효과**
- 원활한 커뮤니케이션을 위한 기본기
- 주로 **Markdown 문법**으로 작성
- 좋은 README 참고: https://github.com/matiassingers/awesome-readme

### .gitignore란?

- **Git이 무시해야 하는 파일이나 폴더를 지정**
- 지정되면 Repository에 업로드되지 않음
- 불필요한 파일, 비밀번호 등 보안 파일을 지정하여 **효율적이고 보안을 유지한 운용**
- 다양한 언어와 프레임워크별 템플릿 존재

### license란?

- SW 사용, 배포, 수정 등의 **권한을 정의**
- 사람들이 어떤 조건으로 코드를 사용하고 변경할 수 있는지를 명확히 규정
- 각 license마다 사용과 배포 조건이 다름
- 개인 공부나 간단한 프로젝트에는 지정하지 않아도 무방
- **타인의 코드 사용 시 반드시 확인해야 함**
- 참고: https://choosealicense.com/

---

## 2. Branch 생성과 Pull Request

GitHub 웹에서 브랜치를 만들고, 파일을 수정해 커밋한 뒤, Pull Request로 main에 병합하는 전체 흐름.

### 1) Branch 생성하기

1. 실습용 Repository(First-Repository) 접속
2. 파일 목록 위의 **N Branch** 표시 클릭 → Branches 화면으로 이동
3. 우측 상단 **New branch** 클릭
4. New branch name 입력 (예: `feature/readme`) — Source는 `main`
5. **Create new branch** 클릭

### 2) Branch 변경하기 (이동)

1. Repository 메인으로 이동
2. 좌측 상단 **main 브랜치 드롭다운** 클릭
3. 생성한 **feature/readme** 브랜치 클릭 → 현재 보는 브랜치가 전환됨

### 3) README 편집하기

1. feature/readme 브랜치 상태에서 README의 **연필 아이콘(Edit file)** 클릭
2. 내용 입력 (예시):

```markdown
# First Repository
**Git & GitHub 학습용 저장소**입니다.
- 브랜치, Pull Request, merge 등 협업 기능을 실습합니다.
```

3. 우측 상단 **Commit changes...** 클릭

### 4) Commit 하기

1. Commit message 입력 (예: `Update README.md`)
2. **Commit directly to the feature/readme branch** 선택 (지금 있는 브랜치에 바로 커밋)
3. **Commit changes** 클릭

### 5) Pull Request 만들기

1. 상단바에서 **Pull requests** 클릭
2. `feature/readme had recent pushes` 배너의 **Compare & pull request** 클릭
3. 좌측 상단의 브랜치 방향 확인:
   - **base**: 최종적으로 변경사항이 **들어가야 하는** 브랜치 (예: main)
   - **compare**: 변경사항을 **보내는** 브랜치 (예: feature/readme)
4. 제목·**Add a description** 입력 (예: "README에 본 Repository에 대한 개요를 추가하였습니다.")
5. **Create pull request** 클릭

### 6) Merge 하기

1. `No conflicts with base branch` — **충돌이 없다면 Merge pull request 클릭**
2. 필요 시 우측 **Reviewers**에서 Pull Request를 검토할 리뷰어를 지정할 수 있다
3. Merge 후 상단바 → **Commits** 클릭해 변경 내용(diff)이 main에 반영되었는지 확인
4. PR 상태가 **Merged** (보라색 뱃지)로 바뀌면 완료

---

## 3. Issue 생성하기

### Issue란?

- **작업 항목, 버그, 기능 요청 등의 추적 및 관리**를 위해 사용하는 도구
- 협업을 위한 도구로서의 기능을 제공
- 담당자(assignee) 설정, Pull Request와 연계하는 등 **작업을 구조화하고 진행 상황을 추적**하는 데 중요한 역할

### Issue Templates 만들기

이슈를 일정한 형식으로 작성하도록 템플릿을 미리 만들어 둘 수 있다.

1. 상단바 → **Settings** 클릭
2. 스크롤을 내려 **Features** 섹션에서 **Issues → Set up templates** 클릭
3. **Add template: select** 드롭다운에서 선택:
   - Bug report — 표준 버그 리포트 템플릿
   - **Feature request** — 표준 기능 요청 템플릿
   - Custom template — 빈 템플릿
4. 추가된 템플릿의 **Preview and edit** 클릭
5. 내용 입력 후 우측 상단 **Propose changes → Commit changes** 클릭

**템플릿 구성 요소**

| 항목 | 설명 |
|---|---|
| Template name | 템플릿 이름. 이슈 생성 시 템플릿 선택 옵션으로 보여짐 |
| About | 템플릿 이름 옆에 보이는 간단한 설명 |
| Template content | 실제 이슈 작성 시의 본문 템플릿 (마크다운 지원) |
| Issue default title | 이슈 제목의 기본값(placeholder) |
| Assignees | 기본으로 배정할 담당자 |
| Labels | 기본으로 붙일 라벨 (버그/기능 등 다양한 라벨 존재) |

**기능 개발 템플릿 예시** (실습 입력값)

- Template name: `기능 개발 템플릿`
- About: `개발해야 하는 기능을 단위별로 명세합니다.`
- Template content:

```markdown
## ✏️ Description
작업에 대한 간단한 설명을 작성합니다.

## ✅ Todos
- [ ] TODO
- [ ] TODO
```

- Issue default title: `[Feat] 로그인 기능 구현`

### Issue 작성하기

1. 상단바 → **Issues** 클릭
2. 우측 상단 **New issue** 클릭
3. 만들어 둔 **기능 개발 템플릿** 클릭 (또는 Blank issue)
4. 제목·본문을 템플릿 형식에 맞게 입력 (예시):

```markdown
## ✏️ Description
필요한 페이지들의 기본 라우팅 구조를 설정하고, 각각의 페이지에서 사용할 기본 레이아웃을 구성합니다.

## ✅ Todos
- [ ] 로그인 페이지와 Admin 페이지의 라우팅 구조 설계
- [ ] 두 페이지에 공통적으로 적용될 기본 레이아웃 구성
```

5. **Create** 클릭
6. 생성된 Issue 확인 — Todos는 체크박스로 표시되어 진행 상황을 추적할 수 있고, 우측 패널에서 Assignees·Labels·Milestone 등을 관리. `Create a branch` 링크로 이슈와 연결된 브랜치를 만들 수도 있다.

---

## 4. Wiki 작성하기

### Wiki란?

- README보다 **더 자세하고 구조적인 문서**를 작성할 수 있는 **프로젝트 지식 저장소** 역할
- **Public Repository를 생성하면 사용 가능** (Private는 유료 플랜 필요)

### 실습용 Repository 만들기

Wiki 실습을 위해 아래 조건으로 새 Repository 생성:

| 항목 | 값 |
|---|---|
| Repository name | Wiki repository |
| Choose visibility | **Public** (필수 — Wiki 사용 조건) |
| Add README | ON |
| Add .gitignore | No .gitignore |
| Add license | No license |

### Wiki 페이지 만들기

1. 상단바 → **Wiki** 클릭
2. **Create the first page** 클릭
3. 내용 입력 (Markdown 지원, Edit mode에서 Markdown 선택 가능). 예시:

```markdown
# 🏠 프로젝트 Wiki

프로젝트의 기본 정보와 개발 내용을 정리한 문서 모음입니다.

---

## 📄 문서 목록

* [📘 프로젝트 소개](#-프로젝트-소개)
* [📁 폴더 구조](#-폴더-구조)
* [🔧 개발 가이드](#-개발-가이드)

---

## 📘 프로젝트 소개

> 이 프로젝트는 기본 페이지 구성, 라우팅, 레이아웃 구현을 중심으로 한 실습용 저장소입니다.
```

4. **Save page** 클릭
5. 결과 확인 — 우측 **Pages** 패널에 문서 목차가 자동 생성되고, `Add a custom sidebar`로 사이드바 구성, `Clone this wiki locally` 주소로 위키 저장소 자체를 clone할 수도 있다.

---

## 5. 핵심 요약

| 기능 | 위치 | 용도 |
|---|---|---|
| Repository 생성 | Create repository | 프로젝트 하나 = 저장소 하나. Public/Private, README, .gitignore, license 설정 |
| Branch | Branches → New branch | 웹에서 브랜치 생성·전환 (예: `feature/readme`) |
| Commit (웹) | 파일 편집 → Commit changes | 연필 아이콘으로 수정 후 현재 브랜치에 직접 커밋 |
| Pull Request | Pull requests → Compare & pull request | base(받는 쪽) ← compare(보내는 쪽), 설명 작성·리뷰어 지정 → Merge |
| Issue | Issues → New issue | 작업·버그·기능 요청 추적. 템플릿으로 형식 통일, Todos 체크박스로 진행 관리 |
| Issue Template | Settings → Features → Set up templates | Template name / About / content / 기본 제목 / Assignees / Labels |
| Wiki | Wiki 탭 | README보다 구조적인 프로젝트 문서. Public 저장소에서 무료 사용 |

**프로젝트 관리 흐름 (권장)**: Issue로 할 일 등록 → 브랜치 생성(`feature/...`) → 작업·커밋 → Pull Request(리뷰) → Merge → Issue 닫기 → 문서는 README/Wiki에 정리
