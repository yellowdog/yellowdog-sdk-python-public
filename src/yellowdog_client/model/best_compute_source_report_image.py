from dataclasses import dataclass
from typing import List, Optional

from .best_compute_source_report_image_availability import BestComputeSourceReportImageAvailability
from .image_os_type import ImageOsType


@dataclass
class BestComputeSourceReportImage:
    id: Optional[str] = None
    suppliedId: Optional[str] = None
    osType: Optional[ImageOsType] = None
    availability: Optional[List[BestComputeSourceReportImageAvailability]] = None
