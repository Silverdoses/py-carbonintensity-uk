from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pandas import Series, DataFrame
import pandas as pd


class IntensityForecast(BaseModel):
    forecast: int
    index: str

    def to_series(self) -> Series:
        record = {"forecast": self.forecast, "index": self.index}
        return pd.Series(record)


class Intensity(IntensityForecast):
    actual: Optional[int] = None

    def to_series(self) -> Series:
        record = super().to_series()
        actual_intensity = Series({"actual": self.actual})
        return pd.concat([record, actual_intensity])


class Measurement(BaseModel):
    from_: datetime = Field(..., alias="from")
    to: datetime
    intensity: Intensity

    def to_series(self) -> Series:
        record = {"from": self.from_, "to": self.to}
        return pd.Series(record).append(self.intensity.to_series())


class MeasurementResponse(BaseModel):
    data: List[Optional[Measurement]]

    def to_dataframe(self) -> DataFrame:
        return pd.DataFrame([measure.to_series() for measure in self.data])
