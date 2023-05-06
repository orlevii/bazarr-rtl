from pathlib import Path

import click

from bazarr_rtl.srt_fix import fix_srt


@click.group()
def main():
    pass


@main.command('version')
def version():
    import importlib.metadata
    v = importlib.metadata.version('bazarr-rtl')
    print(v)


# Map to 2 char lang code
LANG_CODES = {
    'he': 'he',
    'heb': 'he'
    # TODO: support arabic/farsi for backup
}


@main.command('fix')
@click.option('-l', '--lang', default='he', show_default=True)
@click.option('-s', '--srt-path', required=True)
@click.option('-e', '--episode-path', required=True)
@click.option('-k', '--keep-original', is_flag=True, show_default=True)
def fix(srt_path: str, episode_path: str, lang: str, keep_original: bool):
    try:
        srt_path = Path(srt_path)
        episode_path = Path(episode_path)
        directory = episode_path.parent
        if not srt_path.exists():
            print(f'"{srt_path}" does not exists')
            return

        if not directory.exists():
            print(f'Directory "{directory}" does not exists')
            return

        if lang not in LANG_CODES:
            print(f'"{srt_path}" is not RTL language. Got "{lang}"')
            return

        with srt_path.open() as f:
            srt_data = f.read()

        if keep_original:
            backup_srt_path = directory.joinpath(episode_path.name).with_suffix('.he-orig.srt')
            with backup_srt_path.open('w') as f:
                f.write(srt_data)

        new_srt = fix_srt(srt_data)

        with srt_path.open('w') as f:
            f.write(new_srt)
    except Exception as e:
        print(e)


@main.command('recreate', help='Recreate .srt from .*-orig.srt files')
@click.option('--dry-run', is_flag=True, help='Shows all the affected files, doing nothing.')
def recreate(dry_run: bool):
    curr = Path('.')
    originals = list(curr.rglob('*/*.*-orig.srt'))
    for orig_srt in originals:
        lang = orig_srt.with_suffix('').suffix.split('-')[0].strip('.')
        fixed_srt_path = orig_srt.with_suffix('').with_suffix(f'.{lang}.srt')

        msg = f'Fixing "{orig_srt}" -> "{fixed_srt_path}"'
        if dry_run:
            msg = f'[DRY_RUN] {msg}'
        print(msg)

        if not dry_run:
            orig_srt_data = orig_srt.open().read()
            fixed_srt_content = fix_srt(orig_srt_data)
            with fixed_srt_path.open('w') as f:
                f.write(fixed_srt_content)
