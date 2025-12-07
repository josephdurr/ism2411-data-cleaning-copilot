Reflection on using GitHub Copilot for this assignment

I used GitHub Copilot to scaffold two functions in `src/data_cleaning.py`: `load_data`
and `handle_missing_values`. For each, I wrote a clear comment describing the
desired behavior and accepted Copilot's initial suggestion as a starting point.

What Copilot generated
Copilot suggested the initial structure for `load_data` (reading CSV, cleaning
string cells, and coercing numeric columns) and for `handle_missing_values`
(filling or coercing missing numeric fields). I accepted these suggestions and
used them as the foundation for my implementations.

What I modified
I changed variable names to follow a consistent style (e.g., `price_col`,
`qty_col`), made the column detection robust to variations (e.g., `PRICE` vs
`price`), and added explicit median-based filling for missing prices. I also
simplified some logic (e.g., single-pass string stripping) and added comments
before each major step explaining what and why.

What I learned
I learned that Copilot is very useful for quickly generating sensible
boilerplate code (reading files, basic coercion), but it often needs human
review for edge cases and clarity. For example, Copilot's initial filling
strategy did not choose a clear default for missing prices; I explicitly
chose median fill to be robust to outliers. Using Copilot as a pair-programmer
accelerated the work while still requiring deliberate adjustments to meet
project requirements.
