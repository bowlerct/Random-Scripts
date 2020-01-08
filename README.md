# Random-Scripts
Random script of mainly powershell

## New-WeeklyMenu
Modified version from [n3rden](https://github.com/n3rden/Random-Powershell-Scripts/tree/master/New-WeeklyMenu) to build a monthly food menu.

It was modified to have menus for each day except for Sundays as my wife and I usually eat what is left for the week.

## New-MonthlyBudget
Builds a webpage displaying budget information
- Income
- Projected costs
- Actual costs
- Costs per category for the current month and year to date and difference between budgeted and actual

At the end of every month move the file expenses.csv to {YEAR} folder called 'expenses-{MONTH}.csv'. Then start a new expenses.csv file.
Copy the file report.html to {YEAR} folder as report-{MONTH}.html if you want to have a historical monthly view.

Current income is set in Config.ps1. Modify variable $script:userIncome appropriately. 
