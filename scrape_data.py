import json
import thingspeak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import re

ch = thingspeak.Channel(202842)
data = json.loads(ch.get({'results': 10000}))

data = map(lambda x: [x['created_at'], x['field1']], data['feeds'])
data = list(filter(lambda x: x[1] is not None, data))
# x = map(lambda x: [datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%SZ')], data)
# y = map(lambda x: [float(x[1])], data)

x, y = [], []
for i in range(len(data)):
    x.append(datetime.strptime(data[i][0], '%Y-%m-%dT%H:%M:%SZ'))
    y.append(float(data[i][1]))

# print(x, '\n\n\n', y)

# plt.plot(x, y)
# plt.ylabel('some numbers')

# plt.show()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.plot(x,y)
plt.gcf().autofmt_xdate()
plt.show()
