import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!:cup_with_straw:")
st.write(
    """**Choose the fruits you want in your custom Smoothie!**
    """
)

Name_On_Order = st.text_input("Name on Smoothie")
#if Order_name <> "Please enter your name":
st.write("Your Order name is", Name_On_Order)

from snowflake.snowpark.functions import col

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose upto five ingredients:",
     my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders
            values ('""" + ingredients_string + """','""" + Name_On_Order + """',
                    '""" + '0' + """','""" + '1' + """'
            )"""

     
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

