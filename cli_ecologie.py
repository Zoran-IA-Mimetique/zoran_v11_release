"""CLI wrapper for ecologie injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_ecologie.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_ecologie_glyph import EcologieInjector
        inj = EcologieInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_ecologie import audit_ecologie
        print(json.dumps(audit_ecologie(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
