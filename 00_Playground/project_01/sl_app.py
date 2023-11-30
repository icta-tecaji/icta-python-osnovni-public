from __future__ import annotations

import itertools
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import pandas as pd
import streamlit as st
from helpers.file_manipulation import FileManipulationHelpers as fmh
from matplotlib import pyplot as plt
from parsers.log_type_parser import LogTypeParser
from parsers.txt_type_parser import TxtTypeParser
from parsers.xlsx_type_parser import XlsxTypeParser

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


def save_temp_file_and_parse_to_df(
    uploaded_file,
    file_type: str,
    *,
    is_streamlit_obj: bool = True,
) -> pd.DataFrame | None:
    """Save the temp file and parse it to a data frame."""
    if is_streamlit_obj:
        temp_file_path = st.session_state.full_folder_path.joinpath(f"{uploaded_file.name}_temp")
        if not temp_file_path.exists():
            with temp_file_path.open("wb") as f:
                f.write(uploaded_file.getvalue())
    else:
        temp_file_path = uploaded_file.path

    try:
        if file_type == "xlsx":
            parser = XlsxTypeParser(temp_file_path)
        elif file_type == "txt":
            parser = TxtTypeParser(temp_file_path)
        elif file_type == "log":
            parser = LogTypeParser(temp_file_path)
        else:
            raise ValueError(temp_file_path)

        data = parser.load_data()
    except Exception as e:
        st.error(f"Napaka pri branju datoteke: {e}")
        return None
    else:
        return data
    finally:
        if is_streamlit_obj and temp_file_path.exists():
            temp_file_path.unlink()


# --------------------------------- APP --------------------------------- #
st.title("Aplikacija za analizo meritev")


# 1. IZBIRA MAPE ZA ANALIZO
st.write("## Izbira mape za delo")
st.write("Izberi mapo za delo s klikom na spodnji gumb.")
if st.button("Izberi mapo", type="primary"):
    st.session_state.full_folder_path = folder_selector()
    st.session_state.is_file_loaded = False
    st.session_state.file_selection_type = "Izberi iz seznama"
    st.session_state.main_data_frame = None
    st.session_state.loaded_file = None
st.write(f"**Izbrana mapa: {st.session_state.full_folder_path!s}**")


# 2. IZBIRA DATOTEKE ZA ANALIZO
if st.session_state.full_folder_path:
    st.write("## Izbira datoteke za analizo")
    st.radio("Izberi način izbire datoteke: ", ("Izberi iz seznama", "Upload"), key="file_selection_type")
    if st.session_state.file_selection_type == "Upload":
        with st.form("my-form", clear_on_submit=True):
            uploaded_file = st.file_uploader("Izberi datoteko za analizo:", type=["csv", "xlsx", "txt", "log"])
            save_uploaded_file = st.checkbox("Shrani naloženo datoteko")
            submitted = st.form_submit_button("NALOŽI!", type="primary")

            if submitted and uploaded_file is not None:
                st.session_state.loaded_file = None
                st.session_state.is_file_loaded = False
                st.session_state.main_data_frame = None
                file_name = uploaded_file.name
                st.write(f"Naložena datoteka: {file_name}.")
                if save_uploaded_file:
                    st.write(f"Datoteka bo shranjena v mapi {st.session_state.full_folder_path!s}.")
                    with st.session_state.full_folder_path.joinpath(file_name).open("wb") as f:
                        f.write(uploaded_file.getvalue())

            if uploaded_file is not None:
                # 3. NALAGANJE PODATKOV - uploaded file
                with st.spinner("Nalaganje podatkov ..."):
                    # parse uploaded file to dataframe by file type
                    file_type = uploaded_file.name.split(".")[-1]
                    st.session_state.is_file_loaded = True
                    st.session_state.loaded_file = uploaded_file
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
    columns = st.multiselect("Izberite stolpce za prikaz:", st.session_state.main_data_frame.columns)
    # if not columns:
    #     columns = ["time"]
    selected_columns_names = [col for col in st.session_state.main_data_frame.columns if col in columns]
    if st.checkbox("Prikaži celotno tabelo"):
        selected_columns_names = st.session_state.main_data_frame.columns
    st.dataframe(
        st.session_state.main_data_frame[selected_columns_names],
        use_container_width=True,
        # column_config={
        #     "pu_voltage": st.column_config.ProgressColumn(
        #         "pu_voltage",
        #         help="Napetost na PU-ju",
        #         format="%f",
        #         min_value=2230,
        #         max_value=2260,
        #     ),
        # },
    )

    # 5. PRIKAZ GRAFOV
    st.write("## Prikaz grafov")
    prepared_graphs = {
        "Brez": {},
        "Kombinacija motor": {"x": "time", "y": ["motorspeed", "motorpower"]},
    }
    selected_graph = st.selectbox("Izberite graf:", list(prepared_graphs.keys()))

    if selected_graph == "Brez":
        # select only columns that are not NaN
        columns = st.session_state.main_data_frame.columns
        columns = [col for col in columns if not st.session_state.main_data_frame[col].isna().all()]
        x_axis_column = st.selectbox("Izberite stolpec za x os:", columns)
        y_axis_columns = st.multiselect("Izberite stolpec za y os:", columns)
    else:
        x_axis_column = prepared_graphs[selected_graph]["x"]
        y_axis_columns = prepared_graphs[selected_graph]["y"]

    if len(y_axis_columns) == 1:
        # Plot the selected columns
        fig, ax = plt.subplots()
        for col in y_axis_columns:
            ax.plot(st.session_state.main_data_frame[x_axis_column], st.session_state.main_data_frame[col], label=col)
        ax.set_xlabel(x_axis_column)
        ax.set_ylabel("Value")
        ax.legend()
        st.pyplot(fig)
        st.line_chart(st.session_state.main_data_frame, x=x_axis_column, y=y_axis_columns[0])
    elif len(y_axis_columns) > 1:
        fig, ax = plt.subplots()
        fig.subplots_adjust(right=0.75)
        colors_generator = itertools.cycle(["b", "g", "r", "c", "m", "y", "k", "w"])
        all_axes = [ax.twinx() for _ in range(len(y_axis_columns))]
        for val, data in enumerate(zip(y_axis_columns, all_axes)):
            name, ax = data
            color = next(colors_generator)
            ax.spines.right.set_position(("axes", 1 + (val * 0.25)))
            ax.plot(
                st.session_state.main_data_frame[x_axis_column],
                st.session_state.main_data_frame[name],
                color=color,
            )
            ax.set_ylabel(name, color=color)
        st.pyplot(fig)
        # fig_html = mpld3.fig_to_html(fig)
        # components.html(fig_html, height=500, scrolling=True)

    # vrednost1_limit_max = st.number_input("Vrednost 1 - limit max:", value=70000)
    # vrednost2_limit_max = st.number_input("Vrednost 2 - limit max:", value=1000)

    # fig, ax1 = plt.subplots(figsize=(9, 6))
    # ax2 = ax1.twinx()
    # ax1.plot(st.session_state.main_data_frame["time"], st.session_state.main_data_frame["motorspeed"], "g-")
    # ax2.plot(st.session_state.main_data_frame["time"], st.session_state.main_data_frame["motorpower"], "b-")
    # ax1.set_ylim(0, vrednost1_limit_max)
    # ax2.set_ylim(0, vrednost2_limit_max)
    # ax1.set_xlabel("time (s)")
    # ax1.set_ylabel("voltage (g)", color="g")
    # # st.pyplot(fig)

# # deploy te aplikacije, da jo lahko uporabljamo na drugem računalniku
