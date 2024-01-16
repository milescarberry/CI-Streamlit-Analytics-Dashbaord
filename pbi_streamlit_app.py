import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

from plotly import express as exp, graph_objects as go, io as pio

from plotly.subplots import make_subplots

import streamlit as st

import streamlit.components.v1 as components

import pickle

import datetime as dt

from pandas_utils.pandas_utils_2 import *

import warnings




st.set_page_config(


	page_title = "Page Title", 


	layout = 'wide'


	)


sns.set_context("paper", font_scale = 1.4)

pio.templates.default = 'ggplot2'

warnings.filterwarnings("ignore", category=DeprecationWarning)

warnings.filterwarnings("ignore", category=FutureWarning)





@st.cache_data
def get_datasets():


	# Get datasets 

	return (

			pd.read_excel("./pbi_datasets/DIstrict.xlsx"), 

			pd.read_excel('./pbi_datasets/Items.xlsx'), 


			pd.read_excel("./pbi_datasets/Sales.xlsx"),


			pd.read_excel("./pbi_datasets/Stores.xlsx"),


			pd.read_excel("./pbi_datasets/Time.xlsx")


		)


data = get_datasets()



# Dashboard Title


# st.write(

# 	"<h1><center>Title</center></h1>",


# 	unsafe_allow_html = True


# 	)




st.write("<br><br>", unsafe_allow_html = True)



# Some More Text


# st.write(

# 	"<h5><center>Some more text comes here.</center></h5>", 

# 	unsafe_allow_html = True

# 	)



# st.write("<br><br>", unsafe_allow_html = True)





# Sidebar Filters


with st.sidebar:


	st.write(

		"<h1><center>Filters</center></h1><br>", 

		unsafe_allow_html = True

	)





# Do your work here



districts_df = data[0]

items_df = data[1]

sales_df = data[2]

stores_df = data[3]

time_df = data[4]




# st.write("Districts\n")

# st.table(districts_df)

# st.write()

# items_df = items_df.rename({"FamilyNane": "FamilyName"}, axis = 1)


# st.write("Items\n")


# st.table(items_df.sample(4))

# st.write()

# st.write("Sales\n")


# st.table(sales_df.sample(4))


# # st.write(sales_df.ReportingPeriodID.unique())


# st.write("\nStores\n")


# st.table(stores_df.sample(4))


# st.write("\nTime\n")


# st.table(time_df.sample(4))




# Let's take a look at the table Sales:


sales_df['MonthID'] = sales_df['MonthID'].apply(

	lambda x: str(x)[0:4:1] + '-' + str(x)[4:6:1], "%Y-%m"

)





time_df['MonthID'] = time_df.apply(

	lambda x: str(x[2]) + '-' + str(x[1]) , 

	axis = 1

	)



time_df['MonthID'] = time_df['MonthID'].apply(

	lambda x: x.split('-')[0] + '-' + '0' + x.split('-')[1].strip() if len(x.split('-')[1].strip()) == 1 else x


)



# st.table(sales_df.head(5))



sales_df = sales_df.reindex(

	columns = [
	  "MonthID",
	  "ItemID",
	  "Sum_GrossMarginAmount",
	  "Sum_Regular_Sales_Dollars",
	  "Sum_Markdown_Sales_Dollars",
	  "ScenarioID",
	  "ReportingPeriodID",
	  "Sum_Regular_Sales_Units",
	  "Sum_Markdown_Sales_Units",

	  "LocationID"

	]

)




sales_df = pd.merge(

	sales_df, 

	stores_df, 

	how = 'left', 

	left_on = 'LocationID', 


	right_on = 'LID'


).drop(columns = ['LID'])





sales_df = pd.merge(

	sales_df, 

	districts_df, 

	how = 'left', 

	left_on = 'DistrictID', 

	right_on = 'DID'

).drop(columns = ['DID'])



quarter_dict = {"January": "Q1",
 "February": "Q1",
 "March": "Q1",
 "April": "Q2",
 "May": "Q2",
 "June": "Q2",
 "July": "Q3",
 "August": "Q3",
 "September": "Q3",
 "October": "Q4",
 "November": "Q4",
 "December": "Q4"

}






sales_df['OpenDateYear'] = sales_df.OpenDate.apply(lambda x: int(dt.datetime.strftime(x, "%Y")))

sales_df['OpenDateYearMonth'] = sales_df.OpenDate.apply(lambda x: dt.datetime.strptime(dt.datetime.strftime(x, "%Y-%m"), "%Y-%m"))

sales_df['OpenDateMonth'] = sales_df.OpenDate.apply(lambda x: dt.datetime.strftime(x, "%B"))


# st.write(sales_df.head(2))


# sales_df['OpenDateQuarter'] = sales_df['OpenDate'].dt.quarter



sales_df['OpenDateQuarter'] = sales_df.OpenDate.apply(

	lambda x: first_date_of_quarter(x.to_pydatetime())

	)


# st.write(sales_df.OpenDateQuarter)


# sales_df['OpenDateQuarter'] = sales_df.apply(

# 	lambda x: str(x[23]) + '-' + quarter_dict[x[25]], axis = 1

# 	)


# sales_df['OpenDateQuarter'] = sales_df['OpenDateQuarter'].apply(lambda x: x[2::1])


# Handling Missing Values in MonthID column:


sales_df = sales_df.reset_index(drop = True)


sales_month_nan_indices = sales_df[sales_df.MonthID == 'nan-'].index.values


sales_df = sales_df[sales_df.MonthID != 'nan-']


# sales_df['MonthID'].iloc[sales_month_nan_indices] = sales_df[


# sales_df.MonthID == 'nan-'

# ].apply(

# 	lambda x: str(x[6])[:6:1][:4:] + '-' + str(x[6])[:6:1][4::1] if x[0] == 'nan-' else x[0], axis = 1

# 	).values.tolist()




sales_df.MonthID = sales_df.MonthID.apply(lambda x: dt.datetime.strptime(x, "%Y-%m"))


time_df.MonthID = time_df.MonthID.apply(lambda x: dt.datetime.strptime(x, "%Y-%m"))



# st.table(items_df.head(4))




sales_df = pd.merge(

	sales_df, 

	items_df, 

	how = 'left', 

	left_on = 'ItemID', 

	right_on = 'IID'

	).drop(

	columns = ['IID']

	)




sales_df = sales_df.reindex(columns = [
  "MonthID",
  "ItemID",
  "Segment",
  "Category",
  "Buyer",
  "FamilyName",
  "Sum_GrossMarginAmount",
  "Sum_Regular_Sales_Dollars",
  "Sum_Markdown_Sales_Dollars",
  "ScenarioID",
  "ReportingPeriodID",
  "Sum_Regular_Sales_Units",
  "Sum_Markdown_Sales_Units",
  "LocationID",
  "City Name",
  "Territory",
  "PostalCode",
  "OpenDate",
  "OpenDateYear",
  'OpenDateYearMonth',
  "OpenDateMonth",
  'OpenDateQuarter',
  "SellingAreaSize",
  "DistrictName",
  "Name",
  "City",
  "DistrictID",
  "Store Type",
  "Total Rent",
  "DM",
  "BusinessUnitID"

])


# Filtering Some Rows


sales_df = sales_df.reset_index(drop = True)



# st.table(sales_df[sales_df.Sum_GrossMarginAmount < 0].sample(3))


sales_df = sales_df[sales_df.Sum_GrossMarginAmount >= 0]


sales_df = sales_df.reset_index(drop = True)



with st.sidebar:



	if 'metric_option' not in st.session_state:


		st.session_state.metric_option = 'Total Sales'



	if 'time_ax' not in st.session_state:


		st.session_state.time_ax = "Month"



	if 'item_filt' not in st.session_state:


		unique_items = sales_df.ItemID.unique().tolist()


		unique_items.sort()


		st.session_state.item_filt = unique_items



	if 'dms_sel' not in st.session_state:


		unique_dms = sales_df.DM.unique().tolist()


		unique_dms.sort()


		st.session_state.dms_sel = unique_dms



	if 'terr_sel' not in st.session_state:


		unique_terr = sales_df.Territory.unique().tolist()


		unique_terr.sort()


		st.session_state.terr_sel = unique_terr




	if 'cat_sel' not in st.session_state:


		unique_cat = sales_df.Category.unique().tolist()


		unique_cat.sort()


		st.session_state.cat_sel = unique_cat




	if 'months_sel' not in st.session_state:


		st.session_state.months_sel = (

			sales_df.MonthID.min().to_pydatetime(), 

			sales_df.MonthID.max().to_pydatetime()

		)




	if 'rental_months_sel' not in st.session_state:


		st.session_state.rental_months_sel = (

			sales_df.OpenDateYearMonth.min().to_pydatetime(), 

			sales_df.OpenDateYearMonth.max().to_pydatetime()

		)




	# Some Filters For The Upcoming Time Series Graph


	st.write("\n\n")



	# Month Slider



	def change_months_sel():


		st.session_state.months_sel = st.session_state.new_months_sel



	months_sel = st.slider(


	    f"Select Time Period for {st.session_state.metric_option} by {st.session_state.time_ax} Chart",


	    sales_df.MonthID.min().to_pydatetime(),


	    sales_df.MonthID.max().to_pydatetime(),


	    (
	    	sales_df.MonthID.min().to_pydatetime(), 

	    	sales_df.MonthID.max().to_pydatetime()

	    ),


	    format = "YYYY-MM",


	    on_change = change_months_sel,


	    key = 'new_months_sel'


	)



	st.write("\n\n")



	# Rental Month Slider



	def change_rental_months_sel():


		st.session_state.rental_months_sel = st.session_state.new_rental_months_sel




	rental_months_sel = st.slider(


		f"Select Time Period For Total Rent by {st.session_state.time_ax} Chart",


		sales_df.OpenDateYearMonth.min().to_pydatetime(),


		sales_df.OpenDateYearMonth.max().to_pydatetime(),


		(

			sales_df.OpenDateYearMonth.max().to_pydatetime(),


			sales_df.OpenDateYearMonth.min().to_pydatetime()

		),


		format = 'YYYY-MM',


		on_change = change_rental_months_sel,


	    key = 'new_rental_months_sel'



	)



	st.write("\n\n")






	# Select Time Axis



	def change_time_ax():


		st.session_state.time_ax = st.session_state.new_time_ax



	time_axis_dict = {

		"Month": "MonthID", 

		"Quarter": "Quarter", 

		"Year": "Year"

	}


	rental_time_axis_dict = {


		"Month": "OpenDateYearMonth",

		"Quarter": "OpenDateQuarter",

		"Year": "OpenDateYear"


	}



	time_ax = st.selectbox(

	   "Select Time Axis",

	   list(time_axis_dict.keys()),

	   index = 0,


	   on_change = change_time_ax,


	   key = 'new_time_ax'


	)


	time_val = time_axis_dict[time_ax]


	rental_time_val = rental_time_axis_dict[time_ax]


	st.write("\n\n")


	# Item Filter


	items_list = ['All']


	unique_items = sales_df.ItemID.unique().tolist()


	unique_items.sort()


	items_list.extend(unique_items)


	def change_item_filt():


		st.session_state.item_filt = st.session_state.new_item_filt


		if 'All' in st.session_state.item_filt:

			st.session_state.item_filt = unique_items


		elif len(st.session_state.item_filt) == 0:


			st.session_state.item_filt = unique_items


		else:

			pass


	item_filt = st.multiselect(


		"Select Items", 


		items_list, 


		['All'],        # Default Selection


		on_change = change_item_filt,


		key = 'new_item_filt'


	)


	items = []


	if 'All' in item_filt:


		items = unique_items


	else:

		items = item_filt


	st.write("\n\n")



	# District Managers Filter



	dms_list = ['All']


	unique_dms = sales_df.DM.unique().tolist()


	unique_dms.sort()


	dms_list.extend(unique_dms)


	def change_dms_sel():


		st.session_state.dms_sel = st.session_state.new_dms_sel


		if 'All' in st.session_state.dms_sel:


			st.session_state.dms_sel = unique_dms


		elif len(sts.session_state.dms_sel) == 0:

			st.session_state.dms_sel = unique_dms


		else:

			pass



	dms_sel = st.multiselect(

		"Select DM", 

		dms_list, 

		['All'],

		on_change = change_dms_sel,


		key = 'new_dms_sel'


		)


	dms = []


	if 'All' in dms_sel:


		dms = unique_dms


	else:

		dms = dms_sel



	st.write("\n\n")


	# Adding Territory Filter


	terr_list = ['All']

	unique_terr = sales_df.Territory.unique().tolist()

	unique_terr.sort()

	terr_list.extend(unique_terr)


	def change_terr_sel():


		st.session_state.terr_sel = st.session_state.new_terr_sel


		if 'All' in st.session_state.terr_sel:


			st.session_state.terr_sel = unique_terr



		elif len(st.session_state.terr_sel) == 0:


			st.session_state.terr_sel = unique_terr


		else:

			pass




	terr_sel = st.multiselect(

		"Select Territory", 

		terr_list, 

		['All'],

		on_change = change_terr_sel,

		key = 'new_terr_sel'


		)


	terrs = []


	if 'All' in terr_sel:


		terrs = unique_terr


	else:


		terrs = terr_sel



	st.write("\n\n")


	# Category Filter


	cat_list = ['All']


	unique_cat = sales_df.Category.unique().tolist()


	unique_cat.sort()

	cat_list.extend(unique_cat)


	def change_cat_sel():


		st.session_state.cat_sel = st.session_state.new_cat_sel


		if 'All' in st.session_state.cat_sel:


			st.session_state.cat_sel = unique_cat



		elif len(st.session_state.cat_sel) == 0:


			st.session_state.cat_sel = unique_cat



		else:

			pass




	cat_sel = st.multiselect(


		"Select Category", 


		cat_list, 


		['All'],


		on_change = change_cat_sel,


		key = 'new_cat_sel'


		)


	cats = []


	if 'All' in cat_sel:


		cats = unique_cat


	else:


		cats = cat_sel


	st.write("\n\n")



	# Adding Columns: Total Regular Sales, Total Markdown Sales, Total Sales


	sales_df['TotalRegularSales'] = sales_df.Sum_Regular_Sales_Dollars * sales_df.Sum_Regular_Sales_Units


	sales_df['TotalMarkdownSales'] = sales_df.Sum_Markdown_Sales_Dollars * sales_df.Sum_Markdown_Sales_Units


	sales_df['TotalSales'] = (sales_df.Sum_Markdown_Sales_Dollars * sales_df.Sum_Markdown_Sales_Units) + (sales_df.Sum_Regular_Sales_Dollars * sales_df.Sum_Regular_Sales_Units)


	sales_df['TotalUnits'] = sales_df.Sum_Regular_Sales_Units + sales_df.Sum_Markdown_Sales_Units
	

	sales_df = sales_df.reindex(columns = [
	  "MonthID",
	  "ItemID",
	  "Segment",
	  "Category",
	  "Buyer",
	  "FamilyName",
	  "Sum_GrossMarginAmount",
	  "Sum_Regular_Sales_Dollars",
	  "Sum_Markdown_Sales_Dollars",
	  "TotalRegularSales",
	  "TotalMarkdownSales",
	  "TotalSales",
	  "ScenarioID",
	  "ReportingPeriodID",
	  "Sum_Regular_Sales_Units",
	  "Sum_Markdown_Sales_Units",
	  'TotalUnits',
	  "LocationID",
	  "City Name",
	  "Territory",
	  "PostalCode",
	  "OpenDate",
	  "OpenDateYear",
	  'OpenDateYearMonth',
	  "OpenDateMonth",
	  'OpenDateQuarter',
	  "SellingAreaSize",
	  "DistrictName",
	  "Name",
	  "City",
	  "DistrictID",
	  "Store Type",
	  "Total Rent",
	  "DM",
	  "BusinessUnitID"
	])




	# Metrics Filter


	def change_metric_option():


		st.session_state.metric_option = st.session_state.new_metric_option



	metrics_list = [

	# 'Gross Margin', 

	'Total Regular Sales', 

	'Total Markdown Sales', 

	'Total Sales',

	'Total Regular Sales Units', 

	'Total Markdown Sales Units',

	'Total Units'

	]


	metrics_dict = {k: v for k, v in zip(

		metrics_list, 

		[

		# 'Sum_GrossMarginAmount', 

		'TotalRegularSales', 

		'TotalMarkdownSales',

		'TotalSales',

		'Sum_Regular_Sales_Units',

		'Sum_Markdown_Sales_Units',

		'TotalUnits'

		]

		)

	}


	metric_sel = st.selectbox(


		"Select Metric", 


		metrics_list, 


		index = 2,


		on_change = change_metric_option,


		key = 'new_metric_option'



	)



	# Apply Filters To The Data


	graph_df = sales_df[


		(sales_df.ItemID.isin(st.session_state.item_filt)) & 


		(sales_df.DM.isin(st.session_state.dms_sel)) &


		(sales_df.Territory.isin(st.session_state.terr_sel)) &


		(sales_df.Category.isin(st.session_state.cat_sel)) &


		(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


		(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


	]



	# Display Selected Districts


	st.write("\n\n")


	sel_districts = graph_df.DistrictName.unique().tolist()


	sel_districts.sort()


	st.text_input(


		label = "Selected Districts", 


		value = f"{',  '.join(sel_districts)}",


		disabled = True


	)



# KPI (Top Line Metrics)


# Creating 3 Columns

kpi_col1, kpi_col2, kpi_col3 = st.columns([1,1,1])




# Metric KPI

with kpi_col1:


	with st.container(border=True):


		metric_df = sales_df[


			(sales_df.ItemID.isin(st.session_state.item_filt)) & 


			(sales_df.DM.isin(st.session_state.dms_sel)) &


			(sales_df.Territory.isin(st.session_state.terr_sel)) &


			(sales_df.Category.isin(st.session_state.cat_sel)) &


			(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


			(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


		]


		metric_val= metric_df[metrics_dict[metric_sel]].sum()



		if 'unit' not in metric_sel.lower():


			st.metric(


				label = metric_sel, 

				value = f"${metric_val / 1000000:.1f}M", 

				delta=None, 

				delta_color="normal", 

				help=None, 

				label_visibility="visible"


			)


		else:


			st.metric(


				label = metric_sel, 

				value = f"{metric_val / 1000:.1f}K Units", 

				delta=None, 

				delta_color="normal", 

				help=None, 

				label_visibility="visible"


			)



# Home Units KPI


with kpi_col3:



	with st.container(border=True):



		home_sales_df = sales_df[


		(sales_df.ItemID.isin(st.session_state.item_filt)) & 


		(sales_df.DM.isin(st.session_state.dms_sel)) &


		(sales_df.Territory.isin(st.session_state.terr_sel)) &


		(sales_df.Category.isin(st.session_state.cat_sel)) &


		(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


		(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


		]



		home_sales_df = home_sales_df[

		(home_sales_df.Sum_GrossMarginAmount > 10) & 

		(home_sales_df.Category == '090-Home')

		]


		home_sales = home_sales_df.TotalUnits.sum()



		st.metric(


				label = 'Home Category Units', 

				value = f"{home_sales / 1000:.1f}K Units", 

				delta=None, 

				delta_color="normal", 

				help=None, 

				label_visibility="visible"


		)



# Gross Margin Gauge


with kpi_col2:


	with st.container(border=True):


		gauge_df = sales_df[


			(sales_df.ItemID.isin(st.session_state.item_filt)) & 


			(sales_df.DM.isin(st.session_state.dms_sel)) &


			(sales_df.Territory.isin(st.session_state.terr_sel)) &


			(sales_df.Category.isin(st.session_state.cat_sel)) &


			(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


			(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


		]


		st.metric(


			label = 'Total Gross Margin Amount', 

			value = f"${gauge_df['Sum_GrossMarginAmount'].sum() / 1000000:.1f}M", 

			delta=None, 

			delta_color="normal", 

			help=None, 

			label_visibility="visible"


		)




		# fig = go.Figure(

		# 	go.Indicator(

		#     mode = "gauge+number",

		#     value = gauge_df['Sum_GrossMarginAmount'].sum(),

		#     number = dict(valueformat = "$" + ".2s"),

		#     domain = {'x': [0, 1], 'y': [0, 1]},

		#     title = {'text': "Total Gross Margin Amount"},

		#     gauge = dict(

		#     	threshold = dict(

		# 	    		line = dict(color = 'red', width = 0), 

		# 	    		thickness = 0,

		# 	    		value = int(sales_df.Sum_GrossMarginAmount.sum())

		#     		)

		#     	)

		#   )


		# )


		# st.plotly_chart(fig)





# Our Sales and Rent Time Series Charts


# st.write("\n")


# Creating Two Columns


ts_col1, ts_col2 = st.columns(2)



with ts_col1:


	with st.container(height = 430, border=True):



		# Get Data Aggregated By Selected Time Series



		graph_df['MonthName'] = graph_df.MonthID.apply(

			lambda x: dt.datetime.strftime(x, "%B")

		)


		graph_df['Year'] = graph_df.MonthID.apply(


			lambda x: int(dt.datetime.strftime(x, "%Y"))

		)


		# graph_df['Quarter'] = graph_df['MonthID'].dt.quarter


		graph_df['Quarter'] = graph_df['MonthID'].apply(

			lambda x: first_date_of_quarter(x.to_pydatetime())

			)


		# graph_df['Quarter'] = graph_df.MonthName.apply(lambda x: quarter_dict[x])



		graph_df = graph_df.reindex(columns = [
		  "MonthID",
		  "MonthName",
		  "Quarter",
		  "Year",
		  "ItemID",
		  "Segment",
		  "Category",
		  "Buyer",
		  "FamilyName",
		  "Sum_GrossMarginAmount",
		  "Sum_Regular_Sales_Dollars",
		  "Sum_Markdown_Sales_Dollars",
		  "TotalRegularSales",
		  "TotalMarkdownSales",
		  "TotalSales",
		  "ScenarioID",
		  "ReportingPeriodID",
		  "Sum_Regular_Sales_Units",
		  "Sum_Markdown_Sales_Units",
		  "TotalUnits",
		  "LocationID",
		  "City Name",
		  "Territory",
		  "PostalCode",
		  "OpenDate",
		  "OpenDateYear",
		  'OpenDateYearMonth',
		  "OpenDateMonth",
		  'OpenDateQuarter',
		  "SellingAreaSize",
		  "DistrictName",
		  "Name",
		  "City",
		  "DistrictID",
		  "Store Type",
		  "Total Rent",
		  "DM",
		  "BusinessUnitID"
		])


		# graph_df['Quarter'] = graph_df.apply(lambda x: str(x[3]) + '-' + x[2], axis = 1)


		# graph_df['Quarter'] = graph_df['Quarter'].apply(lambda x: x[2::1])


		graph_df = graph_df.groupby(

			[f'{time_val}'], 

			as_index = False, 

			dropna = False

			).agg(

			{

			f"{metrics_dict[metric_sel]}": pd.Series.sum

			}

			)




		graph_df = graph_df.sort_values(by = f'{time_val}', ascending = True)






		# Time Series Plotly Express Chart




		fig = exp.line(


			graph_df, 


			x = f'{time_val}',


			y = f'{metrics_dict[metric_sel]}',



			text = f'{metrics_dict[metric_sel]}'



			)


		fig.update_xaxes(title = f'')


		if 'unit' not in metric_sel.lower():


			fig.update_yaxes(

				title = f'{metric_sel}' + " (in Dollars)"

			)


		else:


			fig.update_yaxes(

				title = f'{metric_sel}'

			)




		hovertemp = ""


		texttemp = ""



		if 'unit' in metric_sel.lower():



			hovertemp = "<br><br>".join(

			[


			"<b>%{x}</b>", 


			f"<b>{metric_sel}: </b>" + "<b>%{y:.2s} units</b><extra></extra>"

			]


			)


			texttemp = "<b>%{y:.2s}<b>"



		else:



			hovertemp = "<br><br>".join(

				[


				"<b>%{x}</b>", 


				f"<b>{metric_sel}: </b>" + "<b>$%{y:.2s}</b><extra></extra>"

				]


				)


			texttemp = "<b>$%{y:.2s}</b>"



		fig.update_traces(

			hovertemplate = hovertemp, 

			texttemplate = texttemp, 

			textposition = 'top center'

		)


		fig.update_layout(

			title = dict(

				text = f"{metric_sel} by {st.session_state.time_ax}<br><br>", 

				x = 0.5, 

				xanchor = 'center', 

				yanchor =  'top'

			)

		)


		fig.update_layout(height = 400)



		# if st.session_state.time_ax == 'Quarter':

		# 	fig.update_xaxes(tickangle = -45)



		# Display Plotly Chart 

		st.plotly_chart(fig, use_container_width = True)





# st.write(graph_df[metrics_dict[metric_sel]].sum())    # Total Number



# st.write("\n\n")


# st.table(

# 	sales_df.groupby(

# 		['Territory']

# 		, 

# 		as_index = False, 

# 		dropna = False

# 		).agg(

# 	{

# 	"TotalSales": pd.Series.sum

# 	}

# 	).sort_values(

# 	by = ['TotalSales'], 

# 	ascending = [False]



# 	).iloc[0, ::1]

# )



# # st.write(


# # 	sales_df[


# # 	(sales_df.Territory == 'PA') & 


# # 	(sales_df.DM.isin(['Carlos Grilo', 'Chris Gray']))


# # 	]['TotalSales'].sum()



# # )



# # Question 5 


# st.write("Total Sales: ")

# st.write(graph_df[metrics_dict[metric_sel]].sum())


# st.write("Best Performing Territory: ")


# st.write(sales_df.groupby(

# 	['Territory'], 

# 	as_index = False, 

# 	dropna = False

# 	).agg(

# 	{"TotalSales": pd.Series.sum}

# 	).sort_values(

# 	by = 'TotalSales', 

# 	ascending = False

# ).head())



with ts_col2:


	with st.container(height = 430, border=True):


		# Store Rental Calculation



		# st.write(sales_df.iloc[::1, 22:26:1])


		# st.write(sales_df.sample(4))


		# st.write("Rental Calc")



		rental_df = sales_df[


			# (sales_df.ItemID.isin(st.session_state.item_filt)) & 


			(sales_df.DM.isin(st.session_state.dms_sel)) &


			(sales_df.Territory.isin(st.session_state.terr_sel)) &


			# (sales_df.Category.isin(st.session_state.cat_sel)) &


			(pd.to_datetime(sales_df.OpenDateYearMonth) >= st.session_state.rental_months_sel[0]) & 


			(pd.to_datetime(sales_df.OpenDateYearMonth) <= st.session_state.rental_months_sel[1])


		]



		rental_grp_df = rental_df.groupby(

			[f'{rental_time_val}'], 

			as_index = False, 

			dropna = False

			).agg(

			{

			f"Total Rent": pd.Series.sum

			}

			)




		rental_grp_df = rental_grp_df.sort_values(

			by = f'{rental_time_val}', 

			ascending = True

		)




		# Time Series Plotly Express Chart


		if st.session_state.time_ax == 'Quarter' or st.session_state.time_ax == 'Month':



			fig = exp.line(


				rental_grp_df, 


				x = f'{rental_time_val}',


				y = f'Total Rent',



				# text = f'Total Rent'



				)


			fig.update_xaxes(title = f'')


			# if 'unit' not in metric_sel.lower():


			fig.update_yaxes(

				title = f'Total Rent' + " (in Dollars)"

			)


			# else:


			# 	fig.update_yaxes(

			# 		title = f'Total Rent'

			# 	)




			# hovertemp = ""


			# texttemp = ""



			# if 'unit' in metric_sel.lower():



			# 	hovertemp = "<br><br>".join(

			# 	[


			# 	"<b>%{x}</b>", 


			# 	f"<b>Total Rent: </b>" + "<b>%{y:.2s} units</b><extra></extra>"

			# 	]


			# 	)


			# 	texttemp = "<b>%{y:.2s}<b>"



			# else:



			hovertemp = "<br><br>".join(

					[


					"<b>%{x}</b>", 


					f"<b>Total Rent: </b>" + "<b>$%{y:.2s}</b><extra></extra>"

					]


			)


			# texttemp = "<b>$%{y:.2s}</b>"



			fig.update_traces(

				hovertemplate = hovertemp

				# texttemplate = texttemp, 

				# textposition = 'top center'

			)


			fig.update_traces(mode='markers+lines')


			fig.update_xaxes(tickangle = -45)


			# if st.session_state.time_ax == 'Quarter':


			# 	fig.update_xaxes(

      #            tickmode = 'array',

      #            tickvals = rental_grp_df[rental_time_val].values,

      #            ticktext= [

      #            '' if i % 6 != 0 else rental_grp_df[rental_time_val].values[i] for i in range(len(rental_grp_df[rental_time_val].values))

      #            ]


      #           )




		else:



			fig = exp.line(


				rental_grp_df, 


				x = f'{rental_time_val}',


				y = f'Total Rent',



				text = f'Total Rent'



				)


			fig.update_xaxes(title = f'')


			# if 'unit' not in metric_sel.lower():


			fig.update_yaxes(

				title = f'Total Rent' + " (in Dollars)"

			)


			# else:


			# 	fig.update_yaxes(

			# 		title = f'Total Rent'

			# 	)




			# hovertemp = ""


			# texttemp = ""



			# if 'unit' in metric_sel.lower():



			# 	hovertemp = "<br><br>".join(

			# 	[


			# 	"<b>%{x}</b>", 


			# 	f"<b>Total Rent: </b>" + "<b>%{y:.2s} units</b><extra></extra>"

			# 	]


			# 	)


			# 	texttemp = "<b>%{y:.2s}<b>"



			# else:



			hovertemp = "<br><br>".join(

					[


					"<b>%{x}</b>", 


					f"<b>Total Rent: </b>" + "<b>$%{y:.2s}</b><extra></extra>"

					]


			)


			texttemp = "<b>$%{y:.2s}</b>"



			fig.update_traces(

				hovertemplate = hovertemp, 

				texttemplate = texttemp, 

				textposition = 'top center'

			)


			# fig.update_traces(mode='markers+lines')



		fig.update_layout(

				title = dict(

					text = f"Total Rent by {st.session_state.time_ax}<br><br>", 

					x = 0.5, 

					xanchor = 'center', 

					yanchor =  'top'

				)

		)



		fig.update_layout(height = 400)



		# Display Plotly Chart 


		st.plotly_chart(fig, use_container_width = True)





# rental_df = sales_df[sales_df.OpenDateYear < 2010].groupby(['OpenDateYear'], as_index = False, dropna = False).agg({"Total Rent": pd.Series.sum}).sort_values(by = 'Total Rent', ascending = True)


# rental_month_df = sales_df[sales_df.OpenDateYear == 2005].groupby(['OpenDateMonth'], as_index = False, dropna = False).agg({"Total Rent": pd.Series.sum}).sort_values(by = 'Total Rent', ascending = True)

# rental_quarter_df = sales_df[sales_df.OpenDateYear == 2005].groupby(['OpenDateQuarter'], as_index = False, dropna = False).agg({"Total Rent": pd.Series.sum}).sort_values(by = 'Total Rent', ascending = True)


# st.dataframe(rental_quarter_df)


# Store Rental Calculation Ends Here




# Comparison Time Series Chart



# two_dms_df = 	sales_df[


# 	(sales_df.Territory == 'PA') & 


# 	(sales_df.DM.isin(['Carlos Grilo', 'Chris Gray']))


# 	].groupby(

# 		['MonthID'], 

# 		as_index = False, 

# 		dropna = False

# 		).agg(

# 		{"TotalSales": pd.Series.sum}

# 		).sort_values(

# 		by = ['MonthID'], 

# 		ascending = [True]

# 	)



# other_dms_df = 	sales_df[


# 	(sales_df.Territory == 'PA') & 


# 	(~sales_df.DM.isin(['Carlos Grilo', 'Chris Gray']))


# 	].groupby(

# 		['MonthID'], 

# 		as_index = False, 

# 		dropna = False

# 		).agg(

# 		{"TotalSales": pd.Series.sum}

# 		).sort_values(

# 		by = ['MonthID'], 

# 		ascending = [True]

# 	)



# # Let's Plot A Time Series Chart



# fig = go.Figure()


# fig.add_trace(



# 	go.Scatter(



# 		x = two_dms_df['MonthID'],


# 		y = two_dms_df['TotalSales'],


# 		mode = 'lines+markers+text',


# 		text = two_dms_df['TotalSales'],


# 		name = 'Carlos Grilo & Chris Gray'



# 	)





# )



# fig.add_trace(


# 	go.Scatter(



# 			x = other_dms_df['MonthID'],


# 			y = other_dms_df['TotalSales'],


# 			mode = 'lines+markers+text',


# 			text = other_dms_df['TotalSales'],


# 			name = 'Others'


# 	)




# )




# fig.update_xaxes(title = 'Month')


# # if 'unit' not in metric_sel.lower():


# fig.update_yaxes(

# 		title = 'Total Sales' + " (in Dollars)"

# )


# # else:


# # 	fig.update_yaxes(

# # 		title = f'{metric_sel}'

# # 	)




# # hovertemp = ""


# # texttemp = ""



# # if 'unit' in metric_sel.lower():



# hovertemp = "<br><br>".join(

# 	[


# 		"<b>%{x}</b>", 


# 		f"<b>Total Sales: </b>" + "<b>$%{y:.2s}</b><extra></extra>"

# 	]


# )


# texttemp = "<b>%{y:.2s}<b>"



# # else:



# # 	hovertemp = "<br><br>".join(

# # 		[


# # 		"<b>%{x}</b>", 


# # 		f"<b>{metric_sel}: </b>" + "<b>$%{y:.2s}</b><extra></extra>"

# # 		]


# # 		)


# # 	texttemp = "<b>$%{y:.2s}</b>"



# fig.update_traces(

# 	hovertemplate = hovertemp, 

# 	texttemplate = texttemp, 

# 	textposition = 'top center'

# )


# fig.update_layout(

# 	title = dict(

# 		text = f"Total Sales by Month (Carlos Grilo & Chris Gray vs. Others In PA)<br><br>", 

# 		x = 0.5, 

# 		xanchor = 'center', 

# 		yanchor =  'top'

# 	)

# )



# # if st.session_state.time_ax == 'Quarter':

# # 	fig.update_xaxes(tickangle = -45)



# # Display Plotly Chart 

# st.plotly_chart(fig, use_container_width = True)


st.write("\n\n")   # New Line Characters


# Total Sales By Territory Donut Chart



donut_df = sales_df[


(sales_df.ItemID.isin(st.session_state.item_filt)) & 


(sales_df.DM.isin(st.session_state.dms_sel)) &


(sales_df.Territory.isin(st.session_state.terr_sel)) &


(sales_df.Category.isin(st.session_state.cat_sel)) &


(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


]



donut_df = donut_df.groupby(

	['Territory'], 

	as_index = False, 

	dropna = False).agg(

	{f"{metrics_dict[metric_sel]}": pd.Series.sum}

	).sort_values(

	by = [f'{metrics_dict[metric_sel]}'], 

	ascending = [False]

	)


labels = donut_df['Territory'].values 


values = donut_df[f'{metrics_dict[metric_sel]}'].values 



fig = go.Figure()



if 'unit' not in metric_sel.lower():



	fig = go.Figure(

		data=[

		go.Pie(

			labels=labels, 

			values=values, 

			texttemplate="<b>%{label}<br>"
	                 "%{percent:.1%}</b>",



	    showlegend = False,

	    # Add bolded labels for each piece of data

	    hovertemplate = "<br><br>".join(

	    	[

		    	"<b>%{label}</b>", 

		    	f"<b>{metric_sel}: </b>" + "<b>$%{value:.2s}</b>", 


		    	"<b>%{percent:.2f}</b><extra></extra>"

		    	""

	    	]

	    )


			)

		]

	)



else:


	fig = go.Figure(

		data=[

		go.Pie(

			labels=labels, 

			values=values, 

			texttemplate="<b>%{label}<br>"
	                 "%{percent:.1%}</b>",



	    showlegend = False,

	    # Add bolded labels for each piece of data

	    hovertemplate = "<br><br>".join(

	    	[

		    	"<b>%{label}</b>", 

		    	f"<b>{metric_sel}: </b>" + "<b>%{value:.2s} units</b>", 


		    	"<b>%{percent:.1%}</b><extra></extra>"

		    	""

	    	]

	    )


			)

		]

	)





fig.update_traces(hole = .5)


fig.update_layout(

	title = dict(

		text = f"{metric_sel} by Territory<br>", 

		x = 0.5, 

		xanchor = 'center', 

		yanchor =  'top'

	)

)



st.plotly_chart(fig, use_container_width = True)





# Gross Margin Scenario Table


st.write("\n\n")


margin_df = sales_df[


	(sales_df.ItemID.isin(st.session_state.item_filt)) & 


	(sales_df.DM.isin(st.session_state.dms_sel)) &


	(sales_df.Territory.isin(st.session_state.terr_sel)) &


	(sales_df.Category.isin(st.session_state.cat_sel)) &


	(pd.to_datetime(sales_df.MonthID) >= st.session_state.months_sel[0]) & 


	(pd.to_datetime(sales_df.MonthID) <= st.session_state.months_sel[1])


]



scen_1 = margin_df[margin_df.ScenarioID == 1]


scen_2 = margin_df[margin_df.ScenarioID == 2]


scen_1_grp = scen_1.groupby(

	['MonthID'], 

	as_index = False, 

	dropna = False

	).agg(

	{"Sum_GrossMarginAmount": pd.Series.sum}

	).sort_values(

	by = 'MonthID', 

	ascending = True

)


scen_1_grp.columns = ['Month', 'Sum of Gross Margin Amount for Scenario 1']



scen_2_grp = scen_2.groupby(

	['MonthID'], 

	as_index = False, 

	dropna = False

	).agg(

	{"Sum_GrossMarginAmount": pd.Series.sum}

	).sort_values(

	by = 'MonthID', 

	ascending = True

)



scen_2_grp.columns = ['Month', 'Sum of Gross Margin Amount for Scenario 2']



scenario_tab = pd.merge(

	scen_1_grp, 

	scen_2_grp, 

	how = 'inner', 

	on = 'Month'


	)



scenario_tab['Total Gross Margin Amount'] = scenario_tab.apply(

	lambda x: x[1] + x[2], 

	axis = 1

	)



scenario_tab['Gross Percentage'] = scenario_tab.apply(

	lambda x: round((x[1] / x[3]) * 100, 2), 

	axis = 1

	)




# Display Scenario Table


# st.dataframe(data = scenario_tab, use_container_width = True, hide_index = True)



# Totals Scenario Table


scen_vals =[

	
	"Total",

	scenario_tab.apply(lambda x: x[1], axis = 1).sum(), 

	scenario_tab.apply(lambda x: x[2], axis = 1).sum(), 

	scenario_tab.apply(lambda x: x[3], axis = 1).sum(), 

	scenario_tab.apply(lambda x: x[4], axis = 1).mean()

]


scen_names = scenario_tab.columns.values.tolist()


scen_dict = {k: v for k, v in zip(scen_names, scen_vals)}


scenario_totals = pd.DataFrame([scen_dict])



scenario_tab['Gross Percentage'] = scenario_tab.apply(

	lambda x: (str(round((x[1] / x[3]) * 100, 2)) + "%").strip(), 

	axis = 1

	)



scenario_tab['Total Gross Margin Amount'] = scenario_tab['Total Gross Margin Amount'].apply(

	lambda x: f"${int(x):,d}"


	)


scenario_tab['Sum of Gross Margin Amount for Scenario 2'] = scenario_tab['Sum of Gross Margin Amount for Scenario 2'].apply(


	lambda x: f"${int(x):,d}"


	)



scenario_tab['Sum of Gross Margin Amount for Scenario 1'] = scenario_tab['Sum of Gross Margin Amount for Scenario 1'].apply(


	lambda x: f"${int(x):,d}"


	)


scenario_tab['Month'] = scenario_tab['Month'].apply(

	lambda x: dt.datetime.strftime(x, "%B %Y")


	)





scenario_totals['Gross Percentage'] = scenario_totals['Gross Percentage'].apply(

	lambda x: (str(round(x, 2)) + "%").strip()

	)



scenario_totals['Total Gross Margin Amount'] = scenario_totals['Total Gross Margin Amount'].apply(

	lambda x: f"${int(x):,d}"


	)


scenario_totals['Sum of Gross Margin Amount for Scenario 2'] = scenario_totals['Sum of Gross Margin Amount for Scenario 2'].apply(


	lambda x: f"${int(x):,d}"


	)



scenario_totals['Sum of Gross Margin Amount for Scenario 1'] = scenario_totals['Sum of Gross Margin Amount for Scenario 1'].apply(


	lambda x: f"${int(x):,d}"


	)



final_scenario_table = pd.concat(

	[scenario_tab, scenario_totals], 

	axis = 0, 

	ignore_index = True

	)


# Display Final Scenario Table


st.write("<h3><center>Final Scenario Table</center></h3><br>", unsafe_allow_html = True)


st.dataframe(data = final_scenario_table, hide_index = True, use_container_width = True)




# CSS Styling Of Elements


def styling_func():


	css = '''


		div[class^='st-emotion-cache-16txtl3'] { 


		 padding-top: 1rem; 


		}


		div[class^='block-container'] { 

		  padding-top: 1rem; 

		}


		[data-testid="stMetric"] {
		    width: fit-content;
		    margin: auto;
		}

		[data-testid="stMetric"] > div {
		    width: fit-content;
		    margin: auto;
		}

		[data-testid="stMetric"] label {
		    width: fit-content;
		    margin: auto;
		}


		[data-testid="stMarkdownContainer"] > p {

          font-weight: bold;

        }


        [data-testid="stMetricValue"] {

          font-weight: bold;
          
        }


        [aria-label="Selected Districts"] {

          font-weight: bold;

        }


        span[class^='st-ar st-c9 st-ca st-cb st-cc st-af'] {

          font-weight: bold;

        }


        div[class^='st-ak st-al st-bc st-bd st-be st-as st-bf st-dk st-ar st-dl st-dm st-dn st-do'] {

          font-weight: bold;

        }


        div[class^='StyledThumbValue st-emotion-cache-10y5sf6 ew7r33m2'] {
        

          font-weight: bold;


        }


        div[class^="st-emotion-cache-1inwz65"] {

          font-weight: bold;

        }

        div[class^="st-emotion-cache-16idsys e1nzilvr5"] {

          color: #262730;

        }


        div[class^="st-emotion-cache-1xarl3l e1i5pmia1"]{

          font-size: 33px;

        }


	'''


	st.write(


		f"<style>{css}</style>", 


		unsafe_allow_html = True
		

	)





styling_func()









# Footer Section



# Mention Data Source



st.write("<br><br><br><br>", unsafe_allow_html = True)




# st.write(

# 	'''<footer class="css-164nlkn egzxvld1"><center><p>Data Source: <a href="https://data.telangana.gov.in/" target="_blank" class="css-1vbd788 egzxvld2">data.telangana.gov.in</a></p></center></footer>''', 


# 	unsafe_allow_html = True


# 	)

