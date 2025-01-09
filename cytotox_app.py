import streamlit as st
import pandas as pd

# Title of the app
st.title("CSV File Converter Cytotox")

# File uploader for the CSV file
uploaded_file = st.file_uploader("Upload your metadata CSV file", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Ensure the required column exists
    if "Compound_name" in df.columns:
        # Extract unique compound names for the dropdown menu
        unique_compounds = df["Compound_name"].dropna().unique()
        selected_compounds = st.multiselect(
            "Select Compound Name(s):",
            options=unique_compounds,
            default=None
        )

        # Filter and process the DataFrame if compounds are selected
        if selected_compounds:
            # Filter rows based on selected Compound_name values
            filtered_df = df[df["Compound_name"].isin(selected_compounds)]

            # Sort the DataFrame by Compound_name to organize rows
            filtered_df = filtered_df.sort_values(by="Compound_name")

            # Keep only the required columns
            required_columns = [
                "Cell_line", 
                "Timepoint_h", 
                "Concentration_microM", 
                "Concentration_logM", 
                "Compound_name", 
                "Cell_viability"
            ]
            filtered_df = filtered_df[required_columns]

            # Show the filtered DataFrame
            st.write("Filtered Data:")
            st.dataframe(filtered_df)

            # Generate the output filename
            if len(selected_compounds) == 1:
                output_filename = f"filtered_metadata_{selected_compounds[0]}.csv"
            else:
                compound_names = "_".join([str(c) for c in selected_compounds])
                output_filename = f"filtered_metadata_{compound_names}.csv"

            # Allow the user to download the filtered data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label=f"Download Filtered CSV ({output_filename})",
                data=csv,
                file_name=output_filename,
                mime="text/csv"
            )
    else:
        st.error("The uploaded CSV file does not contain a 'Compound_name' column.")
