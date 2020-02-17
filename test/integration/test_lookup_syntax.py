def func():
    try:
        import sedre
        result = True
    except NameError:
        result = False
    return result

def test_answer():
    assert func() == True