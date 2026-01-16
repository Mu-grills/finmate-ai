import importlib

def main():
    modules = ["tests.test_calculos"]
    for m in modules:
        importlib.import_module(m)
    print("✅ Testes importados e executados (asserts passaram).")

if __name__ == "__main__":
    main()
