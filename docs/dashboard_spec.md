# Dashboard Spec: Sales Performance (Tableau)

## Pages
1. Executive Overview (single dashboard)
2. Product & Discount Drilldown (optional)

## Executive Overview Layout
### Header KPIs
- Total Sales
- Total Profit
- Profit Margin
- Orders
- AOV

### Trend (center)
- Line: Sales by Month (Order Date)
- Dual axis: Profit by Month

### Geography (right)
- Filled map by State
  - Color: Profit
  - Tooltip: Sales, Profit, Margin, Orders

### Product (bottom left)
- Bar: Profit by Sub-Category (sorted)
- Include a Top-N parameter for Product Name if desired

### Ops Drivers (bottom right)
- Profit Margin by Discount Bucket
- Avg Profit per Order by Ship Mode

## Global Filters
- Order Date (Year)
- Region
- Segment
- Category

## Interactivity
- Dashboard action: Select State -> filter product chart
- Dashboard action: Select Sub-Category -> filter trend chart

## Story-ready Insights (include in tooltip or annotation)
- Loss leaders: sub-categories with negative profit
- Discount bands where margins turn negative
- States with high sales but low margin
