DAYS_PER_YEAR = 365.
MONTHS_PER_YEAR = 12


def calculate_cd(principle: float, rate: float, term: float) -> (float, float):
    '''
    This function returns average monthly dividend and total amount at end of term.

    :param principle: float, the starting capital, dollars
    :param rate: float, the annual interest rate, fraction
    :param term: float, the term, months
    :return: (float, float), a Tuple of the mean monthly return and total at end of term
    '''

    total = principle * (1 + rate / DAYS_PER_YEAR) ** (term * DAYS_PER_YEAR / MONTHS_PER_YEAR)
    mean_return = (total - principle) / term

    return mean_return, total


cd_options = {
    '8-Month': (0.0512, 8),
    '15-Month': (0.0512, 15),
    '29-Month': (0.0405, 29)
}
