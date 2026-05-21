from calculators import loan_calculator as lc
import utilities as ut

#########################################################################################
#
# Variables
#
#########################################################################################
principal = 90000
period = "year"  # month / year
N = 10  # total number of months / years
r = 3  # annual interest rate (in %)

want_csv = True
CSV_FILE = "files/loan.csv"

plot = True

#########################################################################################
#
# / Variables
#
#########################################################################################

#########################################################################################
#
# Main
#
#########################################################################################
# Adjust r and N to selected period
r = r / 1200  # Compound interest always calculated monthly
if period.lower() == "year":
    N = N * 12
elif period.lower() == "month":
    pass
else:
    print(ut.st("error", "Invalid Period"))
    exit(1)

lc.calculate_loan(
    principal,
    N,
    r,
    period=period,
    tocsv=want_csv,
    csv_file=CSV_FILE,
    verbose=True,
    plot=plot,
)

#########################################################################################
#
# / Main
#
#########################################################################################