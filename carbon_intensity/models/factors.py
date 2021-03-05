from typing import List

from pydantic import BaseModel, Field
from pandas import Series, DataFrame
import pandas as pd


class FactorSummary(BaseModel):
    biomass: int = Field(..., alias="Biomass")
    coal: int = Field(..., alias="Coal")
    dutch_imports: int = Field(..., alias="Dutch Imports")
    french_imports: int = Field(..., alias="French Imports")
    gas_combined_cycle: int = Field(..., alias="Gas (Combined Cycle)")
    gas_open_cycle: int = Field(..., alias="Gas (Open Cycle)")
    hydro: int = Field(..., alias="Hydro")
    irish_imports: int = Field(..., alias="Irish Imports")
    nuclear: int = Field(..., alias="Nuclear")
    oil: int = Field(..., alias="Oil")
    other: int = Field(..., alias="Other")
    pumped_storage: int = Field(..., alias="Pumped Storage")
    solar: int = Field(..., alias="Solar")
    wind: int = Field(..., alias="Wind")

    def to_series(self) -> Series:
        return pd.Series(self.dict())


class FactorResponse(BaseModel):
    data: List[FactorSummary]

    def to_dataframe(self) -> DataFrame:
        return pd.DataFrame([measure.to_series() for measure in self.data])
