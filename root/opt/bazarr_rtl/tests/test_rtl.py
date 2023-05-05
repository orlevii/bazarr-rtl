

def test_true():
    # assert 1 == 1
    with open('tests/bad.heb.srt') as f:
        srt_data = f.read()
    with open('tests/fixed.heb.srt') as f:
        expected_data = f.read()

    res = RtlSubFix.fix_srt(srt_data)

    assert res.strip() == expected_data.strip()
