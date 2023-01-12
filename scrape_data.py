from datetime import datetime, timedelta
from bokeh.plotting import figure, ColumnDataSource, figure, curdoc
from bokeh.models import DatetimeTickFormatter, Slider, HoverTool, Slider, DatePicker, MultiChoice
from bokeh.layouts import row
from bokeh.client import push_session
import requests


def get_data_by_day_number(date):
    start_data = str(date)
    end_data = str(date + timedelta(days=1))
    print(start_data, end_data)
    response = requests.get('https://api.thingspeak.com/channels/202842/feeds.json?start={start_data}&end={end_data}'.format(start_data=start_data, end_data=end_data))
    data = response.json()
    data = list(map(lambda x: [x['created_at'], x['field1'], x['field2'], x['field3'], x['field4'], x['field5'], x['field6'], x['field7'], x['field8']], data['feeds']))

    plot_data = {}
    labels = ['temperature'] #, 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180']
    for [index, label] in enumerate(labels):
        temp_data = list(filter(lambda x: x[1 + index] is not None, data.copy()))

        plot_data[label] = {
            'dates': list(map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], temp_data.copy())),
            'values': list(map(lambda x: [float(x[1 + index])], temp_data.copy()))
        }
    return plot_data['temperature']


plot = figure(title="Simple line example", x_axis_label="x", x_axis_type="datetime", y_axis_label="y")

plot.xaxis.formatter=DatetimeTickFormatter(
    hours=["%d.%m.%y %H:%M"],
)

source = ColumnDataSource(data = get_data_by_day_number(datetime.now().replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)))

plot.line(x='dates', y='values', source=source, legend_label="Temp.", line_width=2)

#slider
slider = Slider(start=1, end=31, value=11, step=1, title="Day")
def slider_callback(attr, old, new):
    print(new)
    source.data=get_data_by_day_number(new)
slider.on_change('value', slider_callback)

#hover
hover = HoverTool(tooltips=[('date', '@dates{%d.%m.%y %H:%M}'), ("temperatura", "@values C")],
          formatters={'@dates': 'datetime'})
plot.tools.append(hover)

#datepicker
def date_picker_callback(attr, old, new):
    source.data=get_data_by_day_number(datetime(int(new[0:4]), int(new[5:7]), int(new[8:10])))
date_picker = DatePicker(title='Select date', value="2023-01-12", min_date="2022-01-12", max_date="2024-01-12")
date_picker.on_change('value', date_picker_callback)

layout = row(
    plot,
    date_picker,
)

curdoc().add_root(layout)

session = push_session(curdoc())
session.show(layout)
session.loop_until_closed()