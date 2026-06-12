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

## Build

```bash
mkdocs build --strict
```
