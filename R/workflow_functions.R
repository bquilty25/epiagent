#' Epiverse-TRACE Workflow Functions
#'
#' Reusable functions for outbreak analysis workflows.
#' These functions provide a modular interface to the Epiverse-TRACE pipeline.
#'
#' @author Epiverse-TRACE Team
#' @version 2.0.0

#' Setup Ebola Epidemiological Parameters
#'
#' Creates epiparameter objects for Ebola virus disease based on
#' literature values. Parameters include contact distribution,
#' infectious period, incubation period, and delay distributions.
#'
#' @return Named list of epiparameter objects
#' @export
#' @examples
#' params <- setup_ebola_parameters()
#' params$contact_distribution
setup_ebola_parameters <- function() {
  message("Setting up epidemiological parameters...")

  # Contact distribution - Poisson with mean R0 ~ 2
  contact_distribution <- epiparameter::epiparameter(
    disease = "Ebola Virus Disease",
    epi_name = "contact distribution",
    prob_distribution = epiparameter::create_prob_distribution(
      prob_distribution = "pois",
      prob_distribution_params = c(mean = 2)
    )
  )

  # Infectious period - Gamma distributed, mean ~ 6 days
  infectious_period <- epiparameter::epiparameter(
    disease = "Ebola Virus Disease",
    epi_name = "infectious period",
    prob_distribution = epiparameter::create_prob_distribution(
      prob_distribution = "gamma",
      prob_distribution_params = c(shape = 2, scale = 3)
    )
  )

  # Incubation period - Gamma distributed, mean ~ 10 days
  incubation_period <- epiparameter::epiparameter(
    disease = "Ebola Virus Disease",
    epi_name = "incubation period",
    prob_distribution = epiparameter::create_prob_distribution(
      prob_distribution = "gamma",
      prob_distribution_params = c(shape = 2, scale = 5)
    )
  )

  # Onset to hospitalization delay
  onset_to_hosp <- epiparameter::epiparameter(
    disease = "Ebola Virus Disease",
    epi_name = "onset to hospitalisation",
    prob_distribution = epiparameter::create_prob_distribution(
      prob_distribution = "gamma",
      prob_distribution_params = c(shape = 2, scale = 2)
    )
  )

  # Onset to death delay - Based on Barry et al. 2018
  onset_to_death <- epiparameter::epiparameter(
    disease = "Ebola Virus Disease",
    epi_name = "onset to death",
    prob_distribution = epiparameter::create_prob_distribution(
      prob_distribution = "gamma",
      prob_distribution_params = c(shape = 2.4, scale = 3.33)
    )
  )

  list(
    contact_distribution = contact_distribution,
    infectious_period = infectious_period,
    incubation_period = incubation_period,
    onset_to_hosp = onset_to_hosp,
    onset_to_death = onset_to_death
  )
}

#' Simulate Ebola Outbreak
#'
#' Generates synthetic outbreak data using a branching process model
#' with realistic epidemiological parameters.
#'
#' @param params List of epiparameter objects from setup_ebola_parameters()
#' @param outbreak_size Numeric vector c(min, max) for outbreak size
#' @param start_date Date object for outbreak start
#' @param seed Random seed for reproducibility
#'
#' @return List containing linelist and contacts data frames
#' @export
#' @examples
#' params <- setup_ebola_parameters()
#' outbreak <- simulate_ebola_outbreak(params, outbreak_size = c(100, 500))
simulate_ebola_outbreak <- function(params,
                                    outbreak_size = c(100, 500),
                                    start_date = as.Date("2024-01-01"),
                                    seed = 42) {
  set.seed(seed)

  outbreak <- simulist::sim_outbreak(
    contact_distribution = params$contact_distribution,
    infectious_period = params$infectious_period,
    prob_infection = 0.6,
    onset_to_hosp = params$onset_to_hosp,
    onset_to_death = params$onset_to_death,
    outbreak_size = outbreak_size,
    outbreak_start_date = start_date
  )

  message("Simulated ", nrow(outbreak$linelist), " cases")
  outbreak
}

#' Clean and Tag Outbreak Data
#'
#' Performs data cleaning and applies linelist tags for downstream analysis.
#'
#' @param linelist Data frame with raw outbreak data
#'
#' @return Tagged linelist object
#' @export
#' @examples
#' cleaned <- clean_outbreak_data(outbreak$linelist)
clean_outbreak_data <- function(linelist) {
  cleaned_linelist <- cleanepi::clean_data(
    data = linelist,
    standardize_column_names = list(keep = NULL),
    replace_missing_values = list(
      target_columns = NULL,
      na_strings = c("", "NA", "unknown")
    )
  )

  tagged_linelist <- cleaned_linelist |>
    linelist::make_linelist(
      id = "id",
      date_onset = "date_onset",
      date_reporting = "date_reporting",
      date_admission = "date_admission",
      date_outcome = "date_outcome",
      outcome = "outcome",
      gender = "sex",
      age = "age"
    )

  linelist::validate_linelist(tagged_linelist)
  message("Cleaned and tagged ", nrow(tagged_linelist), " records")
  tagged_linelist
}

#' Estimate Case Fatality Risk
#'
#' Calculates static and rolling CFR estimates with delay correction.
#'
#' @param tagged_linelist Tagged linelist from clean_outbreak_data()
#' @param delay_shape Gamma distribution shape parameter
#' @param delay_scale Gamma distribution scale parameter
#'
#' @return List with static and rolling CFR estimates
#' @export
#' @examples
#' cfr_results <- estimate_cfr(tagged_linelist)
estimate_cfr <- function(tagged_linelist,
                        delay_shape = 2.40,
                        delay_scale = 3.33) {
  # Prepare data
  cases_df <- tagged_linelist |>
    dplyr::as_tibble() |>
    dplyr::group_by(date = date_onset) |>
    dplyr::summarise(cases = dplyr::n(), .groups = "drop") |>
    dplyr::filter(!is.na(date))

  deaths_df <- tagged_linelist |>
    dplyr::as_tibble() |>
    dplyr::filter(outcome == "died") |>
    dplyr::group_by(date = date_outcome) |>
    dplyr::summarise(deaths = dplyr::n(), .groups = "drop") |>
    dplyr::filter(!is.na(date))

  cfr_data <- dplyr::full_join(cases_df, deaths_df, by = "date") |>
    dplyr::arrange(date) |>
    dplyr::mutate(
      cases = tidyr::replace_na(cases, 0),
      deaths = tidyr::replace_na(deaths, 0)
    )

  # Fill missing dates
  all_dates <- seq(min(cfr_data$date), max(cfr_data$date), by = "day")
  cfr_data <- dplyr::tibble(date = all_dates) |>
    dplyr::left_join(cfr_data, by = "date") |>
    dplyr::mutate(
      cases = tidyr::replace_na(cases, 0),
      deaths = tidyr::replace_na(deaths, 0)
    )

  # Delay distribution
  delay_func <- function(x) dgamma(x, shape = delay_shape, scale = delay_scale)

  # Estimate CFR
  cfr_static <- cfr::cfr_static(data = cfr_data, delay_density = delay_func)
  cfr_rolling <- cfr::cfr_rolling(data = cfr_data, delay_density = delay_func)

  list(static = cfr_static, rolling = cfr_rolling, data = cfr_data)
}

#' Create Outbreak Visualizations
#'
#' Generates epidemic curve and rolling CFR plots using tracetheme.
#'
#' @param tagged_linelist Tagged linelist data
#' @param cfr_rolling Rolling CFR estimates
#'
#' @return List of ggplot objects
#' @export
#' @examples
#' plots <- create_visualizations(tagged_linelist, cfr_results$rolling)
create_visualizations <- function(tagged_linelist, cfr_rolling) {
  epicurve_plot <- tagged_linelist |>
    dplyr::as_tibble() |>
    ggplot2::ggplot(ggplot2::aes(x = date_onset)) +
    ggplot2::geom_histogram(binwidth = 7, fill = "steelblue", color = "white") +
    ggplot2::labs(
      title = "Epidemic Curve of Simulated Ebola Outbreak",
      subtitle = "Weekly case counts by date of symptom onset",
      x = "Date of Onset",
      y = "Weekly Cases"
    ) +
    ggplot2::theme_minimal(base_size = 12)

  cfr_plot <- cfr_rolling |>
    ggplot2::ggplot(ggplot2::aes(x = date)) +
    ggplot2::geom_line(
      ggplot2::aes(y = severity_estimate),
      color = "darkred",
      linewidth = 1
    ) +
    ggplot2::geom_ribbon(
      ggplot2::aes(ymin = severity_low, ymax = severity_high),
      fill = "darkred",
      alpha = 0.2
    ) +
    ggplot2::labs(
      title = "Rolling Case Fatality Risk (CFR) Estimates",
      subtitle = "Delay-corrected estimates with 95% confidence interval",
      x = "Date",
      y = "CFR Estimate"
    ) +
    ggplot2::scale_y_continuous(
      labels = scales::percent,
      limits = c(0, 1)
    ) +
    ggplot2::theme_minimal(base_size = 12)

  list(epicurve = epicurve_plot, cfr = cfr_plot)
}
