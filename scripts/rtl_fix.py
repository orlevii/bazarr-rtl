import sys
from pathlib import Path
import srt


SPECIAL_CHARS = '.,:;''()-?!+=*&$^%#@~`" /'
NUMBERS = '1234567890 '


class RtlSubFix:

    @classmethod
    def fix_srt(cls, srt_data: str) -> str:
        subs = list(srt.parse(srt_data))
        for sub in subs:
            lines = [
                cls.fix_line(l)
                for l
                in sub.content.split('\n')
            ]
            sub.content = '\n'.join(lines)
        return srt.compose(subs)

    @staticmethod
    def fix_line(content: str) -> str:
        prefix = ''
        suffix = ''

        while (len(content) > 0 and content[0] in SPECIAL_CHARS):
            prefix += content[0]
            content = content[1:]

        while (len(content) > 0 and content[0] in NUMBERS):
            prefix += content[0]
            content = content[1:]

        while (len(content) > 0 and content[-1] in SPECIAL_CHARS):
            suffix += content[-1]
            content = content[:-1]

        if prefix == ' -':
            prefix = '- '

        if prefix.endswith(' '):
            prefix = ' ' + prefix[:-1]

        if suffix == ' -':
            suffix = '- '

        return suffix + content + prefix


def main():
    try:
        srt_path = Path(sys.argv[1])
        lang_code = sys.argv[2]
        directory = Path(sys.argv[3])
        episode_name = sys.argv[4]
        backup_srt_path = directory.joinpath(episode_name).with_suffix('.he-orig.srt')
        if not srt_path.exists():
            print(f'"{srt_path}" does not exists')
            return
        
        if not directory.exists():
            print(f'Directory "{directory}" does not exists')
            return

        if lang_code not in {'heb', 'he'}:
            print(f'"{srt_path}" is not in Hebrew.. Got "{lang_code}"')
            return

        with srt_path.open() as f:
            srt_data = f.read()

        with backup_srt_path.open('w') as f:
            f.write(srt_data)

        new_srt = RtlSubFix.fix_srt(srt_data)

        with srt_path.open('w') as f:
            f.write(new_srt)
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
