# FINVIZ Industry Filter Codes

이 문서는 FINVIZ Screener API 및 Elite CSV export URL에서 사용하는 FINVIZ industry 이름과 해당 filter code의 매핑을 정리합니다.

**URL 패턴 (Elite CSV Export):**
```
https://elite.finviz.com/export.ashx?v=151&f=ind_{code},cap_smallover&auth={API_KEY}
```

**URL 패턴 (Public Screener):**
```
https://finviz.com/screener.ashx?v=151&f=ind_{code},cap_smallover
```

**Filter code 규칙:** `ind_` + 소문자 industry 이름(공백, 하이픈, 앰퍼샌드, 특수문자 제거)

---

## Aerospace & Defense

| Industry Name | Filter Code |
|---|---|
| Aerospace & Defense | ind_aerospacedefense |

## Auto & Transport

| Industry Name | Filter Code |
|---|---|
| Airlines | ind_airlines |
| Auto Manufacturers | ind_automanufacturers |
| Auto Parts | ind_autoparts |
| Railroads | ind_railroads |
| Recreational Vehicles | ind_recreationalvehicles |
| Trucking | ind_trucking |
| Marine Shipping | ind_marineshipping |

## Basic Materials

| Industry Name | Filter Code |
|---|---|
| Aluminum | ind_aluminum |
| Building Materials | ind_buildingmaterials |
| Chemicals | ind_chemicals |
| Coking Coal | ind_cokingcoal |
| Copper | ind_copper |
| Gold | ind_gold |
| Lumber & Wood Production | ind_lumberwoodproduction |
| Other Industrial Metals & Mining | ind_otherindustrialmetalsmining |
| Other Precious Metals & Mining | ind_otherpreciousmetalsmining |
| Paper & Paper Products | ind_paperpaperproducts |
| Silver | ind_silver |
| Specialty Chemicals | ind_specialtychemicals |
| Steel | ind_steel |
| Uranium | ind_uranium |

## Communication Services

| Industry Name | Filter Code |
|---|---|
| Advertising Agencies | ind_advertisingagencies |
| Broadcasting | ind_broadcasting |
| Electronic Gaming & Multimedia | ind_electronicgamingmultimedia |
| Entertainment | ind_entertainment |
| Internet Content & Information | ind_internetcontentinformation |
| Publishing | ind_publishing |
| Telecom Services | ind_telecomservices |

## Consumer Cyclical

| Industry Name | Filter Code |
|---|---|
| Apparel Manufacturing | ind_apparelmanufacturing |
| Apparel Retail | ind_apparelretail |
| Auto & Truck Dealerships | ind_autotruckdealerships |
| Department Stores | ind_departmentstores |
| Discount Stores | ind_discountstores |
| Footwear & Accessories | ind_footwearaccessories |
| Furnishings, Fixtures & Appliances | ind_furnishingsfixturesappliances |
| Gambling | ind_gambling |
| Home Improvement Retail | ind_homeimprovementretail |
| Internet Retail | ind_internetretail |
| Leisure | ind_leisure |
| Lodging | ind_lodging |
| Luxury Goods | ind_luxurygoods |
| Packaging & Containers | ind_packagingcontainers |
| Personal Services | ind_personalservices |
| Residential Construction | ind_residentialconstruction |
| Resorts & Casinos | ind_resortscasinos |
| Restaurants | ind_restaurants |
| Specialty Retail | ind_specialtyretail |
| Textile Manufacturing | ind_textilemanufacturing |
| Travel Services | ind_travelservices |

## Consumer Defensive

| Industry Name | Filter Code |
|---|---|
| Beverages - Brewers | ind_beveragesbrewers |
| Beverages - Non-Alcoholic | ind_beveragesnonalcoholic |
| Beverages - Wineries & Distilleries | ind_beverageswineriesanddistilleries |
| Confectioners | ind_confectioners |
| Discount Stores | ind_discountstores |
| Education & Training Services | ind_educationtrainingservices |
| Farm Products | ind_farmproducts |
| Food Distribution | ind_fooddistribution |
| Grocery Stores | ind_grocerystores |
| Household & Personal Products | ind_householdpersonalproducts |
| Packaged Foods | ind_packagedfoods |
| Tobacco | ind_tobacco |

## Energy

| Industry Name | Filter Code |
|---|---|
| Oil & Gas Drilling | ind_oilgasdrilling |
| Oil & Gas E&P | ind_oilgasep |
| Oil & Gas Equipment & Services | ind_oilgasequipmentservices |
| Oil & Gas Integrated | ind_oilgasintegrated |
| Oil & Gas Midstream | ind_oilgasmidstream |
| Oil & Gas Refining & Marketing | ind_oilgasrefiningmarketing |
| Thermal Coal | ind_thermalcoal |
| Uranium | ind_uranium |

## Financial Services

| Industry Name | Filter Code |
|---|---|
| Asset Management | ind_assetmanagement |
| Banks - Diversified | ind_banksdiversified |
| Banks - Regional | ind_banksregional |
| Capital Markets | ind_capitalmarkets |
| Credit Services | ind_creditservices |
| Financial Conglomerates | ind_financialconglomerates |
| Financial Data & Stock Exchanges | ind_financialdatastockexchanges |
| Insurance - Diversified | ind_insurancediversified |
| Insurance - Life | ind_insurancelife |
| Insurance - Property & Casualty | ind_insurancepropertycasualty |
| Insurance - Reinsurance | ind_insurancereinsurance |
| Insurance - Specialty | ind_insurancespecialty |
| Insurance Brokers | ind_insurancebrokers |
| Mortgage Finance | ind_mortgagefinance |
| Shell Companies | ind_shellcompanies |

## Healthcare

| Industry Name | Filter Code |
|---|---|
| Biotechnology | ind_biotechnology |
| Diagnostics & Research | ind_diagnosticsresearch |
| Drug Manufacturers - General | ind_drugmanufacturersgeneral |
| Drug Manufacturers - Specialty & Generic | ind_drugmanufacturersspecialtygeneric |
| Health Information Services | ind_healthinformationservices |
| Health Care Plans | ind_healthcareplans |
| Medical Care Facilities | ind_medicalcarefacilities |
| Medical Devices | ind_medicaldevices |
| Medical Distribution | ind_medicaldistribution |
| Medical Instruments & Supplies | ind_medicalinstrumentssupplies |
| Pharmaceutical Retailers | ind_pharmaceuticalretailers |

## Industrials

| Industry Name | Filter Code |
|---|---|
| Aerospace & Defense | ind_aerospacedefense |
| Business Equipment & Supplies | ind_businessequipmentsupplies |
| Conglomerates | ind_conglomerates |
| Consulting Services | ind_consultingservices |
| Electrical Equipment & Parts | ind_electricalequipmentparts |
| Engineering & Construction | ind_engineeringconstruction |
| Farm & Heavy Construction Machinery | ind_farmheavyconstructionmachinery |
| Industrial Distribution | ind_industrialdistribution |
| Infrastructure Operations | ind_infrastructureoperations |
| Integrated Freight & Logistics | ind_integratedfreightlogistics |
| Metal Fabrication | ind_metalfabrication |
| Pollution & Treatment Controls | ind_pollutiontreatmentcontrols |
| Rental & Leasing Services | ind_rentalleasingservices |
| Security & Protection Services | ind_securityprotectionservices |
| Specialty Business Services | ind_specialtybusinessservices |
| Specialty Industrial Machinery | ind_specialtyindustrialmachinery |
| Staffing & Employment Services | ind_staffingemploymentservices |
| Tools & Accessories | ind_toolsaccessories |
| Waste Management | ind_wastemanagement |

## Real Estate

| Industry Name | Filter Code |
|---|---|
| Real Estate - Development | ind_realestatedevelopment |
| Real Estate - Diversified | ind_realestatediversified |
| Real Estate Services | ind_realestateservices |
| REIT - Diversified | ind_reitdiversified |
| REIT - Healthcare Facilities | ind_reithealthcarefacilities |
| REIT - Hotel & Motel | ind_reithotelandmotel |
| REIT - Industrial | ind_reitindustrial |
| REIT - Mortgage | ind_reitmortgage |
| REIT - Office | ind_reitoffice |
| REIT - Residential | ind_reitresidential |
| REIT - Retail | ind_reitretail |
| REIT - Specialty | ind_reitspecialty |

## Technology

| Industry Name | Filter Code |
|---|---|
| Communication Equipment | ind_communicationequipment |
| Computer Hardware | ind_computerhardware |
| Consumer Electronics | ind_consumerelectronics |
| Electronic Components | ind_electroniccomponents |
| Electronics & Computer Distribution | ind_electronicscomputerdistribution |
| Information Technology Services | ind_informationtechnologyservices |
| Scientific & Technical Instruments | ind_scientifictechnicalinstruments |
| Semiconductor Equipment & Materials | ind_semiconductorequipmentmaterials |
| Semiconductors | ind_semiconductors |
| Software - Application | ind_softwareapplication |
| Software - Infrastructure | ind_softwareinfrastructure |
| Solar | ind_solar |

## Utilities

| Industry Name | Filter Code |
|---|---|
| Utilities - Diversified | ind_utilitiesdiversified |
| Utilities - Independent Power Producers | ind_utilitiesindependentpowerproducers |
| Utilities - Regulated Electric | ind_utilitiesregulatedelectric |
| Utilities - Regulated Gas | ind_utilitiesregulatedgas |
| Utilities - Regulated Water | ind_utilitiesregulatedwater |
| Utilities - Renewable | ind_utilitiesrenewable |

---

## 전체 알파벳 인덱스

빠른 조회를 위해 전체 industry filter code를 알파벳 순으로 정리한 목록입니다.

| # | Industry Name | Filter Code |
|---|---|---|
| 1 | Advertising Agencies | ind_advertisingagencies |
| 2 | Aerospace & Defense | ind_aerospacedefense |
| 3 | Airlines | ind_airlines |
| 4 | Aluminum | ind_aluminum |
| 5 | Apparel Manufacturing | ind_apparelmanufacturing |
| 6 | Apparel Retail | ind_apparelretail |
| 7 | Asset Management | ind_assetmanagement |
| 8 | Auto & Truck Dealerships | ind_autotruckdealerships |
| 9 | Auto Manufacturers | ind_automanufacturers |
| 10 | Auto Parts | ind_autoparts |
| 11 | Banks - Diversified | ind_banksdiversified |
| 12 | Banks - Regional | ind_banksregional |
| 13 | Beverages - Brewers | ind_beveragesbrewers |
| 14 | Beverages - Non-Alcoholic | ind_beveragesnonalcoholic |
| 15 | Beverages - Wineries & Distilleries | ind_beverageswineriesanddistilleries |
| 16 | Biotechnology | ind_biotechnology |
| 17 | Broadcasting | ind_broadcasting |
| 18 | Building Materials | ind_buildingmaterials |
| 19 | Business Equipment & Supplies | ind_businessequipmentsupplies |
| 20 | Capital Markets | ind_capitalmarkets |
| 21 | Chemicals | ind_chemicals |
| 22 | Coking Coal | ind_cokingcoal |
| 23 | Communication Equipment | ind_communicationequipment |
| 24 | Computer Hardware | ind_computerhardware |
| 25 | Confectioners | ind_confectioners |
| 26 | Conglomerates | ind_conglomerates |
| 27 | Consulting Services | ind_consultingservices |
| 28 | Consumer Electronics | ind_consumerelectronics |
| 29 | Copper | ind_copper |
| 30 | Credit Services | ind_creditservices |
| 31 | Department Stores | ind_departmentstores |
| 32 | Diagnostics & Research | ind_diagnosticsresearch |
| 33 | Discount Stores | ind_discountstores |
| 34 | Drug Manufacturers - General | ind_drugmanufacturersgeneral |
| 35 | Drug Manufacturers - Specialty & Generic | ind_drugmanufacturersspecialtygeneric |
| 36 | Education & Training Services | ind_educationtrainingservices |
| 37 | Electrical Equipment & Parts | ind_electricalequipmentparts |
| 38 | Electronic Components | ind_electroniccomponents |
| 39 | Electronic Gaming & Multimedia | ind_electronicgamingmultimedia |
| 40 | Electronics & Computer Distribution | ind_electronicscomputerdistribution |
| 41 | Engineering & Construction | ind_engineeringconstruction |
| 42 | Entertainment | ind_entertainment |
| 43 | Farm & Heavy Construction Machinery | ind_farmheavyconstructionmachinery |
| 44 | Farm Products | ind_farmproducts |
| 45 | Financial Conglomerates | ind_financialconglomerates |
| 46 | Financial Data & Stock Exchanges | ind_financialdatastockexchanges |
| 47 | Food Distribution | ind_fooddistribution |
| 48 | Footwear & Accessories | ind_footwearaccessories |
| 49 | Furnishings, Fixtures & Appliances | ind_furnishingsfixturesappliances |
| 50 | Gambling | ind_gambling |
| 51 | Gold | ind_gold |
| 52 | Grocery Stores | ind_grocerystores |
| 53 | Health Care Plans | ind_healthcareplans |
| 54 | Health Information Services | ind_healthinformationservices |
| 55 | Home Improvement Retail | ind_homeimprovementretail |
| 56 | Household & Personal Products | ind_householdpersonalproducts |
| 57 | Industrial Distribution | ind_industrialdistribution |
| 58 | Infrastructure Operations | ind_infrastructureoperations |
| 59 | Information Technology Services | ind_informationtechnologyservices |
| 60 | Insurance - Diversified | ind_insurancediversified |
| 61 | Insurance - Life | ind_insurancelife |
| 62 | Insurance - Property & Casualty | ind_insurancepropertycasualty |
| 63 | Insurance - Reinsurance | ind_insurancereinsurance |
| 64 | Insurance - Specialty | ind_insurancespecialty |
| 65 | Insurance Brokers | ind_insurancebrokers |
| 66 | Integrated Freight & Logistics | ind_integratedfreightlogistics |
| 67 | Internet Content & Information | ind_internetcontentinformation |
| 68 | Internet Retail | ind_internetretail |
| 69 | Leisure | ind_leisure |
| 70 | Lodging | ind_lodging |
| 71 | Lumber & Wood Production | ind_lumberwoodproduction |
| 72 | Luxury Goods | ind_luxurygoods |
| 73 | Marine Shipping | ind_marineshipping |
| 74 | Medical Care Facilities | ind_medicalcarefacilities |
| 75 | Medical Devices | ind_medicaldevices |
| 76 | Medical Distribution | ind_medicaldistribution |
| 77 | Medical Instruments & Supplies | ind_medicalinstrumentssupplies |
| 78 | Metal Fabrication | ind_metalfabrication |
| 79 | Mortgage Finance | ind_mortgagefinance |
| 80 | Oil & Gas Drilling | ind_oilgasdrilling |
| 81 | Oil & Gas E&P | ind_oilgasep |
| 82 | Oil & Gas Equipment & Services | ind_oilgasequipmentservices |
| 83 | Oil & Gas Integrated | ind_oilgasintegrated |
| 84 | Oil & Gas Midstream | ind_oilgasmidstream |
| 85 | Oil & Gas Refining & Marketing | ind_oilgasrefiningmarketing |
| 86 | Other Industrial Metals & Mining | ind_otherindustrialmetalsmining |
| 87 | Other Precious Metals & Mining | ind_otherpreciousmetalsmining |
| 88 | Packaged Foods | ind_packagedfoods |
| 89 | Packaging & Containers | ind_packagingcontainers |
| 90 | Paper & Paper Products | ind_paperpaperproducts |
| 91 | Personal Services | ind_personalservices |
| 92 | Pharmaceutical Retailers | ind_pharmaceuticalretailers |
| 93 | Pollution & Treatment Controls | ind_pollutiontreatmentcontrols |
| 94 | Publishing | ind_publishing |
| 95 | Railroads | ind_railroads |
| 96 | Real Estate - Development | ind_realestatedevelopment |
| 97 | Real Estate - Diversified | ind_realestatediversified |
| 98 | Real Estate Services | ind_realestateservices |
| 99 | Recreational Vehicles | ind_recreationalvehicles |
| 100 | REIT - Diversified | ind_reitdiversified |
| 101 | REIT - Healthcare Facilities | ind_reithealthcarefacilities |
| 102 | REIT - Hotel & Motel | ind_reithotelandmotel |
| 103 | REIT - Industrial | ind_reitindustrial |
| 104 | REIT - Mortgage | ind_reitmortgage |
| 105 | REIT - Office | ind_reitoffice |
| 106 | REIT - Residential | ind_reitresidential |
| 107 | REIT - Retail | ind_reitretail |
| 108 | REIT - Specialty | ind_reitspecialty |
| 109 | Rental & Leasing Services | ind_rentalleasingservices |
| 110 | Residential Construction | ind_residentialconstruction |
| 111 | Resorts & Casinos | ind_resortscasinos |
| 112 | Restaurants | ind_restaurants |
| 113 | Scientific & Technical Instruments | ind_scientifictechnicalinstruments |
| 114 | Security & Protection Services | ind_securityprotectionservices |
| 115 | Semiconductor Equipment & Materials | ind_semiconductorequipmentmaterials |
| 116 | Semiconductors | ind_semiconductors |
| 117 | Shell Companies | ind_shellcompanies |
| 118 | Silver | ind_silver |
| 119 | Software - Application | ind_softwareapplication |
| 120 | Software - Infrastructure | ind_softwareinfrastructure |
| 121 | Solar | ind_solar |
| 122 | Specialty Business Services | ind_specialtybusinessservices |
| 123 | Specialty Chemicals | ind_specialtychemicals |
| 124 | Specialty Industrial Machinery | ind_specialtyindustrialmachinery |
| 125 | Specialty Retail | ind_specialtyretail |
| 126 | Staffing & Employment Services | ind_staffingemploymentservices |
| 127 | Steel | ind_steel |
| 128 | Telecom Services | ind_telecomservices |
| 129 | Textile Manufacturing | ind_textilemanufacturing |
| 130 | Thermal Coal | ind_thermalcoal |
| 131 | Tobacco | ind_tobacco |
| 132 | Tools & Accessories | ind_toolsaccessories |
| 133 | Travel Services | ind_travelservices |
| 134 | Trucking | ind_trucking |
| 135 | Uranium | ind_uranium |
| 136 | Utilities - Diversified | ind_utilitiesdiversified |
| 137 | Utilities - Independent Power Producers | ind_utilitiesindependentpowerproducers |
| 138 | Utilities - Regulated Electric | ind_utilitiesregulatedelectric |
| 139 | Utilities - Regulated Gas | ind_utilitiesregulatedgas |
| 140 | Utilities - Regulated Water | ind_utilitiesregulatedwater |
| 141 | Utilities - Renewable | ind_utilitiesrenewable |
| 142 | Waste Management | ind_wastemanagement |

**총계: 142개 산업**

---

## 참고

1. **Filter code 생성 규칙**: industry 이름에서 공백, 하이픈, 앰퍼샌드(`&`) 및 기타 특수문자를 제거하고 소문자로 변환한 뒤 `ind_`를 접두어로 붙입니다.

2. **복수 섹터 industry**: 일부 industry(예: Uranium)는 FINVIZ의 여러 섹터(Energy, Basic Materials)에 중복 표시됩니다. 어느 섹터 화면에서 접근하든 filter code는 동일합니다.

3. **Industry 변경 가능성**: FINVIZ는 industry를 추가/삭제/개명할 수 있습니다. 이 목록은 2026년 2월 기준이며, 특정 filter code가 결과를 반환하지 않으면 FINVIZ에서 industry 이름을 직접 확인하세요.

4. **필터 결합**: FINVIZ URL에서 여러 industry 필터를 쉼표로 결합할 수 있습니다.
   ```
   f=ind_semiconductors,ind_softwareapplication,cap_smallover
   ```

5. **시가총액 필터**: 테마 탐지에서는 micro-cap 왜곡을 줄이기 위해 항상 `cap_smallover`(시가총액 > $300M)와 함께 사용합니다.

6. **특수 케이스**:
   - "E&P"는 "ep"로 변환(앰퍼샌드 제거)
   - "REIT - " 접두사는 "reit"로 변환(하이픈/공백 제거)
   - "Wineries & Distilleries"는 "wineriesanddistilleries"로 변환(이 경우 앰퍼샌드를 "and"로 처리)
   - 결과가 이상하면 FINVIZ에서 edge case를 직접 검증하세요
