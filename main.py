import QuantLib as ql

# American call options

SPOT_PRICE = 188.64
RISK_FREE_RATE = 0.0525
DIVIDEND_YIELD = 0.0052
VOLATILITY = 0.20
DAYS_TO_MATURITY = 148
STRIKE_PRICE = 190
OPTION_PRICE = 11.05

calendar = ql.NullCalendar()
day_count = ql.Actual360()
today = ql.Date().todaysDate()

ql.Settings.instance().evaluationDate = today
risk_free_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(today, RISK_FREE_RATE, day_count)
)
dividend_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(today, DIVIDEND_YIELD, day_count)
)
spot_handle = ql.QuoteHandle(ql.SimpleQuote(SPOT_PRICE))

expiration_date = today + ql.Period(DAYS_TO_MATURITY, ql.Days)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, STRIKE_PRICE)
exercise = ql.AmericanExercise(today, expiration_date)
american_option = ql.VanillaOption(payoff, exercise)

volatility_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, ql.TARGET(), VOLATILITY, ql.Actual365Fixed()))

# Black-Scholes-Merton
bsm_process = ql.BlackScholesMertonProcess(
    spot_handle, dividend_ts, risk_free_ts, volatility_handle
)

# Binomial Vanilla Engine with the Cox-Ross-Rubinstein (CRR) method
engine = ql.BinomialVanillaEngine(bsm_process, "crr", 1000)
american_option.setPricingEngine(engine)

implied_volatility = american_option.impliedVolatility(
    OPTION_PRICE, bsm_process, 1e-4, 1000, 1e-8, 4.0
)

print("Implied Volatility: ", implied_volatility)
