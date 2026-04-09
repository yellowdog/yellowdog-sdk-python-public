from enum import Enum


class InstancePricingPreference(Enum):
    """
    The preferred :class:`InstancePricing` when running a :class:`TaskGroup`.
    This affects upscaling and claiming.

    :attr:`ON_DEMAND_ONLY` and :attr:`SPOT_ONLY` are restrictive. They prevent using compute that is not On-Demand and
    Spot respectively. These restrictions apply differently in upscaling and claiming. When upscaling, the restriction
    applies to the :class:`WorkerPool` as a whole — a pool mixing Spot and On-Demand sources is not eligible. When
    claiming, the restriction applies per :class:`Worker` — a worker in a mixed pool is still eligible if it individually
    satisfies the pricing requirement.

    :attr:`ON_DEMAND_THEN_SPOT` and :attr:`SPOT_THEN_ON_DEMAND` alter the priority of :class:`WorkerPool`\\s when
    upscaling, and of :class:`Worker`\\s when claiming.

    @see InstancePricing
    """

    ON_DEMAND_ONLY = "ON_DEMAND_ONLY"
    """
    When upscaling, only :class:`WorkerPool`\\s that exclusively provision On-Demand compute.
    When claiming, only use :class:`Worker`\\s running on On-Demand compute.
    """

    SPOT_ONLY = "SPOT_ONLY"
    """
    When upscaling, only :class:`WorkerPool`\\s that exclusively provision Spot compute.
    When claiming, only use :class:`Worker`\\s running on Spot compute.
    """

    ON_DEMAND_THEN_SPOT = "ON_DEMAND_THEN_SPOT"
    """
    When upscaling, order :class:`WorkerPool`\\s by those that:

    - Only create On-Demand compute
    - Create On-Demand and Spot compute
    - Only create Spot compute

    When claiming, order :class:`Worker`\\s by those running on:

    - On-Demand compute
    - Spot compute
    - Configured compute
    """

    SPOT_THEN_ON_DEMAND = "SPOT_THEN_ON_DEMAND"
    """
    When upscaling, order :class:`WorkerPool`\\s by those that:

    - Only create Spot compute
    - Create On-Demand and Spot compute
    - Only create On-Demand compute

    When claiming, order :class:`Worker`\\s by those running on:

    - Spot compute
    - On-Demand compute
    - Configured compute
    """

    def __str__(self) -> str:
        return self.name
