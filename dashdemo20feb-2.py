from dash import dcc, html, Dash, callback, Output, Input
import pandas as pd
import plotly.express as px
app=Dash(__name__)
server=app.server
customer_df=pd.read_csv('P6-UK-Bank-Customers.csv')
# groupby_df=customer_df.groupby('Region',as_index=False).agg(TotalBalance=('Balance','sum'))
# groupby_classification_df=customer_df.groupby('Job Classification',as_index=False).agg(TotalBalance=('Balance','sum'))
# fig=px.bar(x=groupby_df['Region'],y=groupby_df['TotalBalance'])
app.layout=html.Div(children=[
    html.H1('Pandas',style={'background-color':'yellow','border-style':'dashed','text-align':'center'})
,html.Div(children=[html.P('Region')
,dcc.Dropdown(customer_df['Region'].unique(),
                 id='region-dropdown',searchable=True,clearable=True
                 ,style={'width':150,'display':'inline-block'}
                 )],style={'display':'flex'}),
html.Div(children=[    html.P('Job Classification')
,dcc.Dropdown(customer_df['Job Classification'].unique(),
                 id='classification-dropdown',searchable=True,clearable=True
                 ,style={'width':150,'display':'inline-block'}
                 )],style={'display':'flex'})
    , dcc.Graph(id='region-total-balance')
    , dcc.Graph(id='classification-total-balance')
]
)
@callback(
    Output('region-total-balance','figure', allow_duplicate=True),
    Input('classification-total-balance','hoverData'),
    prevent_initial_call=True
)
def update_cross_filter_classification_total_balance(clickdata):
    # print(clickdata)
    if clickdata != None:
        classification=(dict(list(clickdata['points'])[0])['x'])
        # print(dict(list(clickdata['points'])[0])['y'])
        if classification != None:  # if nothing is selected show all region data
            filter_df = customer_df[(customer_df['Job Classification'] == classification)]
            groupby_df = filter_df.groupby('Region', as_index=False).agg(
                TotalBalance=('Balance', 'sum'))
            # print(groupby_classification_df)
            fig = px.bar(groupby_df, x='Region', y='TotalBalance')
            fig.update_layout()
            return fig
@callback(
    Output('classification-total-balance','figure', allow_duplicate=True),
    Input('region-total-balance','clickData'),
    prevent_initial_call=True
)
def update_cross_filter_region_total_balance(clickdata):
    # print(clickdata)
    if clickdata != None:
        region=(dict(list(clickdata['points'])[0])['x'])
        # print(dict(list(clickdata['points'])[0])['y'])
        if region != None:  # if nothing is selected show all region data
            filter_df = customer_df[(customer_df['Region'] == region)]
            groupby_classification_df = filter_df.groupby('Job Classification', as_index=False).agg(
                TotalBalance=('Balance', 'sum'))
            # print(groupby_classification_df)
            fig_class = px.bar(groupby_classification_df, x='Job Classification', y='TotalBalance')
            fig_class.update_layout()
            return fig_class
@callback(
    Output('region-total-balance','figure'),
    Output('classification-total-balance','figure'),
    Input('region-total-balance','clickData'),
    Input('region-dropdown','value'),
    Input('classification-dropdown','value')
)
def update_graph(clickdata,region,classification):

    if region==None: # if nothing is selected show all region data
        if classification==None:
            groupby_df = customer_df.groupby('Region', as_index=False).agg(TotalBalance=('Balance', 'sum'))
            groupby_classification_df=customer_df.groupby('Job Classification',as_index=False).agg(TotalBalance=('Balance','sum'))
        else:
            groupby_df = customer_df.groupby('Region', as_index=False).agg(TotalBalance=('Balance', 'sum'))
            filter_df=customer_df[customer_df['Job Classification']==classification]
            groupby_classification_df = filter_df.groupby('Job Classification', as_index=False).agg(
                TotalBalance=('Balance', 'sum'))
    else:
        filter_df=customer_df[(customer_df['Region']==region)]
        groupby_df = filter_df.groupby('Region', as_index=False).agg(TotalBalance=('Balance', 'sum'))
        if classification==None:
            groupby_classification_df=customer_df.groupby('Job Classification',as_index=False).agg(TotalBalance=('Balance','sum'))
        else:
            filter_df=customer_df[customer_df['Job Classification']==classification]
            groupby_classification_df = filter_df.groupby('Job Classification', as_index=False).agg(
                TotalBalance=('Balance', 'sum'))


    # print(region)
    fig = px.bar(groupby_df,x='Region', y='TotalBalance')
    fig.update_layout()

    fig_class = px.bar(groupby_classification_df, x='Job Classification', y='TotalBalance')
    fig_class.update_layout()

    return fig,fig_class

if __name__=='__main__':
    app.run(debug=True)
