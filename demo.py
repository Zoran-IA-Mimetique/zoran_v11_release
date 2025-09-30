from zoran import inject

def main():
    engine = inject.load("demo")
    result = engine.run("Bonjour le monde mimétique")
    print(result)

if __name__ == "__main__":
    main()
