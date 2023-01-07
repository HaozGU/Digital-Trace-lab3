# Import the necessary libraries
from pytrends.request import TrendReq
from flask import Flask, render_template

import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()    
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

# Create a Flask app
app = Flask(__name__)

pytrends = TrendReq(hl='en-US', tz=120)
# Set the route for the chart page
@app.route('/chart')
@timer
def chart():
    kw_list = ['apple', 'banana']
    pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='FR')
    trend_data = pytrends.interest_over_time() 
    # trend_data.to_csv('trend_data.csv')
    trend_data = trend_data.to_csv(index=True)
    # Render the chart template
    return render_template('chart.html', trend_data=trend_data)

