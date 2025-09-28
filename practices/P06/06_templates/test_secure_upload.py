from pathlib import Path
from src.secure_upload import secure_save, sniff

def test_secure_save_rejects_big(tmp_path: Path):
    data = b"\x89PNG\r\n\x1a\n" + b"0"*5_000_001
    try:
        secure_save(tmp_path, data)
        assert False, "expected error"
    except ValueError as e:
        assert str(e) == "too_big"
