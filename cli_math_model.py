"""CLI wrapper for math_model injector(s)."""
import sys, json
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python cli_math_model.py <file> [--glyph]')
        return
    glyph = '--glyph' in args
    target = [a for a in args if not a.startswith('-')][0]
    if glyph:
        from injecteur_math_model_glyph import MathModelInjector
        inj = MathModelInjector()
        print(json.dumps(inj.audit(target), indent=2, ensure_ascii=False))
    else:
        from injecteur_math_model import audit_math
        print(json.dumps(audit_math(target), indent=2, ensure_ascii=False))
if __name__ == '__main__':
    main()
