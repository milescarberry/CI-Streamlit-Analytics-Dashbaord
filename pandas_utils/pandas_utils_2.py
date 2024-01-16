import numpy as np

import pandas as pd

import matplotlib.pyplot as plt 

import seaborn as sns 

from plotly import graph_objects as go, express as exp, io as pio 

pio.templates.default = 'ggplot2'

import datetime as dt

from math import radians, cos, sin, asin, sqrt



def first_date_of_quarter(date):

    month = date.month

    year = date.year
    
    if month >= 1 and month <= 3:
        quarter_start_month = 1
        quarter_start_year = year
    elif month >= 4 and month <= 6:
        quarter_start_month = 4
        quarter_start_year = year
    elif month >= 7 and month <= 9:
        quarter_start_month = 7
        quarter_start_year = year
    else:
        quarter_start_month = 10
        quarter_start_year = year
    
    first_date = dt.date(quarter_start_year, quarter_start_month, 1)
    
    return first_date



def show_nan(df, nan_criteria = 'nan'):
    
    
    nan_df = pd.DataFrame(round((df.isna().sum() / len(df)) * 100, 2)).reset_index()
    
    
    nan_df.columns = ['column', 'nan_%']
    
    
    if 'nan' not in str(nan_criteria).lower():
        
        
        nan_df = nan_df[nan_df['nan_%'] >= nan_criteria]
        
    
    fig = exp.bar(nan_df, x = 'nan_%', y = 'column')
    
    
    fig.update_layout(bargap = 0.32)
    
    
    fig.show()
    
    
    return None




def unix_to_datetime(df_, colname):
    
    
    return df_[colname].apply(lambda x: dt.datetime.fromtimestamp(int(x) / 1000) if 'nan' not in str(x).lower() else x)





def sns_kdeplot(df, colname, width = 12, height = 4, dpi = 80, linewidth = 1.5, xticks = []):



    plt.figure(figsize = (width, height), dpi = dpi)


    sns.kdeplot(df[colname], linewidth = linewidth)



    if len(xticks) > 0:


        plt.xticks(xticks)



    else:

        pass



    plt.tight_layout()


    plt.show()







def get_value_counts(df, colname):



    # df = df.reset_index(drop = True)


    # all_ids = df.id.values.tolist()


    # ids = df.id.unique()


    # all_ids_indices = []



    # for i in ids:
        
        
    #     all_ids_indices.append(all_ids.index(i))

        
        
    # df = df.loc[all_ids_indices]



    # df = df.reset_index(drop = True)

    
    
    vc_df = pd.DataFrame(round((df[colname].value_counts(dropna = False) / len(df[colname])) * 100, 2)).reset_index()
    
    
    vc_df.columns = [f"{colname}", 'count_%']
    
    
    fig = exp.bar(
        
        vc_df, 
        
        y = f'{colname}', 
        
        x = 'count_%',
        
        orientation = 'h',
        
        text = 'count_%'
    
    )
    
    fig.update_layout(bargap = 0.32)
    
    
    fig.update_layout(title = dict(text = f"{colname} Frequency Distribution"))
    
    
#     fig.update_traces(textposition = 'outside')
    
    
    fig.show()
    





def spherical_distance(lata, latb, lona, lonb):
    
    # Convert from degrees to radians
    
    lata = radians(lata)
    
    latb = radians(latb)
    
    lona = radians(lona)
    
    lonb = radians(lonb)
    
    
    # Use the 'Haversine' Formula
    
    d_lat = latb - lata
    
    d_lon = lonb - lona
    
    
    P = sin(d_lat / 2)**2 + cos(lata) * cos(latb) * sin(d_lon / 2)**2  
    
    
    Q = 2 * asin(sqrt(P)) 
    
    
    R_km = 6371        # The radius of earth in kms.
    
    
    # Compute the outcome
    
    
    return Q * R_km







def stacked_bar_chart_ci(df, colname1, colname2, colname3):


    _grp = df.groupby(

        [colname1, colname2, colname3], 

        as_index = False, 

        dropna = False

    ).agg(


        {"quantity_litres": pd.Series.count}


    )


    _grp.columns = [colname1, colname2, colname3, 'count']




    _ = df.groupby(


        [colname1, colname2], 


        as_index = False, 


        dropna = False).agg(


        {"quantity_litres": pd.Series.count}


    )



    _.columns = [colname1, colname2, 'count']





    _grp['%'] = _grp.apply(


        lambda x: x[3] / (


            _[


                (_[colname1] == x[0]) &


                (_[colname2] == x[1])


            ]['count'].values[0]

        ), 


        axis = 1


    )



    _grp['%'] = _grp['%'].apply(lambda x: round(x * 100, 2))






    _grp['count_overall'] = _grp.apply(


        lambda x: 


            _[


                (_[colname1] == x[0]) &


                (_[colname2] == x[1])


            ]['count'].values[0]

        , 


        axis = 1


    )
    
    
    _grp[f'{colname1}, {colname2}'] = _grp[colname1] + ', ' + _grp[colname2].apply(lambda x: str(x))
    
    
    _grp = _grp.sort_values(by = [colname1, colname2], ascending = [True, True])
    
    
    _cols = _grp.columns.values.tolist()
    
    
    # 100% stacked bar plot



    fig = exp.bar(
        

        _grp, 
        

        y = f'{colname1}, {colname2}', 
        

        x = '%', 
        
        
        text = '%',

        
        orientation = 'h',
        

        color = colname3,


        custom_data = [_grp[colname3], _grp['count'], _grp['%'], _grp['count_overall']]


    )


    fig.update_layout(bargap = 0.32)



    hovertemp = "<br><br>".join(


        [

            "<b>%{y}</b>",


            "<b>%{customdata[0]}</b>",


            "<b>%{x} %</b>",


            "<b>%{customdata[1]} out of %{customdata[3]} flats</b><extra></extra>"

        ]


    )



    fig.update_traces(hovertemplate = hovertemp)


    fig.update_xaxes(showgrid = False)


    fig.update_yaxes(showgrid = False)


    fig.update_layout(

        title = dict(

            text = f"{_cols[0]}, {_cols[1]} & {_cols[2]} 100% Stacked Bar Chart"

        )


    )



    fig.update_layout(height = 1000, width = 780)


    
    fig.show()



    return None





def stacked_bar_chart_ci_2(df, colname1, colname2):


    _grp = df.groupby(

        [colname1, colname2], 

        as_index = False, 

        dropna = False

    ).agg(


        {"quantity_litres": pd.Series.count}


    )


    _grp.columns = [colname1, colname2, 'count']




    _ = df.groupby(


        [colname1], 


        as_index = False, 


        dropna = False).agg(


        {"quantity_litres": pd.Series.count}


    )



    _.columns = [colname1, 'count']





    _grp['%'] = _grp.apply(


        lambda x: x[2] / (


            _[


                (_[colname1] == x[0])


#                 (_[colname2] == x[1])


            ]['count'].values[0]

        ), 


        axis = 1


    )



    _grp['%'] = _grp['%'].apply(lambda x: round(x * 100, 2))






    _grp['count_overall'] = _grp.apply(


        lambda x: 


            _[


                (_[colname1] == x[0])


#                 (_[colname2] == x[1])


            ]['count'].values[0]

        , 


        axis = 1


    )
    
    
#     _grp[f'{colname1}, {colname2}'] = _grp[colname1] + ', ' + _grp[colname2]
    
    
    _grp = _grp.sort_values(by = [colname1], ascending = [True])
    
    
    _cols = _grp.columns.values.tolist()
    
    
    # 100% stacked bar plot



    fig = exp.bar(
        

        _grp, 
        

        y = f'{colname1}', 
        

        x = '%', 
        
        
        text = '%',

        
        orientation = 'h',
        

        color = colname2,


        custom_data = [_grp[colname2], _grp['count'], _grp['%'], _grp['count_overall']]


    )


    fig.update_layout(bargap = 0.32)



    hovertemp = "<br><br>".join(


        [

            "<b>%{y}</b>",


            "<b>%{customdata[0]}</b>",


            "<b>%{x} %</b>",


            "<b>%{customdata[1]} out of %{customdata[3]} flats</b><extra></extra>"

        ]


    )



    fig.update_traces(hovertemplate = hovertemp)


    fig.update_xaxes(showgrid = False)


    fig.update_yaxes(showgrid = False)


    fig.update_layout(

        title = dict(

            text = f"{_cols[0]} & {_cols[1]} 100% Stacked Bar Chart"

        )


    )



    fig.update_layout(height = 1000, width = 780)


    
    fig.show()



    return None






def stacked_bar_chart_ci_4(df, colname1, colname2, colname3, colname4):


    _grp = df.groupby(

        [colname1, colname2, colname3, colname4], 

        as_index = False, 

        dropna = False

    ).agg(


        {"quantity_litres": pd.Series.count}


    )


    _grp.columns = [colname1, colname2, colname3, colname4, 'count']




    _ = df.groupby(


        [colname1, colname2, colname3], 


        as_index = False, 


        dropna = False).agg(


        {"quantity_litres": pd.Series.count}


    )



    _.columns = [colname1, colname2, colname3, 'count']





    _grp['%'] = _grp.apply(


        lambda x: x[4] / (


            _[


                (_[colname1] == x[0]) &


                (_[colname2] == x[1]) &
                
                
                (_[colname3] == x[2])
                


            ]['count'].values[0]

        ), 


        axis = 1


    )



    _grp['%'] = _grp['%'].apply(lambda x: round(x * 100, 2))






    _grp['count_overall'] = _grp.apply(


        lambda x: 


            _[


                (_[colname1] == x[0]) &


                (_[colname2] == x[1]) &
                
                
                (_[colname3] == x[2])


            ]['count'].values[0]

        , 


        axis = 1


    )
    
    
    _grp[f'{colname1}, {colname2}, {colname3}'] = _grp[colname1] + ', ' + _grp[colname2].apply(lambda x: str(x)) + ', ' + _grp[colname3].apply(lambda x: str(x))
    
    
    _grp = _grp.sort_values(by = [colname1, colname2, colname3], ascending = [True, True, True])
    
    
    _cols = _grp.columns.values.tolist()
    
    
    # 100% stacked bar plot



    fig = exp.bar(
        

        _grp, 
        

        y = f'{colname1}, {colname2}, {colname3}', 
        

        x = '%', 
        
        
        text = '%',

        
        orientation = 'h',
        

        color = colname4,


        custom_data = [_grp[colname4], _grp['count'], _grp['%'], _grp['count_overall']]


    )


    fig.update_layout(bargap = 0.32)



    hovertemp = "<br><br>".join(


        [

            "<b>%{y}</b>",


            "<b>%{customdata[0]}</b>",


            "<b>%{x} %</b>",


            "<b>%{customdata[1]} out of %{customdata[3]} flats</b><extra></extra>"

        ]


    )



    fig.update_traces(hovertemplate = hovertemp)


    fig.update_xaxes(showgrid = False)


    fig.update_yaxes(showgrid = False)


    fig.update_layout(

        title = dict(

            text = f"{_cols[0]}, {_cols[1]}, {_cols[2]} & {_cols[3]} 100% Stacked Bar Chart"

        )


    )



    fig.update_layout(height = 1000, width = 780)


    
    fig.show()



    return None





def estimator_bar_chart(df, estimator, colname1, colname2, colname3):
    
    
    
    if estimator.lower().strip() == 'mean':


        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2], 

            as_index = False

        ).agg(

            {colname3: pd.Series.mean}

        )


        _df.columns = [colname1, colname2, colname3 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}', 

            x = colname3 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname3 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname3 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname3}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname3} by {colname1} & {colname2}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()


    
    elif estimator.lower().strip() == 'median':
        
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2], 

            as_index = False

        ).agg(

            {colname3: pd.Series.median}

        )


        _df.columns = [colname1, colname2, colname3 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}', 

            x = colname3 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname3 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname3 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname3}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname3} by {colname1} & {colname2}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()

    
    
    elif estimator.lower().strip() == 'mode':
        
    
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2], 

            as_index = False

        ).agg(

            {colname3: pd.Series.mode}

        )


        _df.columns = [colname1, colname2, colname3 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}', 

            x = colname3 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname3 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname3 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname3}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname3} by {colname1} & {colname2}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()

    
    
    else:
        
        pass
    
    
    

def estimator_bar_chart_2(df, estimator, colname1, colname2):
    
        
        if estimator.lower().strip() == 'mean':
            

            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.mean}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}", 


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()

            

        elif estimator.lower().strip() == 'median':
            
            
            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.median}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}",


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()


        
        elif estimator.lower().strip() == 'mode':
            
        
            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.mode}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}",


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()

        
        
        else:
            
            pass
    
    


def estimator_bar_chart_4(df, estimator, colname1, colname2, colname3, colname4):

    
    if estimator.lower().strip() == 'mean':

        
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.mean}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname4 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()
    
    
    elif estimator.lower().strip() == 'median':
        
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.median}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname4 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()



    
    elif estimator.lower().strip() == 'mode':
        
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.mode}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',

            text = colname4 + f"_{estimator}",

    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()

        
    
    else:
        
        pass








def estimator_bar_chart_2(df, estimator, colname1, colname2):
    
        
        if estimator.lower().strip() == 'mean':
            

            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.mean}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}", 


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()

            

        elif estimator.lower().strip() == 'median':
            
            
            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.median}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}",


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()


        
        elif estimator.lower().strip() == 'mode':
            
        
            df = df.reset_index(drop = True)


            _df = df.groupby(

                [colname1], 

                as_index = False

            ).agg(

                {colname2: pd.Series.mode}

            )


            _df.columns = [colname1, colname2 + f"_{estimator}"]



    #         _df[f'{colname1}, {colname2}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x))



            _cols = _df.columns.values.tolist()



            # 100% stacked bar plot



            fig = exp.bar(

                _df, 

                y = f'{colname1}', 

                x = colname2 + f"_{estimator}", 

                orientation = 'h',
                
                
                text = colname2 + f"_{estimator}",


        #         color = colname3,


                custom_data = [_df[colname2 + f"_{estimator}"]]


            )


            fig.update_layout(bargap = 0.32)



            hovertemp = "<br><br>".join(


                [

                    "<b>%{y}</b>",


                    f"<b>{estimator.title()} {colname2}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


                ]


            )



            fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


            fig.update_xaxes(showgrid = False)


            fig.update_yaxes(showgrid = False)


            fig.update_layout(

                title = dict(

                    text = f"{estimator.title()} {colname2} by {colname1}"

                )


            )



            fig.update_layout(height = 1000, width = 800)


            fig.show()

        
        
        else:
            
            pass
    
    


def estimator_bar_chart_4(df, estimator, colname1, colname2, colname3, colname4):

    
    if estimator.lower().strip() == 'mean':

        
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.mean}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname4 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()
    
    
    elif estimator.lower().strip() == 'median':
        
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.median}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',
            
            
            text = colname4 + f"_{estimator}",


    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()



    
    elif estimator.lower().strip() == 'mode':
        
    
        df = df.reset_index(drop = True)


        _df = df.groupby(

            [colname1, colname2, colname3], 

            as_index = False

        ).agg(

            {colname4: pd.Series.mode}

        )


        _df.columns = [colname1, colname2, colname3, colname4 + f"_{estimator}"]



        _df[f'{colname1}, {colname2}, {colname3}'] = _df[colname1] + ', ' + _df[colname2].apply(lambda x: str(x)) + ', ' + _df[colname3].apply(lambda x: str(x))



        _cols = _df.columns.values.tolist()



        # 100% stacked bar plot



        fig = exp.bar(

            _df, 

            y = f'{colname1}, {colname2}, {colname3}', 

            x = colname4 + f"_{estimator}", 

            orientation = 'h',

            text = colname4 + f"_{estimator}",

    #         color = colname3,


            custom_data = [_df[colname4 + f"_{estimator}"]]


        )


        fig.update_layout(bargap = 0.32)



        hovertemp = "<br><br>".join(


            [

                "<b>%{y}</b>",


                f"<b>{estimator.title()} {colname4}: </b>" + "<b>%{x:.2f}</b><extra></extra>"


            ]


        )



        fig.update_traces(hovertemplate = hovertemp, texttemplate='%{text:.2f}')


        fig.update_xaxes(showgrid = False)


        fig.update_yaxes(showgrid = False)


        fig.update_layout(

            title = dict(

                text = f"{estimator.title()} {colname4} by {colname1}, {colname2} & {colname3}"

            )


        )



        fig.update_layout(height = 1000, width = 800)


        fig.show()

        
    
    else:
        
        pass








# multi_kdeplot function



def multi_kdeplot(
    
    df, colname, 
    
    buildingType = 'AP', 
    
    width = 11, 
    
    height = 4, 
    
    dpi = 80, 
    
    ticks_x = None,
    
    
    not_include = []


):

        
    df = df.reset_index(drop = True)    
        

    all_ids = df.id.values.tolist()
    

    ids = df.id.unique()

    
    all_ids_indices = []



    for i in ids:
        
        
        all_ids_indices.append(all_ids.index(i))

        
        
    df = df.loc[all_ids_indices]


    
    df = df.reset_index(drop = True)
    
    
    
    _df = pd.DataFrame()
    
    
    
    if colname != 'propertySize':
        
        

        _df = df[['buildingType', 'typeDesc', 'propertySize', colname]]
        
    
    
    else:
        
        
        _df = df[['buildingType', 'typeDesc', 'propertySize']]
        
        


    _df['buildingType, typeDesc'] = _df.buildingType + ', ' + _df.typeDesc


    unique_typeDesc = _df.typeDesc.unique().tolist()


    unique_typeDesc.sort()
    
    
    unique_typeDesc = [i for i in unique_typeDesc if i not in not_include]



    plt.figure(figsize = (width, height), dpi = dpi)



    for u in unique_typeDesc:
        


        sns.kdeplot(


                x = _df[(_df.buildingType == buildingType) & (_df.typeDesc == u)][colname], 


                weights = _df[(_df.buildingType == buildingType) & (_df.typeDesc == u)].propertySize,


                label = buildingType + ', ' + u,


                linewidth = 2.5


        )

        
        
        
    if ticks_x == None:


        pass


    else:


        plt.xticks(ticks_x, fontsize = 17)




    plt.yticks(fontsize = 17)


    plt.xlabel(colname, fontsize = 20, labelpad = 20)


    plt.xlabel('Density', fontsize = 20, labelpad = 20)


    plt.legend(loc = 'best')


    plt.title(f"{buildingType} Prop Types {colname} KDE Plot", pad = 15, fontsize = 10)


    plt.tight_layout()


    plt.show()
            