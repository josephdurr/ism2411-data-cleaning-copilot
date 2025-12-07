Reflection on using GitHub Copilot for this assignment

I used GitHub Copilot to scaffold two functions in `src/data_cleaning.py`:
`load_data` and `handle_missing_values`. For each function I wrote a short
comment describing the desired behavior and accepted Copilot's suggested code
as a starting point, then modified the suggestions to meet the assignment
requirements.
desired behavior and accepted Copilot's initial suggestion as a starting point.

What Copilot generated
Copilot produced a useful scaffold for reading the CSV and basic coercion
logic. For `load_data` it suggested reading the file, trimming string cells,
and attempting numeric coercion. For `handle_missing_values` Copilot suggested
a function that would identify numeric columns and fill missing values. These
initial suggestions saved time implementing standard boilerplate.

What I modified
I changed variable names to follow a consistent style (e.g., `price_col`,
`qty_col`), made the column detection robust to variations in case and spacing
(`PRICE` vs `price` vs `Price`), and added explicit handling for dollar signs
and other non-numeric characters before coercion. I also chose a clear
strategy for missing values: fill missing prices with the median price and fill
missing quantities with `1`. These choices ensure consistency and reduce the
chance of dropping useful rows unnecessarily. Finally, I added comments before
each major step explaining what is being done and why, as required by the
assignment.
`qty_col`), made the column detection robust to variations (e.g., `PRICE` vs
`price`), and added explicit median-based filling for missing prices. I also
simplified some logic (e.g., single-pass string stripping) and added comments
before each major step explaining what and why.


What I learned
I learned that Copilot is effective at producing reliable boilerplate (file
I/O, basic string cleanup, numeric coercion) and is a useful time-saver. At
the same time, Copilot suggestions must be reviewed: it may not handle all
edge cases (for example, dollar-formatted prices like `$12.50`, textual noise
such as `abc`, or different column name casings). A concrete example: Copilot
suggested filling missing values, but I explicitly implemented median-based
filling for `price` and a default of `1` for `quantity` to make the behavior
transparent and defensible. Overall, Copilot sped up development while I kept
control over correctness and clarity.

If I had more time I would capture the exact Copilot prompts and suggestions in
the repository (for reproducibility) and add a small unit test covering more
edge cases (non-numeric prices, empty categories).
