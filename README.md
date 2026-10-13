# MP1 Data Processing Pipeline

This project is a command-line data processing pipeline that takes in a dataset, checks it for problems, cleans it, and saves the final result. It starts by loading the input file along with a YAML configuration file that controls how the data should be handled. The pipeline then checks that all required columns are present and removes rows with invalid numeric values. After that, it cleans the data by removing duplicates, handling missing values, and filtering out outliers. The code is organized into separate modules inside the src folder so that each part of the pipeline has its own job, such as loading data, validating it, processing it, saving it, and handling shared utility functions. Once the pipeline finishes, it saves the cleaned dataset in the output folder and prints a short cleaning report showing what changed.

## Example Command

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example Output

```text
Validation complete: 100 -> 98 rows
Processing complete: 98 -> 92 rows
Saved cleaned data to output/clean.csv

{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6,
 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```