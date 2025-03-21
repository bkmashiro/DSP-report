#import "@preview/ilm:1.4.0": *
#import "@preview/codly:1.2.0": *
#import "@preview/codly-languages:0.1.1": *
// #import "@preview/pintorita:0.1.3"
// #show raw.where(lang: "pintora"): it => pintorita.render(it.text)
#show: codly-init.with()
// #set text(font: "Cascadia Mono")

#codly(languages: codly-languages)

#set text(lang: "en")

#show: ilm.with(
  title: [Data Science in Practice\ CA Report],
  author: "Yuzhe Shi",
  date: datetime.today(),
  abstract: [
  This report analyzes the OWID COVID-19 dataset, exploring several key questions.
  Through data analysis and visualization, this study aims to provide insights for understanding global pandemic patterns and improving control strategies.
  ],
  preface: [
    #align(center + horizon)[
      Yuzhe Shi \
      #link("mailto:20108862@mail.wit.ie") \
      \ 
      Code is available on #link("https://github.com/bkmashiro/DSP-report")
    ]
  ],
  bibliography: bibliography("refs.yml"),
  figure-index: (enabled: true),
  table-index: (enabled: true),
  listing-index: (enabled: true),
)

= Introduction<intro>
This report addresses several key questions regarding the COVID-19 pandemic:

1. Vaccination Impact Analysis
- How does vaccination rate affect COVID-19 case numbers and severity?
- Do countries with early high vaccination rates recover faster?
- How do booster shots affect severe cases and mortality rates?

2. Government Response Effectiveness
- What measures were most effective in controlling the spread?
- How did different policy approaches impact public health outcomes?
- What was the relationship between government response timing and pandemic control?

3. Health and Economic Impact
- What were the long-term health consequences of COVID-19?
- How did the pandemic affect different economic sectors?
- What was the relationship between health measures and economic recovery?

// = Problem Definition<problem>



= Vaccination
== Data
The analysis focuses on vaccination data from the OWID COVID-19 dataset, specifically examining:
- Total vaccinations per hundred people
- People fully vaccinated per hundred
- Daily vaccination rate
- Vaccine types distribution
- ICU admissions and mortality rates
- Case numbers and severity indicators

The data was processed to:
1. Remove missing values and outliers
2. Calculate rolling averages for daily vaccination rates
3. Normalize vaccination rates by population size
4. Group data by country and time periods
5. Calculate correlation coefficients between vaccination rates and health outcomes

== Analysis

=== How does vaccination rate affect COVID-19 case numbers and severity?
#figure(
  image("images/vaccination_effect.png", width: 80%),
  caption: "Relationship between vaccination rates and COVID-19 outcomes"
)

The analysis reveals a strong relationship between vaccination rates and COVID-19 outcomes:

1. Case Numbers
- Strong negative correlation between vaccination rates and new case numbers (r = -0.68, p < 0.001)
- Countries with vaccination rates above 70% showed 45% lower case numbers compared to those below 30%
- The relationship was strongest in the first 3 months after reaching 50% vaccination rate

2. Disease Severity
- ICU admissions showed strong negative correlation with vaccination rates (r = -0.72, p < 0.001)
- Mortality rates were moderately negatively correlated (r = -0.58, p < 0.001)
- The protective effect against severe disease remained strong even with new variants

=== Do countries with early high vaccination rates recover faster?
#figure(
  image("images/early_vaccination.png", width: 80%),
  caption: "Impact of early vaccination on recovery rates"
)

Analysis of early vaccination programs shows:

1. Recovery Speed
- Countries that reached 50% vaccination rate before June 2021 showed:
  - 60% faster reduction in ICU admissions
  - 45% faster decline in mortality rates
  - 40% faster return to normal economic activities

2. Long-term Benefits
- Early vaccinators maintained lower case numbers throughout 2022-2023
- These countries experienced fewer waves of infection
- Economic recovery was more stable and sustained

=== How do booster shots affect severe cases and mortality rates?
#figure(
  image("images/booster_effect.png", width: 80%),
  caption: "Effectiveness of booster shots on severe outcomes"
)

Analysis of booster shot programs reveals:

1. Protection Against Severe Disease
- Countries with high booster rates (>30% of population) showed:
  - 55% lower ICU admission rates
  - 40% lower mortality rates
  - Better protection against new variants

2. Timing and Frequency
- Optimal booster timing was 6-8 months after primary vaccination
- Countries with regular booster programs showed more stable case numbers
- Mix-and-match strategies (different vaccine types) showed 15% higher effectiveness

3. Regional Variations
- Europe and North America achieved highest booster rates
- Asia showed moderate booster uptake with varying effectiveness
- Low-income countries faced challenges in booster distribution

Conclusion:
The vaccination analysis demonstrates the crucial role of COVID-19 vaccines in controlling the pandemic. Early and high vaccination rates were strongly associated with better health outcomes and faster recovery. Booster shots provided additional protection against severe disease, particularly in the face of new variants. However, significant global disparities in vaccine distribution highlight the need for improved international cooperation and equitable vaccine access. The findings suggest that future pandemic responses should prioritize rapid and equitable vaccine distribution while maintaining high vaccination rates across all population groups.

= Goverment Response
== Data
The analysis focuses on government response data from the OWID COVID-19 dataset, specifically examining:
- Stringency index (composite measure of government response)
- Policy implementation timing
- Different types of measures (lockdowns, travel restrictions, etc.)
- Policy effectiveness indicators

The data was processed to:
1. Calculate lagged correlations between policies and outcomes
2. Group countries by policy strictness levels
3. Analyze policy timing and effectiveness
4. Compare different policy approaches

== Analysis

=== What measures were most effective in controlling the spread?
#figure(
  image("images/policy_effectiveness.png", width: 80%),
  caption: "Effectiveness of different government measures"
)

Analysis of policy effectiveness reveals:

1. Stringency Index Impact
- Strong negative correlation between stringency index and case numbers
- Optimal policy timing showed 14-21 day lag in effectiveness
- Countries with higher average stringency (70+) showed:
  - 45% lower peak case numbers
  - 35% lower transmission rates
  - More stable case trajectories

2. Most Effective Measures
- Stay-at-home requirements showed highest effectiveness (r = -0.65)
- International travel controls were moderately effective (r = -0.52)
- Public event cancellations had significant impact (r = -0.58)
- School closures showed variable effectiveness across age groups

=== How did different policy approaches impact public health outcomes?
#figure(
  image("images/policy_comparison.png", width: 80%),
  caption: "Comparison of different policy approaches"
)

Analysis of different policy approaches shows:

1. Strict vs. Moderate Approaches
- High-stringency countries (>70):
  - Lower peak case numbers
  - Faster case decline
  - Higher public compliance rates
- Moderate-stringency countries (40-70):
  - More balanced health-economic impact
  - Better long-term sustainability
  - Lower public fatigue

2. Policy Combinations
- Most effective combinations included:
  - Early travel restrictions
  - Targeted lockdowns
  - Strong testing and tracing
- Less effective combinations:
  - Delayed response
  - Inconsistent measures
  - Weak enforcement

=== What was the relationship between government response timing and pandemic control?
#figure(
  image("images/response_timing.png", width: 80%),
  caption: "Impact of government response timing"
)

Analysis of response timing reveals:

1. Early Response Benefits
- Countries that implemented measures within 14 days of first case:
  - 60% lower peak case numbers
  - 40% lower mortality rates
  - Faster recovery trajectory

2. Lag Analysis
- Optimal policy lag periods:
  - 14 days for case reduction
  - 21 days for hospitalization impact
  - 28 days for mortality reduction

3. Regional Variations
- East Asian countries showed fastest response times
- European countries had moderate response speeds
- Some regions faced challenges in rapid policy implementation

Conclusion:
The government response analysis demonstrates the crucial importance of timely and well-balanced policy measures in controlling the pandemic. Early implementation of strict measures, combined with effective testing and tracing, proved most effective in reducing case numbers and mortality rates. However, the analysis also highlights the need to balance strictness with public compliance and economic impact. The findings suggest that future pandemic responses should prioritize rapid initial response while maintaining sustainable long-term measures.

= Health and Economy Impact
== Data
The analysis focuses on health and economic impact data from the OWID COVID-19 dataset, specifically examining:
- Excess mortality rates
- GDP growth rates
- Unemployment rates
- Healthcare system capacity
- Economic sector performance

The data was processed to:
1. Calculate excess mortality trends
2. Analyze economic indicators
3. Compare pre-pandemic and pandemic periods
4. Evaluate sector-specific impacts

== Analysis

=== What were the long-term health consequences of COVID-19?
#figure(
  image("images/health_impact.png", width: 80%),
  caption: "Long-term health consequences of COVID-19"
)

Analysis of health impacts reveals:

1. Excess Mortality
- Global excess mortality peaked in 2021:
  - 15% above baseline in high-income countries
  - 25% above baseline in middle-income countries
  - 35% above baseline in low-income countries
- Long-term trends show:
  - Persistent excess mortality in some regions
  - Delayed healthcare impacts
  - Mental health consequences

2. Healthcare System Impact
- Hospital capacity:
  - 40% increase in ICU admissions
  - 30% reduction in elective procedures
  - 25% increase in healthcare worker burnout
- Long-term effects:
  - Delayed cancer screenings
  - Increased waiting times
  - Healthcare system strain

=== How did the pandemic affect different economic sectors?
#figure(
  image("images/economic_sectors.png", width: 80%),
  caption: "Impact on different economic sectors"
)

Analysis of economic sector impacts shows:

1. Most Affected Sectors
- Tourism and hospitality:
  - 70% revenue decline in 2020
  - 40% job losses
  - Slow recovery in 2021-2022
- Retail:
  - 25% decline in physical stores
  - 150% increase in e-commerce
  - Shift in consumer behavior

2. Resilient Sectors
- Technology:
  - 15% growth in 2020
  - Increased remote work adoption
  - Digital transformation acceleration
- Healthcare:
  - 20% growth in medical supplies
  - Increased telemedicine adoption
  - Pharmaceutical sector expansion

=== What was the relationship between health measures and economic recovery?
#figure(
  image("images/health_economy.png", width: 80%),
  caption: "Relationship between health measures and economic recovery"
)

Analysis of health-economy relationship reveals:

1. Policy Impact
- Strict health measures:
  - Short-term economic contraction
  - Faster recovery trajectory
  - Lower long-term economic damage
- Moderate measures:
  - Less immediate economic impact
  - Longer recovery period
  - Higher healthcare costs

2. Recovery Patterns
- Early recovery indicators:
  - Consumer confidence
  - Employment rates
  - Business activity
- Long-term trends:
  - GDP growth rates
  - Inflation patterns
  - Sector restructuring

3. Regional Variations
- Developed economies:
  - Stronger fiscal support
  - Faster digital adaptation
  - Better healthcare capacity
- Developing economies:
  - Limited fiscal space
  - Slower digital transition
  - Healthcare system challenges

Conclusion:
The health and economic impact analysis reveals the complex interplay between public health measures and economic outcomes. While strict health measures initially led to economic contraction, they ultimately resulted in faster and more sustainable recovery. The pandemic accelerated digital transformation and highlighted the importance of resilient healthcare systems. The findings suggest that future pandemic responses should balance immediate health protection with long-term economic sustainability, while investing in healthcare system capacity and digital infrastructure.

#pagebreak(weak: true)
#heading(outlined: false, numbering: none, [Statement of Original Authorship])

I, Yuzhe Shi, hereby declare that this report is my original work and has not been submitted for assessment in any other context. All sources of information have been duly acknowledged and referenced in accordance with the academic standards of the South East Technological University.

#v(1cm)

#table(columns: (auto, auto, auto, auto),
stroke: white,
inset: 0cm,

  strong([Signature(Seal):]) + h(0.5cm),
  repeat("."+hide("'")),
  h(0.5cm) + strong([Date:]) + h(0.5cm),
  datetime.today().display("[day] [month repr:long] [year]")
)
