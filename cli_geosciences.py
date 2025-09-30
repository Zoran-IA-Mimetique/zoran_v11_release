"""CLI wrapper for geosciences injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_geosciences.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_geosciences_glyph import GeosciencesInjector
        inj = GeosciencesInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_geosciences import audit_geosciences
        print(json.dumps(audit_geosciences(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
