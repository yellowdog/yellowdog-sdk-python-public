from dataclasses import dataclass
from typing import Dict, Optional

from .best_compute_source_report_source_attribute import BestComputeSourceReportSourceAttribute
from .cloud_provider import CloudProvider
from .compute_source_traits import ComputeSourceTraits


@dataclass
class BestComputeSourceReportSource:
    sourceTemplateId: Optional[str] = None
    provisionedSourceId: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    provider: Optional[CloudProvider] = None
    region: Optional[str] = None
    instanceType: Optional[str] = None
    traits: Optional[ComputeSourceTraits] = None
    totalScore: Optional[float] = None
    rank: Optional[int] = None
    attributes: Optional[Dict[str, BestComputeSourceReportSourceAttribute]] = None
