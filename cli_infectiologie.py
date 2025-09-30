"""CLI wrapper for infectiologie injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_infectiologie.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_infectiologie_glyph import InfectiologieInjector
        inj = InfectiologieInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_infectiologie import audit_infectiologie
        print(json.dumps(audit_infectiologie(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
