from dataclasses import dataclass, field
from datetime import timedelta
from typing import ClassVar, Optional

from .retry_properties import RetryProperties


@dataclass
class ServicesSchema:
    """Defines a set of URLs and request retry settings to be used to connect to YellowDog Platform Services."""
    DEFAULT_CONNECTION_TIMEOUT: ClassVar[timedelta] = timedelta(seconds=90)
    """The default connection timeout."""
    retry: RetryProperties = field(default_factory=lambda: RetryProperties())
    defaultUrl: Optional[str] = None
    """The default base URL where services are located. This is the YellowDog Cell URL rather than a service specific path."""
    accountServiceUrl: Optional[str] = None
    """The base URL where the Account service is located. This is the YellowDog Cell URL rather than a service specific path."""
    computeServiceUrl: Optional[str] = None
    """The base URL where the Compute service is located. This is the YellowDog Cell URL rather than a service specific path."""
    logServiceUrl: Optional[str] = None
    """The base URL where the Log service is located. This is the YellowDog Cell URL rather than a service specific path."""
    imagesServiceUrl: Optional[str] = None
    """The base URL where the Images service is located. This is the YellowDog Cell URL rather than a service specific path."""
    schedulerServiceUrl: Optional[str] = None
    """The base URL where the Scheduler service is located. This is the YellowDog Cell URL rather than a service specific path."""
    usageServiceUrl: Optional[str] = None
    """The base URL where the Usage service is located. This is the YellowDog Cell URL rather than a service specific path."""
    cloudInfoServiceUrl: Optional[str] = None
    """The base URL where the Cloud Info service is located. This is the YellowDog Cell URL rather than a service specific path."""
    metricsServiceUrl: Optional[str] = None
    """The base URL where the Metrics service is located. This is the YellowDog Cell URL rather than a service specific path."""
    connectionTimeout: Optional[timedelta] = timedelta(seconds=90)
    """
    The timeout for establishing a TCP connection to a YellowDog Platform service.
    Defaults to :attr:`DEFAULT_CONNECTION_TIMEOUT`.
    Set to ``None`` to disable the connection timeout.
    """

