<#
Requirements
  * Show Categories with budget
  * Show Categories with actual expenses
  * Show Categories with differences between budget and actual
  * Show Categories with year to date expenses
  * Show Budget Overview - projected and actual income / expenses


Design
  Config file - Config.ps1
  Current file - expenses.xsls
  Previous files - YEAR/expenses-MONTH.xsls (calculating expenses_to_date)


Report
  Year / Month
  Overview
    Projected Income, Expenses
    Actual Income, Expenses
    Difference
  Category, Budget, Actual, Difference, YTD

#>

[CmdletBinding()]
Param (
)

#region functions
Function initializeHash {
 Param(
   $hash
 )

 $categories | ForEach-Object {
    $hash.Add($_.Category, 0)
 }
}

Function loadPreviousExpenses {
<#
.SYNOPSIS Loads previous exense files
#>
  Param()

  # find all expense files and load them
  Get-ChildItem -Path "$rootPath\$year" -Filter "expenses-*.csv" | ForEach {
     Log-Write -LineValue "Loading expense file $($_.FullName)"
     $csv = Import-Csv -Path $_.FullName
     
     # now add "Amount" to "Category"
     for($i=0; $i -lt $csv.Count; $i++){
        $cat = $csv.Item($i).Category
        $amt = $csv.Item($i).Amount
        if ($null -eq $cat -or $null -eq $amt) {
           continue
        }
        
        $expenses.$cat += [int]$amt
     }
  }
}

Function loadCurrentExpenses {
  Param()

  Log-Write -LineValue "Loading expense file $rootPath\expenses.csv"
  Import-Csv -Path "$rootPath\expenses.csv" | ForEach-Object {
    if ($null -eq $_.Category -or $null -eq $_.Amount) {
       continue
    }
    
    $currentExpenses.($_.Category) += [int]$_.Amount
  }
}

Function Create-CategoryTable {
<#
.SYNOPSIS
Builds a table with budget information for specified parent category

.EXAMPLE
Create-CategoryTable -category "Housing"

.EXAMPLE
"Housing" | Create-CategoryTable
#>
  Param(
    [Parameter(Mandatory=$true,
      ValueFromPipeline=$true)]
    [string]
    $category
  )

  $cateogryBody = "<table>
    <tr>
     <th>$($category.ToUpper())</th>
     <th>Budgeted</th>
     <th>Actual</th>
     <th>Difference</th>
     <th>YTD</th>
    </tr>"

  # obtain all categories assigned to parent
  $pcats = $categories | Where { $_.Parent -eq $category }

  $budgetTotal = 0
  $actualTotal = 0
  $difTotal = 0
  $ytdTotal = 0

  # loop through and add row for each category
  $pcats | forEach {
    $difAmount = $differences.($_.Category)
    $ytdexpense = $ytdexpenses.($_.Category)
    $actual = $currentExpenses.($_.Category)

    # Add to totals
    $budgetTotal += $_.Budget
    $actualTotal += $actual
    $difTotal += $difAmount
    $ytdTotal += $ytdexpense

    $cateogryBody += "<tr>
     <td style='width:20%;'>$($_.Category)</td>
     <td style='text-align:right;width:20%'>$ $($_.Budget)</td>
     <td style='text-align:right;width:20%'>$ $actual</td>"

    if ( $difAmount -lt 0 ){
      $cateogryBody += "<td style='text-align:right;width:20%;' class='warning'>$ $difAmount</td>"
    }else{
      $cateogryBody += "<td style='text-align:right;width:20%;'>$ $difAmount</td>"
    }

    $cateogryBody += "<td style='text-align:right;width:20%'>$ $ytdexpense</td></tr>"
  }

  # Add totals footer
  $cateogryBody += "<tfoot><tr>
     <td>Totals</td>
     <td style='text-align:right;'>$ $budgetTotal</td>
     <td style='text-align:right;'>$ $actualTotal</td>"

  if($difTotal -lt 0){
     $cateogryBody += "<td style='text-align:right;' class='warning'>$ $difTotal</td>"
  }else{
     $cateogryBody += "<td style='text-align:right;'>$ $difTotal</td>"
  }
  
  $cateogryBody += "<td style='text-align:right;'>$ $ytdTotal</td></tr></tfoot></table>"

  $cateogryBody
}

#endregion

#region declarations
$currentExpenses = @{}
$ytdexpenses = @{}     # Tallies YTD expenses
$differences = @{}  # shows difference between Projected and Actual costs
$rootPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectedCosts = 0
$actualCosts = 0

#endregion

# Load Modules and config file
. "$rootPath\Modules\Logging.ps1"
. "$rootPath\Config.ps1"

Log-Start

initializeHash $currentExpenses
initializeHash $ytdexpenses
initializeHash $differences

loadCurrentExpenses
loadPreviousExpenses
# Add current expenses to ytd totals
foreach($key in $currentExpenses.Keys){
  $ytdexpenses.$key += $currentExpenses.$key
}


#calculate current month differences between budgeted and actual
$categories | ForEach-Object {
   $differences.($_.Category) = $_.Budget - $currentExpenses.($_.Category)
}


# Calculate Projected / Actual costs
$categories | ForEach-Object {
   $projectedCosts += $_.Budget
   $actualCosts += $currentExpenses.($_.Category)
}


#Create Report
# Overview
$htmlPartsStart += "<div style='padding:1em 0em 0em 0em;margin:0pt 0pt 10pt 0pt; display:flex;width:100%'>
<table>
 <caption>$(Get-Date -UFormat %B) Monthly Budget Overview</caption>
 <tr>
  <td class='overviewTitle'>Income</td>
  <td class='default'>$ $userIncome</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Projected Costs</td>
  <td class='default'>$ $projectedCosts</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Actual Costs</td>
  <td class='default'>$ $actualCosts</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Balance (income - actual costs)</td>
  <td class='default'>$ $($userIncome - $actualCosts)</td>
 </tr>
</table>
</div>"

# Left Panel
$htmlPartsStart += "<div id=leftPanel class='floatLeft'>"
$htmlLeftPanelCats | forEach {
  $htmlPartsStart += Create-CategoryTable $_
}
$htmlPartsStart += "</div>"

# Right Panel
$htmlPartsStart += "<div id=rightPanel class='floatRight'>"
$htmlRightPanelCats | forEach {
  $htmlPartsStart += Create-CategoryTable $_
}
$htmlPartsStart += "</div>"

# Footer
$htmlPartsStart += $htmlPartsEnding

Out-File -Force -FilePath "$rootPath\report.html" -InputObject $htmlPartsStart

Log-Finish
