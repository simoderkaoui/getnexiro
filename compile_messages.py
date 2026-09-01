"""
Compile .po files to .mo using Python's built-in tools.
Fallback for when GNU gettext is not installed.

Usage: python compile_messages.py
"""

import os
import struct


def parse_po(po_path):
    """Parse a .po file and return a dict of msgid -> msgstr."""
    messages = {}
    current_msgid = []
    current_msgstr = []
    in_msgid = False
    in_msgstr = False

    def save_current():
        msgid = ''.join(current_msgid)
        msgstr = ''.join(current_msgstr)
        # Store all entries including the header (empty msgid)
        messages[msgid] = msgstr

    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            stripped = line.strip()

            # Skip comments
            if stripped.startswith('#'):
                continue

            # Empty line: save current and reset
            if not stripped:
                if in_msgid or in_msgstr:
                    save_current()
                current_msgid = []
                current_msgstr = []
                in_msgid = False
                in_msgstr = False
                continue

            if stripped.startswith('msgid '):
                # Save previous entry if any
                if in_msgstr:
                    save_current()
                current_msgid = []
                current_msgstr = []
                # Extract the quoted string
                value = stripped[6:].strip()
                if value.startswith('"') and value.endswith('"'):
                    current_msgid.append(unescape(value[1:-1]))
                in_msgid = True
                in_msgstr = False

            elif stripped.startswith('msgstr '):
                value = stripped[7:].strip()
                if value.startswith('"') and value.endswith('"'):
                    current_msgstr.append(unescape(value[1:-1]))
                in_msgid = False
                in_msgstr = True

            elif stripped.startswith('"') and stripped.endswith('"'):
                # Continuation line
                content = unescape(stripped[1:-1])
                if in_msgid:
                    current_msgid.append(content)
                elif in_msgstr:
                    current_msgstr.append(content)

        # Save last entry
        if in_msgid or in_msgstr:
            save_current()

    return messages


def unescape(s):
    """Unescape PO file escape sequences."""
    return (s
            .replace('\\n', '\n')
            .replace('\\t', '\t')
            .replace('\\"', '"')
            .replace('\\\\', '\\'))


def generate_mo(messages):
    """Generate .mo binary content from a messages dict."""
    # Ensure the header (empty msgid) has proper charset
    if '' in messages:
        header = messages['']
        if 'charset=' not in header.lower():
            # Inject charset into existing header
            header = header.replace('Content-Type: text/plain;',
                                    'Content-Type: text/plain; charset=UTF-8;')
            if 'Content-Type' not in header:
                header += '\nContent-Type: text/plain; charset=UTF-8\n'
            messages[''] = header
    else:
        # Create a minimal header
        messages[''] = (
            'Content-Type: text/plain; charset=UTF-8\n'
            'Content-Transfer-Encoding: 8bit\n'
        )

    # Sort keys for binary search in .mo format
    keys = sorted(messages.keys())
    n = len(keys)

    # Encode all strings
    key_bytes_list = []
    val_bytes_list = []
    for key in keys:
        key_bytes_list.append(key.encode('utf-8'))
        val_bytes_list.append(messages[key].encode('utf-8'))

    # Compute offsets
    # Header: 7 * 4 = 28 bytes
    # Original table: n * 8 bytes (length + offset pairs)
    # Translation table: n * 8 bytes
    # Then string data follows
    header_size = 28
    table_size = n * 8
    strings_offset = header_size + 2 * table_size

    # Compute positions for original strings
    key_offsets = []
    pos = strings_offset
    for kb in key_bytes_list:
        key_offsets.append((len(kb), pos))
        pos += len(kb) + 1  # +1 for null terminator

    # Compute positions for translation strings
    val_offsets = []
    for vb in val_bytes_list:
        val_offsets.append((len(vb), pos))
        pos += len(vb) + 1  # +1 for null terminator

    # Build the file
    output = bytearray()

    # Magic number (little-endian)
    output += struct.pack('<I', 0x950412de)
    # Revision (0.0)
    output += struct.pack('<I', 0)
    # Number of strings
    output += struct.pack('<I', n)
    # Offset of original string table
    output += struct.pack('<I', header_size)
    # Offset of translation string table
    output += struct.pack('<I', header_size + table_size)
    # Hash table size (0 = unused)
    output += struct.pack('<I', 0)
    # Hash table offset
    output += struct.pack('<I', 0)

    # Original string table
    for length, offset in key_offsets:
        output += struct.pack('<II', length, offset)

    # Translation string table
    for length, offset in val_offsets:
        output += struct.pack('<II', length, offset)

    # String data (originals)
    for kb in key_bytes_list:
        output += kb + b'\x00'

    # String data (translations)
    for vb in val_bytes_list:
        output += vb + b'\x00'

    return bytes(output)


def po_to_mo(po_path, mo_path):
    """Convert a .po file to a .mo file."""
    messages = parse_po(po_path)

    # Count non-header translations
    count = sum(1 for k, v in messages.items() if k and v)

    mo_data = generate_mo(messages)

    with open(mo_path, 'wb') as f:
        f.write(mo_data)

    print(f"  Compiled: {po_path} -> {mo_path} ({count} translations)")


def main():
    """Find and compile all .po files in the locale directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')

    if not os.path.exists(locale_dir):
        print("Error: locale/ directory not found.")
        return

    compiled = 0
    for root, dirs, files in os.walk(locale_dir):
        for filename in files:
            if filename.endswith('.po'):
                po_path = os.path.join(root, filename)
                mo_path = po_path[:-3] + '.mo'
                try:
                    po_to_mo(po_path, mo_path)
                    compiled += 1
                except Exception as e:
                    print(f"  Error compiling {po_path}: {e}")
                    import traceback
                    traceback.print_exc()

    print(f"\nDone! Compiled {compiled} translation file(s).")


if __name__ == '__main__':
    main()
