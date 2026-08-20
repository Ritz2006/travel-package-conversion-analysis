#!/usr/bin/env python
# coding: utf-8

# In[4]:


from flask import Flask , render_template 
import pandas as pd 
import plotly.express as px


# In[5]:


app =  Flask(__name__)


# In[7]:


df =  pd.read_csv('../Data/Travel.csv')


# In[9]:


# Missing Data
for col in df.columns:
    if df[col].dtypes!='object':
        df[col] = df[col].fillna(int(df[col].mean()))
    else:
        df[col] = df[col].fillna(df[col].mode()[0])


# In[10]:


# Remove outliers
for col in df.columns:
    if df[col].dtypes!='object':
        lower = df[col].mean()-(3*df[col].std())
        upper = df[col].mean()+(3*df[col].std())
        df = df[df[col].between(lower,upper)]


# In[25]:


def create_conversion_chart(column):
    summary = (df.groupby(column).agg(Count=('ProdTaken','size'),
                                      conversion=(
                                          'ProdTaken', lambda x: round(x.mean()*100))).reset_index())
    fig = px.bar(
        summary,
        x=column,
        y='Count',
        text ='Count',
        title = f'{column} Analysis'
    )
    fig.add_scatter(
        x=summary[column],
        y=summary['conversion'],
        mode = 'lines+markers+text',
        text = summary['conversion'],
        textposition='top center',
        name='Conversion %'
        
        
    )
    fig.update_layout(
        height = 350,
        title_x=0.5,
        margin = dict(l=10,r=10,t=50,b=10),
        legend =dict(orientation='h',x=1.1,y=0.5,xanchor='center'))
    
    return fig.to_html(full_html=False) # return fig.show()


# In[35]:


create_conversion_chart('TypeofContact')


# In[36]:


@app.route('/')
def dashboard():
    total_customers = len(df)
    buyers = int(df['ProdTaken'].sum())
    conversion = round(df['ProdTaken'].mean()*100,0)
    avg_income = int(df['MonthlyIncome'].mean())
    charts = []
    categorical_cols = [col for col in df.columns if df[col].dtypes=='object']
    for col in categorical_cols :
        charts.append(create_conversion_chart(col))
    scatter = px.scatter(
        df,
        x='MonthlyIncome',
        y='Age',
        color=df['ProdTaken'].astype(str),
        title='income vs Conversion')
    scatter.update_layout(
        template='plotly_white',
        height = 500
    )
    scatter_chart =  scatter.to_html(full_html=False)

    return render_template(
        'index.html',
        total_customers=total_customers,
        buyers=buyers,
        conversion = conversion ,
        avg_income = avg_income,
        charts=charts,
        scatter_chart = scatter_chart)
    


# In[37]:


if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




