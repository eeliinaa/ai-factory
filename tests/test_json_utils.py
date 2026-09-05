from ai_product_factory.utils.json_utils import extract_json_object


def test_extract_json_object_direct() -> None:
    result = extract_json_object('{"ok": true}')
    assert result["ok"] is True


def test_extract_json_object_from_wrapped_text() -> None:
    result = extract_json_object('prefix {"ok": true} suffix')
    assert result["ok"] is True
