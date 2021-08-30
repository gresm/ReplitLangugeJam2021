from typing import List


word_chars = {chr(i) for i in range(65, 91)}.union(
    {chr(i) for i in range(97, 123)}.union({chr(i) for i in range(48, 58)}))

end_line: str = "\n"
sequence_char = "\""


def lang_split(txt: str) -> List[List[str]]:
    ret = []

    for line in txt.split(end_line):
        lno = []
        cur = ""
        seq = False
        for char in line:
            if char == sequence_char:
                seq = not seq
            elif seq:
                cur += char
                continue

            if char in word_chars:
                cur += char
            elif not char.isspace():
                if cur:
                    lno.append(cur)
                lno.append(char)
                cur = ""
            else:
                if cur:
                    lno.append(cur)
                cur = ""
        ret.append(lno)
    return ret
