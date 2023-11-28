from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import pandas as pd
import streamlit as st
from helpers.file_manipulation import FileManipulationHelpers as fmh
from parsers.log_type_parser import LogTypeParser
from parsers.txt_type_parser import TxtTypeParser
from parsers.xlsx_type_parser import XlsxTypeParser

st.write(st.session_state)

# Session states
if "full_folder_path" not in st.session_state:
    st.session_state.full_folder_path = None
if "is_file_loaded" not in st.session_state:
    st.session_state.is_file_loaded = False
if "file_selection_type" not in st.session_state:
    st.session_state.file_selection_type = "Izberi iz seznama"
if "main_data_frame" not in st.session_state:
    st.session_state.main_data_frame = None
if "loaded_file" not in st.session_state:
    st.session_state.loaded_file = None


# Functions
def folder_selector() -> Path | None:
    """Return a selected foldername or None."""
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    # Folder picker button
    return Path(filedialog.askdirectory(parent=root))


def save_temp_file_and_parse_to_df(uploaded_file, file_type: str, *, is_streamlit_obj: bool = True) -> pd.DataFrame:
    """Save the temp file and parse it to a data frame."""
    if is_streamlit_obj:
        temp_file_path = st.session_state.full_folder_path.joinpath(f"{uploaded_file.name}_temp")
        if not temp_file_path.exists():
            with temp_file_path.open("wb") as f:
                f.write(uploaded_file.getvalue())
    else:
        temp_file_path = uploaded_file.path

    if file_type == "xlsx":
        parser = XlsxTypeParser(temp_file_path)
    elif file_type == "txt":
        parser = TxtTypeParser(temp_file_path)
    elif file_type == "log":
        parser = LogTypeParser(temp_file_path)
    else:
        raise ValueError(temp_file_path)

    data = parser.load_data()

    if is_streamlit_obj and temp_file_path.exists():
        temp_file_path.unlink()

    return data


st.title("Aplikacija za analizo meritev")

# --------------------------------- APP --------------------------------- #
# 1. IZBIRA MAPE ZA ANALIZO
st.write("## Izbira mape za delo")
st.write("Izberi mapo za delo s klikom na spodnji gumb.")
if st.button("Izberi mapo", type="primary"):
    st.session_state.full_folder_path = folder_selector()
    st.session_state.is_file_loaded = False
    st.session_state.file_selection_type = "Izberi iz seznama"
    st.session_state.main_data_frame = None
st.write(f"**Izbrana mapa: {st.session_state.full_folder_path!s}**")


# 2. IZBIRA DATOTEKE ZA ANALIZO
if st.session_state.full_folder_path:
    st.write("## Izbira datoteke za analizo")
    st.radio("Izberi način izbire datoteke: ", ("Izberi iz seznama", "Upload"), key="file_selection_type")
    if st.session_state.file_selection_type == "Upload":
        st.session_state.is_file_loaded = False
        st.session_state.main_data_frame = None
        with st.form("my-form", clear_on_submit=True):
            uploaded_file = st.file_uploader("Izberi datoteko za analizo:", type=["csv", "xlsx", "txt", "log"])
            save_uploaded_file = st.checkbox("Shrani naloženo datoteko")
            submitted = st.form_submit_button("NALOŽI!", type="primary")

            if submitted and uploaded_file is not None:
                file_name = uploaded_file.name
                st.write(f"Naložena datoteka: {file_name}.")
                st.session_state.is_file_loaded = True
                if save_uploaded_file:
                    st.write(f"Datoteka bo shranjena v mapi {st.session_state.full_folder_path!s}.")
                    with st.session_state.full_folder_path.joinpath(file_name).open("wb") as f:
                        f.write(uploaded_file.getvalue())

            if uploaded_file is not None:
                # 3. NALAGANJE PODATKOV - uploaded file
                with st.spinner("Nalaganje podatkov ..."):
                    # parse uploaded file to dataframe by file type
                    file_type = uploaded_file.name.split(".")[-1]
                    st.session_state.main_data_frame = (
                        pd.read_csv(uploaded_file)
                        if file_type == "csv"
                        else save_temp_file_and_parse_to_df(uploaded_file, file_type)
                    )

    elif st.session_state.file_selection_type == "Izberi iz seznama":
        parsable_files = fmh.get_all_files_from_folder(st.session_state.full_folder_path)
        parsable_files_dict = {file.file_id: file for file in parsable_files}
        parsable_files_name_to_id_map = {file.name: file.file_id for file in parsable_files}
        selected_file_name = st.selectbox("Izberi datoteko za analizo: ", parsable_files_name_to_id_map.keys())
        # 3. NALAGANJE PODATKOV - seznam
        if selected_file_name and st.button("NALOŽI!", type="primary"):
            st.session_state.is_file_loaded = False
            st.session_state.main_data_frame = None
            st.session_state.loaded_file = None
            with st.spinner("Nalaganje podatkov ..."):
                st.session_state.loaded_file = parsable_files_dict[parsable_files_name_to_id_map[selected_file_name]]
                st.session_state.is_file_loaded = True
                st.session_state.main_data_frame = (
                    pd.read_csv(st.session_state.loaded_file.path)
                    if st.session_state.loaded_file.name.split(".")[-1] == "csv"
                    else save_temp_file_and_parse_to_df(
                        st.session_state.loaded_file,
                        st.session_state.loaded_file.name.split(".")[-1],
                        is_streamlit_obj=False,
                    )
                )

# 4. PRIKAZ PODATKOV
if (
    st.session_state.is_file_loaded
    and st.session_state.main_data_frame is not None
    and st.session_state.loaded_file is not None
):
    st.write("## Prikaz podatkov")
    st.write("Izbrana datoteka:", st.session_state.loaded_file.name)
    st.dataframe(st.session_state.main_data_frame)
    st.checkbox("Podatki so prikazani v tabeli zgoraj.")

#     elif file_selection_type == "Izberi iz seznama":
#         st.session_state.file_selected = False
#         parsable_files = fmh.get_all_files_from_folder(st.session_state.full_folder_path)
#
#         meritev_dataframe = load_data_from_local_file(selected_file_object.path)
#         if meritev_dataframe is not None:
#             st.session_state.file_selected = True


# if "file_selected" not in st.session_state:
#     st.session_state.file_selected = False

# if "selected_columns_checkbox_state " not in st.session_state:
#     st.session_state.selected_columns_checkbox_state = {}


# @st.cache_data


# st.write(st.session_state.file_selected)
# # Prikaz podatkov če je datoteka izbrana
# if st.session_state.file_selected:
#     st.write("## Prikaz podatkov")
#     columns_to_show = []
#     cols = st.columns(3)
#     for id, column_name in enumerate(meritev_dataframe.columns):
#         state = cols[id % 3].checkbox(column_name)
#         st.session_state.selected_columns_checkbox_state[column_name] = state

#     selected_columns_names = [
#         column_name for column_name, state in st.session_state.selected_columns_checkbox_state.items() if state
#     ]
#     st.dataframe(meritev_dataframe[selected_columns_names])

# # df = pd.read_csv("out_data/OutputLog_COM74_20231122-140136.log.csv")
# # df["pressure_water_level_sen[mm]"] = df["pressure_water_level_sen[mm]"].str.replace(",", ".").astype(float)
# # st.dataframe(df)

# # max_column_to_show = st.slider("Število stolpcev za prikaz na grafu:", 1, 10, 1)
# # st.write(max_column_to_show)

# # selected_column = st.selectbox("Izberi stolpec za prikaz na grafu: ", df.columns)
# # st.write("Izbrani stolpec:", selected_column)

# # # prikažemo poljubno število stolpcev
# # # all columns checkbox


# # st.write("## Graf")
# # df["time"] = pd.to_datetime(df["time"])
# # df["motor_speed[rpm]"] = df["motor_speed[rpm]"].astype(int)
# # df = pd.DataFrame({
# # 'date': [timestampStr, millis],
# # 'second column': [10, 20]
# # })


# # st.write(df.dtypes)
# # st.write("Data:", df[["time", "motor_speed[rpm]"]])
# # st.line_chart(df, x="time", y="motor_speed[rpm]")

# # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# # st.line_chart(chart_data)

# # TODO pointerji na grafu
# # deploy te aplikacije, da jo lahko uporabljamo na drugem računalniku
# #
