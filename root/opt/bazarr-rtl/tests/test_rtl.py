from bazarr_rtl.srt_fix import fix_srt


def test_true():
    with open('tests/bad.heb.srt') as f:
        srt_data = f.read()
    with open('tests/fixed.heb.srt') as f:
        expected_data = f.read()

    res = fix_srt(srt_data)

    assert res.strip() == expected_data.strip()
