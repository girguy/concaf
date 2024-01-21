from sys import set_asyncgen_hooks
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


class Visualizer:
    def __init__(self, players_df, nations_df, clubs_df, fixtures_df,
                 outcomes_df, games_df, past_games_df):

        self._players_df = players_df
        self._nations_df = nations_df
        self._clubs_df = clubs_df
        self._fixtures_df = fixtures_df
        self._outcomes_df = outcomes_df
        self._games_df = games_df
        self._past_games_df = past_games_df

    def define_title(self, title, x_pos, y_pos):
        title_format = {
            'text': f"<span style='color: #FFFFFF; font-family: Gill San;'>{title}</span>",
            'x': x_pos,
            'y': y_pos,
            'xanchor': 'center',
            'yanchor': 'top'
            }
        return title_format

    def kpi(self, title, number, height, font_size, background_plot_color, plot_color):
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=number,
            number={'font': {'size': 50, 'color': plot_color, 'family': "Gill San"}}
        ))

        fig.update_layout(
            title=self.define_title(title, 0.5, 0.8),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            autosize=False,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,  # dark grey
            plot_bgcolor=plot_color
        )

        st.plotly_chart(fig,
                        use_container_width=True,
                        config=dict({'staticPlot': True}))

    def plot_players_per_league(self, title, width, height, font_size, background_plot_color):
        fig = go.Figure()

        df = pd.DataFrame({
            'League': ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1'],
            'PlayerCount': [320, 280, 300, 290, 310]  # Sample data
            })
        df = df.sort_values(by='PlayerCount', ascending=True)

        fig.add_trace(go.Bar(
            x=df['PlayerCount'],
            y=df['League'],
            text=df['PlayerCount'],
            orientation='h',
            width=0.7,
            marker=dict(
                color='#006400'
            )
        ))

        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color,
            bargap=0.4,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.0  # gap between bars of the same location coordinate.
            )

        fig.update_xaxes(visible=False)

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))


    def plot_fifa_ranking(self, title, width, height, font_size, background_plot_color):
        # Sample data for 26 countries
        data = {
            'Nation': [
                'Senegal', 'Tunisia', 'Nigeria', 'Algeria', 'Morocco',
                'Egypt', 'Ghana', 'Cameroon', 'Mali', 'Burkina Faso',
                'DR Congo', 'Ivory Coast', 'South Africa', 'Guinea',
                'Cape Verde', 'Uganda', 'Zambia', 'Benin', 'Gabon',
                'Congo', 'Madagascar', 'Niger', 'Libya', 'Mauritania',
                'Kenya', 'Zimbabwe'
                ],

            'FIFA Ranking': [
                20, 27, 32, 35, 43, 49, 50, 53, 57, 60,
                61, 65, 67, 70, 72, 75, 76, 80, 82, 85,
                87, 88, 89, 90, 92, 93
                ]
                }

        df = pd.DataFrame(data)

        fig = go.Figure(
            data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color=background_plot_color,
                                fill_color="black"),
                    cells=dict(values=[df.Nation, df['FIFA Ranking']],
                               line_color=background_plot_color,
                               fill_color=background_plot_color,
                               font=dict(color=['white', 'green']),
                               height=25))]
                        )

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))

    def market_value_per_team(self, title, width, height, font_size, background_plot_color):
        data = {
            'Country': [
                'Senegal', 'Tunisia', 'Nigeria', 'Algeria', 'Morocco',
                'Egypt', 'Ghana', 'Cameroon', 'Mali', 'Burkina Faso',
                'DR Congo', 'Ivory Coast', 'South Africa', 'Guinea',
                'Cape Verde', 'Uganda', 'Zambia', 'Benin', 'Gabon',
                'Congo', 'Madagascar', 'Niger', 'Libya', 'Mauritania',
                'Kenya', 'Zimbabwe'
                ],

            'MarketValue': [
                200, 150, 180, 160, 175, 190, 140, 130, 120, 110,
                105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45,
                40, 35, 30
                ]
                }

        df = pd.DataFrame(data)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Country'], y=df['MarketValue'], marker_color="#006400"))

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        fig.update_xaxes(showgrid=False, zeroline=False, tickangle=-45)
        fig.update_yaxes(showgrid=False, zeroline=False)

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))

    def position_market_value(self, title, width, height, font_size, background_plot_color):
        df = pd.DataFrame({
            'Position': ["Defense", "Offense", "Keeper", "Midfield"],
            'MarketValue': [100, 120, 30, 40]  # Sample data
            })
        df = df.sort_values(by='MarketValue', ascending=True)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['MarketValue'],
            y=df['Position'],
            text=df['MarketValue'],
            orientation='h',
            width=0.7,
            marker=dict(
                color='#006400'
            )
        ))

        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color,
            bargap=0.4,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.0  # gap between bars of the same location coordinate.
            )

        fig.update_xaxes(visible=False)

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))

    def average_age_and_cap(self, title, width, height, font_size, background_plot_color):
        data = {
            'Country': ['Egypt', 'Nigeria', 'Senegal', 'Algeria', 'Morocco',
                        'Ghana', 'Cameroon', 'Mali', 'Burkina Faso', 'Tunisia',
                        'DR Congo', 'Ivory Coast', 'South Africa', 'Guinea',
                        'Cape Verde', 'Uganda', 'Zambia', 'Benin', 'Gabon',
                        'Congo', 'Madagascar', 'Niger', 'Libya', 'Mauritania',
                        'Kenya', 'Zimbabwe'],
            'AverageAge': [25, 26, 27, 24, 25, 26, 27, 23, 24, 26, 
                           25, 24, 27, 25, 26, 23, 24, 25, 26, 24,
                           23, 25, 26, 24, 27, 25],  # Sample average ages
            'AverageCaps': [50, 60, 55, 45, 50, 65, 40, 70, 75, 80, 
                            35, 45, 50, 55, 60, 40, 45, 50, 55, 45,
                            35, 40, 45, 50, 55, 60]  # Sample average number of caps
        }

        df = pd.DataFrame(data)

        # Create a bubble chart using Plotly Graph Objects
        fig = go.Figure()

        # Create a bubble chart using Plotly Graph Objects
        fig = go.Figure(data=[
            go.Scatter(
                x=df['AverageAge'],
                y=df['AverageCaps'],
                mode='markers+text',
                marker=dict(
                    size=df['AverageCaps'],
                    color=df['AverageAge'],  # Color by Average Age
                    colorscale='Greens',
                    showscale=True
                ),
                text=df['Country']
            )
        ])

        # Update layout
        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95),
            xaxis_title='Average Age',
            yaxis_title='Average Caps',
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=True,
            margin=dict(l=10, r=10, b=10, t=50, pad=4),
            bargap=0.4,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.0,  # gap between bars of the same location coordinate.
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
        )

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))

    def results(self, title, width, height, font_size, background_plot_color):
        data = {
            'Date': ['20/01/2023', '21/01/2023'],
            'Team 1': ['Ivory Coast', 'Congo'],
            'Team 2': ['Burkina Faso', 'Tanzania'],
            'Results': ['2 - 1', '1 - 1'],
            'Phase': ['Group', 'Group']
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        fig = go.Figure(
            data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color=background_plot_color,
                                fill_color="black"),
                    cells=dict(values=[df['Date'], df['Team 1'], df['Team 2'], df['Results'], df['Phase']],
                               line_color=background_plot_color,
                               fill_color=background_plot_color,
                               font=dict(color=['white', 'white', 'white', "#006400", 'white']),
                               height=25))]
                        )

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95),
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':False}))

    # Function to get the base64 string of an image
    def get_image_base64(self, image_path):
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Function to display an image with round shape
    def display_round_image(self, image_path, alt_text):
        base64_string = self.get_image_base64(image_path)
        return f'<img src="data:image/png;base64,{base64_string}" alt="{alt_text}" style="border-radius: 50%; width: 100px; height: 100px;">'

    # Display match information with round flags
    def display_match_info(self, team1, team1_img, team2, team2_img):
        team1_html = self.display_round_image(team1_img, team1)
        team2_html = self.display_round_image(team2_img, team2)

        # Custom layout using HTML
        html = f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <div style="text-align: center; margin-right: 40px;">
                    {team1_html}
                    <p>{team1}</p>
                </div>
                <div style="font-size: 44px; margin-right: 40px;">VS</div>
                <div style="text-align: center;">
                    {team2_html}
                    <p>{team2}</p>
                </div>
            </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    def odd_circle(self, odd_name, percentage, width, height, font_size, color_1, color_2):
        colors = [color_2, 'white']
        percentages = [percentage, 100-percentage]

        fig = go.Figure()
        fig.add_trace(go.Pie(values=percentages, hole=.7, name=odd_name))
        fig.update_traces(textinfo="none", marker=dict(colors=colors))

        text = "<span style='color:" + 'white' + "'>"+odd_name
        fig.update_layout(title={
                'text': text, 
                'y':0.97,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            legend=dict(orientation="h"),
            font=dict(size=font_size),
            showlegend=False,
            autosize=True,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            annotations=[dict(text=str(percentage)+"%", x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor=color_1,
            )

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot':True}))

    def more_than_15_goals(self):
        pass

    def more_than_25_goals(self):
        pass

    def more_than_35_goals(self):
        pass
