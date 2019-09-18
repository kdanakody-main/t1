for x in range(len(lottoticketlist)):
	print("{}\t{}\t{}\t{}\n".format(lottoticketlist[x].value, lottoticketlist[x].nmatch, lottoticketlist[x].has_been_checked, lottoticketlist[x].registrant))

for x in range(len(lottoticketlist)):
	lottoticketlist[x].checkTicket(winning_numbers, [0, 10, 100, 1000])


