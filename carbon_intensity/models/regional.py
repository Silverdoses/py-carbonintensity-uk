from typing import List
from datetime import datetime

from pandas import DataFrame, Series
import pandas as pd
from pydantic import BaseModel, Field

from .measurements import IntensityForecast
from .mixes import GenerationMixDetails, MixComponent


class Region(BaseModel):
    region_id: int = Field(..., alias="regionid")
    dno_region: str = Field(..., alias="dnoregion")
    short_name: str = Field(..., alias="shortname")

    def to_series(self):
        record = {
            "region_id": self.region_id,
            "dno_region": self.dno_region,
            "short_name": self.short_name,
        }
        return Series(record)


class RegionGenerationMix(Region):
    intensity: IntensityForecast
    generation_mix: List[MixComponent] = Field(..., alias="generationmix")

    def to_series(self):
        record = Series(
            {
                **self.intensity.dict(),
                **{item.fuel: item.percentage for item in self.generation_mix},
            }
        )
        return super().to_series().append(record)


class RegionListDetails(BaseModel):
    from_: datetime = Field(..., alias="from")
    to: datetime
    regions: List[RegionGenerationMix]

    def to_dataframe(self) -> DataFrame:
        record = Series({"from": self.from_, "to": self.to})
        regions = [region.to_series().append(record) for region in self.regions]
        return DataFrame(regions)


# Model for https://api.carbonintensity.org.uk/regional
class RegionListResponse(BaseModel):
    data: List[RegionListDetails]

    def to_dataframe(self) -> DataFrame:
        return pd.concat([details.to_dataframe() for details in self.data])


class RegionIntensity(GenerationMixDetails):
    intensity: IntensityForecast

    def to_series(self) -> Series:
        return super().to_series().append(self.intensity.to_series())


class RegionDetails(Region):
    data: List[RegionIntensity]

    def to_dataframe(self) -> DataFrame:
        region_intensity = pd.concat([details.to_series() for details in self.data])
        record = pd.concat([self.to_series(), region_intensity])
        return DataFrame([record])


# Model for https://api.carbonintensity.org.uk/regional/{region_name}
class RegionResponse(BaseModel):
    data: List[RegionDetails]

    def to_dataframe(self) -> DataFrame:
        return pd.concat([item.to_dataframe() for item in self.data])
