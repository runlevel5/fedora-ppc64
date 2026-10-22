#!/usr/bin/python3
"""Replace a UTF-8 constant in a Java class file.

Usage: suwayomi-arch-alias.py CLASS OLD NEW

Suwayomi's ARCH.from() throws "Unsupported architecture" for any os.arch
it does not list, which stops the server on ppc64le. The architecture is only
reported in the server info and used to pick a CEF (Chromium) download, which
Kaori disables, so the spec renames one of the RISC-V aliases ("riscv32") in
ARCH$RISCV.class to "ppc64" (aliases are prefix matches, so this also matches
"ppc64le").

Constant pool entries are referenced by index, not by offset, so a UTF-8
entry can change length without touching the rest of the class.
"""

import struct
import sys

# Sizes of the constant pool entries other than CONSTANT_Utf8 (tag 1)
SIZES = {3: 4, 4: 4, 5: 8, 6: 8, 7: 2, 8: 2, 9: 4, 10: 4, 11: 4, 12: 4,
         15: 3, 16: 2, 17: 4, 18: 4, 19: 2, 20: 2}


def main():
    path, old, new = sys.argv[1], sys.argv[2].encode(), sys.argv[3].encode()
    data = open(path, 'rb').read()
    if data[:4] != b'\xca\xfe\xba\xbe':
        sys.exit(f'{path}: not a class file')

    count = struct.unpack_from('>H', data, 8)[0]
    pos, index, found = 10, 1, None
    while index < count:
        tag = data[pos]
        if tag == 1:
            length = struct.unpack_from('>H', data, pos + 1)[0]
            if data[pos + 3:pos + 3 + length] == old:
                if found is not None:
                    sys.exit(f'{path}: {old.decode()!r} occurs more than once')
                found = (pos, length)
            pos += 3 + length
        else:
            pos += 1 + SIZES[tag]
        # Long and double entries take two slots
        index += 2 if tag in (5, 6) else 1

    if found is None:
        sys.exit(f'{path}: {old.decode()!r} not found')
    start, length = found
    data = (data[:start + 1] + struct.pack('>H', len(new)) + new
            + data[start + 3 + length:])
    open(path, 'wb').write(data)


if __name__ == '__main__':
    main()
