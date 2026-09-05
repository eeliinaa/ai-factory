from ai_product_factory.core.response_parser import ResponseParser


def test_parse_research_response_valid_json() -> None:
    parser = ResponseParser()
    raw = '{"evidence_summary":"ok","candidates":[]}'

    result = parser.parse_research_response(raw)

    assert result.parsed is True
    assert result.payload["evidence_summary"] == "ok"


def test_parse_research_response_with_wrapped_text() -> None:
    parser = ResponseParser()
    raw = 'before {"evidence_summary":"ok","candidates":[]} after'

    result = parser.parse_research_response(raw)

    assert result.parsed is True


def test_parse_research_response_invalid_json() -> None:
    parser = ResponseParser()
    raw = "not-json"

    result = parser.parse_research_response(raw)

    assert result.parsed is False
    assert result.error is not None
