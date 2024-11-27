def enUTF8(st: str) -> bytes:
    return st.encode('utf-8')


def deUTF8(st: str) -> bytes:
    return st.decode('utf-8')
