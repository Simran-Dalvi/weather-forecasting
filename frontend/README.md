The frontend of this app should look like:

# What pages should you actually show?

I'd make 4 pages.

## 1. Dashboard — /

This is the page your boss/client sees first.

Show:

┌─────────────────────────────────────────────────────────────┐
│ Weather Intelligence                         Pune, India   │
│ Updated 5 min ago                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🌡 Current Temp      💧 Humidity     🌧 Rain     🌬 Wind  │
│     28.4°C               72%          0.0 mm      12 km/h │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│       NEXT-HOUR TEMPERATURE                                │
│                                                             │
│              29.1°C                                        │
│        Expected at 6:00 PM                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Temperature Trend                                           │
│       ╭────╮                                                │
│   ────╯    ╰────╮                                           │
│                  ╰────                                      │
│                                                             │
├───────────────────────────────┬─────────────────────────────┤
│ Humidity                      │ Rainfall                    │
│       chart                   │       chart                 │
└───────────────────────────────┴─────────────────────────────┘

This is your main presentation page.

Don't overload it with 15 charts.

## 2. Forecast page — /forecast

This demonstrates the actual ML component.

Something like:

Next-hour prediction
Current temperature       28.4°C

Predicted temperature     29.1°C
                          ↑ +0.7°C

Prediction time           17:00
Target time               18:00

Then:

Recent predictions vs actual

This is very important.

You already have prediction data and eventually evaluation data.

Plot:

predicted temperature
actual temperature

on the same line chart.

Predicted vs actual temperature

Use your stored predictions and subsequently observed temperatures to evaluate the one-hour-ahead model.

Predicted
Actual
28°C
28.4°C
28.8°C
29.2°C
29.6°C
10:00
11:00
12:00
13:00
14:00

Those numbers above are illustrative. Don't put them into your application. Your frontend should consume the actual API data.

Also show:

Model Performance

MAE       0.38°C
RMSE      0.58°C
R²        0.97

But label these clearly as offline evaluation metrics, not current live accuracy.

## 3. Weather History — /weather

This is where your pretty charts live.

I'd have:

Temperature

Line chart — last 24h / 7 days.

Humidity

Line chart.

Rainfall

Bar chart.

Soil conditions

Two lines:

soil temperature
soil moisture
Pressure / wind

Could be smaller cards/charts.

Add a simple range selector:

[ 24 Hours ] [ 7 Days ] [ 30 Days ]

This makes the application feel like an actual product rather than a ML demo.

## 4. System / Model page — /system

This is optional from a normal user perspective, but I'd include it for your portfolio/demo.

Show:

Pipeline Status

✓ Data ingestion
✓ Data processing
✓ Feature engineering
✓ Prediction
✓ Prediction storage

Last pipeline run
05 Oct 2026  |  12:00 PM

Data source
Open-Meteo

Location
Pune

Model
Temperature — 1 Hour Ahead

5. Navigation

Keep it very simple.

Weather AI
────────────────

Dashboard
Forecast
Weather History
System

────────────────
Pune, India
● System Online

Don't create 10 pages.

For your project, 4 is enough.