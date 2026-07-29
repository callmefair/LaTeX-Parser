from src.config import MD_GLOB
from glob import glob
from pathlib import Path
import re

def lexer(latex):
    token_list = []
    while len(latex) > 0:
        depth = 0
        j = 1
        if latex[0] == "\\":
            while j < len(latex) and (latex[j].isalpha() or j == 1):
                j += 1
            token_list.append(latex[0:j])
            latex = latex[j:]
        elif latex[0] == "{":
            depth += 1
            while depth > 0:
                if latex[j] == "{":
                    depth += 1
                elif latex[j] == "}":
                    depth -= 1
                j += 1
            token_list.append(latex[0:j])
            latex = latex[j:]
        elif latex[0] == " ":
            latex = latex[1:]
        else:
            token_list.append(latex[0])
            latex = latex[1:]

    return token_list

ARITY = {
    "\\dfrac": 2, "\\tfrac": 2, "\\stackrel": 2, "\\frac": 2, "\\overline": 1, "\\underline": 1, "\\sqrt": 1,
    "\\mathrm": 1, "\\text": 1, "\\vec": 1, "\\hat": 1,
}

def attach_args(pieces):
    attach_list = []
    while len(pieces) > 0:
        j = 0
        if ARITY.get(pieces[0]):
            j = ARITY[pieces[0]]
            if j <= len(pieces) - 1:
                attach_list.append("".join(pieces[0:j+1]))
                pieces = pieces[j+1:]
            else:
                attach_list.append(pieces[0])
                pieces = pieces[1:]
        else:
            attach_list.append(pieces[0])
            pieces = pieces[1:]
    return attach_list

def merge_scripts(attached):
    merge_list = []
    while len(attached) > 1:
        if attached[0] == "_" or attached[0] == "^":
            if len(merge_list) > 0:
                merged_latex = merge_list[-1] + attached[0] + attached[1]
                merge_list = merge_list[:-1]
                merge_list.append(merged_latex)
                attached = attached[2:]
            else:
                merge_list.append(attached[0])
                attached = attached[1:]
        else:
            merge_list.append(attached[0])
            attached = attached[1:]
    if len(attached) > 0:
        merge_list.append(attached[0])
    return merge_list

"""
4. 투명 명령어 처리 (TRANSPARENT 집합)
   \overline, \left, \right, \, \; 같은 것은 토큰으로 잡지 않고,
   인자 '안쪽'으로 재귀해 들어가서 내부만 토큰화.

"""
TRANSPARENT = {"\\overline", "\\underline", "\\left", "\\right", "\\,", "\\;", "\\!"}

SPLITTERS = {
    "=", "+", "-", "<", ">", "\\le", "\\ge", "\\ne", "\\in", "\\to",
    "\\leq", "\\geq", "\\approx", "\\sim", "\\neq",
    "\\rightarrow", "\\longrightarrow", "\\subset", "\\Longleftrightarrow"  
    }
def split_terms(merged):
    split_list = []
    j = 0
    depth = 0
    while len(merged) > 0:
        while j < len(merged):
            if merged[j] in ("(", "["):
                depth += 1
            elif merged[j] in (")", "]"):
                depth -= 1
            elif depth == 0 and merged[j] in SPLITTERS:
                if merged[j] == "-" and j == 0:
                    j += 1
                    continue
                if j > 0:
                    split_list.append(('term', merged[0:j]))
                    split_list.append(('split', merged[j]))
                    merged = merged[j+1:]
                    j = 0
                    break
            j += 1
        if j == len(merged):
            split_list.append(('term', merged[0:j]))
            merged = merged[j+1:]
    return(split_list)

def build(splitted):
    annotated = ""
    terms = {}
    num_term = 0
    tokens = {}
    num_token = 0

    def htmlterm(i):
        return "\\htmlData{term=" + str(i) + "}"
    def htmltoken(i, term):
        return "\\htmlData{token=" + str(i) + "}{" + term + "}"
    
    while len(splitted) > 0:
        while len(splitted) > 0 and splitted[0][0] == 'term':
            content = splitted[0][1]
            annotated += htmlterm(num_term) + "{"
            terms[str(num_term)] = " ".join(content)
            num_term += 1
            for i in range(len(content)):
                annotated += htmltoken(num_token, content[i])
                tokens[str(num_token)] = content[i]
                num_token += 1
            annotated += "}"
            splitted = splitted[1:]
        if len(splitted) > 0 and splitted[0][0] == 'split':
            annotated += splitted[0][1]
            splitted = splitted[1:]
    return {
        'annotated': annotated,
        'tokens': tokens,
        'terms': terms,
    }

def tokenize(latex: str) -> dict:
    return build(split_terms(merge_scripts(attach_args(lexer(latex)))))

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

def load_formulas() -> dict:
    formula_dict = {}
    md_paths = sorted(glob(MD_GLOB, recursive=True))

    for path in md_paths:
        with open(path, "r", encoding="utf-8") as f:
            highlight = " ".join([line.lstrip("> ").strip() for line in f if line.startswith(">")])
        md_name = Path(path).stem
        two_dollar = re.findall(r"\$\$(.*?)\$\$", highlight, re.DOTALL)
        if two_dollar:
            formula_dict[md_name] = "\\\\".join([f.strip() for f in two_dollar])
            continue
        one_dollar = re.findall(r"\$(.*?)\$", highlight)
        if one_dollar:
            formula_dict[md_name] = max(one_dollar, key=len)

    return formula_dict

RAW_FORMULAS = load_formulas()

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
"""
RAW_FORMULAS = {
    "다르부 적분": r"\overline{\int_{I}} f = \inf_{P:\,\mathrm{Partition}(I)} U(f,P)",
}
"""

if __name__ == "__main__":
    d = load_formulas()
    print(len(d), "개")
    for k, v in d.items():
        print(f"[{k}]\n  {v}\n")
    print(get_page("Thm. Weak Law of Large Number")["terms"])