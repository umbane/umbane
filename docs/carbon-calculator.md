# Carbon Credit Calculator

## Overview

The carbon credit calculator estimates the amount of CO2 emissions that can be offset based on renewable energy production.

## Calculation Formula

```
credits = energy_kwh × emission_factor
```

### Default Values

| Parameter | Value | Unit |
|-----------|-------|------|
| Emission Factor | 500 | grams CO2/kWh |

### Example Calculations

| Energy (kWh) | CO2 Offset (grams) | CO2 Offset (kg) |
|--------------|-------------------|-----------------|
| 1 | 500 | 0.5 |
| 10 | 5,000 | 5 |
| 100 | 50,000 | 50 |
| 1,000 | 500,000 | 500 |

## Emission Factors

### South Africa
- **Grid average**: ~900g CO2/kWh (mostly coal)
- **Source**: Eskom coal-heavy generation mix

### International Standards
- **EU grid**: ~400g CO2/kWh
- **US grid**: ~450g CO2/kWh  
- **World average**: ~500g CO2/kWh

### Sources
- South Africa: Eskom annual reports
- International: IEA, EPA, European Environment Agency

## Implementation

### API Endpoint

```
GET /chainlink/calculate-credits?energy_kwh={value}
```

### Response

```json
{
  "energy_kwh": 100,
  "credits": "50000",
  "calculation": "100 kWh × 500g CO2/kWh = 50000g CO2 offset"
}
```

## Future Improvements

- [ ] Add configurable emission factor
- [ ] Support different regions/countries
- [ ] Add carbon price conversion (USD/ZAR)
- [ ] Include verification via Chainlink oracle
- [ ] Add timestamp for audit trail

## References

- [IPCC Emission Factors](https://www.ipcc.ch/)
- [IEA Emission Factors](https://www.iea.org/)
- [South Africa Energy Outlook](https://www.eesk.co.za/)
