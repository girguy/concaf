from sys import set_asyncgen_hooks
import streamlit as st
import plotly.graph_objects as go


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

    def define_title(self, title, x_pos, y_pos, title_font):
        title_format = {
            'text': f"<span style='color: #FFFFFF; font-family: {title_font};'>{title}</span>",
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
            title=self.define_title(title, 0.5, 0.8, title_font='sans-serif'),
            autosize=False,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,  # dark grey
            plot_bgcolor=plot_color
        )

        st.plotly_chart(fig, use_container_width=True, config=dict({'staticPlot': True, 'displaylogo': False}))


    def plot_players_per_league(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['PlayerCount'],
            y=df['Country'],
            text=df['PlayerCount'],
            orientation='h',
            width=0.7,
            marker=dict(
                color='#006400'
            )
        ))

        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95, title_font='sans-serif'),
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color,
            bargap=0.4,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.0  # gap between bars of the same location coordinate.
            )

        fig.update_xaxes(visible=True)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})


    def plot_fifa_ranking(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure(
            data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color=background_plot_color,
                                fill_color="black"),
                    cells=dict(values=[df['Nation'], df['Nation Ranking']],
                               line_color=background_plot_color,
                               fill_color=background_plot_color,
                               font=dict(color=['white', 'green'], size=14),
                               height=25))]
                        )

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95, title_font='sans-serif'),
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

    def market_value_per_team(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Nation'],
            y=df['MarketValue'],
            orientation='v',
            width=0.7,
            marker=dict(
                color='#006400'
            )))

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95, title_font='sans-serif'),
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        fig.update_xaxes(showgrid=False, zeroline=False, tickangle=-45)
        fig.update_yaxes(showgrid=False, zeroline=False)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

    def position_market_value(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure()

        text = (df['MarketValue']/1000000).to_list()
        text = ['%.2f' % elem for elem in text]

        fig.add_trace(go.Bar(
            x=df['MarketValue'],
            y=df['Position'],
            text=text,
            orientation='h',
            width=0.7,
            marker=dict(
                color='#006400'
            )
        ))

        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95, title_font='sans-serif'),
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color,
            )

        fig.update_xaxes(visible=True)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

    def average_age_and_cap(self, title, df, width, height, font_size, background_plot_color):
        # Create a bubble chart using Plotly Graph Objects
        fig = go.Figure()

        # Create a bubble chart using Plotly Graph Objects
        fig = go.Figure(data=[
            go.Scatter(
                x=df['AgeAverage'],
                y=df['AverageCap'],
                mode='markers+text',
                marker=dict(
                    size=df['AverageCap'],
                    color=df['AgeAverage'],  # Color by Average Age
                    colorscale='Greens',
                    showscale=True
                ),
                text=df['Nationality']
            )
        ])

        # Update layout
        fig.update_layout(
            title=self.define_title(title, 0.5, 0.95, title_font='sans-serif'),
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

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

    def results(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure(
            data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color=background_plot_color,
                                fill_color="black"),
                    cells=dict(values=[df['Date'], df['HomeTeam'], df['AwayTeam'], df['Result']],
                               line_color=background_plot_color,
                               fill_color=background_plot_color,
                               font=dict(color=['white', 'white', 'white', "#006400", 'white'], size=14),
                               height=25))]
                        )

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95, title_font='sans-serif'),
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

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
        colors = [color_2, 'black']
        percentages = [percentage, 100-percentage]

        fig = go.Figure()
        fig.add_trace(go.Pie(values=percentages, hole=.9, name=odd_name))
        fig.update_traces(textinfo="none", marker=dict(colors=colors))

        title = "<span style='color:white; font-family:sans-serif; font-size:13px;'>" + odd_name
        fig.update_layout(title={
                'text': title,
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            showlegend=False,
            autosize=True,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            annotations=[dict(text=str(percentage)+"%", x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor=color_1,
            )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})

    def past_games(self, title, df, width, height, font_size, background_plot_color):
        fig = go.Figure(
            data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color=background_plot_color,
                                fill_color="black"),
                    cells=dict(values=[df['Date'], df['HomeTeam'], df['AwayTeam'], df['Result'], df['Phase']],
                               line_color=background_plot_color,
                               fill_color=background_plot_color,
                               font=dict(color=['white', 'white', 'white', "#006400", '#006400'], size=14),
                               height=25))]
                        )

        fig.update_layout(
            title=self.define_title(f'{title}', 0.5, 0.95, title_font='sans-serif'),
            autosize=False,
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=40, pad=4),
            paper_bgcolor=background_plot_color,
            plot_bgcolor=background_plot_color
            )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})
