import pandas as pd

def split_excel_to_csv(filepath, output_dir="data/cleaned"):
    """
    Splits an Excel file into separate CSV files based on sheet names.

    Args:
        filepath (str): Path to the input Excel file.
        output_dir (str, optional): Directory to save the output CSV files. 
                                    Defaults to "outputs".
    """
    sheets = pd.read_excel(filepath, sheet_name=None)

    for sheet_name, df in sheets.items():
        output_file = f"{output_dir}/{sheet_name}.csv"
        df.to_csv(output_file, index=False)
        
split_excel_to_csv('data/raw/vmd_database.xlsx')