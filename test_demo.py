from zoran import inject

def test_demo_engine():
    engine = inject.load("demo")
    result = engine.run("test")
    assert "Zoran a bien injecté" in result
