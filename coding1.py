import pandas as pd
from collections import defaultdict
import argparse
import logging
from typing import Set, Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def validate_columns(df: pd.DataFrame, required_columns: Set[str]) -> None:
    """Validate that all required columns are present in the DataFrame."""
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing one or more required columns: {missing}")


def load_and_prepare_data(csv_file_path: str) -> pd.DataFrame:
    """Load CSV file and prepare DataFrame by stripping column names."""
    try:
        df = pd.read_csv(csv_file_path)
        df.columns = df.columns.str.strip()
        logging.info("Loaded data with columns: %s", df.columns.tolist())
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {csv_file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing the CSV file: {csv_file_path}")


def group_product_views(df: pd.DataFrame) -> pd.DataFrame:
    """Group product views by Parent org and Brand."""
    return df.groupby(['Parent org', 'Brand'])['Product View Count'].sum().reset_index()


def calculate_parent_totals(grouped_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total product views per Parent org."""
    return grouped_df.groupby('Parent org')['Product View Count'].sum().reset_index().sort_values(
        by='Product View Count', ascending=False
    )


def build_brand_map(grouped_df: pd.DataFrame) -> Dict[str, List[Tuple[str, int]]]:
    """Create a mapping of Parent org to its Brands and their view counts."""
    org_brand_map = defaultdict(list)
    for _, row in grouped_df.iterrows():
        org_brand_map[row['Parent org']].append(
            (row['Brand'], row['Product View Count']))
    return org_brand_map


def format_report(parent_totals: pd.DataFrame, brand_map: Dict[str, List[Tuple[str, int]]]) -> str:
    """Generate a formatted report as a string."""
    report_lines = []
    for _, parent_row in parent_totals.iterrows():
        parent_org = parent_row['Parent org']
        total_views = parent_row['Product View Count']
        report_lines.append(f"{parent_org} : {total_views}")
        brands_sorted = sorted(
            brand_map[parent_org], key=lambda x: x[1], reverse=True)
        for brand, count in brands_sorted:
            report_lines.append(f" {brand} : {count}")
        report_lines.append("")  # Blank line between parent orgs
    return "\n".join(report_lines)


def analyze_product_views(csv_file_path: str) -> None:
    """Main function to analyze product views from a CSV file."""
    required_columns = {'Parent org', 'Brand', 'Product View Count'}
    df = load_and_prepare_data(csv_file_path)
    validate_columns(df, required_columns)
    grouped_views = group_product_views(df)
    parent_totals = calculate_parent_totals(grouped_views)
    brand_map = build_brand_map(grouped_views)
    report = format_report(parent_totals, brand_map)
    print(report)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze product views from a CSV file.")
    parser.add_argument("csv_path", help="Path to the input CSV file")
    args = parser.parse_args()
    try:
        analyze_product_views(args.csv_path)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
