from datetime import datetime, timedelta
from bokeh.plotting import figure, ColumnDataSource, figure, curdoc
from bokeh.models import DatetimeTickFormatter, Slider, HoverTool, Slider, DatePicker, MultiChoice
from bokeh.layouts import row, column
from bokeh.client import push_session
import requests


labels = ['temperature']
date = datetime.now().replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)

def get_data_by_day_number():
    print(labels)
    start_data = str(date)
    end_data = str(date + timedelta(days=1))
    print(start_data, end_data)
    response = requests.get('https://api.thingspeak.com/channels/202842/feeds.json?start={start_data}&end={end_data}'.format(start_data=start_data, end_data=end_data))
    data = response.json()
    data = list(map(lambda x: [x['created_at'], x['field1'], x['field2'], x['field3'], x['field4'], x['field5'], x['field6'], x['field7'], x['field8']], data['feeds']))

    plot_data = {'dates': [], 'values': []}
    # labels = ['temperature', 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180']
    for [index, label] in enumerate(labels):
        temp_data = list(filter(lambda x: x[1 + index] is not None, data.copy()))

        plot_data['dates'].append(list(map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], temp_data.copy())))
        plot_data['values'].append(list(map(lambda x: [float(x[1 + index])], temp_data.copy())))
        # plot_data[label] = {
        #     'dates': list(map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], temp_data.copy())),
        #     'values': list(map(lambda x: [float(x[1 + index])], temp_data.copy()))
        # }

    return plot_data


plot = figure(title="Simple line example", x_axis_label="x", x_axis_type="datetime", y_axis_label="y")
plot.xaxis.formatter=DatetimeTickFormatter(
    hours=["%d.%m.%y %H:%M"],
)

source = ColumnDataSource(data = get_data_by_day_number())

plot.multi_line(xs='dates', ys='values', source=source, legend_label="Temp.", line_width=2)

#slider
slider = Slider(start=1, end=31, value=11, step=1, title="Day")
def slider_callback(attr, old, new):
    print(new)
    source.data=get_data_by_day_number()
slider.on_change('value', slider_callback)

#hover
hover = HoverTool(tooltips=[('date', '@dates{%d.%m.%y %H:%M}'), ("temperatura", "@values C")],
          formatters={'@dates': 'datetime'})
plot.tools.append(hover)

#datepicker
def date_picker_callback(attr, old, new):
    global date
    date = datetime(int(new[0:4]), int(new[5:7]), int(new[8:10]))
    source.data=get_data_by_day_number()
date_picker = DatePicker(title='Select date', value="2023-01-12", min_date="2022-01-12", max_date="2024-01-12")
date_picker.on_change('value', date_picker_callback)

#Multichoice
def multichoice_callback(attr, old, new):
    global labels
    labels = new
    get_data_by_day_number()
OPTIONS = ['temperature', 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180']
multi_choice = MultiChoice(value=['temperature'], options=OPTIONS)
multi_choice.on_change('value', multichoice_callback)

layout = row(
    plot,
    column(date_picker,
    multi_choice)
)

curdoc().add_root(layout)

session = push_session(curdoc())
session.show(layout)
session.loop_until_closed()