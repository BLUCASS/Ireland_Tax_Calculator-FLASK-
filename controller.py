class Payslip:

    def get_payslip(self, salary, state) -> str:
        '''This method returns the payslip'''
        salary = float(salary)
        prsi = self.__get_prsi(salary)
        paye = self.__get_paye(salary, state)
        usc = self.__get_usc(salary)
        if usc != 0: weekly_usc = usc[-1]["weekly_total"]
        else: weekly_usc = 0
        net_salary = salary - prsi - paye - weekly_usc
        return {'salary': salary, 'prsi': prsi, 'paye': paye, 
                'net_salary': round(net_salary, 2), 'usc': weekly_usc}

    def __get_prsi(self, salary) -> float:
        '''It calculates the Paying Social Insurance (PRSI). 
        
        For more information, check the Citizens Information's webpage:
        https://shorturl.at/clBFO

        -€352 or less a week, you are exempt. 
        -Over €352 you pay 4% on all your earnings. 
        -Between €352 and €424, you get a credit to reduce the PRSI (limit €12)

        Steps:
        1. Calculate one-sixth of your earnings over €352.01.
        2. Subtract this from the max tapered credit to get your PRSI credit.
        3. Calculate the basic PRSI charge at 4% of your earnings.
        4. Deduct the PRSI credit from the PRSI charge to get the amount you pay.
        '''
        if salary <= 352: return 0
        if 352.01 <= salary <= 424: 
            one_sixth = 12 - ((salary - 352) / 6)
            four_pc = (salary * 4) / 100
            prsi = round(four_pc - one_sixth, 2)
            return prsi
        full_prsi = round(((salary * 4) / 100), 2)
        return full_prsi
    
    def __get_paye(self, salary, state) -> float:
        '''This function calculates the Income Tax Paid (PAYE), according to 
        the Revenue's website in the date this program was made.
        
        For more information, check the Revenue's webpage:
        https://shorturl.at/oyBUW

        To calculate, the amount for a single person:
        € 42000 per year
        € 807.70 per week (€ 42000 / 52)

        If the salary is less than this number, you discount the deduction from 
        the value. Otherwise, you take 20% up to this value and 40% from the rest.
        After that you sum the amounts to get the gross tax, the NET tax will be
        the gross - deduction.
        '''
        deduction = round(((1875 + 1875) / 52),2)
        if salary < 807.70:
            tax = (salary * 20) / 100
            if tax < deduction: return 0
            paye = round((tax - deduction), 2)
            return paye
        amount_taxable = salary - 807.70
        tax_standard = round(((807.70 * 20) / 100), 2)
        tax_higher = round(((amount_taxable * 40) / 100), 2)
        gross_tax = tax_higher + tax_standard
        net_tax = round((gross_tax - deduction), 2)
        return net_tax


    def __get_usc(self, salary) -> float:
        '''This function calculates your Universal Social Charge. Although you 
        may not have to pay income tax based on your entitlement to tax credits 
        or by use of losses or capital allowances, you may still have to pay the 
        Universal Social Charge on your income.
        
        For more information, check the Revenue's webpage:
        https://shorturl.at/ijnoq

        You are exempt from USC if your gross income is €13000 or less, otherwise:
        0.5%    Up to €12,012
        2%	    From €12,012.01 to €25,760
        4%	    From €25,760.01 to €70,044
        8%	    €70,044.01 and over
        11%	    Self-employed income over €100,000

        After taking theses steps, you will have the annual total, then just
        take this amount ant divide it by 52. That should be your weekly USC.
        '''
        gross_income = round((salary * 52), 2)
        if gross_income < 13000: return 0
        usc = (12012 * 0.5) / 100
        total_1 = gross_income - 12012
        usc_tot = usc
        if total_1 >= 13747.99:
            usc1 = (13747.99 * 2) / 100
            total_2 = total_1 - 13747.99
            usc_tot += usc1
            if total_2 > 44283.99:
                usc2 = (44283.99 * 4) / 100
                usc_tot += usc2
                total_3 = total_2 - 44283.99
                usc3 = (total_3 * 8) / 100
                usc_tot += usc3
                return [{'0.5': 12012.00, 'usc': round(usc, 2)},
                        {'2.0': 13747.99, 'usc': round(usc1, 2)},
                        {'4.0': 44283.99, 'usc': round(usc2, 2)},
                        {'8.0': round(total_3, 2), 'usc': round(usc3, 2)},
                        {'annual_total': round(usc_tot, 2), 
                         'weekly_total': round((usc_tot / 52), 2)}]
            usc2 = (total_2 * 4) / 100
            usc_tot += usc2
            return [{'0.5': 12012.00, 'usc': round(usc, 2)},
                    {'2.0': 13747.99, 'usc': round(usc1, 2)},
                    {'4.0': round(total_2, 2), 'usc': round(usc2, 2)},
                    {'annual_total': round(usc_tot, 2), 
                     'weekly_total': round((usc_tot / 52), 2)}]
        usc1 = (salary * 2) / 100
        usc_tot += usc1
        return [{'0.5': 12012.00, 'usc': round(usc, 2)}, 
                {'2.0': round(total_1, 2), 'usc': round(usc1, 2)}, 
                {'annual_total': round(usc_tot, 2), 
                 'weekly_total': round((usc_tot / 52), 2)}]
    
    def export_usc(self, salary) -> str:
        '''This public method exports the USC when called outside the Class'''
        usc = self.__get_usc(salary)
        return usc