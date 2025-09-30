"""CLI wrapper for genetique injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_genetique.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_genetique_glyph import GenetiqueInjector
        inj = GenetiqueInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_genetique import audit_genetique
        print(json.dumps(audit_genetique(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
