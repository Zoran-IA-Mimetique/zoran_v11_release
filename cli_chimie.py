"""CLI wrapper for chimie injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_chimie.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_chimie_glyph import ChimieInjector
        inj = ChimieInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_chimie import audit_chimie
        print(json.dumps(audit_chimie(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
