
<#
Object to hold information about a category
#>
$Source = @"
using System;

public class Category {
  public string parent;
  public string name;
  public double budget;
  public double currentCost;
  private double costToDate;
  
  public Category():this(string.Empty, string.Empty, 0.0 ){ }

  public Category(string parent, string name, double budget){
    this.parent = parent;
    this.name = name;
    this.budget = budget;
    this.currentCost = 0.0;
    this.costToDate = 0.0;
  }

  public double getCostToDate { get { return costToDate; } }
  public double addCostToDate { set { costToDate += value; } }

}
"@

Add-Type -Language CSharp -TypeDefinition $Source
Remove-Variable Source

$script:LogFolder = "$rootPath\Log"
$script:year = $(Get-Date).Year

<# Income #>
# person 1     wk 1 + wk 2
$script:userIncome = 2500 + 2500
# person 2
$script:userIncome += 2900 + 2900

# Uncomment when the person has 3 checks that month
#$script:userIncome += 2500
#$script:userIncome += 2900


<# Report layout #>
$script:htmlPartsStart = "<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>Monthly Budget</title>
<style>
#leftPanel, #rightPanel { width: 48%; }
.floatLeft { float: left; }
.floatRight { float: right; }
table { width:100%; border:1px solid black; margin-top: 1em; border-collapse: collapse; }
table caption { font-weight: bold; font-size: 1.2em; }
th { text-align: left; }
td { }
tfoot { font-weight: bold; border:1px solid black;}
tr:nth-child(even) { background: #76B7F5;}
tr:nth-child(odd) { background: #A9CFF3;}
.overviewTitle { font-weight: bold; width: 50%; }
.default { background-color:white; }
.warning { background-color: red; }
</style>
</head>
<body>
<div id=main>"

$script:htmlPartsEnding = "</div>
<div style='padding:2em 0em 0em 0em;display:flex;width:100%'>
Generated on $(Get-Date)
</div></body></html>"

$script:htmlLeftPanelCats = "Housing","Rental","Transportation","Insurance","Personal"
$script:htmlRightPanelCats = "Food","Entertainment","Loans","Taxes","Investments","Donations","Legal","Pets"
