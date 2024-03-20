# Import python packages
import streamlit as st
import requests
import pandas
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be:"+name_on_order)

from snowflake.snowpark.functions import col

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
st.datafrane(pd_df)

st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients ', 
            my_dataframe,
            max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

    #st.write(my_insert_stmt)
    #st.stop
    
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your smoothie is ordered, ' + name_on_order + '!',icon="✅")


