def initialize():
    ''' Initializes global variables to initial state '''
    global is_disabled
    is_disabled = False # Boolean: true iff card has been disabled

    global last_day, last_month
    last_day = 0 # int, holds the day of the last transaction
    last_month = 0 # int, holds the month of the last transaction

    global country_list
    country_list = [None, None] # List of 2 strings that holds the last 2 countries the transaction was made in. Most recent is in index 0

    global uninteresting_debt, interesting_debt
    uninteresting_debt = 0 # How much debt has been accrued this month
    interesting_debt = 0 # How much debt is gaining interest

    global INTEREST_RATE
    INTEREST_RATE = 0.05 # How much interest is compounded monthly

def date_same_or_later(day1, month1, day2, month2):
    ''' Return True iff the date specified by day1, month1 is the same day as day2, month2, or occurs after day2, month2. All parameters are ints '''
    if month1 < month2: return False
    if month1 > month2: return True
    return day1 >= day2 # If the months are the same, then days must be checked

def all_three_different(c1, c2, c3):
    ''' Return True iff all three values of c1, c2, and c3 are different. If any value is None,
    then automatically return true'''
    if c1 == None or c2 == None or c3 == None:
        return False # Prevents None from being treated as a unique country
        # For this code, only c1 needs to be checked for None
    return c1 != c2 and c2 != c3 and c1 != c3 # c1 != c2 and c2!= c3 does not imply c1 != c3

def purchase(amount, day, month, country):
    ''' Simulate a purchase. If the card is disabled, or the date given by day, month comes
    before the last transaction, return "error" and nothing more is done. Otherwise, update date
    and debt variables (see update_date() for implementation). Then, If this country
    and the last two countries are all different, disable the card and return "error".
    Otherwise, increment uninteresting_debt by amount and return None.
    Amount is a float, day and month are ints, and country is a string. '''

    global is_disabled

    if is_disabled:
        # Initial check for disabled card
        return "error"

    global countries
    if all_three_different(country_list[0], country_list[1], country):
        # Check for if the last 3 visited countries are all different
        is_disabled = True
        return "error"

    if not update_date(day, month): return "error"
    # Checks if the given date is valid and updates debts when appropriate, see update_date for implementation.

    # All conditions are passed
    global uninteresting_debt
    uninteresting_debt += amount
    # Shift countries over one
    country_list[1] = country_list[0]
    country_list[0] = country
    return None

def amount_owed(day, month):
    ''' Return "error" if the date specified by day, month comes before the last transaction
    date. Otherwise, return the amount owed on the date specified by day, month (after
    calculating interest). Day, month should specify a valid date as ints. '''
    if not update_date(day, month): return "error"
    # Checks if the given date is valid and updates debts when appropriate, see update_date for implementation.

    return uninteresting_debt + interesting_debt

def pay_bill(amount, day, month):
    ''' Return "error" if the date specified by day, month comes before the last transaction
    date. Otherwise, reduces the current debt by amount, first discounting from interesting_debt
    and then discounting from uninteresting_debt. Amount is a float greater than 0, and day,
    monthshould specify a valid date as ints '''
    if not update_date(day, month): return "error"
    global interesting_debt, uninteresting_debt
    if amount <= interesting_debt:
        # If the payment cannot fully pay off the interesting_debt
        interesting_debt -= amount
    else:
        # If the payment is more than interesting_debt, set interesting to 0
        # and remove the difference from uninteresting_debt
        uninteresting_debt -= (amount - interesting_debt)
        interesting_debt = 0

def update_date(curr_day, curr_month):
    ''' Return False if the date given by curr_day, curr_month is invalid (before last_day,
    last_month). Otherwise, update last_day and last_month variables appropriately. If the
    month is incremented, apply interest for each additional month (where uninteresting_debt
    skips interest the first month), and return True after all operations are complete.
    curr_day, curr_month should specify a valid date as ints.
    '''

    global last_day, last_month

    if not date_same_or_later(curr_day, curr_month, last_day, last_month):
        # Check for if date given is invalid (comes before last transaction)
        return False

    last_day = curr_day # Always update the day, even if the days are the same.

    if curr_month > last_month:     # Only update debts if the month is incremented
        months_passed = curr_month - last_month # The number of months to accumulate interest
        last_month = curr_month

        global interesting_debt, uninteresting_debt
        interesting_debt *= (1 + INTEREST_RATE) ** months_passed
        # Multiplies the interesting_debt by INTEREST_RATE for each month that passes
        interesting_debt += uninteresting_debt * (1 + INTEREST_RATE) ** (months_passed - 1)
        # Same as the interesting_debt but doesn't include the first month
        uninteresting_debt = 0
        # All the uninteresting_debt is transferred to interesting_debt
    return True

initialize()
## Testing
if __name__ == "__main__":
    ## Testing date_same_or_later()
    print("\ndate_same_or_later: ") # Tests important dates' relationship
    print("1, 1 is after 1, 1:", date_same_or_later(1, 1, 1, 1)) # Same T
    print("1, 2 is after 1, 1:", date_same_or_later(1, 2, 1, 1)) # Month bigger T
    print("1, 1 is after 1, 2:", date_same_or_later(1, 1, 1, 2)) # Month smaller F
    print("2, 1 is after 1, 1:", date_same_or_later(2, 1, 1, 1)) # Day bigger T
    print("1, 1 is after 2, 1:", date_same_or_later(1, 1, 2, 1)) # Day smaller F
    print("2, 2 is after 1, 1:", date_same_or_later(2, 2, 1, 1)) # Both bigger T
    print("2, 1 is after 1, 2:", date_same_or_later(2, 1, 1, 2)) # Day bigger, month smaller F
    print("1, 2 is after 2, 1:", date_same_or_later(1, 2, 2, 1)) # Day smaller, month bigger T

    ## Testing all_three_different()
    print("\nall_three_different: ") # Tests multiple cases
    print("1, 1, 1", all_three_different(1, 1, 1))
    print("1, 2, 1", all_three_different(1, 2, 1))
    print("1, 1, 2", all_three_different(1, 1, 2))
    print("2, 1, 1", all_three_different(2, 1, 1))
    print("0, 1, 0", all_three_different(0, 1, 0))
    print("0, 0, 1", all_three_different(0, 0, 1))
    print("1, 0, 0", all_three_different(1, 1, 0))
    print("1, 0, None", all_three_different(1, 0, None))

    print("2, 1, 3", all_three_different(2, 1, 3)) # Only this one should return true

    ## Test A1: Interest with $0
    print("\n$0 Interest") # Base case, checking for $0 functionality
    initialize()
    print(amount_owed(1, 1))
    print(amount_owed(1, 12))
    # Should maintain $0 throughout the months

    ## Test A2: Generic interest
    print("\nGeneric Interest:") # Testing simple interest with $1200 principal, seeing if basic interest functions properly
    initialize()
    purchase(1200, 1, 1, "CANADA")
    for i in range(1, 13):
        print("Month " + str(i) + ":", amount_owed(1, i))
        # Prints the interest accrued each month: should follow 1020*1.05^(n-2)
        # At December, should be 1200 * 1.05^10 = $1954.67

    ## Test A3: $100 each month
    print("\n$100 purchase + interest each month") # Testing $100 payments each month to see if debt accruement works properly
    initialize()

    for i in range(1, 13):
        purchase(100, 1, i, "CANADA")
        print("Month " + str(i) + ":", amount_owed(1, i))
        # Prints the interest accrued each month.
        # At the end, the interest should be 100 (dec) + 100 (nov) + 100 * 1.05 (oct) + 100 * 1.05 ** 2 (sep) + ... + 100 * 1.05 ** 10 (jan) = $1520.68

    ## Test B1: Purchase $100 pay $100 each month
    print("\nPurchase $100 and Pay $100 each week") # Confirms whether or not purchase and pay work in sync with each other
    initialize()

    for i in range(1, 4):
        purchase(100, 1, i, "CANADA")
        pay_bill(100, 1, i)
        print("Month " + str(i) + ":", amount_owed(1, i))

    ## Test B2: Purchase and Pay
    print("\nPurchase and Pay") # Test paying off bills in the middle of accruing interest
    initialize()

    purchase(100, 1, 1, "CANADA")
    print("Month 1:", amount_owed(1, 1)) # $100 uninteresting, $0 interesting
    print("Month 2:", amount_owed(1, 2)) # $0 uninteresting, $100 interesting,

    # $100 * 1.05 = $105 after interest
    pay_bill(100, 1, 3) # $0 uninteresting, $105 - 100 = $5 interesting
    purchase(100, 1, 3, "CANADA")
    print("Month 3:", amount_owed(1, 3)) #$100 uninteresting, $5 interesting
    print("Month 4:", amount_owed(1, 4)) #$0 uninteresting, $105.25 interesting

    # $105.25 * 1.05 = $110.51 after interest
    pay_bill(100, 1, 5) # $0 uninteresting, $110.51 - 100 = $10.51 interesting
    purchase(100, 1, 5, "CANADA")
    print("Month 5:", amount_owed(1, 5)) # $100 uninteresting, $10.51 interesting
    print("Month 6:", amount_owed(1, 6)) # $0 uninteresting, $111.04 interesting

    purchase(100, 1, 6, "CANADA")
    #Pay whole bill ($211.04) --> testing paying current bill
    pay_bill(211.04, 1, 6)
    print("Final Amount month 6:", amount_owed(1,6))

    ## Test C: Errors
    print("\nError testing") # Check all potential errors (date, lock, and is_locked)
    initialize()

    purchase(100, 1, 1, "CANADA")
    purchase(100, 1, 2, "EAST CANADA")
    print("Testing all 3 functions' date errors:")
    print(purchase(100, 1, 1, "CANADA"))
    print(amount_owed(1, 1))
    print(pay_bill(100, 1, 1))

    purchase(50, 1, 2, "EAST CANADA")
    purchase(50, 1, 2, "NORTH CANADA") # No disabling, since last two countries are EAST CANADA, EAST CANADA, and NORTH CANADA

    print("\nInvalid date + 3 countries: Should disable the card")
    print(purchase(100, 1, 1, "SOUTH CANADA")) # Should disable the card completely
    print(purchase(100, 10, 2, "CANADA"))
    print("Amount owed:", amount_owed(1, 5)) # Should go through, because a disabled card won't update the date with an invalid purchase (200 + 100*1.05) * 1.05 ^ 2 = $336.2625


    print("\n2 purchases -- Should be disabled (1st b/c date, 2nd b/c disabled)")
    print(purchase(100, 1, 1, "BRAZIL")) # Date before last purchase
    print(purchase(100, 1, 12, "BRAZIL")) # Date after, but still error because disabled (date is not updated)
    print("Current debt: $", amount_owed(1, 12), sep = "") # Interest should apply --> (200 + 100 * 1.05) * 1.05^ 9 = $473.16

    print("\nInvalid date - Latest transaction at Dec 1")
    print(amount_owed(1, 4), sep = "") # Will not run because time has already advanced to Dec 1

    ## Test D: Sample provided
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1)) #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2)) #30.0 (=80-50)
    print("Now owing:", amount_owed(6, 3)) #31.5 (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3)) #71.5 (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3)) #41.5 (=71.5-30)
    print("Now owing:", amount_owed(1, 5)) #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5)) #83.65375
    print(purchase(50, 3, 5, "United States")) #error (3 diff. countries in
    # a row)
    print("Now owing:", amount_owed(3, 5)) #83.65375 (no change, purchase
    # declined)
    print(purchase(150, 3, 5, "Canada")) #error (card disabled)
    print("Now owing:", amount_owed(1, 6)) #85.8364375
    #(43.65375*1.05+40)

    ##
    print("TEST CASE 13")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "France")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80 interest building debt
    purchase(80, 1, 2, "China")  # FRAUD - ERROR, still 80
    purchase(80, 2, 2, "France")  # ALREADY FRAUD - ERROR, still 80
    print("Now owing:", amount_owed(29, 2))  # 80 (80 interest, 0 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 84.0 (84 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 4.0 (4 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # ALREADY FRAUD - ERROR, still 4
    purchase(80, 2, 3, "France")  # ALREADY FRAUD - ERROR, still 4
    print("Now owing:", amount_owed(31, 3))  # 4.0 (4 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 4.2 (4.2 interest, 0 non-interest)

    ##
# regular purchase (1 /month), pays back at beginning of next month
    print("TEST CASE 1")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(80, 1, 2)
    purchase(80, 1, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 80.0
    pay_bill(80, 1, 3)
    purchase(80, 1, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 80.0

    # regular purchase (1 /month), pays half at beginning of next month
    print("TEST CASE 2")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(40, 1, 2)  # 40
    purchase(80, 1, 2, "Canada")  # 120 (40 + 80)
    print("Now owing:", amount_owed(29, 2))  # 120.0 (40 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 122.0 (40*1.05+80 interest, 0 non-interest)
    pay_bill(40, 1, 3)  # 82.0 (82 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 162.0 (82 interest, 80 non-interest)
    print("Now owing:", amount_owed(31, 3))  # 162.0 (82 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 166.1 (86.1+80 interest, 0 non-interest)

    # regular purchase (2 /month), pays back at beginning of next month
    print("TEST CASE 3")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(160, 1, 2)
    purchase(80, 1, 2, "Canada")
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 80.0
    pay_bill(160, 1, 3)
    purchase(80, 1, 3, "Canada")
    purchase(80, 2, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 80.0

    # regular purchase (2 /month), pays half at beginning of next month
    print("TEST CASE 4")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # buy once, pay in june in full, check in december
    print("TEST CASE 5")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(15, 6))  # 80->80->84->88.2->92.61->97.2405(in june)
    pay_bill(97.24050000000001, 15, 6)
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))

    # buy once, pay in june in partial, check in december
    print("TEST CASE 6")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(15, 6))  # 80->80->84->88.2->92.61->97.2405(in june)
    pay_bill(10, 15, 6)  # 87.2405 remaining
    print("Now owing:", amount_owed(15, 6))  # 87.2405->91.602525(july)->96.18265125->100.9917838125->106.0413730031->
    print("Now owing:", amount_owed(31, 12))  # 111.3434416533 in november -> 116.9106137359 in december

    # buy once, buy again in early june, pay in june in full for jan debt+interest, check in december
    print("TEST CASE 7")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(97.2405, 15, 6)  # 80 new debt remaining
    print("Now owing:", amount_owed(15, 6))  # 80
    print("Now owing:", amount_owed(31, 12))  # 80->80->84->88.2->92.61->97.2405->102.102525

    # buy once, buy again in early june, pay in june (slightly more than jan debt+interest), check in december
    print("TEST CASE 8")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(100, 15, 6)  # 77.2405 (all new debt) remaining
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))  # 77.2405->77.2405->81.102525->85.15765125
    # ->89.4155338125->93.8863105031->98.5806260283 (at dec)

    # buy once, buy again in early june, pay in june (slightly less than jan debt+interest), check in december
    print("TEST CASE 9")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(90, 15, 6)  # 87.2405 remaining (7.2405 old debt)
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))  # 80+7.2405(june)->80+7.602525 (87.602525)->91.98265125->96.5817838125
    # ->101.4108730031->106.4814166533->111.805487486

    # buy once, forget about the card
    print("TEST CASE 10")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 12))  # 80->80(feb)->(80*1.05^10)(dec)130.3115701422

    # buy once, pay back immediately forget about the card
    print("TEST CASE 11")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    pay_bill(80, 1, 1)
    print("Now owing:", amount_owed(31, 12))  # 0

    # TEST 4 but with alternating 2 countries
    print("TEST CASE 12")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "France")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "France")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "France")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # TEST 4 but with alternating 3 countries
    print("TEST CASE 13")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "France")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80 interest building debt
    purchase(80, 1, 2, "China")  # FRAUD - ERROR, still 80
    purchase(80, 2, 2, "France")  # ALREADY FRAUD - ERROR, still 80
    print("Now owing:", amount_owed(29, 2))  # 80 (80 interest, 0 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 84.0 (84 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 4.0 (4 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # ALREADY FRAUD - ERROR, still 4
    purchase(80, 2, 3, "France")  # ALREADY FRAUD - ERROR, still 4
    print("Now owing:", amount_owed(31, 3))  # 4.0 (4 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 4.2 (4.2 interest, 0 non-interest)

    # TEST 4 but with same country -> then 2 other countries
    print("TEST CASE 14")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "China")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "France")  # FRAUD, STILL 244 (164 interest, 80 non-interest)
    print("Now owing:", amount_owed(31, 3))  # 244 (164 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 252.2 (164*1.05+80 interest, 0 non-interest)

    # TEST 4 but with 3 countries, but each country purchase twice
    print("TEST CASE 15")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "France")  # 160 (80 + 80)
    purchase(80, 2, 2, "France")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "China")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "China")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # Fraud early on, but don't pay back
    print("TEST CASE 16")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 1, "France")
    purchase(30, 2, 1, "Germany")
    purchase(30, 3, 1, "Germany")
    print("Now owing:", amount_owed(31, 1))  # 130.0
    print("Now owing:", amount_owed(31, 2))  # 130.0
    print("Now owing:", amount_owed(31, 3))  # 130*1.05
    print("Now owing:", amount_owed(31, 12))  # 130*1.05**10=211.7563014811

    # Fraud early on, but pay back
    print("TEST CASE 17")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 1, "France")
    purchase(30, 2, 1, "Germany")
    purchase(30, 3, 1, "Germany")
    pay_bill(130, 3, 1)
    print("Now owing:", amount_owed(31, 1))  # 0
    print("Now owing:", amount_owed(31, 2))  # 0
    print("Now owing:", amount_owed(31, 3))  # 0
    print("Now owing:", amount_owed(31, 12))  # 0

    # Fraud early on, but pay back
    print("TEST CASE 18")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 2, "France")
    pay_bill(90, 3, 2)  # now owe 40 non interest
    purchase(30, 3, 3, "Germany")
    purchase(30, 4, 4, "Germany")
    print("Now owing:", amount_owed(31, 3))  # 40 interested money
    print("Now owing:", amount_owed(31, 12))  # 40*1.05**9
