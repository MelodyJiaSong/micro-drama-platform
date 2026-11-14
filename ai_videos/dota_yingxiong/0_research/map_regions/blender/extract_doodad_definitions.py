"""Read local WC3 object definitions, including ordinary MPQ file encryption."""
from pathlib import Path
import io
import json
import struct
import zlib
import bz2
import mpyq

ROOT = Path(__file__).resolve().parents[2]


def read_file(archive, name):
    entry = archive.block_table[archive.get_hash_table_entry(name).block_table_index]
    archive.file.seek(entry.offset + archive.header['offset'])
    raw = archive.file.read(entry.archived_size)
    key = archive._hash(name.split('\\')[-1], 'TABLE')
    if entry.flags & 0x20000:
        key = ((key + entry.offset) ^ entry.size) & 0xffffffff
    encrypted = bool(entry.flags & 0x10000)
    def decrypt(data, k):
        n = len(data) // 4 * 4
        return archive._decrypt(data[:n], k & 0xffffffff) + data[n:]
    def unpack(data, size):
        if entry.flags & 0x200 and len(data) < size:
            if data[0] == 2:
                return zlib.decompress(data[1:])
            if data[0] == 16:
                return bz2.decompress(data[1:])
            raise ValueError(f'Unsupported compression {data[0]}')
        return data
    if entry.flags & 0x1000000:
        result = unpack(decrypt(raw, key) if encrypted else raw, entry.size)
    else:
        sector_size = 512 << archive.header['sector_size_shift']
        count = (entry.size + sector_size - 1) // sector_size
        table_size = (count + 1 + bool(entry.flags & 0x4000000)) * 4
        table = decrypt(raw[:table_size], key - 1) if encrypted else raw[:table_size]
        offsets = struct.unpack('<' + 'I' * (table_size // 4), table)
        parts = []
        for i in range(count):
            data = raw[offsets[i]:offsets[i+1]]
            if encrypted:
                data = decrypt(data, key + i)
            parts.append(unpack(data, min(sector_size, entry.size - i*sector_size)))
        result = b''.join(parts)
    assert len(result) == entry.size, (len(result), entry.size)
    return result


def parse(data, levels=True):
    stream = io.BytesIO(data)
    def integer():
        return struct.unpack('<i', stream.read(4))[0]
    def text():
        return stream.read(4).decode('ascii')
    def string():
        value = bytearray()
        while (b := stream.read(1)) != b'\x00':
            if not b:
                raise EOFError()
            value.extend(b)
        return value.decode('utf-8', errors='replace')
    version = integer()
    result = []
    for custom in (False, True):
        for _ in range(integer()):
            base, new = text(), text()
            fields = []
            for _ in range(integer()):
                field, kind = text(), integer()
                variation, pointer = (integer(), integer()) if levels else (0, 0)
                value = integer() if kind == 0 else struct.unpack('<f',stream.read(4))[0] if kind in (1,2) else string()
                end = text()
                fields.append(dict(field=field, kind=kind, variation=variation, pointer=pointer, value=value))
            result.append(dict(id=new if custom else base, base=base, custom=custom, fields=fields))
    assert stream.tell() == len(data), (stream.tell(), len(data))
    return dict(version=version, objects=result)


if __name__ == '__main__':
    source = ROOT / 'base_layout_refs/DotA_v6.83d.w3x'
    content = source.read_bytes()
    offset = content.index(b'MPQ\x1a')
    archive = mpyq.MPQArchive(io.BytesIO(content[offset:]), listfile=False)
    raw = read_file(archive, 'war3map.w3d')
    target = ROOT / 'map_regions/navigation'
    (target / 'war3map.w3d').write_bytes(raw)
    result = parse(raw)
    (target / 'doodad_definitions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
