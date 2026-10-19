# Global values: prices are whole cents to avoid rounding errors.
CLOTHING = {'T-Shirt': (800, 1800), 'Jeans': (2200, 4800),
            'Hoodie': (1800, 4000), 'Jacket': (3500, 7500), 'Dress': (2800, 6000)}
# Supply values are (package price, units per package).
SUPPLIES = {'Shopping bags': (2500, 500), 'Gift boxes': (4000, 100),
            'Receipt paper': (1800, 1)}
FIXED = {'Rent': 150000, 'Utilities': 35000, 'Labor': 1800000,
         'Equipment leases': 250000}


def money(cents):
    sign = ''
    if cents < 0:
        sign = '-'
    cents = abs(cents)
    return f'{sign}${cents // 100:,}.{cents % 100:02d}'
