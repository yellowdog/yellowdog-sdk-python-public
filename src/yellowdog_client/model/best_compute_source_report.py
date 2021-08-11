from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from .best_compute_source_report_constraint import BestComputeSourceReportConstraint
from .best_compute_source_report_image import BestComputeSourceReportImage
from .best_compute_source_report_preference import BestComputeSourceReportPreference
from .best_compute_source_report_source import BestComputeSourceReportSource
from .compute_requirement_supported_operations import ComputeRequirementSupportedOperations


@dataclass
class BestComputeSourceReport:
    createdTime: Optional[datetime] = None
    requirementTemplateId: Optional[str] = None
    provisionedRequirementId: Optional[str] = None
    namespace: Optional[str] = None
    selectedSourceTemplateIds: Optional[List[str]] = None
    rejectedSourceTemplateIds: Optional[List[str]] = None
    sourcesConsidered: int = 0
    sourcesSelected: int = 0
    totalRanks: int = 0
    image: Optional[BestComputeSourceReportImage] = None
    constraints: Optional[Dict[str, BestComputeSourceReportConstraint]] = None
    preferences: Optional[Dict[str, BestComputeSourceReportPreference]] = None
    sources: Optional[List[BestComputeSourceReportSource]] = None
    requirementSupportedOperations: Optional[ComputeRequirementSupportedOperations] = None
