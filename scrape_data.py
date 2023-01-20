from datetime import datetime, timedelta
from bokeh.plotting import figure, ColumnDataSource, figure, curdoc
from bokeh.models import DatetimeTickFormatter, Slider, HoverTool, Slider, DatePicker, Select
from bokeh.layouts import row, column
from bokeh.client import push_session
import requests


date = datetime.now().replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
end_data_global = str(date + timedelta(days=1))
labels = ['temperature']
for_index = ['temperature', 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180']

def get_data_by_day_number(start_data = None, end_data = None):
    if start_data is None:
        start_data = str(date)
    if end_data is None:
        end_data = str(end_data_global)
    response = requests.get('https://api.thingspeak.com/channels/202842/feeds.json?start={start_data}&end={end_data}'.format(start_data=start_data, end_data=end_data))
    data = response.json()
    data = list(map(lambda x: [x['created_at'], x['field1'], x['field2'], x['field3'], x['field4'], x['field5'], x['field6'], x['field7'], x['field8']], data['feeds']))

    plot_data = {}
    for [index, label] in enumerate(labels):
        temp_data = list(filter(lambda x: x[1 + for_index.index(labels[0])] is not None, data.copy()))

        plot_data[label] = {
            'dates': list(map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], temp_data.copy())),
            'values': list(map(lambda x: [float(x[1 + for_index.index(labels[0])])], temp_data.copy()))
        }
    return plot_data[labels[0]]


plot = figure(title="Dane z sali L.2.7.14BT", x_axis_label="x", x_axis_type="datetime", y_axis_label="y")

plot.xaxis.formatter=DatetimeTickFormatter(
    hours=["%d.%m.%y %H:%M"],
)

source = ColumnDataSource(data = get_data_by_day_number())

plot.line(x='dates', y='values', source=source, line_width=2)

#slider
slider = Slider(start=1, end=31, value=11, step=1, title="Day")
def slider_callback(attr, old, new):
    source.data=get_data_by_day_number()
slider.on_change('value', slider_callback)

#hover
hover = HoverTool(tooltips=[('data', '@dates{%d.%m.%y %H:%M}'), ("wartość", "@values")],
          formatters={'@dates': 'datetime'})
plot.tools.append(hover)

#datepicker
def date_picker_callback(attr, old, new):
    global date
    date = datetime(int(new[0:4]), int(new[5:7]), int(new[8:10]))
    source.data=get_data_by_day_number()
date_picker = DatePicker(title='Select starting date:', value="2023-01-20", min_date="2022-01-12", max_date="2024-01-12")
date_picker.on_change('value', date_picker_callback)

#datepicker end
def date_end_picker_callback(attr, old, new):
    global end_data_global
    end_data_global = datetime(int(new[0:4]), int(new[5:7]), int(new[8:10]))
    source.data=get_data_by_day_number(end_data=end_data_global)
date_picker_end = DatePicker(title='Select end date:', value="2023-01-20", min_date="2022-01-12", max_date="2024-01-12")
date_picker_end.on_change('value', date_end_picker_callback)

#select
def select_callback(attr, old, new):
    global labels
    labels = [new]
    source.data=get_data_by_day_number(end_data=end_data_global)
select = Select(title="Sensor:", value="temperature", options=['temperature', 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180'])
select.on_change('value', select_callback)

layout = row(
    plot,
    column(
        row(date_picker, date_picker_end),
        select
    )
)

curdoc().add_root(layout)

session = push_session(curdoc())
session.show(layout)
session.loop_until_closed()