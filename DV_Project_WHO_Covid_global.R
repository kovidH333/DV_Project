library(shiny)
library(dplyr)
library(plotly)
library(readr)

# Read the dataset
data <- read_csv("https://covid19.who.int/WHO-COVID-19-global-data.csv")

# Convert Date_reported to Date format
data$Date_reported <- as.Date(data$Date_reported)

ui <- fluidPage(
  titlePanel("COVID-19 Dashboard"),
  
  
  sidebarLayout(
    sidebarPanel(
      selectInput("country", "Select a country:",
                  choices = unique(data$Country)),
      br(),
      dateRangeInput("dates", "Select date range:", 
                     start = min(data$Date_reported), end = max(data$Date_reported),
                     min = min(data$Date_reported), max = max(data$Date_reported)),
      width = 3
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("New Cases Over Time (Bar Plot)", plotlyOutput("newCases_bar")),
        tabPanel("Cumulative Cases Over Time (Line Plot)", plotlyOutput("cumulativeCases_plot")),
        tabPanel("New Deaths Over Time (Bar Plot)", plotlyOutput("newDeaths_bar")),
        tabPanel("Cumulative Deaths Over Time (Line Plot)", plotlyOutput("cumulativeDeaths_plot")),
        tabPanel("Death per Cases (Scatter Plot)", plotlyOutput("deathPerCases_plot")),
        tabPanel("Cases Distribution by WHO Region (Pie Chart)", plotlyOutput("casesByRegion_pie")),
        tabPanel("Latest Data Table", tableOutput("latestData_table"))
      )
    )
  )
)

server <- function(input, output) {
  
  # Filter data based on selected country and date range
  filtered_data <- reactive({
    filtered <- data %>%
      filter(Country == input$country,
             Date_reported >= input$dates[1], Date_reported <= input$dates[2])
    
    if (nrow(filtered) == 0) {
      warning("No data available for the selected country and date range.")
      return(NULL)
    }
    
    return(filtered)
  })
  
  # Generate bar chart of new cases over time
  output$newCases_bar <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    plot_ly(filtered_data(), x = ~Date_reported, y = ~New_cases, type = "bar",
            text = ~paste("Date: ", Date_reported, "<br>New Cases: ", New_cases)) %>%
      layout(title = "New Cases Over Time (Bar Plot)", xaxis = list(title = "Date"), yaxis = list(title = "New Cases"))
  })
  
  # Generate plot of cumulative cases over time
  output$cumulativeCases_plot <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    plot_ly(filtered_data(), x = ~Date_reported, y = ~Cumulative_cases, type = "scatter", mode = "lines",
            line = list(color = 'green'),
            text = ~paste("Date: ", Date_reported, "<br>Cumulative Cases: ", Cumulative_cases)) %>%
      layout(title = "Cumulative Cases Over Time (Line Plot)", xaxis = list(title = "Date"), yaxis = list(title = "Cumulative Cases"))
  })
  
  # Generate bar chart of new deaths over time
  output$newDeaths_bar <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    plot_ly(filtered_data(), x = ~Date_reported, y = ~New_deaths, type = "bar",
            text = ~paste("Date: ", Date_reported, "<br>New Deaths: ", New_deaths)) %>%
      layout(title = "New Deaths Over Time (Bar Plot)", xaxis = list(title = "Date"), yaxis = list(title = "New Deaths"))
  })
  
  # Generate plot of cumulative deaths over time
  output$cumulativeDeaths_plot <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    plot_ly(filtered_data(), x = ~Date_reported, y = ~Cumulative_deaths, type = "scatter", mode = "lines",
            line = list(color = 'purple'),
            text = ~paste("Date: ", Date_reported, "<br>Cumulative Deaths: ", Cumulative_deaths)) %>%
      layout(title = "Cumulative Deaths Over Time (Line Plot)", xaxis = list(title = "Date"), yaxis = list(title = "Cumulative Deaths"))
  })
  
  # Generate plot of death per cases over time
  output$deathPerCases_plot <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    plot_ly(filtered_data(), x = ~Cumulative_cases, y = ~Cumulative_deaths, type = "scatter", mode = "markers",
            text = ~paste("Date: ", Date_reported, "<br>Cumulative Cases: ", Cumulative_cases, "<br>Cumulative Deaths: ", Cumulative_deaths)) %>%
      layout(title = "Death per Cases (Scatter Plot)", xaxis = list(title = "Cumulative Cases"), yaxis = list(title = "Cumulative Deaths"))
  })
  
  # Generate pie chart of cases by WHO region
  output$casesByRegion_pie <- renderPlotly({
    if (is.null(filtered_data())) return(NULL)
    
    region_data <- data %>%
      group_by(WHO_region) %>%
      summarise(Total_cases = sum(Cumulative_cases, na.rm = TRUE))
    
    plot_ly(region_data, labels = ~WHO_region, values = ~Total_cases, type = "pie",
            text = ~paste("Region: ", WHO_region, "<br>Total Cases: ", Total_cases)) %>%
      layout(title = "Cases Distribution by WHO Region (Pie Chart)")
  })
  
  # Generate latest data table
  output$latestData_table <- renderTable({
    if (is.null(filtered_data())) return(NULL)
    
    latest_data <- filtered_data() %>%
      slice_max(Date_reported) %>%
      select(-Date_reported)
    
    latest_data
    
  })
  
}

shinyApp(ui = ui, server = server)
