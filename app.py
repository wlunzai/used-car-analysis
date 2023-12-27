import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

def set_transparent(ax, fig):
    """
    Set Plot background to transparent
    """
    ax.patch.set_alpha(0.0)
    fig.patch.set_alpha(0.0)

    return ax, fig

def main():

    # Prep Data
    # Get dataframe from provided csv file
    df = pd.read_csv('data/used_car.csv')

    # Set mapping for Categorial data
    # Mapping for location
    location_dict = {
        "Bandung": 1,
        "Bekasi": 2,
        "Bogor": 3,
        "Depok": 4,
        "Jakarta Barat": 5, 
        "Jakarta Pusat": 6,
        "Jakarta Selatan": 7, 
        "Jakarta Timur": 8,
        "Jakarta Utara": 9,
        "Malang": 10, 
        "Surabaya": 11, 
        "Tangerang Selatan": 12,
        "Unknown": 13
    }

    # Mapping for Transmision
    transmission_dict = {
        "Manual": 0, 
        "Automatic": 1
    }

    df['total_feature'] = df.iloc[:, 7:-3].sum(axis=1)
    df['car_age'] = 2023 - df['year']
    df['location_map'] = df['location'].map(location_dict)
    df['transmission_map'] = df['transmission'].map(transmission_dict)
    df['engine_cc'] = df['car name'].str.split(' ').str[-1].astype(float)

    # Get summary of car listings by brand
    brand_count = df.groupby(by='brand').size()

    # Get the top 5 brands with most car listings
    brand_count = brand_count.sort_values(ascending=False).head(5)
    brand_count = brand_count.sort_values(ascending=True)

    # Streamlit Webapp
    # Set streamlit page configuration and main title
    st.set_page_config(page_title="Used Car Listing Analysis", page_icon="🚗",  layout="centered")
    st.title("Used Car Listing Analysis")

    # Introduction header
    st.header("Introduction")
    st.markdown("A dataset containing information on various used car listings in Indonesia was provided. The purpose of this analysis is to identify the most preferred brand in used car listings and the main attributes that contribute to listing price. ")
    st.markdown("---")

    # Section 1 - Most Popular Brand and their Price Range
    st.subheader("Which Car Brand Dominated the Used Car Market?")

    describe_data_by_brand = """
            The dataset can be grouped by car brand, resulting **13** different car brands, which are BMW, Chevrolet, Daihatsu, Datsun, Ford, Honda, Hyundai, Mazda, Mitsubishi, Missan, Suzuki, Toyota and Wuling.

            An analysis was done to investigate the number of used car listings by car brand.
        """

    st.markdown(describe_data_by_brand)
    st.markdown("")

    
    # Format plot size
    width1 = 0.4
    fig1, ax1 = plt.subplots(figsize=(7,2))
    brand_count.plot(
        kind='barh', 
        legend=False, 
        y=brand_count.index, 
        x = brand_count.values, 
        ax=ax1, 
        width=width1, 
        color='darkviolet'
        )

    # Hide border and ticks in the plot
    for spine in ax1.spines.values():
        spine.set_visible(False)

    ax1.set_ylabel('')
    ax1.tick_params(bottom=False, left=False, labelbottom=False)
    ax1.tick_params(axis='y', labelsize='small', colors='white')

    # Set Background to transparent
    ax1, fig1 = set_transparent(ax1, fig1)

    # Get data value label for each bar
    vmax = brand_count.values.max()
    for i, value in enumerate(brand_count):
        ax1.text(value+vmax*0.02, i, f'{value:,}', fontsize='small', va='center', color='white')

    # Display plot
    st.pyplot(fig1)

    brand_barchart_describe = """
        Chart above shows the top 5 used car brands based on the listings.
        - The top 5 car brands that dominated the Used Car Market has accounted for **523** listings, representing more than :blue[**85%**] of the total listings. 
        - Toyota dominated the used car listings for Indonesia, with **171** listings, accounting for :blue[**28%**] of the total listings.
    """
    # Display indent for point form
    st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            padding-left:40px;
        }
        </style>
    ''', unsafe_allow_html=True)
    st.markdown(brand_barchart_describe)
    st.markdown("---")

    # Section 2 - Factors that contribute to the price listing
    st.subheader("What Affects the Listing Price?")
    listing_describe = """
        The dataset also consists of attributes and features available in each used car listing with their listing price in Rupiah (Rp). Following are a list of attributes and features available for each listing:
        - Year of the car manufactured
        - Mileage (KM) traveled by the car
        - Location where car are listed for sale
        - Car Transmission type (Automatic or Manual)
        - Car License plate type (even plate or odd plate)
        - Rear Camera (Yes or No)
        - Sun Roof (Yes or No)
        - Auto Retract Mirror (Yes or No)
        - Electric Parking Brake (Yes or No)
        - Map Navigator (Yes or No)
        - Vehicle Stability Control (Yes or No)
        - Keyless Push Start (Yes or No)
        - Sports Mode (Yes or No)
        - 360 Camera View (Yes or No)
        - Power Sliding Door (Yes or No)
        - Auto Cruise Control (Yes or No)

        On top of the provided attributes and features column, we are able to obtain the engine size of each used car listing in cubic centrimetres (cc) based on the provided car name. Taking example of a used car listing with car name Toyota YARIS S TRD 1.5, the engine cc for the car is 1.5.

        As such, we are able to add one more car attributes to the above list:
        - Engine CC

        As some of the used car has multiple features, another attributes on total feature available on the car was added into the analysis as well.

        With the list of features determined, pairplots between different attributes and features against the used car listing price were plotted to study the relationship between them. 
    """
    st.markdown(listing_describe)

    # Pair Plot chart Settings
    marker_color = {'color':'darkorange'}

    sns.set(
        rc=
        {
            'figure.figsize':(4,2),
            'axes.facecolor':(0,0,0,0), 
            'figure.facecolor':(0,0,0,0), 
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'axes.grid': False
            }
            )
    

    # Create pair plot to see the relationship between each attributes/features to the used car listing price
    pp1 = sns.pairplot(
        data=df,
        y_vars=['price (Rp)'],
        x_vars=['car_age', 'mileage (km)', 'engine_cc', 'transmission', 'location_map'],
        plot_kws=marker_color
    )

    pp2 = sns.pairplot(
        data=df,
        y_vars=['price (Rp)'],
        x_vars=['plate type', 'rear camera', 'sun roof', 'auto retract mirror'],
        plot_kws=marker_color
    )

    pp3 = sns.pairplot(
        data=df,
        y_vars=['price (Rp)'],
        x_vars=['electric parking brake', 'map navigator', 'vehicle stability control','keyless push start'],
        plot_kws=marker_color
    )

    pp4 = sns.pairplot(
        data=df,
        y_vars=['price (Rp)'],
        x_vars=[ 'sports mode', '360 camera view', 'power sliding door', 'auto cruise control', 'total_feature'],
        plot_kws=marker_color
    )

    for pairplot in [pp1, pp2, pp3, pp4]:
        st.pyplot(pairplot)

    pairplot_describe = """
        From the charts, we can see that the attributes and features that has significant impact on its listing price are :red[**Year of Car Manufactured, Engine CC, Car Transmission Type, Sun Roof, Electric Parking Brake, Map Navigator, 360 Camera View and Auto Cruise Control**].

        A further analysis is performed to understand the level of impact for each element on the listing price.
    """
    st.markdown(pairplot_describe)

    # Perform Ordinary Least Squares Regression on main contributors
    y = df['price (Rp)']
    x = df[['car_age', 'engine_cc', 'transmission_map', 'sun roof', 'electric parking brake', 'map navigator', '360 camera view', 'auto cruise control']]
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()

    # Extract the coefficients from the model
    coef = model.params[1:]
    
    # Plot a horizontal bar chart based on the coefficient value
    fig2 = plt.figure()
    ax2 = plt.axes()

    coef.plot(
        kind='barh', 
        legend=False, 
        y=coef.index, 
        x=coef.values, 
        ax=ax2,
        width=width1, 
        color='firebrick'
        )
    
    # Hide plot label and lines
    for spine in ax2.spines.values():
        spine.set_visible(False)

    ax2.set_ylabel('')
    ax2.set_xlabel('')

    # Set plot label size
    ax2.tick_params(bottom=False, left=False)
    ax2.tick_params(axis='y', labelsize='xx-small', colors='white')
    ax2.tick_params(axis='x', labelsize='xx-small', colors='white')
    ax2.xaxis.offsetText.set_fontsize('xx-small')
    
    # Set Background to transparent
    ax2, fig2 = set_transparent(ax2, fig2)
    st.pyplot(fig2)

    impact_description = """
        Odinary Least Squares (OLS) Regression was performed to investigate the impact of the selected attributes and features on the used car listing price. From the graph, it shows that the top 5 attributes or features that will lead to higher used car price are:
        - Engine CC
        - Map Navigator
        - 360 Camera View
        - Electric Parking Brake
        - Car Transmission Type

        in which, Engine CC is the main attribute the determine the used car lisiting price in Indonesia.
    """
    st.markdown(impact_description)
    st.markdown("---")

    # Recommendation
    st.subheader("Recommendation")
    recommendation_describe= """
        With this study, we have gained insights on the significance of each attributes and features on the used car pricing. A recommendation of feature for future car price listing is to create a machine learning model that can suggest used car price for the sellers based on the car attributes and available features.
    """
    st.markdown(recommendation_describe)
    st.markdown("---")

    # Summary
    st.subheader("Summary")
    summary_describe = """
        An analysis was performed on 609 used car lisitngs in Indonesia. The most dominated car brand in used car listing is Toyota and the main driver for impacting the car price is Engine CC of the car.
    """
    st.markdown(summary_describe)

if __name__ == "__main__":
    main()