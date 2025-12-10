#!/usr/bin/env python3
# fardthon minimal interpreter — handles Print, Numbers, ASCII, Loops (while/end), Comparison (==)

import sys
from sys import argv  

# helper: identify header name from a token consisting of repeated "fard"
def header_name(token):
    if token is None:
        return None
    token = token.strip()
    if token == "":
        return None
    if len(token) % 4 != 0:
        return None
    reps = len(token) // 4
    headers = [
        "Comparison", "Boolean", "Conditionals", "Variables",
        "ASCII", "Loops", "Numbers", "Arithmetic", "Print"
    ]
    if 1 <= reps <= len(headers):
        return headers[reps - 1]
    return None

# map f/a/r/d -> digits '0'..'3'
_digit_map = str.maketrans("fard", "0123")

def base4_chunk_to_int(chunk):
    # chunk is a string of '0'..'3' digits (from translate)
    if chunk == "":
        return 0
    return int(chunk, 4)

def decode_ascii_data(line):
    # line consists of f/a/r/d characters (no header)
    s = line.strip()
    # left-pad with 'f' so len % 4 == 0
    pad = (-len(s)) % 4
    s = ("f" * pad) + s
    digits = s.translate(_digit_map)
    out = []
    for i in range(0, len(digits), 4):
        chunk = digits[i:i+4]
        val = base4_chunk_to_int(chunk)
        out.append(chr(val))
    return "".join(out)

def decode_number_data(line):
    # line is f/a/r/d digits representing a base-4 number -> return Python int
    s = line.strip()
    if s == "":
        return 0
    digits = s.translate(_digit_map)
    return int(digits, 4)

# load file
def load_tokens(path=argv[1]):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]
    # drop blank lines
    return [ln for ln in lines if ln.strip() != ""]

# evaluate a "value" starting at index i
# supports Numbers header (consumes header+data) and ASCII header (header+data)
# returns (value, new_index)
def eval_value(tokens, i):
    if i >= len(tokens):
        raise IndexError("Unexpected EOF when expecting a value")
    tok = tokens[i]
    h = header_name(tok)
    if h == "Numbers":
        # next line is data
        if i + 1 >= len(tokens):
            raise IndexError("Numbers header without data")
        num = decode_number_data(tokens[i+1])
        return num, i + 2
    if h == "ASCII":
        if i + 1 >= len(tokens):
            raise IndexError("ASCII header without data")
        txt = decode_ascii_data(tokens[i+1])
        return txt, i + 2
    # raw data line (no header): try to interpret as base4 number
    if all(ch in "fard" for ch in tok):
        return decode_number_data(tok), i + 1
    raise ValueError(f"Cannot interpret token as value: {tok!r}")

# run interpreter
def run(tokens):
    ip = 0
    # simple variable store if needed later
    vars_store = {}

    # helper to run a block (list of tokens) as a sub-program (to support loop body execution)
    def run_block(block_tokens):
        run(block_tokens)

    while ip < len(tokens):
        tok = tokens[ip]
        h = header_name(tok)

        # PRINT: header (Print) then next line is ASCII data header+data or ASCII header expected
        if h == "Print":
            # expect next header to be ASCII
            if ip + 1 >= len(tokens):
                raise IndexError("Print header without following content")
            # allow either: Print -> ASCII header -> data
            next_h = header_name(tokens[ip + 1])
            if next_h == "ASCII":
                txt, new_ip = eval_value(tokens, ip + 1)
                # print without extra newline (but we'll add newline)
                sys.stdout.write(txt + "\n")
                ip = new_ip
                continue
            else:
                # if next line is raw ascii data (fard stream), decode directly
                txt = decode_ascii_data(tokens[ip + 1])
                sys.stdout.write(txt + "\n")
                ip += 2
                continue

        # LOOPS: header (Loops) then subtype token on next line (a token "fard"*N where N indicates subtype)
        if h == "Loops":
            # consume Loops header
            if ip + 1 >= len(tokens):
                raise IndexError("Loops header without subtype token")
            subtype_token = tokens[ip + 1]
            if len(subtype_token) % 4 != 0:
                raise ValueError("Invalid loop subtype token")
            subtype = len(subtype_token) // 4  # 1 -> while, 2 -> for (not implemented), 3 -> end
            ip += 2

            # WHILE
            if subtype == 1:
                # Expect a Comparison header next, then left and right values
                if ip >= len(tokens):
                    raise IndexError("While missing comparison")
                comp_tok = tokens[ip]
                comp_header = header_name(comp_tok)
                if comp_header != "Comparison":
                    raise ValueError("While expects a Comparison header")
                # consume comparison header
                comp_reps = len(comp_tok) // 4
                # map comp_reps to operator
                comp_map = {1: "==", 2: "!=", 3: "<", 4: ">"}
                op = comp_map.get(comp_reps, "==")
                ip += 1
                # eval left and right values
                left_val, ip = eval_value(tokens, ip)
                right_val, ip = eval_value(tokens, ip)

                # find body start = ip , find matching Loops header with subtype 3 (end)
                body_start = ip
                body_end = None
                scan = body_start
                while scan < len(tokens):
                    if header_name(tokens[scan]) == "Loops":
                        # check subtype of this loops token's next token (if exists)
                        if scan + 1 < len(tokens):
                            sub_token = tokens[scan + 1]
                            if len(sub_token) % 4 == 0 and (len(sub_token) // 4) == 3:
                                body_end = scan
                                break
                    scan += 1
                if body_end is None:
                    raise IndexError("While missing Loops:End marker")

                # execute loop: re-evaluate left/right each iteration (left/right may be constants)
                # to allow modifications inside body, we evaluate left/right fresh by re-parsing from the original left/right tokens:
                # For simplicity here left_val and right_val are either ints or strings; treat only ints for comparison
                # Build left/right token spans for re-evaluation:
                # We'll capture the tokens that represented left and right values by scanning backwards from body_start
                # Simpler: re-evaluate using the original left/right values (constant) — fine for while 1==1
                # Run loop (infinite if condition always true); user-provided program may be infinite
                def cond_true():
                    a = left_val
                    b = right_val
                    if op == "==":
                        return a == b
                    if op == "!=":
                        return a != b
                    if op == "<":
                        return a < b
                    if op == ">":
                        return a > b
                    return False

                # loop body tokens slice:
                body_tokens = tokens[body_start:body_end]
                # execute until condition false (or forever)
                while cond_true():
                    # execute body tokens by running a fresh interpreter on the slice
                    run(body_tokens)
                # advance ip after the end marker (which is at body_end and its subtype token occupies body_end+1)
                ip = body_end + 2
                continue

            # END marker — nothing to do at top-level, just continue
            if subtype == 3:
                continue

            # other subtypes not implemented
            raise NotImplementedError("Loop subtype not implemented")

        # otherwise: skip unknown token
        ip += 1

if __name__ == "__main__":
    tokens = load_tokens(argv[1])
    run(tokens)
