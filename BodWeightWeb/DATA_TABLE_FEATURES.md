# Data Table & Export Features Guide

## 🎉 New Features Added!

Your app now includes a comprehensive data table section with CSV export functionality below the weight trend chart.

---

## 📊 What's Been Added

### **1. Three Data Views (Tabs)**

#### **Tab 1: Daily Data**
- Shows average weight for each day
- Sorted by most recent date first
- Rounded to 1 decimal place
- Clean, readable format

**Columns:**
- Date
- Average Weight (lbs)

#### **Tab 2: Monthly Averages**
- Shows average weight for each month
- Displays as "January 2025", "February 2025", etc.
- Sorted by most recent month first
- Rounded to 1 decimal place

**Columns:**
- Month
- Average Weight (lbs)

#### **Tab 3: Raw Data**
- Shows all individual records (filtered by your selection)
- Includes all details: Date, Name, Position, Weight
- Sorted by most recent date first
- Complete dataset for detailed analysis

**Columns:**
- Date
- Name
- Position
- Weight (lbs)

---

## 💾 CSV Export Functionality

Each tab has its own **"Download as CSV"** button:

### **Daily Data Export**
- Filename: `daily_weight_data_[Selection].csv`
- Example: `daily_weight_data_John_Smith.csv`
- Contains: Date and daily average weights

### **Monthly Data Export**
- Filename: `monthly_weight_data_[Selection].csv`
- Example: `monthly_weight_data_All_Individuals.csv`
- Contains: Month names and monthly average weights

### **Raw Data Export**
- Filename: `raw_weight_data_[Selection].csv`
- Example: `raw_weight_data_Running_Back.csv`
- Contains: All individual records with full details

---

## 📈 Summary Statistics

Below the data tables, you'll see 4 key metrics:

1. **Total Records** - Number of data points
2. **Average Weight** - Mean weight across all records
3. **Minimum Weight** - Lowest recorded weight
4. **Maximum Weight** - Highest recorded weight

These update based on your Individual/Position selection.

---

## 🎯 How Users Will Use This

### **Scenario 1: Coach reviewing individual progress**
1. Select "Individual" mode
2. Choose athlete name
3. View the chart
4. Scroll down to "Daily Data" tab
5. Click "Download Daily Data as CSV"
6. Open in Excel for further analysis

### **Scenario 2: Position group analysis**
1. Select "Position" mode
2. Choose "Running Back"
3. View monthly trends in the chart
4. Switch to "Monthly Averages" tab
5. Download CSV for reporting
6. Share with coaching staff

### **Scenario 3: Complete data export**
1. Select "All Individuals"
2. Go to "Raw Data" tab
3. See every single record
4. Download complete dataset
5. Use for statistical analysis

---

## 📋 Page Layout

```
┌─────────────────────────────────────────┐
│  Body Weight Trends Over Time           │
│  Latest data entry: Oct 09, 2025        │
├─────────────────────────────────────────┤
│  ○ Individual  ○ Position               │
│  [Dropdown: Select Individual]          │
├─────────────────────────────────────────┤
│                                         │
│         [WEIGHT TREND CHART]            │
│                                         │
├─────────────────────────────────────────┤
│  📋 Data Table                          │
├─────────────────────────────────────────┤
│  | Daily Data | Monthly Avg | Raw Data |│
│  ├────────────┴─────────────┴──────────┤│
│  │ Date       │ Avg Weight (lbs)       ││
│  │ 2025-10-09 │ 185.3                  ││
│  │ 2025-10-08 │ 186.1                  ││
│  │ 2025-10-07 │ 185.8                  ││
│  │ ...        │ ...                    ││
│  └────────────┴────────────────────────┘│
│  [📥 Download Daily Data as CSV]        │
├─────────────────────────────────────────┤
│  📊 Summary Statistics                  │
│  ┌──────┬──────┬──────┬──────┐         │
│  │ 150  │185.5 │172.3 │198.7 │         │
│  │Total │Avg   │Min   │Max   │         │
│  └──────┴──────┴──────┴──────┘         │
└─────────────────────────────────────────┘
```

---

## 🔧 Technical Details

### **Data Formatting**
- Dates: YYYY-MM-DD format in CSV
- Weights: Rounded to 1 decimal place
- Sorting: Most recent first (descending)
- Names: Preserved as-is from dataset

### **File Naming**
- Spaces in names replaced with underscores
- Example selections:
  - "John Smith" → `daily_weight_data_John_Smith.csv`
  - "All Individuals" → `monthly_weight_data_All_Individuals.csv`
  - "Defensive Line" → `raw_weight_data_Defensive_Line.csv`

### **CSV Structure**
All CSV files include:
- Header row with column names
- No index column
- UTF-8 encoding
- Compatible with Excel, Google Sheets, etc.

---

## 💡 Use Cases

### **For Coaches:**
- Download monthly data to track position group trends
- Export raw data for performance reviews
- Create custom reports in Excel

### **For Athletes:**
- Download personal daily data
- Track progress over time
- Share with trainers

### **For Analytics:**
- Export complete dataset
- Perform statistical analysis
- Create custom visualizations

### **For Reporting:**
- Generate monthly reports
- Compare individuals or positions
- Archive historical data

---

## 🎨 Visual Features

### **Interactive Tables:**
- Sortable columns (click headers)
- Scrollable if data is long
- Full-width display
- Clean, professional appearance

### **Download Buttons:**
- Clear download icon (📥)
- Descriptive labels
- One-click download
- Instant file generation

### **Summary Metrics:**
- Large, easy-to-read numbers
- Color-coded cards
- Updates in real-time
- Responsive layout

---

## ✅ What's Great About This

1. **No Extra Tools Needed** - Export directly from the app
2. **Multiple Views** - Choose the data granularity you need
3. **Filtered Exports** - CSV matches what you're viewing
4. **Professional Format** - Ready for Excel/Sheets
5. **Quick Access** - One click to download
6. **Comprehensive** - From summary to raw details

---

## 🚀 Next Steps

Your app now has:
- ✅ Password protection
- ✅ Interactive weight chart
- ✅ Three data table views
- ✅ CSV export for each view
- ✅ Summary statistics
- ✅ Last updated indicator

Ready to deploy with full data access and export capabilities!
