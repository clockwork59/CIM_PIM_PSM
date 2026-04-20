import pandas as pd
import os
import re

# Paths
source_file = "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/concept/副本JHPDL规范 20251201.xlsx"
output_dir = "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/concept/data dictionary"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

print(f"Reading file: {source_file}")

try:
    # Read all sheets
    # sheet_name=None reads all sheets and returns a dictionary of DataFrames
    all_sheets = pd.read_excel(source_file, sheet_name=None)
    
    print(f"Found {len(all_sheets)} sheets.")

    for sheet_name, df in all_sheets.items():
        # Sanitize sheet name for filename
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', sheet_name)
        output_path = os.path.join(output_dir, f"{safe_name}.csv")
        
        # Save to CSV
        # index=False to exclude the row numbers
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved: {output_path}")

    print("All sheets processed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
