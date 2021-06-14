# Defi-Tvl Analysis

> A brief study of the TVL of some DeFi platforms in R.

This project is divided in *two parts*:

1. The **first** is about a general study of the TVL across multiple platforms.
2. The **second part** focuses on a speficic case, in particular it's an analysis of the **Farms APR** of pancake swap.

## Requirements

To run the code in the `.Rmd` files you need to install the [cryptoprice package](https://github.com/fradeca01/cryptoprice). To install the package, run the following code in **R Console**:

```
devtools::install_github("fradeca01/cryptoprice")
```

Other required pacakages are:

* cowplot
* DBI
* RSQLite
* libridate
* modelr
* dplyr
* tidyrto
* ggplot2
* jsonlite
* httr
* dygraphs
* xts

To run the **first part** [Part1-TVL.Rmd](https://github.com/fradeca01/Defi-Tvl/blob/main/Part1-TVL.Rmd) it's advisable to download [tvl(2021-06-12).rds](https://github.com/fradeca01/DeFi-Tvl-Analysis/blob/main/tvl(2021-06-12).rds). If you want to download updated data directly from the API you need to uncomment lines 51-53 and comment line 57. Note that the following analysis may become wrong if you use updated data. 

To run the **second part** [Part2-TVL.Rmd](https://github.com/fradeca01/Defi-Tvl/blob/main/Part2-apr.Rmd) you need to download the following [files](https://uniudamce-my.sharepoint.com/:f:/g/personal/154259_spes_uniud_it/EhohMC4-EAxMkkeAwCi-hXIBVfZrsmgs9u9ohWm9LtFOIw?e=wu3N6K). Just move the folder inside your project folder.

To run the **presentation** [Presentation.rmd](https://github.com/fradeca01/Defi-Tvl/blob/main/Presentation.Rmd) you need to download this files:

* [protocols.rds](https://github.com/fradeca01/Defi-Tvl/blob/main/protocols.rds)
* [plots.rds](https://github.com/fradeca01/Defi-Tvl/blob/main/plots.rds)
* [aprPlots.rds](https://github.com/fradeca01/Defi-Tvl/blob/main/aprPlots.rds)
