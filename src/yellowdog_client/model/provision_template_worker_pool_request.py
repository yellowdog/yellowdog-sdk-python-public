from dataclasses import dataclass
from typing import Optional

from .compute_requirement_template_usage import ComputeRequirementTemplateUsage
from .provisioned_worker_pool_properties import ProvisionedWorkerPoolProperties


@dataclass
class ProvisionTemplateWorkerPoolRequest:
    requirementTemplateUsage: ComputeRequirementTemplateUsage
    provisionedProperties: Optional[ProvisionedWorkerPoolProperties] = None
