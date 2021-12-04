import pandas as pd
import numpy as np
import math

    '''
    DCF Model:
    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None


    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model
        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the first 5 years using the short term growth rate
        4. Add the discounted value of the FCC from year 6 to the 10th year using the medium term growth rate
        5. Add the discounted value of the FCC from year 10 to the 20th year using the long term growth rate
        6. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        7. Return the stock fair value as PV divided by num of shares outstanding
        '''
        #TODO 
        # hint check out the DiscountedCashFlowModel notebook, you can almost copy-and-paste the code from there
        FCC = self.stock.get_free_cashflow()
        current_cash = self.stock.get_cash_and_short_term_investments()
        WACC = self.stock.lookup_wacc_by_beta(self.stock.get_beta())
        EPS5Y = self.short_term_growth_rate
        EPS6To10Y = self.medium_term_growth_rate
        EPS10To20Y = self.long_term_growth_rate
        total_debt = self.stock.get_total_debt()
        shares = self.stock.get_num_shares_outstanding()
        # ...
        DF = 1/(1+ WACC)
        DCF = 0
        for i in range(1, 6):
            DCF += FCC * (1+ EPS5Y)**i * DF ** i
            
        CF5 = FCC * (1+EPS5Y)**5
        for i in range(1, 6):
            DCF += CF5 * (1+EPS6To10Y)**i * DF ** (i+5)

        CF10 = CF5 * (1+EPS6To10Y)**5
        for i in range(1, 11):
            DCF += CF10 * (1+EPS10To20Y)**i * DF **(i + 10)
            
        PV = current_cash - total_debt + DCF
        result = PV/shares
        #end TODO
        return(result)
