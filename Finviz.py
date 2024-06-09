import pandas as pd
from finvizfinance.quote import finvizfinance

from finvizfinance.insider import Insider

finsider = Insider(option='top owner trade')

print(finsider.get_insider().head())

