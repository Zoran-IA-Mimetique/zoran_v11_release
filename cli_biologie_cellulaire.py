"""CLI wrapper for biologie_cellulaire injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_biologie_cellulaire.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_biologie_cellulaire_glyph import BiologieCellulaireInjector
        inj = BiologieCellulaireInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_biologie_cellulaire import audit_biologie
        print(json.dumps(audit_biologie(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
