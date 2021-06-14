library(shiny)
library(tidyverse)
library(dygraphs)

protocols = readRDS("protocols.rds")

ui = fluidPage(
        
        titlePanel("TVL Data"),
        
        sidebarLayout(
            sidebarPanel(
                #     # Continent input
                selectInput("platform", "Platform", 
                            choices = protocols$name),
                
                checkboxInput("btc", "Show ETH Price:",
                              value = TRUE)
            ),
            
            
            # scatter plot output
            mainPanel(
                dygraphOutput("scatterPlot")
            )
        )
    )
    
server = function(input, output) {
        
        output$scatterPlot <- 
            renderDygraph({
                if(input$btc == TRUE){
                    dygraph(protocols$dygraphsEth[[input$platform]], main = input$platform) %>%
                        dyAxis("y", label = "TVL (Bilion $)") %>%
                        dySeries("totalLiquidityUSD", label = "TVL", color = "red") %>%
                        dyOptions(axisLineWidth = 1.5, fillGraph = TRUE, drawGrid = FALSE) %>%
                        dyRangeSelector(dateWindow = c("2021-04-01", "2021-06-09"))%>%
                        dySeries("ethPrice", label = "ETH", color = "blue")
                } else {
                    dygraph(protocols$dygraphsNoEth[[input$platform]], main = input$platform) %>%
                        dyAxis("y", label = "TVL (Bilion $)") %>%
                        dySeries("totalLiquidityUSD", label = "TVL", color = "red") %>%
                        dyOptions(axisLineWidth = 1.5, fillGraph = TRUE, drawGrid = FALSE) %>%
                        dyRangeSelector(dateWindow = c("2021-04-01", "2021-06-09"))
                    
                }
            })
}

shinyApp(ui = ui, server = server)