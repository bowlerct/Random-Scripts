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
        
        Write-Log $("Adding past expense {0} for category {1}" -f $amt, $cat.toUpper())
        $categories.($cat.toUpper()).addCostToDate($amt)
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
    
    $cat = $_.Category.toUpper()
    if ( $categories.Keys -contains $cat ) {
        $categories.($cat).currentCost += $_.Amount
        Write-Log ("Adding current expense for cateogry {0}" -f $cat)
    }
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
    # Parent Category
    [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
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

  # totals for parent category
  $budgetTotal = 0
  $actualTotal = 0
  $difTotal = 0
  $ytdTotal = 0

  # obtain all categories assigned to parent category and build table
  $categories.Values | Where { $_.Parent -eq "$category" } | sort -Property Name | ForEach {
    $difAmount = $_.Budget - $_.currentCost

    # Add to parent category totals
    $budgetTotal += $_.Budget
    $actualTotal += $_.currentCost
    $difTotal += $difAmount
    $ytdTotal += $_.getCostToDate

    $cateogryBody += "<tr>
     <td style=''>{0}</td>
     <td style='text-align:right;width:15%'>$ {1:n2}</td>
     <td style='text-align:right;width:15%'>$ {2:n2}</td>" -f $_.name, $_.Budget, $_.currentCost

    if ( $difAmount -lt 0 ){
      $cateogryBody += "<td style='text-align:right;width:15%;' class='warning'>$ {0:n2}</td>" -f $difAmount
    }else{
      $cateogryBody += "<td style='text-align:right;width:15%;'>$ {0:n2}</td>" -f $difAmount
    }

    $cateogryBody += "<td style='text-align:right;width:15%'>$ {0:n2}</td></tr>" -f $_.getCostToDate
  }

  # Add totals footer
  $cateogryBody += "<tfoot><tr>
     <td>Totals</td>
     <td style='text-align:right;'>$ {0:n2}</td>
     <td style='text-align:right;'>$ {1:n2}</td>" -f $budgetTotal, $actualTotal

  if($difTotal -lt 0){
     $cateogryBody += "<td style='text-align:right;' class='warning'>$ {0:n2}</td>" -f $difTotal
  }else{
     $cateogryBody += "<td style='text-align:right;'>$ {0:n2}</td>" -f $difTotal
  }
  
  $cateogryBody += "<td style='text-align:right;'>$ {0:n2}</td></tr></tfoot></table>" -f $ytdTotal

  $cateogryBody
}

#endregion

#region declarations
$rootPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectedCosts = 0
$actualCosts = 0
$categories = @{}

#endregion

# Load Modules and config file
. "$rootPath\Modules\Logging.ps1"
. "$rootPath\Config.ps1"

Log-Start

<# Categories with budget #>
Log-Write "Loading category file $rootPath\Categories.csv"
Import-Csv "$rootPath\Categories.csv" | ForEach-Object {
   # should not be any duplicates
   if ( $null -eq $_.Category) {
      continue
   }
   $cat = $_.Category.toUpper()
   $categories.Add( $cat, $(New-Object Category($_.Parent, $cat, $_.budget) ) )
   Log-Write $("Loaded Categroy {0} {1} {2}" -f $_.Parent, $cat, $_.budget)
}

loadCurrentExpenses
loadPreviousExpenses

# Add current expenses to ytd totals
$categories.Values | foreach {
  $_.addCostToDate($_.currentCost)
}

# Calculate Total Projected / Actual costs
$categories.Values | ForEach {
   $projectedCosts += $_.Budget
   $actualCosts += $_.currentCost
}


#Create Report
Log-Write "Writing html overiew"
# Overview
$htmlPartsStart += "<div style='padding:0.5em 0em 0em 0em;margin:0pt 0pt 10pt 0pt; display:flex;width:100%'>
<table>
 <caption>{0} Monthly Budget Overview</caption>
 <tr>
  <td class='overviewTitle'>Income</td>
  <td class='default'>$ {1:n2}</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Projected Costs</td>
  <td class='default'>$ {2:n2}</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Actual Costs</td>
  <td class='default'>$ {3:n2}</td>
 </tr>
 <tr>
  <td class='overviewTitle'>Balance (income - actual costs)</td>
  <td class='default'>$ {4:n2}</td>
 </tr>
</table>
</div>" -f $(Get-Date -UFormat %B), $userIncome, $projectedCosts, $actualCosts, $($userIncome - $actualCosts)

# Left Panel
Log-Write "Writing html left panel"
$htmlPartsStart += "<div id=leftPanel class='floatLeft'>"
$htmlLeftPanelCats | forEach {
  $htmlPartsStart += Create-CategoryTable $_
}
$htmlPartsStart += "</div>"

# Right Panel
Log-Write "Writing html right panel"
$htmlPartsStart += "<div id=rightPanel class='floatRight'>"
$htmlRightPanelCats | forEach {
  $htmlPartsStart += Create-CategoryTable $_
}
$htmlPartsStart += "</div>"

# Footer
Log-Write "Writing html footer"
$htmlPartsStart += $htmlPartsEnding

Out-File -Force -FilePath "$rootPath\report.html" -InputObject $htmlPartsStart
Log-Write "html file can be found here $rootPath\report.html"


Log-Finish
