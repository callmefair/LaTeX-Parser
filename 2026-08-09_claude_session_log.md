# 2026-08-09 세션 기록 — 클로드가 직접 수정한 것만

멘토링 직전~막판 3시간 동안 급한 것들 처리하면서 **내가(Claude) 직접 코드를 건드린 부분만** 정리. 방향 결정이나 나머지 구현(symbol/general 분기, retrieve() wikitext 붙이기, header_divide 인덱스 추가 등)은 전부 본인이 직접 짠 것들이라 여기 안 넣음. 나중에 이해하고 다시 짜볼 때 "뭐가 왜 깨졌었는지" 참고용.

---

## 1. `src/tokenizer.py` — 토크나이저 버그 4종

### 1-1. `\left|`, `\left\{` 등이 KaTeX에서 안 그려짐

**증상**: `\left(`는 되는데 `\left|`, `\left\{`, `\left\langle`는 렌더 실패.

**원인**: `NO_TOKEN` 집합에 `(`, `)`, `[`, `]`만 있고 `|`, `\{`, `\}`, `\langle` 등이 없어서, `\left` 뒤의 델리미터가 `\htmlData{...}`로 감싸져 `\left`와 델리미터 사이가 끊어짐.

```python
# before
NO_TOKEN = {"(", ")", ",", "[", "]", ".", "\\left", "\\right"}

# after
NO_TOKEN = {
    "(", ")", ",", "[", "]", ".", "\\left", "\\right",
    "|", "\\|", "\\{", "\\}", "\\lfloor", "\\rfloor",
    "\\lceil", "\\rceil", "\\langle", "\\rangle", "/",
}
```

### 1-2. `\mathbb{R}` 렌더 실패 (`\mathbb`와 `{R}`이 따로 쪼개짐)

**원인**: `ARITY` 딕셔너리에 `\mathbb`이 아예 없어서 인자와 병합이 안 됨.

```python
# ARITY에 추가
"\\mathbb": 1, "\\mathcal": 1, "\\mathbf": 1, "\\mathfrak": 1, "\\boldsymbol": 1,
"\\bar": 1, "\\tilde": 1, "\\dot": 1, "\\widehat": 1, "\\widetilde": 1,
```

### 1-3. `\mathrm dx` → `\mathrmd`로 깨짐 (`Undefined control sequence`)

**원인**: 원본이 `\mathrm{d}`가 아니라 TeX 관례대로 `\mathrm d`(중괄호 없이 다음 토큰 하나만 인자로)였는데, `attach_args`가 그냥 문자열을 이어붙여서(`"".join(...)`) `\mathrm`+`d` = `\mathrmd`라는 없는 명령어가 됨. 같은 이유로 `\hat x`도 `\hatx`로 깨졌었음(아직 안 걸렸을 뿐).

```python
# src/tokenizer.py, attach_args() 안
# before
attach_list.append("".join(pieces[0:j+1]))

# after — 인자에 원래 중괄호가 없으면 직접 {}로 감싸서 이어붙임
merged = pieces[0]
for arg in pieces[1:j+1]:
    merged += arg if arg.startswith("{") else "{" + arg + "}"
attach_list.append(merged)
```

### 1-4. `\left(...\right)^2`, `\left|...\right|` (내부에 `-`/`+` 있을 때) 렌더 실패

**원인 A** (`split_terms`): 항을 나눌 때 depth를 `(`, `[`, `)`, `]` 문자로만 셌지 `\left`/`\right` 자체는 안 세서, `\left|...\right|`처럼 괄호가 아닌 델리미터를 쓰면 depth가 계속 0으로 유지 → 내부의 `-` 같은 SPLITTER에서 항이 잘못 쪼개짐 (`\left`와 `\right`가 서로 다른 `\htmlData{term=N}{...}`에 들어가버려서 KaTeX가 짝을 못 찾음).

```python
# src/tokenizer.py, split_terms() 안
# before
if merged[j] in ("(", "["):
    depth += 1
elif merged[j] in (")", "]"):
    depth -= 1

# after
if merged[j] in ("(", "[", "\\left"):
    depth += 1
elif merged[j] in (")", "]", "\\right"):
    depth -= 1
```

**원인 B** (`build`): `merge_scripts`가 `)` 뒤에 오는 `^2`/`_n`을 붙여서 `")^2"`라는 합쳐진 문자열을 만드는데, bare 처리 체크가 "정확히 일치"만 봐서 `")^2" != ")"`라 통째로 `\htmlData`에 감싸짐 → `\right` 바로 뒤에 델리미터 대신 `\htmlData`가 와서 파싱 실패.

```python
# src/tokenizer.py, build() 안
# before
if content[i] in NO_TOKEN:

# after — "정확히 일치" 대신 "NO_TOKEN 원소로 시작하는지"
if any(content[i] == nt or content[i].startswith(nt) for nt in NO_TOKEN):
```

---

## 2. `main.py` — `/query`를 스트리밍으로 변경

**전**: `graph.invoke()`로 답변이 다 만들어질 때까지 기다렸다가 JSON 한 번에 반환.

**후**: `async def` + `StreamingResponse`. `graph.astream(..., stream_mode=["messages", "updates"])`로 토큰 조각(`"messages"`)과 노드별 state 조각(`"updates"`, 여기서 `sources` 챙김)을 동시에 받아서, 토큰은 오는 대로 `yield`, 맨 끝에 `sources`를 `\n\n[[SOURCES]]{JSON}` 구분자로 한 번 더 `yield`.

- `astream_events`가 아니라 `astream(stream_mode=...)`를 쓴 이유: 그래프를 감싸고 있는 `langfeather.wrap_runnable()`이 `astream_events`는 구현을 안 해놨어서(소스 직접 확인함), `astream`만 통과시켜줌.
- `generate()` 노드 내부 코드(`chain.invoke(state)`)는 **하나도 안 바꿔도** 스트리밍이 됨 — `stream_mode="messages"`는 그래프를 어떻게 실행하느냐의 문제지, 노드 안에서 `.invoke()`를 쓰든 `.stream()`을 쓰든 상관없음.

---

## 3. `static/index.html` — 프론트

### 3-1. 답변 안의 `$...$` LaTeX가 그냥 텍스트로 보이던 문제

- `<head>`에 `<script src="/katex/contrib/auto-render.min.js"></script>` 추가 (이미 로컬에 파일은 있었음)
- `addMessage()`에서 `div.textContent = text` 뒤에 `renderMathInElement(div, {...})` 호출 추가. `textContent`로 먼저 안전하게 텍스트를 넣고 그 다음 수식만 후처리 렌더링하는 거라 XSS 걱정 없음.

### 3-2. `sendQuery()` 스트리밍 대응

- `res.json()` → `res.body.getReader()`로 바꿔서 오는 대로 `pending.textContent`에 이어붙임 (타이핑 효과)
- `$...$`가 스트리밍 중간에 반쪽만 오면 깨지니까 `renderMathInElement`는 스트림 다 끝난 뒤 딱 한 번만 호출
- `\n\n[[SOURCES]]` 마커로 답변 본문과 출처 JSON을 분리

---

## 4. `src/prompt.py` — 마크다운 출력 문제

**증상**: 답변에 `**굵게**` 같은 마크다운이 별표 그대로 노출됨 (화면은 LaTeX만 렌더하지 마크다운 렌더러는 없어서).

**수정**: 마크다운 렌더러를 새로 붙이는 대신(시간/XSS 리스크 고려), 프롬프트에 마크다운 쓰지 말라는 규칙을 추가. `SYMBOL_PROMPT`, `GENERAL_PROMPT` 둘 다에 아래 섹션 추가:

```
# 출력 형식
화면은 일반 텍스트와 $...$/$$...$$ LaTeX 수식만 렌더링합니다. 마크다운 문법(**굵게**, # 제목,
- 목록, 백틱 코드블록 등)은 그대로 별표/샵 기호가 그대로 노출되니 쓰지 마세요.
강조하고 싶으면 문장으로 풀어서 쓰세요.
```

---

## 참고: 이번엔 안 건드린 것

- 답변 속도 개선 (ㄷ 목록 3번) — 시간상 스킵하기로 합의함
- `tests/test_tokenizer.py`가 지금 없는 `EXAMPLES`를 import하려다 에러나는 것 — 기존부터 있던 문제, 이번 변경과 무관, 손 안 댐
