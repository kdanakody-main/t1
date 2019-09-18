'''Something to to with taxes.
    1. Perhaps a program which parses user's input line by line to generate a tax report
    2. Able to apply a tax rate in a pre-defined bin
    3. External program has already generated description of user's earnings
    4. Tax report must be parseable eg. json or list 
    5. Tax must be able to be applied in brackets

    Parameters:
    1. User id=
    2. User earnings=
    3. Place to search for user's earnings =
    4. tax brackets to apply =
    5. output = xyz (json file)

    Writing a policy:
    1. Bracket #xyz = lowerlimit - upperlimit @ percenttocharge%
    2. tax break for xyz = code, percentage to deduct, min and max to qualify
    3. policy # = xyz

    -Code interpreted linebyline/ errorchecked so that policy does not need to be rewritten
        if syntax error
    -Syntax for commands
        -startpol::
        -end
        -startret::uid
            prompt for uid
        -end
        -tot_earnings:xyz
        -breakdown_loc:
        -policy:
        -output:(name)

        -bracket::lower,upper,rate
            prompts for options
        -breakpol::
            prompts
        -editpol:#
        -viewpol:#

        TODO

        -in transactions
            *implement function to aggregate all transactions from a single user and sort by accounts
            *   function should also tally up tax codes
            *   export all of this data into a json file in format of <breakdown> class
        -in taxes
            *implement a function to read json breakdown files
            *add an interface which parses instructions re: how to calculate taxes
            *export tax calculation to another json file
        -in transactions again
            *read a tax summary
            *present it to the user
            *give the user an option to pay said summary
        -in taxes again
            *show a status regarding paid status of taxes
            *perhaps need a tax account class in <accounts> which <taxes> can communicate with

        '''

policy_list = []
break_list = []

in_policy = 0
in_return = 0
in_break = 0

class policy:
    def __init__(self, num):
        self.num = num
        self.brackets = {0:None} #{1: [min, max, %], 2: [min, max, %] }
        self.breaks = {0:None} # { code: [min, max, %], code [min, max, %] }
        global policy_list
        policy_list.append(self)
    def new_bracket(self, lower, upper, rate):
        index = self.brackets[list(self.brackets.keys())[-1]]
        self.brackets[index+1] = [lower, upper, rate]
        return index
    def new_break(self, code, lower, upper, rate):
        self.breaks[code] = [lower, upper, rate]
        return code
    def edit_bracket(self, index, lower=None, upper=None, rate=None):
        if index in self.brackets.keys():
            if lower:
                self.brackets[index][0] = lower
            elif upper:
                self.brackets[index][1] = upper
            elif rate:
                self.brackets[index][2] = rate
            else: return None
        else: return None
    def edit_break(self, code, lower=None, upper=None, rate=None):
        if code in self.breaks.keys():
            if lower:
                self.breaks[code][0] = lower
            elif upper:
                self.breaks[code][1] = upper
            elif rate:
                self.breaks[code][2] = rate
            else: return None
        else: return None

    
class ret:
    def __init__(self, uid, num):
        self.num = num
        self.uid = uid
        self.policy = None
        self.breakdown = None
    
class breakdown:
    def __init__(self):
        self.income = 0
        self.coded_exceptions = [] #[ [code, amount], [code, amount], [code, amount] ]
        self.uid = 0

def getcmd():
    ln = 1
    eol = 0
    while not eol:
        uin = input("Line {} ".format(ln))
        if uin == '':
            eol =1
        else:
            toparse = uin.split(':')

#parse(str, str)
# 
def parse(cmd1, cmd2):
    global in_policy
    global in_return
    global in_break
    if cmd1 == 'startpol':
        active = check_active()
        if active:
            print("Error: {} currently in progress".format())
        pol = policy(len(policy_list+1))
        in_policy = pol
        return 0
    elif cmd1 == '':
        pass

def check_active():
    if in_policy:
        return 'policy'
    elif in_break:
        return 'break'
    elif in_return:
        return 'return'
    else: return False