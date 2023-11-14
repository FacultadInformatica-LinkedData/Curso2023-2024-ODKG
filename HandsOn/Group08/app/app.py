import streamlit as st
import pandas as pd
from api import request
from wiki_data_api import obtain_desc_img


@st.cache_data
def load_states():
    df = pd.read_csv("./app/static/states.csv")
    return list(df["stateName"])


def main():

    st.title("University Ontology")

    states = load_states()

    state_selected = st.selectbox(
        "Selected a state to filter",
        states,
        index=None,
        placeholder="Selected a State of US",
    )


    with st.spinner('Requesting Info to Ontology'):
        df = request(state_selected)

    if isinstance(df, pd.DataFrame):

        if df.empty:
            st.write("No data for this state")
        else:

            columns_to_drop = ["longitude", "latitude"]
            df_map = df[columns_to_drop].copy()

            df.drop(columns=columns_to_drop, inplace=True)

            st.dataframe(
                df,
                column_config={
                    "website": st.column_config.LinkColumn("Website"),
                    "uriUniWikiData": st.column_config.LinkColumn("Wiki Data Uni URI"),
                    "gRate": st.column_config.ProgressColumn(
                        "AVG Graduation Rate",
                        help="The AVG Graduation Rate",
                        min_value=0,
                        max_value=100,
                    ),
                })

            st.map(df_map)

            st.header("Wiki data info of a selected University or College")

            nameUni = st.selectbox(
                "Selected a university to see more details",
                list(df["nameUni"]),
                index=None,
                placeholder="Selected a University or College",
            )

            if nameUni:

                st.write('Selected to show the University:', nameUni)

                df_uni = df.loc[df['nameUni'] == nameUni]

                df_uni_show = df_uni[['nameUni', 'nameCity', "uriUniWikiData"]]

                st.dataframe(
                    df_uni_show,
                    hide_index=True,
                    column_config={
                        "uriUniWikiData": st.column_config.LinkColumn("Wiki Data link"),
                        "nameUni": st.column_config.TextColumn(
                            "University Name"),
                        "nameCity": st.column_config.TextColumn(
                            "City Name")

                    })

                qualifier = str(
                    df_uni["uriUniWikiData"].values[0]).split("/")[-1]

                if qualifier:
                    description, img_url = obtain_desc_img(qualifier)

                    if img_url:
                        with st.spinner('Loading IMG'):
                            st.image(img_url, caption=description,
                                     use_column_width=True)
                    else:
                        st.write("This Qualifier is not mapped")

    else:
        st.warning("The API is down")


if __name__ == "__main__":
    main()
