from pathlib import Path
from upload_secure import secure_save, sniff_image_type

def test_sniff_image_type_ok_png():
    assert sniff_image_type(b"\x89PNG\r\n\x1a\n123")

def test_secure_save_too_big(tmp_path: Path):
    data = b"\x89PNG\r\n\x1a\n" + b"0"*5_000_001
    try:
        secure_save(tmp_path, data)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "too_big"
