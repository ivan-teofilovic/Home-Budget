from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FilterParams(BaseModel):
    category_id: int | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
