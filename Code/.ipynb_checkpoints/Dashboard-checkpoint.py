import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from PIL import Image

# Load data
data = pd.read_csv("OutputData/final.csv")
data["Date"] = pd.to_datetime(data['Date'])
event_date = pd.read_csv("InputData/MajorEvents.csv")
event_date['Date'] = pd.to_datetime(event_date['Date']) # convert Date column to datetime format
ret_diffs = pd.read_csv("OutputData/RetDiff.csv")
ret_diffs["Date"] = pd.to_datetime(ret_diffs['Date'])
img = Image.open('pics/Garganta.png')

# Title the dashboard
"""
# Company Returns Over 20 Years Based on 10k Changes
"""

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Report"])

    if page == "Home":any
        
        ## Added code inside
        # Create a sidebar with a dropdown menu
        # Create a sidebar with a dropdown menu
        options1 = ['Metal', 'Energy', 'Semiconductor', "Transport", "Food"]
        all_option1 = 'All of Them'
        if st.sidebar.checkbox('Select all industries', False):
            option1 = [all_option1]
        else:
            option1 = st.sidebar.multiselect('Which company do you want to visualize?', options1)

        # Highlight event date
        option2 = st.sidebar.selectbox(
            'Which event do you want to visualize?',
             event_date['Event'].unique())
        
        st.sidebar.markdown("[To see the code which produces the visualizations please visit the project repo](https://github.com/jum223/FrontToBack)")

        # Filter data based on selected options
        if all_option1 in option1:
            data_filtered = data.copy()
        else:
            data_filtered = data.query("Industry in @option1")
            
        sns.set_style("whitegrid", {'axes.grid': True, 'grid.color': '.8', 'grid.linestyle': '-'})

        # Create plot
        if option1 or (all_option1 in option1):
            fig, ax = plt.subplots()
            if all_option1 in option1:
                for ind in data_filtered["Industry"].unique():
                    industry_df = data_filtered[data_filtered['Industry'] == ind]
                    sns.lineplot(x='Date', y='Cum_ret', data=industry_df, label=ind, ax=ax, ci=None)
            else:
                for col in option1:
                    industry_df = data_filtered[data_filtered['Industry'] == col]
                    sns.lineplot(x='Date', y='Cum_ret', data=industry_df, label=col, ax=ax, ci=None)


            date = event_date.loc[event_date['Event'] == option2, 'Date'].iloc[0]

            plt.axvline(date, color='red', linestyle='--', label='Event Date')

            plt.xlim(date - pd.Timedelta(days=20), date + pd.Timedelta(days=20))

            # set x-axis ticks
            xticks = [date - pd.Timedelta(days=20), date, date + pd.Timedelta(days = 3),date + pd.Timedelta(days = 10), date + pd.Timedelta(days=20)]
            xticklabels = ['t-20', date.strftime('%Y-%m-%d'), "t+3", "t+10", 't+20']
            plt.xticks(xticks, xticklabels)
            plt.xticks(rotation=45)
            sns.despine(right=True, top=True, bottom = True, left = True)

            # add title and axis labels
            plt.title('Cumulative Returns by Industry')
            plt.xlabel('Date')
            plt.ylabel('Cumulative Return')

            # move the legend to the bottom right corner
            plt.legend(loc='upper left')

            ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
            #ax.set_axis_off()


            # show the plot
            st.pyplot(fig)

        else:
            """
            #### Industry Returns around major events in the armed conflict
            """
            st.image(img, caption='Ukrainian Soldiers')

        if all_option1 in option1:
            industries = ret_diffs['Industry'].unique()
        else:
            industries = option1

        # Divide the page into equal-sized columns
        col1, col2, col3 = st.columns(3)

        if option1:
            if all_option1 in option1:
                for i, industry in enumerate(industries):
                    industry_returns_filtered = ret_diffs[(ret_diffs['Industry'] == industry) & (ret_diffs['Date'] == date)]
                    box_content = []
                    for _, row in industry_returns_filtered.iterrows():
                        ret3_value = row['ret3'] * 100
                        ret3_color = 'red' if ret3_value < 0 else 'green'
                        ret3_str = f"{ret3_value:.2f}%"
                        ret3_display = f"% difference t+3: <span style='color:{ret3_color};'>{ret3_str}</span>"
                        box_content.append(ret3_display)
                        ret10_value = row['ret10'] * 100
                        ret10_color = 'red' if ret10_value < 0 else 'green'
                        ret10_str = f"{ret10_value:.2f}%"
                        ret10_display = f"% difference t+10: <span style='color:{ret10_color};'>{ret10_str}</span>"
                        box_content.append(ret10_display)
                    # Display the box in the appropriate column
                    if i % 3 == 0:
                        box_column = col1
                    elif i % 3 == 1:
                        box_column = col2
                    else:
                        box_column = col3
                    with box_column:
                        st.subheader(industry + ' Returns')
                        st.markdown("<br>".join(box_content), unsafe_allow_html=True)

            else:
                for i, industry in enumerate(industries):
                    industry_returns_filtered = ret_diffs[(ret_diffs['Industry'] == industry) & (ret_diffs['Date'] == date)]
                    box_content = []
                    for _, row in industry_returns_filtered.iterrows():
                        ret3_value = row['ret3'] * 100
                        ret3_color = 'red' if ret3_value < 0 else 'green'
                        ret3_str = f"{ret3_value:.2f}%"
                        ret3_display = f"% difference t+3: <span style='color:{ret3_color};'>{ret3_str}</span>"
                        box_content.append(ret3_display)
                        ret10_value = row['ret10'] * 100
                        ret10_color = 'red' if ret10_value < 0 else 'green'
                        ret10_str = f"{ret10_value:.2f}%"
                        ret10_display = f"% difference t+10: <span style='color:{ret10_color};'>{ret10_str}</span>"
                        box_content.append(ret10_display)

                    if i % 3 == 0:
                        box_column = col1
                    elif i % 3 == 1:
                        box_column = col2
                    else:
                        box_column = col3
                    with box_column:
                        st.subheader(industry + ' Returns')
                        st.markdown("<br>".join(box_content), unsafe_allow_html=True)
                        
                # Adding Event Descriptions
        if option1 or (all_option1 in option1):
            if option2 == "Invasion Announcement":
                """
                ## Invasion Announcement:
                ##### Febuary 24, 2022
                """
                "In the early hours of February 24, Russian President Vladimir Putin ordered his troops into Ukraine. Kyiv’s Western allies had been warning of looming Russian aggression for months. Still, Putin’s decision came as a shock to many in Ukraine and across the world. Speaking on Russian state television, he announced the launch of what he called a “special military operation” to “demilitarize” and “denazifiy” Ukraine. Moments later, the first explosions were heard across Ukraine."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "Following Russia’s invasion of Ukraine, the percentage change in returns after 3 days seemed relatively positive with Food, Transport, Energy, and Metal industries experiencing a growth between 0.57% and 4.65%. The longer term returns, 10 days after the event, showed energy and metal percent returns changes increasing to 17.83% and 12.79% respectively. The food returns also increased to 2.16%, while the semiconductors and transport returns experienced marginal decreases. Looking ahead at 20 days after the event, energy and metal industries experienced a sharp decline in returns, while the remaining industries leveled out."
            elif option2 == "Ukraine announces it will defend its territory":
                """
                ## Ukraine announces it will defend its territory: 
                ##### Febuary 25, 2022
                """
                "Amid the chaos of the opening hours of the war, rumors started to swirl about Ukraine’s leadership fleeing the country. Ukrainian President Volodymyr Zelensky and his team reacted by filming a video of themselves in central Kyiv, reassuring the nation. “We are all here defending our independence, our state and it will remain so. Glory to our defenders! Glory to our women defenders! Glory to Ukraine!” Zelensky said. The president had refused a US offer to evacuate, according to the Ukrainian government, saying: “I need ammunition, not a ride.“"
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "One day after Russia announced their invasion, Ukraine announced that they will defend their territory and fight for their country. As this news comes only one day after the invasion announcement, industry returns for the metal, energy, transportation, food, and semiconductor do not change drastically enough to make a new supportive analysis statement."
            elif option2 == "Refugee Crisis in Poland": 
                """
                ## Refugee Crisis in Poland:
                ##### March 2, 2022
                """
                "The brutality of Russia’s invasion forced hundreds of thousands of Ukrainian civilians to flee the country. The United Nations’ refugee agency (UNHCR) said that at least 100,000 people had left their homes in the first 24 hours of the military assault. Thousands of cars formed queues at the borders, with people waiting several days to cross into neighboring Poland. Many others fled by train, waiting at train stations for days to cram into overcrowded carriages. The majority were women, children and the elderly, as men of fighting age were largely prohibited from leaving the country."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "As the refugee crisis in Poland grows as hundreds of thousands are forced from their homes, the following occurred to each of the industry sectors. Within the first 3 days, energy, metal, and food industries experienced a percentage change of 7.54%, 3.69%, and 1.28% respectively. The longer term returns, 10 days after the event showed a split between the energy and metal industries who were experiencing growth while food, transport, and semiconductors experienced a percentage change of -2.07%, -0.41%, and -4.7% respectively."
            elif option2 == "Irpin Bridge Evacuation":
                """
                ## Irpin Bridge Evacuation
                ##### March 6, 2022
                """
                "As Russian troops began to approach Kyiv, people living in the northwestern suburbs of the capital got caught up in some of the heaviest street-by-street fighting of the war so far. The main bridge crossing the Irpin River was destroyed by Ukrainians to thwart a Russian advance, which made evacuations difficult. According to the Ukrainian authorities, hundreds of civilians died attempting to flee."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "Following the Irpin Bridge Evacuation, all industries experienced slight decreases in their percentage change except for transportation and semiconductors who experienced percentage change growths of 2.12% and 3.91% respectively. When looking at day 10 after the event, the energy, metal, and food industries experienced percentage changes of -9.5%, -0.53%, and -5.6% respectively. This comes as a shock as energy and metal industry returns remained vigilant throughout the start of the war but have since been declining. Meanwhile, the transportation and semiconductors experienced percentage changes of 6.16% and 3.91% respectively over the same period."
            elif option2 == "Mariupol Hospital Attack":
                """
                ## Mariupol Hospital Attack
                ##### March 9, 2022
                """
                "A maternity hospital in the southeastern city of Mariupol was hit by a Russian missile. The attack came despite Russia agreeing to a 12-hour pause in hostilities to allow refugees to evacuate. A photo of a pregnant woman injured in the bombing being carried on a stretcher outside the devastated hospital became emblematic of Russia’s senseless aggression against its neighbor."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "The percentage change in returns 3 days after the Mariupol Hospital attack revealed increases to both the transport, energy, and metal industries, with returns of 1.03%, 1.34%, and 3.92% respectively. Looking at the 10 day period after the event, energy returns dropped -5.74% and food with -3.91%, while transport, semiconductors, and metal industries experienced percentage changes of 2.6%, 0.78%, and 2.3% respectively. Looking at returns 20 days after the event, shows both energy and metal industries now overlapping with semiconductor returns."
            elif option2 == "Mariupol Theater Bombing":
                """
                ## Mariupol Theater Bombing
                ##### March 16, 2022
                """
                "The bombing of Mariupol’s Drama Theater was among the most brazen of Russia’s attacks on civilians. Ukrainian officials estimated 1,300 people were sheltering in the theater in the centre of a city which had, at that point, been under siege for weeks. Around 300 died that day, authorities said at the time, but subsequent reports suggested the death toll could be higher. Russia, which had been bombarding the city for weeks, denied its forces were responsible."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "Only a week after the Mariupol Hospital attack, the Mariupol Theater was bombed which resulted in negative percentage changes for only the food and transportation industries. Meanwhile energy, metal, and semiconductor industries experienced positive percentage changes of 3.59%, 1.24% and 0.90% respectively. At this point when looking at the graph, it can be seen that the energy and metal industries have percent changes that follow one another as they have similar graphs over the time period. Looking at 10 days after the event, energy, metal, and semiconductors experienced percent changes in returns of 10.57%, 5.56% and 1.76% respectively."
            elif option2 == "War crimes uncovered":
                """
                ## War crimes uncovered
                ##### April 1, 2022
                """
                "When Russian troops withdrew from Bucha in early April, they left behind a trail of destruction — and evidence of summary executions, brutality and indiscriminate shelling. Images showing dozens of bodies of civilians scattered around a single street in Bucha prompted calls for Russia to be investigated for war crimes. Russia made baseless claims that the images were fake and has prosecuted several Russian journalists and dissidents who spoke up about the killings for spreading “false information” about the war. International experts from the Organization for Security and Cooperation in Europe said they found “grave breaches” of international humanitarian law by Russian forces."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "The percentage change in returns 3 days after the war crimes were uncovered resulted in negative returns for most industries except the semiconductor industry, which had returns increase by 0.67%, while the rest ranged from -0.57% to -1.32%. The longer term returns, 10 days after the event showed a split between industries. The food, energy and metal industries all had positive returns, 4.65%, 1.22% and 1.22% respectively. The transport and semiconductor industries had major decreases in returns, -4.83% and -9.38% respectively."
            elif option2 == "Sunking of Russian main ship":
                """
                ## Sunking of Russian main ship
                ##### April 14, 2022
                """
                "Moskva, the flagship of Russia’s Black Sea fleet, sank on April 14. The cause remains disputed. Ukraine said it hit the Moskva with anti-ship cruise missiles, sparking a fire that detonated stored ammunition. Russia blamed a fire of unknown origin. Whatever the reason, the loss of the guided-missile cruiser was a major military embarrassment for Russia and its biggest wartime loss of a naval ship in 40 years."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "3 days after the sinking of the Russian flagship, most industries were on level with their reaction to this event, returns ranged between -0.66% and 1.25%, worst and best of being the food and energy industries respectively. 10 days after the event returns ranged from -7.03% and 4.31%, both extremes being that of the energy and transport industries."
            elif option2 == "Mariupol Steel Plant Defence":
                """
                ## Mariupol Steel Plant Defence
                ##### May 17, 2022
                """
                "The sprawling Azovstal steel plant in Mariupol became another symbol of Ukrainian resistance in the face of a much larger enemy. Defenders of the plant withstood weeks of relentless Russian bombardment before finally surrendering in May. Ukrainian officials praised the fighters, saying their fierce defense of the complex had stalled Russian forces and prevented the capture of Zaporizhzhia, further west."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "3 days after the successful defense by Ukrainian troops at the Mariupol Steel Plant, stock returns varied from -1.79% through 1.71%, the transportation having the lowest and the energy industry with the highest returns. 10 days after the event, returns varied significantly between industries. The food industry had the lowest returns with a -3.11% and the energy industry had the highest returns, with 7.27%."
            elif option2 == "Russian retreat from Kharkiv":
                """
                ## Russian retreat from Kharkiv
                ##### September 1, 2022
                """
                "A blistering Ukrainian counteroffensive in eastern Ukraine in September recaptured large swaths of territory and forced Russian troops to flee the Kharkiv region. Moscow tried to spin the hasty withdrawal as “regrouping.” But in a sign of just how badly things were going for Russia, the military was publicly criticized by a number of high-profile Kremlin loyalists including Chechen leader Ramzan Kadyrov, who supplied thousands of fighters to the offensive."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "3 days after the Russian retreat from Kharkiv, returns varied slightly for most firms. The food industry had returns -0.41%, thus being the lowest and the highest was the energy industry with 3.84%. 10 days after the event, the food industry had the lowest returns with -3.40%, and the highest was the metal industry, with 2.58%."
            elif option2 == "Russia starts mobilization":
                """
                ## Russia starts mobilization
                ##### September 21, 2022
                """
                "Following a string of embarrassing defeats in Ukraine, Putin announced Russia’s first mobilization since World War II on September 21. The controversial draft sparked protests — a rare sight in Russia — and an exodus of men of fighting age from the country. The partial mobilization was beset by errors and produced fighters that were poorly equipped and largely untrained. However, it significantly increased Russia’s troop numbers."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "3 days after Russia started its mobilization effort, all the industries acted differently to this event. The energy industry had the lowest returns, of -7.10%, while the food industry had the highest returns with 0.87%. 10 days after the event, returns were split between all industries. The industries with positive returns were the food and energy industries, 0.84% and 1.10% respectively. The metal, transportation, and semiconductor industries all had decreasing returns, -0.11%, -1.03%, and -1.26% respectively."
            elif option2 == "Crimea Bridge Attack":
                """
                ## Crimea Bridge Attack
                ##### October 8, 2022
                """
                "In another major blow to Moscow, the only bridge connecting Russia with the Crimean Peninsula was severely damaged by an explosion. The Kerch Strait road-and-rail bridge is both strategically important and hugely symbolic. It was opened by Putin in 2018, four years after Russia illegally annexed Crimea from Ukraine."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "Most industries’ return differences from the date of the event to the given time frames seem to oscillate around a certain range of percentage differences, suggesting that this event didn’t have much significance on the operations or supply chains of the businesses in these industries. Nevertheless, the semiconductor industry did observe a decrease in returns, 3 days after such an event returns decreased by 3.08%, and 10 days after the event industry returns decreased even further to 6.6% approximately. The reason for this could be that the attack on the bridge supposed a greater threat to the supply of food products than any other industry."
            elif option2 == "Kyiv Blackout":
                """
                ## Kyiv Blackout
                ##### October 10, 2022
                """
                "A new phase of the war began when Russia launched the first of several waves of missile strikes on Ukraine’s critical energy infrastructure. Using missiles, artillery shells and Iranian-made drones, Moscow began targeting Ukrainian power facilities, leaving large areas of the country without power and water."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "From this visualization, it is notable to see how the energy industry saw a steady increase in returns post Kyiv blackout. This event involved several waves of missile strikes on Ukraine’s critical energy infrastructure, so it is not surprising to see this trend. After the event, Ukraine probably demanded a greater supply of energy in the form of oil or natural gas from its allied counterparts leading to increased returns in the energy industry as a consequence"
            elif option2 == "Kherson city liberation":
                """
                ## Kherson city liberation
                ##### November 12, 2022
                """
                "After eight months of brutal Russian occupation, the southern city of Kherson was liberated on November 12, prompting scenes of celebration by residents. Russia’s hasty withdrawal from the west bank of the Dnipro River was another bleak moment for Moscow, since Kherson was the only Ukrainian regional capital that Russian forces had captured. Putin himself had formally declared Kherson to be Russian territory just weeks before his troops’ retreat."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "Judging by the visualization produced, it seems like the Kherson city liberation did not have much of an effect on the returns of the different industries, we don’t see an abrupt change in returns in none of the industries shortly after the event. Nevertheless, it is apparent that the semiconductor industry started observing decreased returns starting 10 days after the event. Given the longer time frame other factors outside of the war could be causing the materialization of this phenomenon, but it could also be argued that this could be due to increased disruptions in the supply chain."
            elif option2 == "Zelensky visits White House":
                """
                ## Zelensky visits White House
                ##### December 21, 2022
                """
                "On December 21, Zelensky traveled to Washington, DC to meet with US President Joe Biden at the White House and to address the US Congress. It was a historic and consequential visit, the first foreign trip Zelensky had made since Russia launched its invasion. Just ahead of Zelensky’s arrival, the Biden administration announced it was sending nearly $2 billion in additional security assistance to Ukraine — including a sophisticated new Patriot air defense system."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "The strengthening of relationships between the Western world represented by the United States and Ukraine doesn’t seem to have much of an effect on industry returns shortly after the event. However, between 10 days and 20 days after the attack, all industry returns appear to increase except the food industry which continues on a downward trend since the event date."
            elif option2 == "Germany sends tanks":
                """
                ## Germany sends tanks
                ##### January 25, 2023
                """
                "After weeks of geopolitical squabbling, a major moment arrived on January 25 when Germany announced it would provide Leopard 2 tanks to Kyiv and allow other European countries to export the German-made battle tank. At the same time, Biden said the US would send 31 M1 Abrams tanks to Ukraine. The move was hailed as a breakthrough in the West’s military support for Ukraine and signaled a bullish view in the West about Ukraine’s ability to reclaim occupied territory."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "The line graph shows how industries are for the most part unaffected by such a crucial event that marked a turning point in the West’s military aid policy during the war. The only significant trend observed for all industries is the abrupt decrease in returns observed between 3 days and 10 days after the event, which in this case is due to an announcement of an increase in interest rates by the Fed on February 1st."
            elif option2 == "Biden visits Kyiv":
                """
                ## Biden visits Kyiv
                ##### February 20, 2023
                """
                "Biden made a highly symbolic surprise visit to Kyiv on February 20, his first since Russia’s full-scale invasion. Standing alongside Zelensky, the US president recalled how the pair spoke by phone as Russian forces rolled in. “One year later, Kyiv stands. And Ukraine stands. Democracy stands,” Biden declared. “The Americans stand with you and the world stands with you.” Zelensky said Biden’s visit brought Ukraine “closer to victory.” The two leaders went on a walkabout in Kyiv just as air raid sirens sounded across the city."
                if all_option1 in option1:
                    """
                    ## Analysis:
                    """
                    "As seen in the graph, the only industry which saw a decrease in returns shortly after the event is the metals industry with a decrease of 0.82%. The rest of the industries increased their returns anywhere in the range of 1% to 1.75% approximately. In the longer time frame 10 days after the event, all industries continued with this upward trend in returns, with the metal industry seeing the greatest increase in terms of percentage magnitude with 6.92%."

        
    elif page == "Report":
        st.title("Report")
        """
        # Preface / Context

Throughout history, wars have had a profound impact on markets and economies. From World War I and World War II to the Gulf War and the Syrian Civil War, conflicts have resulted in significant economic disruptions, with markets reacting to the uncertainty and instability brought about by these events. In some cases, the impact has been short-lived, while in others, the effects have been long-lasting and far-reaching. For example, during World War II, the United States' entry into the conflict led to increased government spending on military production and created new job opportunities in the defense industry, which helped stimulate economic growth. In contrast, the Gulf War in the early 1990s led to a significant increase in oil prices due to concerns over supply disruptions, which caused a slowdown in economic activity.

In the case of the Russian-Ukraine conflict, the impact on markets has been complex and varied. The conflict has had a significant impact on energy markets, with oil and gas prices fluctuating due to concerns over supply disruptions and geopolitical tensions. Other affected markets have been the metals market given that Russia and Ukraine are key producers and sources of nickel, aluminum, titanium, iron, steel, and critical minerals. It is even estimated by 
The industry association UK Metallurg Prom and Oxford Economics that a third of the metal industry’s capacity has been destroyed and production is about 65% lower. The semiconductor industry has also been heavily affected due to supply chain issues and production shortages, stemming from the fact that Russia and Ukraine are major producers of neon and palladium, which are key materials needed to manufacture semiconductors. The transport industry has also been heavily affected, with many industrial ports, airports, and other transportation centers in the area being closed due to the war hazards, reduced tourism could also have a negative effect on the transport industry. The food industry also stands to lose from the war. Prior to the war Ukraine and Russia combined produced about one third of the world’s wheat demand, and they are also important sources of fertilizer, cooking oil and feed grains such as corn. 

Given the importance of markets and their impact on global economies, it is crucial to understand how conflicts such as the Russian-Ukraine conflict affect them. By analyzing the impact of the conflict on various sectors, we can gain valuable insights into the ways in which geopolitical events shape economic activity and help policymakers develop strategies to mitigate the effects of these events on markets.

# Introduction

The main objective of this project is to determine the extent to which reported key event dates in the Russo-Ukrainian war affected the returns for major firms in the energy, food, transport, semiconductors and metal industries from the start of the conflict until today. The use of visualizations and the calculation of the cumulative returns 20 days before and after a reported key event would serve to support the main hypothesis and answer the research question at hand.  

# Initial Hypothesis

We initially hypothesized that energy and metal industries would be most affected by the Russia-Ukraine War because of how significant these nations are in contributing to the production of these goods. Both nations are considered heavy players in global markets for the production of nickel, aluminum, titanium, iron, steel, and critical minerals. The conflict has also disrupted supply chains and has led to Europe’s efforts to reduce reliance on Russian energy. The price of fuel and energy within the European Union has also risen as Russia decided to suspend gas deliveries to several European Union countries, further impacting the situation. For these reasons, we believe that as the Russia-Ukraine conflict continues, these industries will face the greatest volatility and change.

# Data

The data that was used for this project included key event dates of the war, list of firms in the largest traded exchange-traded funds (ETF) for each industry, adjusted close stock prices for all the firms in the previously mentioned list, and the S&P 500 adjusted close prices for the specific time period. 

The key event dates were collected from CNN’s interactive Russo-Ukrainian war archive which outlined key events throughout the war. We collected 17 key event dates for the war. The data was manually written out. Web scraping was a possibility however due to the very limited amount of dates, it would be best to manually write out all 17 key dates rather than deploying some sort of a web scraping algorithm. In addition, it was more efficient to write them out and less hassle to deal with the html code which wrote all dates as strings and not in a date format. 

Next the S&P 500 adjusted close prices were downloaded through the use of ```yf.download``` function in Python. The selected dates were from 2/12/2022 through 4/10/2023. It was best to download this range of dates due to the fact that there is a start to the war and the end to the key event dates on the CNN website. However there were more prices downloaded due to the analysis that would be conducted in this report. The analysis consisted of  looking at  10 dates before and after an event, which required more dates and prices to be downloaded. 

The energy industry firm stocks that were downloaded were from the Vanguard Energy Index Fund ETF (VDE). The file that was downloaded was a CSV file, containing a list of firms that are part of this ETF. It had a total of 112 observations, these firms traded their shares in the U.S stock market and are also tracked by Yahoo Finance. The firms ranged from coal & consumable fuels, integrated oil & gas, oil & gas drilling, oil & gas equipment & services, oil & gas exploration & production, oil & gas exploration & marketing, and oil & gas storage & transportation.

The food industry firm stocks that were downloaded were from the First Trust Nasdaq Food & Beverage ETF (FTXG). It was a CSV file that contained a list of 30 observations, these firms were found to trade in the U.S stock market and also tracked by Yahoo Finance. The firms found in this ETF ranged from food products, soft drinks, fruit and grain processing, distillers and vintners, farming, fishing, ranching, and plantations. 

The transportation industry firm stocks that were downloaded came from the SPDR S&P Transportation ETF (XTN). It was a CSV file that contained a list of 47 observations. The firms in this ETF operated in cargo ground transportation, passenger airlines, air freight & logistics, marine, passenger ground transportation, rail transportation, and trucking. All the firms in this list were tracked by Yahoo Finance. 

The semiconductor industry firm stocks that were downloaded came from SPDR S&P Semiconductor ETF (XSD). It was recorded in a CSV file that contained a list of 38 observations. The firms in this ETF operated specifically in the semiconductor industry, including firms such as NVIDIA, Micron Technology, Intel Corporation, Advanced Micro Devices Inc. and many more. All of these companies trade in the U.S stock market and were also tracked by Yahoo Finance. 

The metal industry firm stocks were downloaded from a list of steel and iron ore focused firms. The downloaded CSV file contained 17 observations, mostly firms located in the U.S, such as Allegheny Technologies Incorporated, Carpenter Technology Corporation, Commercial Metals Company, etc. All of these stocks traded in the U.S stock market and were also tracked by Yahoo Finance.

After downloading the data for the different ETFs we accessed the column which identified the firms by their ticker and converted them to a list. This list of firms is what we then passed to the ````yfinance.download``` function which downloaded the pricing data for the firms of interest within the date range we specified. 

# Methodology

### Calculating Daily Returns for each Industry

After the initial download of the firm’s adjusted closing price by date, the first step was to calculate daily returns for each firm in the industries. This would then allow for the calculation of the excess and cumulative returns. 

We used the following code:

```python
metal_prices = metal_prices.sort_values(['Firm', 'Date'])
metal_prices['Daily Returns'] = metal_prices.groupby('Firm')['Adj Close'].pct_change()
```

The above code snippet is an example of how we calculated the daily returns of the firms in the metal industry, one can assume that this same algorithm was used for the rest of the industries. The use of a .groupby function separated the dataset between firms, which would not allow for firms to merge its returns and kept calculating daily returns within each individual firm. The use of the ```.pct_change()``` function is what calculates the daily return for the adjusted close (adjusted closing price) variable which is performed by taking the difference (expressed as a percentage) between the adjusted closing price of a firm in a given trading day and the adjusted closing price of a firm the next trading day. This was done for all five industries.

### Calculating Daily Returns for S&P 500

```python
market_ret.columns = ['Firm','Date','Adj Close']
market_ret['Firm'] = "sp500"
market_ret['Daily Returns'] = market_ret['Adj Close'].pct_change()
market_ret
```

This code calculated the daily returns for the S&P 500, which would come to serve as the market return which would then be compared to the different industry returns. The need to calculate the daily returns is to directly compare them to the firms’ daily returns from the metal, food, transportation, semiconductor, and energy industries, which would allow for the calculation of the excess returns. 

### Calculating Excess Returns

```python
metal_excess_returns = metal_prices.groupby(['Firm', 'Date'])['Daily Returns'].mean() - market_ret.set_index('Date')['Daily Returns']
metal_excess_returns = metal_excess_returns.reset_index()
metal_excess_returns = metal_excess_returns.rename(columns={'Daily Returns': 'Excess Returns'})
metal_excess_returns["Industry"] = "Metal"
```
The code above calculates the excess returns for the firms in the metal industry. It uses the daily returns from the firms in the metal industry and subtracts it to the S&P 500 daily returns. A positive excess return would demonstrate that a firm in the metal industry outperformed the S&P 500, and any negative excess value would show that the S&P 500 index outperformed a firm in the metal industry. This was repeated for all five industries in order to calculate their excess returns. We then added an extra column to specify which industry the given first belongs to. This final step is performed in preparation of the cumulative returns over different time frames by industry. 

### Calculating Cumulative Returns

```python
event_ret_df = pd.DataFrame()
industries = ['Food', 'Transport', 'Semiconductor', 'Energy', 'Metal']
for index, row in event_dates.iterrows():
    event = row['Event']
    date = row['Date']
    # Define the start and end dates for the subset
    start_date = pd.to_datetime(date) - pd.Timedelta(days=20)
    end_date = pd.to_datetime(date) + pd.Timedelta(days=20)

    for industry in industries:
        sub_df = inter_df.query("Date >= @start_date and Date <= @end_date and Industry == @industry")
        sub_df_cum = sub_df.assign(R=1+sub_df['Excess Returns']).assign(cumret=lambda x: x.groupby(['Firm'])['R'].cumprod()).groupby(['Date'])['cumret'].mean().reset_index(name='Cum_ret')
        sub_df_cum["Event"] = event
        sub_df_cum["EventDate"] = date
        sub_df_cum["Industry"] = industry
        event_ret_df = pd.concat([event_ret_df, sub_df_cum])

event_ret_df["Cum_ret"] = event_ret_df["Cum_ret"] - 1
event_ret_df["EventDate"] = pd.to_datetime(event_ret_df["EventDate"])
event_ret_df["Date"] = pd.to_datetime(event_ret_df["Date"])
event_ret_df.to_csv("../OutputData/final.csv")
```

This code essentially calculates cumulative returns by date for every industry for every major event in the war. The outer for-loop iterates over the major events dataframe, it then specifies a time frame for which cumulative returns are to be calculated, in our case we use 20 days before and after the event as we thought that this time frame would allow for a visual comparison of returns pre and post the events. 

The code then subsets the data to include only the rows that are within the time range and belonging to a certain industry, there is an inner for loop which iterates over the different values in the “Industry” column which allows for the calculation of cumulative returns by industry by event.

The resulting computed values, along with some other variable identifiers like the day of the event, the industry, and the nature of the event are then added into a dataframe which was created empty. The resulting dataframe is our final dataset which will be then used to produce the different visualizations seen in the “Home” tab of the dashboard. 

# The Final Dataset

In our final dataset every observation represents a calculation of a cumulative return for a specific industry for a specific event, which would allow us to plot cumulative returns by industry by events. Please note that the industries’ returns are cumulated separately for each event to allow for a better understanding and analysis of how events impact industry stock returns. This dataset contains a total of 2405 observations and 5 different columns, which are 'Date', 'Cum_ret', 'Event', 'EventDate', 'Industry'. If you have followed the steps to run the code in the readme file of the repo (link available in the home tab of the dashboard), you can inspect the nature of the dataset created which is called final.csv and is found within the OutputData folder.

# Calculating Return Differences 

```python
rets = []
industries = ['Food', 'Transport', 'Semiconductor', 'Energy', 'Metal']
for index, row in event_dates.iterrows():
    event = row['Event']
    date = row['Date']

    sub_df = event_ret_df.query("Event == @event")
    sub_df['Date'] = pd.to_datetime(sub_df['Date'])
    last_date = sub_df['Date'].max()
    date1 = date + pd.Timedelta(days=3)
    date2 = date + pd.Timedelta(days=10)
    
    plt.figure(figsize=(8, 6))
    for industry in industries:
        industry_df = sub_df[sub_df['Industry'] == industry]
        sns.lineplot(x='Date', y='Cum_ret', data=industry_df, label=industry)
    
    plt.axvline(date, color='red', linestyle='--', label='Event Date')
    plt.axvline(date1, color='red', linestyle='--', label='Event Date + 3')
    plt.axvline(date2, color='red', linestyle='--', label='Event Date + 10')
    plt.xlim(date - pd.Timedelta(days=20), date + pd.Timedelta(days=20))
    
    for line in plt.gca().lines:
        if line.get_label() in industries: 
            x = mpl_dates.date2num(date)
            x1 = mpl_dates.date2num(date1)
            x2 = mpl_dates.date2num(date2)
            y = np.interp(x, line.get_xdata().astype(np.float64), line.get_ydata().astype(np.float64))
            y1 = np.interp(x1, line.get_xdata().astype(np.float64), line.get_ydata().astype(np.float64))
            y2 = np.interp(x2, line.get_xdata().astype(np.float64), line.get_ydata().astype(np.float64))
            result = {"Date": date, "Industry": line.get_label(), 'ret0': y, "ret3": y1, "ret10": y2}
            rets.append(result)
    
    plt.close()

rets_df = pd.DataFrame(rets)
```
```python
rets_df["retDiff3"] = rets_df["ret3"] - rets_df["ret0"]
rets_df["retDiff10"] = rets_df["ret10"] - rets_df["ret0"]
rets_df = rets_df.drop(['ret3', 'ret10','ret0'], axis=1)
rets_df.rename(columns = {"retDiff3": "ret3", "retDiff10": "ret10"}, inplace = True)
rets_df.to_csv("../OutputData/RetDiff.csv")
rets_df.head(10)
```
The above code blocks are used to calculate return differences between the event date and some days after the event. We decided to calculate return differences 3 days after the event to allow for a numerical comparison and look at the short term effects of the event. We also wanted to look at return differences 10 days after the event, this allows for a numerical comparison within a longer time frame and could help us gain further insights into whether the effects of an event in the war are long lived or not. Even though the first code block might seem confusing, it is essentially accessing the return variable at times 0, 3 days after and 10 days after the event. Rather than using data points from our dataset to calculate the return differences we used the return values from the line graph, this solved one of the main limitations of our data, the fact that many dates are not actual trading days, meaning that in some cases we did not have a datapoint for a return on a given date. This also means that some return difference calculations are approximations, they are based on a point in the line graph which might be within two data points. For example if 3 days after the event, the day is a non-trading day, we don’t have return data for that date so instead we use the value displayed by the line graph.    

The second code block just serves to calculate return differences between the return values at different point in times which were accessed above. This was a complimentary dataset that we wanted to use for our analysis. We thought that mere line graph visualizations, could explain a general picture and trends but we also thought that we needed to have concrete numerical values which would allow for faster comparison between industries.  

# Creating our Dashboard

Our dashboard was created using the streamlit package. We organized the dashboard into two parts, the main window and the sidebar. From the sidebar the user can access the home page as well as the report. The sidebar also allows the user to select which industry and event they would like to see graphed. The main homepage features a graph created by the industry and event selected. The homepage also features a description of the event that was obtained from the CNN interactive timeline article, as well as our analysis of each industry at the time the event occurred. 

# Conclusion
In our analysis of the industry returns for Metal, Transport, Energy, Semiconductors, and Food, we observed that the Metal and Energy sectors were significantly impacted in the early days of the Russia-Ukraine conflict due to the nations' substantial contributions to the production of these goods. However, as the conflict progressed and major events unfolded, we did not notice any considerable changes in the other industry returns.

Despite our initial hypothesis, the observed impact on various industries during the conflict was not as significant as anticipated. To draw more accurate conclusions, further data analysis and consideration of other factors affecting the stock market, such as the Federal Reserve raising interest rates, may be necessary.

# Sources and Citations
- “Russian Invasion of Ukraine: A Timeline of Key Events on the 1st Anniversary of the War.” CNN, Cable News Network, https://www.cnn.com/interactive/2023/02/europe/russia-ukraine-war-timeline/index.html.
- Argirova, H. (2023, March 27). A steel plant ready for war shows a hit to Ukraine's economy. AP NEWS. Retrieved May 2, 2023, from https://apnews.com/article/russia-ukraine-war-economy-metal-industry-6494b245289f795ff2c3da87e9d2eba1# 
- KPMG. (2022, August 17). Ukraine-Russia sector considerations: Semiconductor Industry. KPMG. Retrieved May 2, 2023, from https://kpmg.com/xx/en/home/insights/2022/08/semiconductor-considerations.html 
- Aizenman, N. (2023, February 27). The impact of the Ukraine War on food supplies: 'it could have ... - NPR. Goats and Soda. Retrieved May 3, 2023, from https://www.npr.org/sections/goatsandsoda/2023/02/27/1159630215/the-russia-ukraine-wars-impact-on-food-security-1-year-later
"""

if __name__ == "__main__":
    main()


