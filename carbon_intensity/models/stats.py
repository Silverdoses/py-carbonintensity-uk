from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pandas import DataFrame, Series
import pandas as pd


class IntensityStat(BaseModel):
    max: int
    average: int
    min: int
    index: str

    def to_series(self) -> Series:
        return pd.Series(self.dict())


class StatsDetails(BaseModel):
    from_: datetime = Field(..., alias="from")
    to: datetime
    intensity: IntensityStat = Field(..., alias="intensity")

    def to_series(self) -> Series:
        record = Series({"from": self.from_, "to": self.to})
        return pd.concat([record, self.intensity.to_series()])


# Model for https://api.carbonintensity.org.uk/intensity/stats/{from}/{to}
class StatsListResponse(BaseModel):
    data: List[Optional[StatsDetails]]

    def to_dataframe(self) -> DataFrame:
        return DataFrame([stats.to_series() for stats in self.data])
