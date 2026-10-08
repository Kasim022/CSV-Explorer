# CSV Explorer

A Streamlit app for quickly exploring CSV and Excel files. Upload a dataset and get an instant preview, summary stats and interactive charts, with no code needed.

https://github.com/user-attachments/assets/4d0704da-2e64-4f44-85a6-d54cbb57b5d3

## Features
- Upload **CSV, XLSX or XLS** files
- Data preview in a searchable, sortable table
- Dataset overview: rows, columns, missing values, memory usage, duplicate rows
- Basic file safety check (file type matches its contents, flags spreadsheet formula injection). This is not a full antivirus scan.
- Chart builder with bar, line, scatter, pie, histogram and map views, all interactive and downloadable

## Built with
Python, Streamlit, Pandas, Plotly

## Run it locally
1. Install the dependencies: `pip install -r requirements.txt`
2. Start the app: `python -m streamlit run "CSV Explorer.py"`


## Notes
- Not every column combination works with every chart type. If a chart fails, try a different selection.
Future Updates: Colour themes, more chart types, 3D visualisation and machine learning (random forest with adjustable parameters).



