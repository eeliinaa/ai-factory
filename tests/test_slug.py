import pytest

from ai_product_factory.utils import slugify_topic


def test_slugify_topic_basic() -> None:
    assert slugify_topic("Professional Workflow Products") == "professional_workflow_products"


def test_slugify_topic_strips_symbols() -> None:
    assert slugify_topic("  Etsy!!! Templates ### ") == "etsy_templates"


def test_slugify_topic_raises_on_empty() -> None:
    with pytest.raises(ValueError):
        slugify_topic("   ")
