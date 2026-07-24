# src/tokenizer.py
r"""LaTeX 문자열을 클릭 가능한 토큰으로 가공하는 모듈. ★ 여기는 네 영역 ★

[계약 - 프론트엔드와의 약속]
tokenize(latex) -> dict:
    {
        "annotated": str,   # \htmlData{token=N}{...} / \htmlData{term=N}{...}가 심어진 LaTeX
        "tokens": {str: str},  # {"0": "\\int_{I}", ...}  토큰 id → 원본 LaTeX (빨간 박스)
        "terms":  {str: str},  # {"0": "\\overline{\\int_{I}} f", ...} 항 id → 원본 LaTeX (파란 박스)
    }
- 토큰은 \htmlData{token=N}{원본조각}으로 감싼다 (빨간 박스가 될 부분)
- 항은 \htmlData{term=N}{...}으로 감싼다 (파란 박스). 토큰 wrapper는 항 wrapper '안'에 중첩됨
- KaTeX는 중첩된 \htmlData를 문제 없이 처리함 (node로 검증 완료)
- id는 JSON 키라서 str. 프론트는 이 테이블만 읽으므로 내부 구현은 완전 자유

[구현 권장 순서 - 단계별로 커밋하면 좋음]
1. lexer(latex) -> list[str]
   문자열을 원시 조각으로 스캔: "\명령어"(알파벳 연속), "{...}"(중괄호 균형 맞춰 통째로),
   그 외 한 글자씩. 공백은 버리거나 보존 규칙 정하기.
   ※ 중괄호 짝 맞추기는 depth 카운터 하나면 됨. 여기가 첫 pytest 대상.
2. 명령어 인자 붙이기
   ARITY 딕셔너리(\frac: 2, \overline: 1, \sqrt: 1 ...)를 보고
   명령어 뒤의 {group}들을 그 명령어에 합쳐 하나의 조각으로.
3. _{} / ^{} 붙이기
   조각 리스트를 다시 순회하며 "_" 나 "^"를 만나면
   (앞 조각) + (_또는^) + (뒤 조각)을 하나로 병합. 네 규칙 그대로.
4. 투명 명령어 처리 (TRANSPARENT 집합)
   \overline, \left, \right, \, \; 같은 것은 토큰으로 잡지 않고,
   인자 '안쪽'으로 재귀해 들어가서 내부만 토큰화.
5. 항 나누기 (SPLITTERS 집합)
   최상위 레벨(중괄호 depth 0)에서 = + - < > \le \ge 등을 만나면 항 경계.
   경계 기호 자체는 토큰도 항도 아님.
6. 재조립
   각 토큰을 \htmlData{token=N}{...}로, 각 항을 \htmlData{term=N}{...}로
   감싸며 문자열을 다시 이어붙이고 테이블과 함께 반환.

tests/test_tokenizer.py 에 단계별 테스트 케이스 있음. 1번부터 통과시켜 나가면 됨.
"""

# 구현할 때 쓰라고 미리 놓아둔 상수들 (내용은 네가 조정)
ARITY = {
    "\\frac": 2, "\\overline": 1, "\\underline": 1, "\\sqrt": 1,
    "\\mathrm": 1, "\\text": 1, "\\vec": 1, "\\hat": 1,
}
TRANSPARENT = {"\\overline", "\\underline", "\\left", "\\right", "\\,", "\\;", "\\!"}
SPLITTERS = {"=", "+", "-", "<", ">", "\\le", "\\ge", "\\ne", "\\in", "\\to"}


def tokenize(latex: str) -> dict:
    r"""LaTeX 문자열 → {"annotated", "tokens", "terms"}.

    ★ TODO: 여기부터 전부 네 영역 ★
    위 docstring의 1~6 순서 추천. 완성 전까지는 NotImplementedError를
    그대로 두면 /page 엔드포인트가 아래 EXAMPLES fallback을 사용함.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 데모용 fallback. tokenize()가 완성되면 이 블록과 main.py의 fallback 분기만 지우면 됨.
# 수식: 다르부 상적분  \overline{\int_I} f = \inf_{P:Partition(I)} U(f,P)
# KaTeX 0.16 + trust:true 렌더링 검증 완료.
# ---------------------------------------------------------------------------
EXAMPLES = {
    "다르부 적분": {
        "annotated": (
            r"\htmlData{term=0}{\overline{\htmlData{token=0}{\int_{\htmlData{token=1}{I}}}}\; "
            r"\htmlData{token=2}{f}} = "
            r"\htmlData{term=1}{\htmlData{token=3}{\inf_{P:\,\mathrm{Partition}(I)}} "
            r"\htmlData{token=4}{U}\!\left(\htmlData{token=5}{f},\htmlData{token=6}{P}\right)}"
        ),
        "tokens": {
            "0": r"\int_{I}",
            "1": r"I",
            "2": r"f",
            "3": r"\inf_{P:\,\mathrm{Partition}(I)}",
            "4": r"U",
            "5": r"f",
            "6": r"P",
        },
        "terms": {
            "0": r"\overline{\int_{I}}\; f",
            "1": r"\inf_{P:\,\mathrm{Partition}(I)} U(f,P)",
        },
    },
}


def get_page(title: str) -> dict:
    """페이지 제목 → 토큰화 결과. main.py의 /page/{title}가 호출하는 진입점.

    지금은: 네 tokenize()를 먼저 시도하고, 미구현이면 EXAMPLES에서 찾는다.
    나중엔: md 파일에서 title에 해당하는 수식 원문을 읽어 tokenize()에 넘기면 됨.
    """
    raw = RAW_FORMULAS.get(title)
    if raw is not None:
        try:
            return tokenize(raw)
        except NotImplementedError:
            pass
    if title in EXAMPLES:
        return EXAMPLES[title]
    raise KeyError(title)


# 페이지별 수식 원문. 지금은 하드코딩, 나중에 md 파싱으로 교체.
RAW_FORMULAS = {
    "다르부 적분": r"\overline{\int_{I}} f = \inf_{P:\,\mathrm{Partition}(I)} U(f,P)",
}
