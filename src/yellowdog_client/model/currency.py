from enum import Enum


class Currency(Enum):
    AED = "AED"
    """UAE Dirham"""
    ARS = "ARS"
    """Argentinian Peso"""
    AUD = "AUD"
    """Australian Dollar"""
    BDT = "BDT"
    """Bangladeshi Taka"""
    BGN = "BGN"
    """Bulgarian Lev"""
    BHD = "BHD"
    """Bahraini Dinar"""
    BRL = "BRL"
    """Brazilian Real"""
    CAD = "CAD"
    """Canadian Dollar"""
    CHF = "CHF"
    """Swiss Frank"""
    CLP = "CLP"
    """Chilean Peso"""
    CNY = "CNY"
    """Chinese Yuan"""
    COP = "COP"
    """Colombian Peso"""
    CRC = "CRC"
    """Costa Rican Colon"""
    CZK = "CZK"
    """Czech Koruna"""
    DKK = "DKK"
    """Danish Krone"""
    EGP = "EGP"
    """Egyptian Pound"""
    EUR = "EUR"
    """Euro"""
    GBP = "GBP"
    """British Pound"""
    HUF = "HUF"
    """Hungarian Forint"""
    HKD = "HKD"
    """Hong Kong Dollar"""
    HRK = "HRK"
    """Croatian Kuna"""
    IDR = "IDR"
    """Indonesian Rupiah"""
    ILS = "ILS"
    """Israeli New Shekel"""
    INR = "INR"
    """Indian Rupee"""
    ISK = "ISK"
    """Icelandic Krona"""
    JPY = "JPY"
    """Japanese Yen"""
    KRW = "KRW"
    """South Korean Won"""
    KWD = "KWD"
    """Kuwaiti Dinar"""
    NOK = "NOK"
    """Norwegian Krone"""
    NZD = "NZD"
    """New Zealand Dollar"""
    MXN = "MXN"
    """Mexican Peso"""
    MYR = "MYR"
    """Malaysian Ringgit"""
    PEN = "PEN"
    """Peruvian Sol"""
    PHP = "PHP"
    """Philippine Peso"""
    PKR = "PKR"
    """Pakistani Rupee"""
    PLN = "PLN"
    """Poland Zloty"""
    QAR = "QAR"
    """Qatari Rial"""
    RON = "RON"
    """Romanian Leu"""
    RSD = "RSD"
    """Serbian Dinar"""
    RUB = "RUB"
    """Russian Ruble"""
    SAR = "SAR"
    """Saudi Riyal"""
    SEK = "SEK"
    """Swedish Krone"""
    SGD = "SGD"
    """Singapore Dollar"""
    THB = "THB"
    """Thai Baht"""
    TRY = "TRY"
    """Turkish Lira"""
    TWD = "TWD"
    """Taiwan Dollar"""
    USD = "USD"
    """US Dollar"""
    VND = "VND"
    """Vietnamese Dong"""
    ZAR = "ZAR"
    """South African Rand"""

    def __str__(self) -> str:
        return self.name