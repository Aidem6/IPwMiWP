import json
import thingspeak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

ch = thingspeak.Channel(202842)
data = json.loads(ch.get({'results': 5000}))

data_structure = {
    "created_at": "2016-12-13T13:54:29Z",
    "description": "Monitoring parametr\u00f3w mikroklimatu wewn\u0105trz pomieszczenia (temperatura, wilgotno\u015b\u0107, ci\u015bnienie, nat\u0119\u017cenie \u015bwiat\u0142a, ruch) ",
    "field1": "Temperatura (DHT-22) [\u00b0C]",
    "field2": "Wilgotno\u015b\u0107 wzgl\u0119dna (DHT-22) [%]",
    "field3": "Nat\u0119\u017cenie \u015bwiat\u0142a (BH-1750) [lx]",
    "field4": "Ci\u015bnienie atm. (BMP-180) [hPa]",
    "field5": "Temp. grzejnika (DS18B20) [\u00b0C]",
    "field6": "Temperatura (DS18B20) [\u00b0C]",
    "field7": "Ruch (PIR)",
    "field8": "Temperatura  (BMP-180) [\u00b0C]",
    "id": 202842,
    "last_entry_id": 2749954,
    "latitude": "52.403363",
    "longitude": "16.949372",
    "name": "L.2.7.14BT",
    "updated_at": "2018-09-04T07:49:05Z"
  }

data = list(map(lambda x: [x['created_at'], x['field1'], x['field2'], x['field3'], x['field4'], x['field5'], x['field6'], x['field7'], x['field8']], data['feeds']))

plot_data = {}
labels = ['temperature', 'humidity', 'light', 'pressure', 'radiator_temperature', 'temperature_DS18B20', 'movement', 'temperature_BMP180']
for [index, label] in enumerate(labels):
    temp_data = list(filter(lambda x: x[1 + index] is not None, data.copy()))
    plot_data[label + '_dates'] = list(map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], temp_data.copy()))
    plot_data[label + '_values'] = list(map(lambda x: [float(x[1 + index])], temp_data.copy()))

fig, axs = plt.subplots(8)
plt.gcf().autofmt_xdate()
fig.suptitle('Data from L.2.7.14BT')
for [index, label] in enumerate(labels):
    axs[index].plot(plot_data[label + '_dates'], plot_data[label + '_values'])
    axs[index].set_title(label)
    axs[index].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.subplots_adjust(hspace=1)

plt.show()
