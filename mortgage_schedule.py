import numpy as np


class MortgagePaymentSchedule():
    def __init__(
        self,
        interest_pct_annual, 
        term_years,
        initial_amount
    ):
        self.interest_pct_annual = interest_pct_annual
        self.term_years = term_years
        self.initial_amount = initial_amount
        self._outstanding = None
        self._interest_added = None
        
    @property
    def interest_monthly(self):
        return self.interest_pct_annual / 1200
    
    @property
    def term_months(self):
        return self.term_years * 12
    
    @property
    def repayment(self):
        r = self.interest_monthly
        term = self.term_months
        return self.initial_amount * (r * (1 + r) ** term) / ((1 + r) ** term - 1)
    
    def compute_schedule(self):
        self._outstanding = np.zeros(self.term_months + 1)
        self._outstanding[0] = self.initial_amount
        self._interest_added = np.zeros(self.term_months)
        
        for i in range(self.term_months):
            self._interest_added[i] = self._outstanding[i] * self.interest_monthly
            self._outstanding[i + 1] = self._outstanding[i] * (1 + self.interest_monthly) - self.repayment
    
    @property
    def outstanding(self):
        if self._outstanding is None:
            self.compute_schedule()
        return self._outstanding
    
    @property
    def interest_added(self):
        if self._interest_added is None:
            self.compute_schedule()
        return self._interest_added
    
    @property
    def total_interest(self):
        return self.interest_added.sum()
    
    @property 
    def total_interest_pct(self):
        return self.total_interest / self.initial_amount * 100.


def optimal_term_for_target_monthly_repayment(initial_amount: float, interest_pct_annual: float, target_monthly_repayment: float, max_years: int=25):
    """
    Compute the approximate optimal term for a given monthly repayment target
    """
    yr_dict = {}
    above = None

    for yr in range(max_years + 1, 0, -1):
        obj = MortgagePaymentSchedule(interest_pct_annual=interest_pct_annual, term_years=yr, initial_amount=initial_amount)
        yr_dict[yr] = obj.repayment
    
        if yr_dict[yr] > target_monthly_repayment:
            above = yr
            break
        
        below = yr

    return below, above, yr_dict
