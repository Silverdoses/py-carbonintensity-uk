from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from pandas import DataFrame, Series
import pandas as pd


class MixComponent(BaseModel):
    fuel: str
    percentage: float = Field(..., alias="perc")

    def to_series(self) -> Series:
        return pd.Series(self.dict())


class GenerationMixDetails(BaseModel):
    from_: datetime = Field(..., alias="from")
    to: datetime
    generation_mix: List[MixComponent] = Field(..., alias="generationmix")

    def to_series(self) -> Series:
        record = {
            "from": self.from_,
            "to": self.to,
            **{item.fuel: item.percentage for item in self.generation_mix},
        }
        return pd.Series(record)


class GenerationMixResponse(BaseModel):
    data: GenerationMixDetails

    def to_dataframe(self) -> DataFrame:
        return pd.DataFrame([self.data.to_series()])
