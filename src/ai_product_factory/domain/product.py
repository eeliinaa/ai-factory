from pydantic import BaseModel

from .enums import ProductType


class ProductPlan(BaseModel):
    product_type: ProductType
    product_title: str
    product_summary: str
    buyer_problem: str
    solution_promise: str
    packaging_strategy: str


class SelectedProduct(BaseModel):
    candidate_id: str
    product_type: ProductType
    product_title: str
    product_summary: str
    buyer_problem: str
    solution_promise: str
    packaging_strategy: str
