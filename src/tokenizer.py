from src.config import MD_GLOB
from glob import glob
from pathlib import Path
import re

class TokenizerError(Exception): pass

class TokenizeUnavailable(TokenizerError):
    def __init__(self, formula: str):
        self.formula = formula
        super().__init__(f"분류할 수 없는 수식입니다: {formula}")

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
    "\\mathrm": 1, "\\text": 1, "\\vec": 1, "\\hat": 1, "\\begin": 1, "\\end": 1,
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
    "\\rightarrow", "\\longrightarrow", "\\subset", "\\Longleftrightarrow", "&", "\\\\",
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
            elif depth == 0 and (merged[j] in SPLITTERS or merged[j].startswith("\\begin") or merged[j].startswith("\\end")):
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

NO_TOKEN = {"(", ")", ",", "[", "]", ".", "\\left", "\\right"}

def build(splitted, start_term=0, start_token=0):
    annotated = ""
    terms = {}
    num_term = start_term
    tokens = {}
    num_token = start_token

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
                if content[i] in NO_TOKEN:
                    annotated += content[i]
                else:
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
        'next_term': num_term,
        'next_token': num_token,
    }

def tokenize(latex: str, start_term=0, start_token=0) -> dict:
    try:
        return build(split_terms(merge_scripts(attach_args(lexer(latex)))), start_term, start_token)
    except Exception as err:
        raise TokenizeUnavailable(latex) from err

def load_formulas() -> dict:
    formula_dict = {}
    md_paths = sorted(glob(MD_GLOB, recursive=True))

    for path in md_paths:
        with open(path, "r", encoding="utf-8") as f:
            highlight = " ".join([line.lstrip("> ").strip() for line in f if line.startswith(">")])
        md_name = Path(path).stem
        two_dollar = re.findall(r"\$\$(.*?)\$\$", highlight, re.DOTALL)
        if two_dollar:
            formula_dict[md_name] = [f.strip() for f in two_dollar]
            continue
        one_dollar = re.findall(r"\$(.*?)\$", highlight)
        if one_dollar:
            formula_dict[md_name] = [max(one_dollar, key=len)]

    return formula_dict

RAW_FORMULAS = load_formulas()
WIKI_SECTIONS = {}

def tokenize_sections(sections) -> dict:
    result = {"sections": [], "tokens": {}, "terms": {}}
    current_term = 0 
    current_token = 0
    for dict in sections:
        annotated = []
        for raw in dict["formulas"]:
            try:
                tkf = tokenize(raw, start_term=current_term, start_token=current_token)
            except Exception:
                annotated.append(raw)
                continue
            annotated.append(tkf['annotated'])
            current_term = tkf['next_term']
            current_token = tkf['next_token']
            result["terms"].update(tkf["terms"])
            result["tokens"].update(tkf["tokens"])
        result["sections"].append({
            "section": dict["section"],
            "formulas": annotated,
        })
    return result

def get_page(title: str) -> dict:
    if title in WIKI_SECTIONS:
        return tokenize_sections(WIKI_SECTIONS[title])
    formulas = RAW_FORMULAS.get(title)
    if formulas is None:
        raise KeyError(title)
    return tokenize_sections([{"section": "", "formulas": formulas}])

if __name__ == "__main__":
    pieces = merge_scripts(attach_args(lexer(r"\begin{align} a &= b \\ c &= d \end{align}")))
    print(pieces)
    print(split_terms(pieces))