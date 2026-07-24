# test/test_tokenizer.py
# 실행: pytest test/test_tokenizer.py -v
# tokenize()가 미구현(NotImplementedError)이면 전부 skip 처리되고,
# 구현을 시작하면 자동으로 진짜 테스트가 됨. 쉬운 것부터 순서대로 통과시켜 보자.
import pytest
from src.tokenizer import tokenize, get_page, EXAMPLES


def try_tokenize(latex):
    """미구현이면 skip. 구현 후엔 그대로 실행."""
    try:
        return tokenize(latex)
    except NotImplementedError:
        pytest.skip("tokenize() 아직 미구현")


# ---------- 0단계: fallback이 항상 살아있는지 (지금도 통과해야 함) ----------

def test_fallback_page():
    result = get_page("다르부 적분")
    assert set(result) == {"annotated", "tokens", "terms"}
    assert len(result["tokens"]) == 7

def test_fallback_annotated_has_all_ids():
    ex = EXAMPLES["다르부 적분"]
    for tid in ex["tokens"]:
        assert f"token={tid}" in ex["annotated"]
    for tid in ex["terms"]:
        assert f"term={tid}" in ex["annotated"]


# ---------- 1~3단계: 기본 토큰화 ----------

def test_single_symbol():
    # 가장 단순한 입력: 기호 하나 = 토큰 하나, 항 하나
    r = try_tokenize(r"x")
    assert list(r["tokens"].values()) == ["x"]
    assert len(r["terms"]) == 1

def test_backslash_command_is_one_token():
    # \alpha 는 통째로 한 토큰
    r = try_tokenize(r"\alpha")
    assert list(r["tokens"].values()) == [r"\alpha"]

def test_subscript_attaches():
    # 네 규칙: _{} 는 앞 토큰에 붙는다
    r = try_tokenize(r"x_{i}")
    assert r"x_{i}" in r["tokens"].values()

def test_sub_and_superscript_attach():
    r = try_tokenize(r"\sum_{i=1}^{n}")
    assert r"\sum_{i=1}^{n}" in r["tokens"].values()


# ---------- 4단계: 투명 명령어 ----------

def test_overline_is_transparent():
    # \overline 자체는 토큰이 아니고, 안쪽 \int_{I} 가 토큰
    r = try_tokenize(r"\overline{\int_{I}}")
    values = list(r["tokens"].values())
    assert not any(v.startswith(r"\overline") for v in values)
    assert r"\int_{I}" in values


# ---------- 5단계: 항 나누기 ----------

def test_equals_splits_terms():
    r = try_tokenize(r"a = b")
    assert len(r["terms"]) == 2
    # 경계 기호 '='는 토큰도 항도 아님
    assert "=" not in r["tokens"].values()
    assert "=" not in r["terms"].values()

def test_plus_splits_terms():
    r = try_tokenize(r"x^{2} + 2x = 0")
    assert len(r["terms"]) == 3  # x^2 / 2x / 0

def test_braces_protect_splitters():
    # 중괄호 '안'의 = 는 항을 나누면 안 됨 (\sum_{i=1} 의 = 처럼)
    r = try_tokenize(r"\sum_{i=1}^{n} x_{i}")
    assert len(r["terms"]) == 1


# ---------- 6단계: 재조립 계약 ----------

def test_annotated_contains_htmldata():
    r = try_tokenize(r"x = y")
    assert r"\htmlData{token=" in r["annotated"]
    assert r"\htmlData{term=" in r["annotated"]

def test_all_ids_consistent():
    # 테이블의 모든 id가 annotated 문자열에 실제로 존재해야 함
    r = try_tokenize(r"\overline{\int_{I}} f = \inf_{P} U(f,P)")
    for tid in r["tokens"]:
        assert f"token={tid}" in r["annotated"]
    for tid in r["terms"]:
        assert f"term={tid}" in r["annotated"]
