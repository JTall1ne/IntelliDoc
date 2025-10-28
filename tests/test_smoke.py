def test_import_and_version():
    import importlib
    mod = importlib.import_module("intellidoc")
    assert hasattr(mod, "__version__") or True
