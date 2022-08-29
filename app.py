import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd


########### Define your variables ######

tabtitle = 'Adult Income Data'
sourceurl = 'https://archive.ics.uci.edu/ml/datasets/adult'
githublink = 'https://github.com/adam-tanner-24/08-EDA-3-Week-Project'
# here's the list of possible columns to choose from.


########## Set up the chart
path = 'https://github.com/adam-tanner-24/08-EDA-3-Week-Project/blob/d02c18c57859830bbdb82cc9c8e19af6ac094abe/assets/EDA_Sensus.csv'


df = pd.read_csv(path,
                 names=["index", "age", "workclass","fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country"],
                 index_col=False,
                 on_bad_lines='skip')

#Creating apply function to bucketize hours-per-week series
def hour_per_week_bucket(hour):
    if hour < 10:
        return '< 10 Hours'
    if hour > 10 and hour <= 20:
        return '11 - 20 Hours'
    if hour >20 and hour <=30:
        return '21 - 30 Hours'
    if hour >30 and hour <=40:
        return '31 - 40 Hours'
    if hour > 40 and hour <=50:
        return '41 - 50 Hours'
    if hour > 50 and hour <=60:
        return '51 - 60 Hours'
    if hour > 60:
        return '61+ Hours'
#Applying the defined function and returning first 5 rows
df['hours-per-week-bucket']=df['hours-per-week'].apply(hour_per_week_bucket)


list_of_columns=list(df.columns)
list_of_columns.remove('age')
list_of_columns.remove('education')
list_of_columns.remove('education-num')
list_of_columns.remove('capital-gain')
list_of_columns.remove('capital-loss')
list_of_columns.remove('hours-per-week')
list_of_columns.remove('fnlwgt')
#Column list = [workclass, marital-status, occupation, relationship, race, sex, native-country]

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Census Data Analysis'),
    html.Div([
        html.H6('Select a variable for analysis:'),
        dcc.Dropdown(
            id='options-drop',
            options=[{'label': i, 'value': i} for i in list_of_columns],
            value='native-country')]), 
    html.Div([dcc.Graph(id='figure-1')]),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),])


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Analysis on {varname} compared to Education Level'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Average Education Level"
    
    #data_chart = df.groupby([varname])['education-num'].mean().reset_index(name='Avg Education-Num')
    data_chart = df.groupby(['native-country'])['education-num'].mean().reset_index(name='Avg Education-Num')
    
    #data = go.Bar(x=data_chart[varname],
                 #y=data_chart['Avg Education-Num'])
    data = go.Bar(x=data_chart['native-country'],
                  y=data_chart['Avg Education-Num'])
    
    fig = go.Figure([data])
    #fig = px.bar(data_chart, x=[varname],y='Avg Education-Num')


    # data=go.Choropleth(
    #     locations=df['State Code'], # Spatial coordinates
    #     locationmode = 'USA-states', # set of locations match entries in `locations`
    #     z = df[varname].astype(float), # Data to be color-coded
    #     colorscale = mycolorscale,
    #     colorbar_title = mycolorbartitle,    )
    #fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
