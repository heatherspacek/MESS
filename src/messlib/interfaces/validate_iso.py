import hashlib


""" work copied from
https://github.com/project-slippi/slippi-launcher/blob/main/src/main/verify_iso.ts
Our requirements are probably not strictly the same as slippi-launcher's requirements,
but the work is done already."""

ISO_VALIDITIES = {
    # Valid hashes
    "d4e70c064cc714ba8400a849cf299dbd1aa326fc": ("NTSC-U 1.02", True),
    "6e83240872d47cd080a28dea7b8907140c44bef5": ("NTSC-U 1.02 NKIT", True),
    "3bf23f7c87caadfc983954eb8c6cf2823fa8713b": ("NTSC-U 1.02 GCZ", True),
    "2a2a5d42b0d4f8773e313c29ab0df095392f20d4": ("NTSC-U 1.02 CISO", True),
    "e63d50e63a0cdd357f867342d542e7cec0c3a7c7": ("NTSC-U 1.02 Scrubbed #1", True),
    "55109bc139b947c8b96b5fc913fbd91245104db8": ("NTSC-U 1.02 Scrubbed #2", True),
    "2ce0ccfc8c31eafe2ff354fe03ac2dd94c20b937": ("NTSC-U 1.02 Scrubbed #3", True),
    "49a04772e0a5d1974a4b1c8a7c0d1d71184f3978": ("NTSC-U 1.02 Scrubbed #4", True),
    "71255a30a47b4c6aabb90308d7a514d09d93a7b5": ("NTSC-J 1.02", True),
    "e9ab27b4f8fdfb72adae214f834e201d14944f50": ("NTSC-J 1.02 GCZ", True),
    # Invalid hashes
    "2f0bed5e1d92ebb187840c6e1a2f368ce35f6816": ("20XX 3.02", False),
    "7f6926f2f35940f5f697eb449c9f3fbd3639dd45": ("20XX 4.07++", False),
    "49fd53b0a5eb0da9215846cd653ccc4c3548ec69": ("20XX 4.07++ UCF", False),
    "4521c1753b0c9d5c747264fce63e84b832bd80a1": ("Training Mode v1.1", False),
    "c89cb9b694f0f26ee07a6ee0a3633ba579e5fa12": ("NTSC-U 1.00 Scrubbed # 1", False),
    "5ab1553a941307bb949020fd582b68aabebecb30": ("NTSC-U 1.00", False),
    "5ecab83cd72c0ff515d750280f92713f19fa46f1": ("NTSC-U 1.01", False),
    "d0a925866379c546ceb739eeb780d011383cb07c": ("PAL", False),
    "fe23c91b63b0731ef727c13253b6a8c6757432ac": ("NTSC-J 1.00", False),
    "f7ff7664b231042f2c0802041736fb9396a94b83": ("NTSC-J 1.01", False),
    "c7c0866fbe6d7ebf3b9c4236f4f32f4c8f65b578": ("Taikenban (demo)", False),
}


def validate_iso(input_path: str):
    with open(input_path) as fstream:
        digest = hashlib.sha1(fstream).hexdigest()
    try:
        return ISO_VALIDITIES[digest]
    except KeyError:
        return ("Unrecognized", False)
