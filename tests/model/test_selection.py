from yellowdog_client.model.selection import includes, excludes


def test_selection_includes_factory_function():
    things_to_include = ["x", "y"]
    selection = includes(things_to_include)
    assert selection.includes == things_to_include
    assert selection.excludes is None


def test_selection_excludes_factory_function():
    things_to_exclude = ["x", "y"]
    selection = excludes(things_to_exclude)
    assert selection.excludes == things_to_exclude
    assert selection.includes is None
