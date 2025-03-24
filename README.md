# California Cost of Living Dashboard

## Developer Information
**Name:** Lauren Landa  
**Course:** CS-150 Community Computing Action

## Project Overview

### Region Selection: California
I chose California as the focus for this cost of living dashboard because it represents one of the most economically diverse and dynamic regions in the United States. California has experienced significant economic shifts over the past few decades, with dramatic changes in housing affordability, income inequality, and overall cost of living. As the most populous state with the largest economy in the US, California offers rich datasets that demonstrate the complex interplay between income growth and rising expenses.

### Project Description
This interactive dashboard allows users to explore California's economic trends and cost of living factors from the 1990s to 2020. The application visualizes the relationship between median household income and various expense categories, helping users understand affordability changes over time and how their personal income compares to state averages.

## Datasets

### Selected Datasets
The dashboard incorporates six key datasets from the Federal Reserve Economic Data (FRED):

1. **Minimum Wage Data (CaliMinWage.csv)**  
   Historical California state minimum wage rates

2. **Energy & Gas Per Capita Expenditures (energyGasPC.csv)**  
   Per capita personal consumption expenditures on gasoline and other energy goods

3. **Healthcare Per Capita Expenditures (healthCarePC.csv)**  
   Per capita personal consumption expenditures on healthcare services

4. **Housing & Utilities Per Capita Expenditures (housingUtliPC.csv)**  
   Per capita personal consumption expenditures on housing and utilities

5. **Leisure Goods Per Capita Expenditures (leisureGoodsPC.csv)**  
   Per capita personal consumption expenditures on recreational goods and vehicles

6. **Median Household Income (medianHouseIncomeCal.csv)**  
   Historical median household income data for California

### Data Selection Rationale
These datasets were selected because they:
- Cover a comprehensive timespan (approximately 30 years)
- Represent the most significant expense categories for typical households
- Allow for meaningful comparisons between income growth and expense growth
- Provide per capita figures that enable standardized comparisons
- Come from a reliable, authoritative source (Federal Reserve)

## Data Source Citations

All data was sourced from the Federal Reserve Economic Data (FRED) database:

- Federal Reserve Bank of St. Louis, State Minimum Wage Rate for California [STTMINWGCA], retrieved from FRED, Federal Reserve Bank of St. Louis
- Federal Reserve Bank of St. Louis, Per Capita Personal Consumption Expenditures: Gasoline and Other Energy Goods in California, retrieved from FRED, Federal Reserve Bank of St. Louis
- Federal Reserve Bank of St. Louis, Per Capita Personal Consumption Expenditures: Healthcare in California, retrieved from FRED, Federal Reserve Bank of St. Louis
- Federal Reserve Bank of St. Louis, Per Capita Personal Consumption Expenditures: Housing and Utilities in California, retrieved from FRED, Federal Reserve Bank of St. Louis
- Federal Reserve Bank of St. Louis, Per Capita Personal Consumption Expenditures: Recreational Goods and Vehicles in California, retrieved from FRED, Federal Reserve Bank of St. Louis
- Federal Reserve Bank of St. Louis, Median Household Income in California, retrieved from FRED, Federal Reserve Bank of St. Louis

## Strategic Visualization Decisions

To create an effective data visualization dashboard, I've incorporated several key strategies from the Science of Data Visualization:

1. **Interactive Filtering and Time Range Selection**
   - Implemented a year range slider to allow users to focus on specific time periods
   - Created interactive category selectors to enable comparison between different expense types

2. **Thoughtful Color Coding**
   - Established a consistent color scheme across the dashboard (defined in the COLORS dictionary)
   - Used color to distinguish between different expense categories
   - Applied red for negative indicators and green for positive indicators in the key metrics section

3. **Multiple Visualization Perspectives**
   - Provided three different data view options: actual values, percentage change, and inflation-adjusted figures
   - Created both raw data tables and visual graphs to support different analytical approaches
   - Included ratio analysis to show relationships between income and expenses

4. **Contextual Information and Guidance**
   - Added explanatory text to help users interpret the comparative analysis
   - Included complete data source information and citations
   - Designed a personal income comparison tool to make the data personally relevant

5. **Responsive Layout Design**
   - Implemented a responsive Bootstrap layout that works on various screen sizes
   - Organized content into logical tabs for better information architecture
   - Used consistent styling and spacing for visual clarity

## Example Data Stories

### 1. The Housing Affordability Crisis

Users can explore how housing costs have outpaced income growth in California over the past three decades. The dashboard reveals:
- The widening gap between median household income growth and housing expense growth
- The declining income-to-housing ratio over time, indicating deteriorating affordability
- How different time periods (pre-2008 recession, post-recession recovery, etc.) show varying patterns in the relationship between income and housing costs
- How a user's personal income compares to what's needed for housing affordability in different eras

### 2. Healthcare Cost Burden Analysis

The dashboard enables analysis of how healthcare expenses have evolved relative to income:
- How healthcare costs have grown as a percentage of median household income
- Comparison of healthcare inflation against general income growth
- Identification of specific time periods when healthcare costs accelerated most rapidly
- Analysis of how minimum wage increases have or haven't kept pace with rising healthcare costs

### 3. Economic Resilience Through Recessions

Users can investigate California's economic resilience through major economic downturns:
- Comparison of how different expense categories responded during the 2001 and 2008 recessions
- Analysis of recovery patterns in income vs. expenses after economic shocks
- Visualization of which expense categories are most volatile during economic downturns
- Exploration of how the income-to-expense ratio changes during periods of economic stress
