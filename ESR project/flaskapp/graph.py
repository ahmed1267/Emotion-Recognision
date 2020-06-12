import plotly.graph_objs as go
import plotly
import json

def create_plot(x,y):
	"""
		create_plot(x,y)
		it's take two axis and return a countplot graph
		using plotly
	"""
	fig = go.Figure()
	data = [
		go.Bar(
			x=x, # assign x as the dataframe column 'x'
			y=y,

		)
	]

	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON