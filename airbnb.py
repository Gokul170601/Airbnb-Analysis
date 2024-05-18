import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import time

from sqlalchemy import create_engine

#mysql alchemy engine created to querying with MYSQL Database

engine = create_engine("mysql+mysqlconnector://root:@localhost/airbnb") 


#set up page configuration for streamlit
icon='https://avatars.githubusercontent.com/u/698437?s=280&v=4'
st.set_page_config(page_title='AIRBNB ',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide',menu_items={"about":'This streamlit application was developed by M.Gokul'})

title_text = '''<h1 style='font-size: 36px;color:#ff5a5f;text-align: center;'>AIRBNB</h1><h2 style='font-size: 24px;color:#008891;text-align: center;'>Explore Your Dream Stays</h2>'''
st.markdown(title_text, unsafe_allow_html=True)

#set up home page and optionmenu 
selected = option_menu("MainMenu",
                        options=["OVERVIEW","HOME","DISCOVER","INSIGHTS","ABOUT"],
                        icons=["list icon","house", "globe","lightbulb","info-circle"],
                        default_index=1,
                        orientation="horizontal",
                        styles={"container": {"width": "100%","border": "1px ridge  ","background-color": "#002b36","primaryColor": "#FF69B4"},
                                "icon": {"color": "#F8CD47", "font-size": "20px"}})

#set up the details for option 'overview'
if selected == "OVERVIEW":

    st.subheader(':red[Project Title :]')
    st.markdown('<h5> Airbnb Analysis',unsafe_allow_html=True)

    st.subheader(':red[Domain :]')
    st.markdown('<h5> Travel Industry, Property Management and Tourism',unsafe_allow_html=True)

    st.subheader(':red[Technologies :]')
    st.markdown('<h5> Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.',unsafe_allow_html=True)

    st.subheader(':red[Overview :]')
    bullet_points = [
    " Accessed and processed a JSON dataset containing Airbnb data from 2019",
    "Utilized Python for data transformation, ensuring it fit into a structured DataFrame",
    "Applied data preprocessing techniques, including cleaning and organizing, to enhance data quality and usability",
    "Leveraged the MySQL Python connector to establish a relational database",
    "Inserted the preprocessed data into appropriate tables within the database",
    "Developed an interactive dashboard using Streamlit, providing users with a platform to explore insights from the dataset",
    "Incorporated dynamic visualizations with Plotly to enrich the dashboard's analytical capabilities"
    ]

    for point in bullet_points:
        st.markdown(f"**- {point}**")
    
    
    st.subheader(':red[Features :]')
    
    st.markdown('''**In the 'Home' section of our project, users can explore detailed hotel information by selecting a country.
                This feature provides an overview of each hotel, including price, room type, description, and ratings.**''')           
    st.markdown('''**In the 'Discover' section, users have the opportunity to explore countries through dynamic geo-visualizations,
                supplemented with price insights. Additionally, users can refine their exploration by selecting specific property
                types and room types, allowing for a more tailored search experience.**''')              
    st.markdown('''**In the 'Insight' section, users explore two categories: 'Top Insights' and 'Filtered Insights'. 'Top Insights' 
                offer pre-defined queries with insightful analysis, while 'Filtered Insights' allow users to select specific criteria for tailored visualizations.**''')

    st.subheader(':red[Power BI :]')
    st.markdown("**I demonstrated this project in Power BI. Click the button below to get a glimpse of my dashboard.**")

    image_path='Airbnb_Dashboard.png'

    if 'show_image' not in st.session_state:
        st.session_state.show_image = False

    if st.button('View Dashboard'):
        st.session_state.show_image = not st.session_state.show_image
    
    if st.session_state.show_image:
        st.image(image_path, caption='Power BI Dashboard', use_column_width=True)
    

    st.subheader(':red[About :]')
    st.markdown('''**Hello! I'm Gokul, a MBA graduate with a keen interest in data science and analytics.
                Currently on an exciting journey into the world of data science...**''')
    st.link_button('Linkedin','https://www.linkedin.com/in/gokul-m-j17/') 
    

#set up the details for option 'Home 
if selected == "HOME":
    col1,col2=st.columns([2,1])

    with col2:
        st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExN292YXdvdjhnZ3djYXhhenhlMXkyem0xcDdwYjZzcWYxNTdoYmlyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AErExHJVxRbkm5hPkB/giphy.gif",use_column_width=True)

    with col1:

        st.write(' ')
        st.subheader(':red[Embark on Your Journey]')
        st.markdown('''**Start Your Adventure with Airbnb! Dive into detailed hotel listings and find the perfect accommodation for your next journey.**''')

        df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
        selected_country= st.selectbox("Search destinations",options=df_Country['country'].tolist(),index=None)
        st.write(' ')

        df_street=pd.read_sql_query('''SELECT DISTINCT street from hotels_info WHERE country =%s''',
                                    con=engine,params=[(selected_country,)])
        selected_street= st.selectbox("Select Street",options=df_street['street'].tolist(),index=None)
        st.write(' ')

        df_hotels=pd.read_sql_query('''SELECT DISTINCT name from hotels_info WHERE street =%s''',
                                    con=engine,params=[(selected_street,)])
        selected_Hotel=st.selectbox('Select Hotel',options=df_hotels['name'].tolist(),index=None)


        st.write("Selected Accommodation:", f"<span style='color:#F8CD47'>{selected_Hotel}</span>", unsafe_allow_html=True)
        

    if selected_Hotel:
        more=st.button('Click for Details')


        if more:
            st.write(":red[Note: The information provided below is from the year 2019.]")

                
            df=pd.read_sql_query('''SELECT name,listing_url,description,country,price,images,property_type,room_type,amenities,
                                        host_picture_url,host_name,host_url,host_about,host_location,overall_score,rating,number_of_reviews
                                        from hotels_info
                                        join rooms_info on hotels_info.id=rooms_info.id
                                        JOIN host_info on hotels_info.id = host_info.id
                                        join reviews_info on hotels_info.id = reviews_info.id
                                        where name= %s ''',con=engine,params=[(selected_Hotel,)])
                
            extract_detail = df.to_dict(orient='records')[0] 
            c1,c2=st.columns(2)
            with c1:
                    st.write('**:green[Basic Details]**')
                    st.write("**:violet[Name :]**", f'**{extract_detail['name']}**')
                    st.write("**:violet[Website Url :]**",extract_detail['listing_url'])
                    st.write("**:violet[country :]**",f'**{extract_detail['country']}**')
                    st.write("**:violet[Description :]**",extract_detail['description'])
                    st.write("**:violet[Price in $ :]**",f'**{extract_detail['price']}**')
                    st.write("**:violet[Total Reviews :]**",f'**{extract_detail['number_of_reviews']}**')
                    st.write("**:violet[Overall Score:]**", f"**{extract_detail['overall_score']} &nbsp;&nbsp;&nbsp; **:violet[Rating:]** {extract_detail['rating']}**")
                    st.write("**:violet[Room Picture :]**")
                    st.image(extract_detail['images'],width=300)

            with c2:
                    st.write('**:green[Room Details]**')
                    st.write("**:violet[Property Type :]**",f'**{extract_detail['property_type']}**')
                    st.write("**:violet[Room Type :]**",f'**{extract_detail['room_type']}**')
                    st.write("**:violet[Amenities :]**",f'**{extract_detail['amenities']}**')
                    st.write('**:green[Host Details]**')
                    st.write("**:violet[Host Name :]**",f'**{extract_detail['host_name']}**')
                    st.write("**:violet[Host Url :]**",extract_detail['host_url'])
                    st.write("**:violet[Host location :]**",f'**{extract_detail['host_location']}**')
                    st.write("**:violet[Host About :]**",f'**{extract_detail['host_about']}**')
                    st.write("**:violet[Host Picture :]**")
                    st.image(extract_detail['host_picture_url'],width=300)


            df=pd.read_sql_query('''SELECT  reviewer_name,comments FROM comments_info 
                                        join hotels_info on comments_info.id =hotels_info.id
                                        where name=%s LIMIT 10''',con=engine,params=[(selected_Hotel,)])
                
            st.write('**:green[Top Comments]**')
            st.dataframe(df,hide_index=True,use_container_width=True)

#set up the details for option 'Discover'
if selected == "DISCOVER":
    st.subheader(":red[Explore Accommodation by Country]")

    df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
    selected_country= st.selectbox("select country",options=df_Country['country'].tolist(),index=None)
    
    if selected_country:
            
            chek=st.checkbox(f"Click to view Accommodation by Property wise and room type in {selected_country} ")

            if not chek:
        
                df=pd.read_sql_query('''  SELECT name as 'HotelName',price, SUBSTRING_INDEX(coordinates, ', ', 1) AS longitude,
                                    SUBSTRING_INDEX(coordinates, ', ', -1) AS latitude  FROM hotels_info
                                    where country = %s  ''',con=engine,params=[(selected_country,)])
                
                df[['longitude','latitude']]=df[['longitude','latitude']].astype('float')
                
                fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                        hover_name='HotelName',zoom=10,
                                        hover_data={'longitude':False,'latitude':False, 'price': True},
                                        color_discrete_sequence=px.colors.colorbrewer.Blues_r)
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

                st.plotly_chart(fig,use_container_width=True)

            if chek:
                st.subheader(f":red[Explore Accommodation by Property wise and room type in {selected_country}]")

                df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
                selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

                df_room=pd.read_sql_query('''SELECT DISTINCT room_type from rooms_info join hotels_info on rooms_info.id=hotels_info.id
                                where property_type=%s and country =%s  ''',engine,params=[(selected_prop,selected_country)])
                selected_room=st.radio('select a Room type',options=df_room['room_type'].tolist(),index=None)

                if selected_room:

                    df=pd.read_sql_query(''' SELECT name as 'HotelName', property_type,room_type,price,
                                                SUBSTRING_INDEX(coordinates, ', ', 1) AS longitude,
                                                SUBSTRING_INDEX(coordinates, ', ', -1) AS latitude  
                                                FROM hotels_info   JOIN rooms_info ON hotels_info.id = rooms_info.id 
                                                WHERE country = %s AND property_type =%s and room_type=%s
                                                GROUP BY name,property_type,room_type; ''',con=engine,params=[(selected_country,selected_prop,selected_room)])
                    
                    df[['longitude','latitude']]=df[['longitude','latitude']].astype('float')
                    
                    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                            hover_name='HotelName',zoom=10,
                                            hover_data={'longitude':False,'latitude':False, 'price': True,'property_type':True,'room_type':True},
                                            color_discrete_sequence=px.colors.colorbrewer.Blues_r)
                    fig.update_layout(mapbox_style="open-street-map")
                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

                    st.plotly_chart(fig,use_container_width=True)

#set up the details for option 'Insight'
if selected == "INSIGHTS":
    select_insight=option_menu('',options=["TOP INSIGHTS","FILTER INSIGHTS"],
                                    icons=["bar-chart", "toggles"],
                                    orientation='horizontal',
                                    styles={"container":{"border":"2px ridge "},
                                    "icon": {"color": "#F8CD47", "font-size": "20px"}})
            
    if select_insight =="TOP INSIGHTS":

        opt=['Top 10 Accommodation with Highest price',
            'Top 10 Accommodation with Lowest price ',
            'Number of Hotels Count by Country',
            'Room Type Distribution by Country',
            'Host with Highest Listing',
            'Top 10 Accommodation with Highest Reviews',
            'Hotels Count by Rating',
            'Average Availability of Stays by Country',
            'Average Accommodation Prices by Country',
            'Property type Distribution by country',]
        
        query=st.selectbox(':red[Select a Query]',options=opt,index=None)

        def stream1():
                for i in t_1:
                    yield i + ''
                    time.sleep(0.02)
        def stream2():
                for i in t_2:
                        yield i + ''
                        time.sleep(0.02)
        def stream3():
                for i in t_3:
                        yield i + ''
                        time.sleep(0.02)
        def stream4():
                for i in t_4:
                        yield i + ''
                        time.sleep(0.02)


        if query==opt[0]:
            col1,col2=st.columns(2)

            with col1:
                df=pd.read_sql_query('''SELECT name,country, MAX(price) as 'price' from hotels_info 
                                        GROUP by name ORDER by max(price) DESC LIMIT 10''',con=engine)
                
                fig=px.bar(df,y='name',x='price',color='name',
                        hover_data=['name','country'],title='Top 10 Accommodation with Highest price',
                        color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)
            
            with col2:
                fig=px.pie(df,names='name',values='price',color='name',
                        title='Percentage of Top 10 Accommodation with Highest price',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                st.markdown('<br>', unsafe_allow_html=True)

                t_1='''🟡 Istanbul, Turkey: "Center of Istanbul Sisli" stands out as the most expensive accommodation with a price of 48,842 Turkish Lira,
                reflecting its prime location in the heart of Istanbul's vibrant Sisli district.'''                                   
                
                t_2='''🟡 Hong Kong: The city boasts several high-priced accommodations, including "HS1-2人大床房+丰泽､苏宁､百脑汇+女人街+美食中心" and 
                "良德街3号温馨住宅" priced at 11,681 Hong Kong Dollars each, suggesting a strong demand for upscale lodging options in this bustling metropolis.'''               
                
                t_3='''🟡 Brazil: Not to be outdone, Brazil features luxurious accommodations like "Apartamento de luxo em Copacabana - 4 quartos" and "Deslumbrante apartamento na AV.Atlantica"
                with prices exceeding 6,000 Brazilian Reais, catering to travelers seeking premium experiences along the country's picturesque coastlines'''
                

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())

        if query==opt[1]:
            col1,col2=st.columns(2)

            with col1:
                df=pd.read_sql_query('''SELECT name,country, min(price) as 'price' from hotels_info 
                                        GROUP by name ORDER by min(price)  LIMIT 10''',con=engine)
                
                fig=px.bar(df,y='name',x='price',color='name',
                        hover_data=['name','country'],title='Top 10 Accommodation with Lowest price',
                        color_continuous_midpoint='Viridis')
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)
            
            with col2:
                fig=px.pie(df,names='name',values='price',color='name',
                        title='Percentage of Top 10 Accommodation with Lowest price',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                st.markdown('<br>', unsafe_allow_html=True)

                t_1='''🟡 Among the top 10 accommodations listed, the most budget-friendly options are found in Portugal and Spain.'''
                
                t_2='''🟡 Portugal offers the most affordable accommodations, with prices ranging from  9 to 13 dollers.'''
                
                t_3='''🟡 Spain also provides reasonably priced options, with room rates starting at 10 and 12 dollers.'''
                
                t_4='''🟡 Notably, Canada appears in the top 10 list with a "Good room" priced at $13, reflecting a competitive pricing compared to European destinations.'''

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

        if query==opt[2]:
            col1,col2=st.columns(2)
            
            with col1:
                df=pd.read_sql_query('''SELECT country,COUNT(name) as 'Hotel Count' FROM hotels_info GROUP BY country
                                    order by COUNT(name) Desc  ''',con=engine)

                fig=px.bar(df,x='country',y='Hotel Count',color='country',
                        hover_name='country',title="Number of Hotels Count by Country",
                        color_discrete_sequence=px.colors.qualitative.Plotly_r)
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)

            with col2:
                fig=px.pie(df,names='country',values='Hotel Count',color='country',
                        title="Number of Hotels by Country in percentage",
                        color_discrete_sequence=px.colors.carto.Purpor_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                t_1='''🟡 The United States dominates the Airbnb market with 1,222 listings, indicating a significant presence of accommodations in the country.'''
                
                t_2='''🟡 Turkey, Canada, and Spain follow closely behind, with 661, 649, and 633 listings respectively, showcasing a strong presence of Airbnb properties in these regions.'''
                
                t_3='''🟡 Australia, Brazil, and Hong Kong also demonstrate substantial Airbnb activity, with 610, 606, and 600 listings respectively, 
                            suggesting a diverse range of accommodation options available to travelers.'''
                
                t_4='''🟡 Portugal and China round out the list with 555 and 19 listings respectively, highlighting varying levels of Airbnb adoption in different regions.'''
                
                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

        if query==opt[3]:
            
                df=pd.read_sql_query('''SELECT country,room_type,count(room_type) as 'count of room type' from rooms_info
                                    JOIN hotels_info on rooms_info.id = hotels_info.id
                                    GROUP by country, room_type''',con=engine)
                
                fig = px.sunburst(df, path=['country', 'room_type'], values='count of room type',
                        title='Room Types by Country', color_continuous_scale='RdBu')
                st.plotly_chart(fig,use_container_width=True)
                

                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True)

                with col2:


                    t_1='''🟡 Entire homes and apartments are the most popular Airbnb listings in the US, 
                        Canada, Portugal, Australia, Hong Kong, and Spain. This suggests travelers in these areas prefer private spaces.'''
                    
                    t_2='''🟡 Some countries, like Canada, Portugal, Australia, Hong Kong, and Spain, also have private rooms for travelers
                        seeking a budget-friendly option with some privacy. Interestingly, Turkey has more private rooms than entire listings'''
                    
                    t_3='''🟡 Shared rooms, where guests share space with the host or others, are the least common option across all countries.
                            This could be due to travelers wanting more privacy or cultural norms.'''
                    
                    t_4='''🟡 China has fewer listings overall, and most are entire homes/apartments.
                    This could be due to regulations or travel patterns specific to China.'''
                    
                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

        if query==opt[4]:
            
                df=pd.read_sql_query('''SELECT host_id,host_name,count(host_id)as 'total listing' FROM host_info
                                        GROUP by host_id,host_name ORDER by COUNT(host_id) desc limit 10''',con=engine)
                
                fig=px.bar(df,x='host_name',y='total listing',color='host_name',
                        hover_name='host_name',title="Host with Highest Listing",
                        color_discrete_sequence=px.colors.diverging.Temps_r)
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True)

                with col2:

                    st.markdown('<br>', unsafe_allow_html=True)

                    t_1='''🟡 Jov leads the pack with an impressive tally of 18 listings, showcasing a significant presence in the accommodation landscape.'''

                    t_2='''🟡 Sonder follows closely with 11 listings, indicating a substantial contribution to the Airbnb platform.'''

                    t_3='''🟡 Alejandro and Eva&Jacques each boast 9 listings, further diversifying the options available to Airbnb guests.'''

                    t_4='''🟡 Feels Like Home, Liiiving, Mark, Marina, Captain Cook Resorts, and Debe round out the top hosts, each offering between 6 to 7 listings,
                            reflecting the rich variety of accommodations available worldwide.'''

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())
                
        if query==opt[5]:
            
                df=pd.read_sql_query('''SELECT name,max(number_of_reviews) as 'Total reviews' FROM reviews_info
                                    JOIN hotels_info on reviews_info.id=hotels_info.id GROUP by hotels_info.id
                                    ORDER by MAX(number_of_reviews) DESC LIMIT 10''',con=engine)
                
                fig=px.bar(df,y='name',x='Total reviews',color='name',
                        hover_name='name',title='Top 10 Accommodation with Highest Reviews',
                        color_discrete_sequence=px.colors.qualitative.Bold_r)
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True)

                with col2:

                    t_1='''🟡 Diverse Accommodation Options: This collection of top-reviewed Airbnb stays showcases a diverse range of accommodation options, 
                    from private studios to spacious apartments, each offering unique experiences and amenities.'''

                    t_2='''🟡 Popular Destinations: Situated in sought-after locations like Waikiki and close to landmarks such as La Sagrada Familia,
                        these accommodations provide convenient access to attractions and transportation.'''

                    t_3='''🟡 Consistent Guest Satisfaction: With numerous positive reviews, these stays consistently deliver exceptional service,
                    cleanliness, and overall guest satisfaction.'''

                    t_4='''🟡 Trusted Choices for Travelers: These Airbnb listings are trusted by travelers for their reliability and positive feedback,
                        making them dependable options for a comfortable and enjoyable stay.'''

                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

        if query==opt[6]:
                
                df=pd.read_sql_query('''SELECT  rating ,count(id) as 'total stays'from reviews_info
                                GROUP by rating order by rating desc ''',con=engine)
                
                fig=px.line(df,x='rating',y='total stays',markers=True,
                        title='Hotels Count by Rating')
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True,use_container_width=True)
                
                with col2:

                    t_1='''🟡 Distribution of Ratings: The majority of Airbnb listings have ratings ranging from 90 to 100, with the highest concentration around the 100 rating mark.'''
                    
                    t_2='''🟡 Highly Rated Listings: A significant number of listings receive ratings of 95 and above, indicating a high level of satisfaction among guests.'''
                    
                    t_3='''🟡 Variety of Ratings: While most listings have high ratings, there is also diversity in ratings across the platform, with some listings receiving ratings below 80.'''
                    
                    t_4='''🟡 Room for Improvement: Despite the overall positive trend, there are opportunities for improvement in some listings, 
                            as reflected in the lower ratings received by a small percentage of accommodations.'''
                    
                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

        if query==opt[7]:
                
                df=pd.read_sql_query('''SELECT country,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)  as 'avg_availability_60',
                                    AVG(availability_365) as 'avg_availability_365' from rooms_info
                                    join hotels_info on rooms_info.id=hotels_info.id GROUP by country ''',con=engine)
                
                fig = px.bar(df, x='country', y=['avg_availability_30', 'avg_availability_60', 'avg_availability_365'],
                            title='Average Availability of Stays by Country',
                            labels={'value': 'Average Availability', 'variable': 'Availability Period', 'country': 'Country'},
                            barmode='group')

                st.plotly_chart(fig,use_container_width=True)
                
                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True)

                with col2:

                    t_1=''' 🟡 For shorter-term stays (30 days), Australia, Canada, Spain, and the United States offer durations ranging from 8 to 10 days on average.'''
                    
                    t_2='''🟡 Brazil, Hong Kong, and Portugal provide moderate availability for stays of 60 days, averaging between 20 and 25 days.'''
                    
                    t_3='''🟡 China leads in availability for longer-term stays (365 days), offering approximately 235 days on average.'''
                    
                    t_4='''🟡 Turkey stands out with the longest availability for both 60 and 365 days, providing around 45 and 256 days, respectively, on average.'''

                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

        if query==opt[8]:
                
                df=pd.read_sql_query('''SELECT country ,AVG(price) as 'Average Price' from hotels_info 
                                    group by country order by AVG(price) desc ''',con=engine)

                fig=px.bar(df,x='country',y='Average Price',color='country',
                        hover_name='country',title='Average Accommodation Prices by Country')

                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True,use_container_width=True)

                with col2:

                    t_1='''🟡 Varied Pricing: Accommodation prices span a wide range, from luxurious in Hong Kong to budget-friendly in Portugal. 
                        This diversity allows travelers to choose options that align with their budget and preferences. '''

                    t_2='''🟡 Value for Money: Turkey and Spain offer affordable stays without compromising quality, making them ideal choices for
                        budget-conscious travelers seeking comfortable accommodations.'''
                    
                    t_3='''🟡 Budget Flexibility: Options cater to every budget, ensuring there's something for everyone across these countries.
                            Whether travelers are looking for upscale experiences or budget-friendly stays, they can find suitable options.'''
                    
                    t_4='''🟡 Tailored Choices: With diverse options available, travelers can easily find accommodations that fit their budget and preferences,
                        guaranteeing a pleasant stay. From cozy guesthouses to modern apartments, there's something for every type of traveler. '''

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

        if query==opt[9]:
            
                df=pd.read_sql_query('''SELECT country,property_type,count(room_type) as 'Property Count' from rooms_info
                                    JOIN hotels_info on rooms_info.id = hotels_info.id
                                    GROUP by country,property_type''',con=engine)
                
                fig = px.sunburst(df, path=['country','property_type'], values='Property Count',
                        title='Property type Distribution by country', color_continuous_scale='RdBu')
                st.plotly_chart(fig,use_container_width=True)
                
                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(df,hide_index=True)

                with col2:


                    t_1='''🟡 The most common property types across these countries are Apartments, reflecting the popularity 
                            of urban living spaces and providing comfortable accommodation options for travelers.'''
                    
                    t_2='''🟡 Other prevalent property types include Houses, Townhouses, and Condominiums, offering diverse choices 
                            for different preferences and travel styles.'''
                    
                    t_3='''🟡 Additionally, unique accommodations such as Lofts, Serviced Apartments, and Boutique Hotels cater to travelers 
                            seeking distinctive and memorable lodging experiences.'''
                    
                    t_4='''🟡 Overall, the availability of a wide range of property types highlights the diversity and richness of accommodation 
                                options in these countries, accommodating various traveler needs and preferences.'''
                    
                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

    if select_insight =="FILTER INSIGHTS":

        Ques=['Property wise Accommodation count and Average price for specific country',
                'Room type wise Accommodation count and Average price for specific country',
                'Average Availability days for specific property and country',
                'Country wise Average price of stays for specific Property and Room type',
                'Average pricing and fees for a speciific country',
                'Cancellation Policy-wise Stays Count for a Specific Country',]
        
        query=st.selectbox(':red[Select a Query]',options=Ques,index=None)

        if query==Ques[0]:

            st.markdown('<br>', unsafe_allow_html=True)
            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            if selected_country:

                df=pd.read_sql_query('''SELECT property_type,avg(price)  as 'Average price',COUNT(property_type) as 'Total Stays' from rooms_info 
                                        join hotels_info on rooms_info.id=hotels_info.id   where country= %s
                                        GROUP by property_type''',con=engine,params=[(selected_country,)])
                
                fig=px.scatter(df,x='property_type',y='Total Stays',color='property_type',
                        labels={'property_type': 'Property Type', 'Total Stays': 'Total Stays'},
                        title=f'Property wise Accommodation count for {selected_country}')
                
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    fig=px.pie(df,names='property_type',values='Average price',color='property_type',
                            title=f'Property wise Average price for {selected_country}',
                            color_discrete_sequence=px.colors.qualitative.Safe)
                    
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.write('**Dataframe**')
                    st.dataframe(df,hide_index=True,use_container_width=True)


        if query==Ques[1]:

            st.markdown('<br>', unsafe_allow_html=True)
            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            if selected_country:

                df=pd.read_sql_query('''SELECT room_type,avg(price)  as 'Average price',COUNT(room_type) as 'Total Stays' from rooms_info 
                                        join hotels_info on rooms_info.id=hotels_info.id   where country= %s
                                        GROUP by room_type''',con=engine,params=[(selected_country,)])
                
                fig=px.bar(df,x='room_type',y='Total Stays',color='room_type',
                        labels={'room_type': 'Room Type', 'Total Stays': 'Total Stays'},
                        title=f'Room Type wise Accommodation count for {selected_country}',barmode='group')
                
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    fig=px.pie(df,names='room_type',values='Average price',color='room_type',
                            title=f'Room Type wise Average price for {selected_country}',
                            color_discrete_sequence=px.colors.qualitative.Safe)
                    
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.write('**Dataframe**')
                    st.dataframe(df,hide_index=True,use_container_width=True)
            
        if query==Ques[2]:

            st.markdown('<br>', unsafe_allow_html=True)

            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
            selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

            if selected_prop:

                df=pd.read_sql_query('''SELECT country,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)  as 'avg_availability_60',
                                        AVG(availability_365) as 'avg_availability_365' from rooms_info
                                        join hotels_info on rooms_info.id=hotels_info.id 
                                        where country =%s AND property_type=%s ''',con=engine,params=[(selected_country,selected_prop)])
                    
                fig = px.bar(df, x='country', y=['avg_availability_30', 'avg_availability_60', 'avg_availability_365'],
                                title=f'Average Availability days for {selected_prop} in {selected_country}',
                                labels={'value': 'Average Availability', 'variable': 'Period'},
                                barmode='group')
                st.plotly_chart(fig,use_container_width=True)

                st.write('**Dataframe**')
                st.dataframe(df,hide_index=True,use_container_width=True)

        if query==Ques[3]:
            st.markdown('<br>', unsafe_allow_html=True)

            df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info ''',con=engine)
            selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

            df_room=pd.read_sql_query('''SELECT DISTINCT room_type from rooms_info 
                                        where property_type=%s ''',engine,params=[(selected_prop,)])
            selected_room=st.radio('select a Room type',options=df_room['room_type'].tolist(),index=None)

            if selected_room:

                df=pd.read_sql_query('''SELECT country, AVG(price) as 'average price' FROM hotels_info 
                                        JOIN rooms_info ON hotels_info.id = rooms_info.id 
                                        WHERE rooms_info.property_type =%s and rooms_info.room_type=%s
                                        GROUP BY country;''',con=engine,params=[(selected_prop,selected_room)])
                
                fig = px.bar(df, x='country', y='average price',color='country',
                                title=f'country wise Average price of stay for {selected_prop} and {selected_room}',
                                labels={'country': 'country', 'average price': 'average price'},
                                color_discrete_sequence=px.colors.qualitative.Bold_r)
                
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True,use_container_width=True)

        if query==Ques[4]:
                st.markdown('<br>', unsafe_allow_html=True)
                
                df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
                selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

                if selected_country:
                    chek=st.checkbox(f"Click to view pricing details by property type in {selected_country}.")

                    if not chek:

                        df=pd.read_sql_query('''SELECT country,AVG(weekly_price) as 'avg Weekly price',AVG(monthly_price)  as 'avg Monthly price',
                                            AVG(security_deposit) as 'avg security deposit', AVG(cleaning_fee) as 'avg cleaning price'
                                            from hotels_info  where country=%s GROUP by country ''',con=engine,params=[(selected_country,)])
                        
                        fig = px.bar(df, x='country', y=['avg Weekly price', 'avg Monthly price', 'avg security deposit','avg cleaning price'],
                                    title=f'Average Pricing and Fees of stays in {selected_country} ',
                                    labels={'value':'Average pricing', 'variable':'cataogory' },
                                    barmode='group')
                        
                        st.plotly_chart(fig,use_container_width=True)

                    if chek:

                        df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
                        selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

                        if selected_prop:

                            df=pd.read_sql_query('''SELECT country,AVG(weekly_price) as 'avg Weekly price',AVG(monthly_price)  as 'avg Monthly price',
                                                    AVG(security_deposit) as 'avg security deposit', AVG(cleaning_fee) as 'avg cleaning price'
                                                    from hotels_info  join rooms_info on hotels_info.id=rooms_info.id
                                                    where country=%s and property_type=%s GROUP by country''',con=engine,params=[(selected_country,selected_prop)])
                            
                            fig = px.bar(df, x='country', y=['avg Weekly price', 'avg Monthly price', 'avg security deposit', 'avg cleaning price'], 
                                        title=f'Average Price & Fees in {selected_country} - property type : {selected_prop}',
                                        labels={'value':'Average pricing', 'variable':'cataogory' },
                                        color_discrete_sequence=px.colors.qualitative.D3_r,
                                        barmode='group')
                            
                            st.plotly_chart(fig,use_container_width=True)

        if query==Ques[5]:
            st.markdown('<br>', unsafe_allow_html=True)
                
            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            if selected_country:
                    chek=st.checkbox(f"Click to view property wise count of stays for {selected_country} ")

                    if not chek:

                        df=pd.read_sql_query('''SELECT cancellation_policy, COUNT(*) AS 'Stays Count' FROM hotels_info
                                JOIN rooms_info ON hotels_info.id = rooms_info.id
                                WHERE country = %s GROUP BY cancellation_policy''',con=engine,params=[(selected_country,)])
                        
                        fig = px.bar(df, x='cancellation_policy', y='Stays Count', color='cancellation_policy',
                                    title=f'Cancellation Policy-wise Stays Count for {selected_country}',
                                    labels={'cancellation_policy': 'Cancellation Policy', 'Stays Count': 'Stays Count'})
                        
                        st.plotly_chart(fig,use_container_width=True)

                    if chek:

                        df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
                        selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

                        if selected_prop:

                            df=pd.read_sql_query('''SELECT country, cancellation_policy, COUNT(*) AS 'Stays Count' FROM hotels_info
                                JOIN rooms_info ON hotels_info.id = rooms_info.id
                                WHERE country =%s and  property_type=%s
                                GROUP BY country, cancellation_policy''',con=engine,params=[(selected_country,selected_prop)])
                            
                            fig = px.pie(df, values='Stays Count', names='cancellation_policy',hole=0.3,
                                    title=f'Cancellation Policy-wise Stays Count for {selected_prop} in {selected_country}',
                                    labels={'Stays Count': 'Stays Count', 'cancellation_policy': 'Cancellation Policy'})
                            
                            st.plotly_chart(fig,use_container_width=True)

#set up the details for option 'About'
if selected=="ABOUT":
        st.subheader(':red[What is Airbnb ?]')
        st.markdown('''Airbnb is a popular online marketplace that connects people who want to rent out their properties with travelers seeking accommodations.
                    It allows individuals to rent out their homes, apartments, rooms, or other lodging accommodations to guests. Airbnb offers a wide range of accommodation
                    options in various locations around the world, providing travelers with unique and personalized experiences while offering hosts an opportunity 
                    to earn income from their properties.''')
        st.subheader(':red[History :]')
        st.markdown('''History of Airbnb In 2008, Brian Chesky (the current CEO), Nathan Blecharczyk, and Joe Gebbia, established the company now known as Airbnb.
                    The idea blossomed after two of the founders started renting air mattresses in their San Francisco home to conference visitors. Hence, the original name of Airbed & Breakfast.         
                    In 2009, the name Airbnb was introduced and its offerings grew beyond air mattresses to include spare rooms, apartments, entire houses, and more. 
                    The locations in which it operated grew, as well. By 2011, Airbnb had opened an office in Germany and in 2013, it established a European headquarters in Dublin, Ireland. 
                    Its primary corporate location is still San Francisco.''')
        
        st.subheader(':red[Pricing :]')
        st.markdown('''The total amount that guests pay for a room or other space on Airbnb includes the host's price plus Airbnb's guest service fee (a maximum of 14.2%).
                    Hosts pay Airbnb a fee of approximately 3%''')
        
        st.link_button('AIRBNB WEBSITE',url='https://www.airbnb.co.in/')

        st.subheader(':red[FAQ]')

        with st.expander('**Who is CEO of Airbnb?**'):
            st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQms4guS1SX_UTgYEEwbCWy9HQutO7HUGmr8cUwVdXsBw&s',width=100)
            st.write('''Brian Chesky is the co-founder and Chief Executive Officer of Airbnb and sets the vision and strategy for the company.''')
                

        with st.expander('**Is Airbnb legal in India?**'):
            st.write('''Yes, Airbnb is legal in India as long as you have all the required licenses and permissions to start one.
                    In India, there are several legal registrations required before hosting on Airbnb. Firstly, you must register your property with the local
                    municipality and obtain a valid license to operate as an accommodation provider.''')
            
        with st.expander('**What is the full meaning of Airbnb?**'):
            st.write('''Airbnb, as in “**Air Bed and Breakfast,**” is a service that lets property owners rent out their spaces to travelers looking for a place to stay.
                    Travelers can rent a space for multiple people to share, a shared space with private rooms, or the entire property for themselves.''')
            
        with st.expander('**How is Airbnb different from hotels?**'):
            st.write('''In general, Airbnb is cheaper than hotels because Airbnb does not have to pay for the overhead costs of a hotel or the general management of such a large operation.''')

        with st.expander('**What type of hotel is Airbnb?**'):
            st.write('''an Airbnb can be anything from a hotel, to a quaint B&B, to a treehouse, to a tent, to an igloo, to a church, the list goes on… What makes 
                    an Airbnb property popular with guests is how special and unique it is able to be, and this doesn't have to rely solely on the architecture (or lack thereof)''')
            
        
        
        st.subheader(':red[More About Airbnb]')

        col1,col2=st.columns(2)
        with col1:
                st.video('https://www.youtube.com/watch?v=dA2F0qScxrI&list=PLe_YVMnS1oXZb4zCNsh_fRqXh5kgx21V_')
        with col2:
                st.video('https://www.youtube.com/watch?v=I4MCFPG0MZg&list=PLe_YVMnS1oXZb4zCNsh_fRqXh5kgx21V_&index=4')
