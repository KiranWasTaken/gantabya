
### Functionality:

1.  **Import necessary modules:**
    *   `datetime` and `timedelta` for date calculations.
    *   `TravelCost` from `.models` to fetch historical travel costs.
    *   `Avg` and `F` from `django.db.models` for database aggregations and field access.
    *   `random` for generating random numbers for seasonality adjustments.

2.  **Define `cost_estimation` function:**
    *   Takes `destination_id`, `start_date`, `end_date`, and `budget` as input.
    *   Calculates a date range for historical data, spanning one year before and after the `start_date`.

3.  **Query historical data:**
    *   Filters the `TravelCost` model based on `destinationID` and the calculated date range.
    *   Uses `annotate` to extract the year and month from the `start_date`.
    *   Uses `values` to retrieve only the `title`, `price`, and `start_date` fields for optimization.

4.  **Iterate through historical data:**
    *   Initializes an empty list `optimized_costs` to store optimized travel costs.
    *   Initializes `total_optimized_cost` to 0.0 to accumulate the total optimized cost.
    *   Loops through each `item` in the `historical_data` QuerySet.

5.  **Apply seasonality adjustment:**
    *   Retrieves the month from the `start_date` of the current `item`.
    *   Defines a list `peak_season_months` representing peak travel months.
    *   If the month is in `peak_season_months`, increase the `price` by a random factor between 1.1 and 1.2.
    *   Otherwise, decrease the `price` by a random factor between 0.9 and 0.95.

6.  **Apply budget constraint:**
    *   If the adjusted `price` exceeds the provided `budget`, reduce the `price` to 90% of the budget.

7.  **Store optimized cost:**
    *   Append a dictionary containing the `title` and adjusted `price` to the `optimized_costs` list.
    *   Add the adjusted `price` to the `total_optimized_cost`.

8.  **Return results:**
    *   Return the `optimized_costs` list and the `total_optimized_cost`.

This function provides a baseline for estimating travel costs, incorporating adjustments for seasonality and budget constraints. Further enhancements could include more sophisticated algorithms, real-time data integration, and user-specific preferences.
