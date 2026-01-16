# backend/core/patterns.py

# Ara fem servir claus en ANGLÈS
PATTERNS = {
    # IBAN (Es queda igual, és estàndard)
    "IBAN": r'ES\d{2}(?:[\s-]*\d){20}',

    # DNI/NIE -> ID_CARD
    "ID_CARD": r'[XYZxyz]?\d{7,8}[-\s]?[A-Za-z]',

    # EMAIL (Igual)
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',

    # TARGETA_CREDIT -> CREDIT_CARD
    "CREDIT_CARD": r'\b(?:\d[ -]*?){13,19}\b',
    
    # TELEFON -> PHONE
    "PHONE": r'\b(\+34|0034|34)?[ -]*(6|7|8|9)[ -]*([0-9][ -]*){8}\b'
}
