# portfolio

김민식 Software Engineer 기술 포트폴리오 사이트입니다.

검수된 공개 경력, 오픈소스, 프로젝트, 활동, 개발 원칙 문서와 증빙 링크만 포함합니다.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

로컬 미리보기 주소: `http://127.0.0.1:8000/portfolio/`

- 한국어: `http://127.0.0.1:8000/portfolio/`
- English: `http://127.0.0.1:8000/portfolio/en/`

## Lint

```bash
pnpm install
pnpm run lint:md
```

If `pnpm` is not installed locally:

```bash
npx pnpm@11.5.2 install --frozen-lockfile
npx pnpm@11.5.2 run lint:md
```

## Structure Check

한국어와 영어 본문은 각각 검수할 수 있도록 `*.md`, `*.en.md` 파일로 유지합니다.
사이트 탐색 구조는 `mkdocs.yml`의 단일 `nav`에서 관리하고, 영어 표시는
`nav_translations`로 변환합니다.

```bash
source .venv/bin/activate
pnpm run test:structure
pnpm run check:structure
```

구조 검사는 번역 파일 쌍, 한·영 heading outline, `nav` 중복·누락,
영어 navigation 번역 누락을 확인합니다.

## Build

```bash
mkdocs build --strict
```
