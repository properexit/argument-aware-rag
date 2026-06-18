# Worked example

**Claim** ('Loranne Ausley "voted six times to tax your savings."')

- Gold label: **False**
- Predicted label: **False**
- Rationale: The claim that Loranne Ausley voted six times to tax savings is misleading. The evidence shows she voted against measures but the specific assertion about taxing savings is not supported and contradicted by details on exemptions and exclusions in the tax laws.

## Role-targeted queries

- **support** (kept 5/20): premise = "The tax didn't touch pensions, CDs, savings accounts and 401(k) plans; it applied to investments such as stocks, bonds and mutual funds"
  - query: Evidence confirming that: The tax didn't touch pensions, CDs, savings accounts and 401(k) plans; it applied to investments such as stocks, bonds and mutual funds. Context claim: Loranne Ausley "voted six times to tax your savings."
- **support** (kept 5/20): premise = "They were against cutting the state's intangible tax"
  - query: Evidence confirming that: They were against cutting the state's intangible tax. Context claim: Loranne Ausley "voted six times to tax your savings."
- **support** (kept 5/20): premise = 'back in 2001, Rubio voted against an amendment offered by Democrats that would have increased the amount that could be exempted from the tax (but not as much as Republicans wanted)'
  - query: Evidence confirming that: back in 2001, Rubio voted against an amendment offered by Democrats that would have increased the amount that could be exempted from the tax (but not as much as Republicans wanted). Context claim: Loranne Ausley "voted six times to tax your savings."
- **support** (kept 5/20): premise = 'he cast three other votes in favor of proposals that would have cut the intangible tax in some form or another, but not eliminate it altogether. By the RPOF logic, because the tax remained in place, Rubio cast four votes to tax your savings'
  - query: Evidence confirming that: he cast three other votes in favor of proposals that would have cut the intangible tax in some form or another, but not eliminate it altogether. By the RPOF logic, because the tax remained in place, Rubio cast four votes to tax your savings. Context claim: Loranne Ausley "voted six times to tax your savings."
- **attack** (kept 5/20): premise = 'The RPOF actually is talking about three bills, and really, four votes -- a vote to lower the intangible tax rate from 1 mill to .75 mill, a vote to raise the exemption amounts, and then two votes to repeal the tax entirely'
  - query: Evidence contradicting or refuting that: The RPOF actually is talking about three bills, and really, four votes -- a vote to lower the intangible tax rate from 1 mill to .75 mill, a vote to raise the exemption amounts, and then two votes to repeal the tax entirely. Context claim: Loranne Ausley "voted six times to tax your savings."
- **attack** (kept 5/20): premise = "there weren't really six of them"
  - query: Evidence contradicting or refuting that: there weren't really six of them. Context claim: Loranne Ausley "voted six times to tax your savings."
- **attack** (kept 5/20): premise = 'Republican U.S. Senate nominee Marco Rubio voted four times to tax your savings -- in one year'
  - query: Evidence contradicting or refuting that: Republican U.S. Senate nominee Marco Rubio voted four times to tax your savings -- in one year. Context claim: Loranne Ausley "voted six times to tax your savings."
- **attack** (kept 5/20): premise = 'saying "savings" is a bit broad'
  - query: Evidence contradicting or refuting that: saying "savings" is a bit broad. Context claim: Loranne Ausley "voted six times to tax your savings."
- **attack** (kept 5/20): premise = "the votes in question weren't for tax hikes"
  - query: Evidence contradicting or refuting that: the votes in question weren't for tax hikes. Context claim: Loranne Ausley "voted six times to tax your savings."

## Evidence by role

### support (20 passages)

- role_fit=1.00 nli=entailment pid=2251::13
  > The second problem is that even those families that do pay the tax would not pay it on half their savings, as the ad states. Because of the exclusions, the "effective" tax rate -- that is, the tax levied divided by the total amount of assets considered under the tax -- averages around 20 percent , according to the liberal Center on Budget and Policy Priorities.

- role_fit=1.00 nli=entailment pid=453::7
  > But McCain's assertion about whom capital gains taxes would affect is another story. He says they would affect "mutual funds and 401(k)s." He's right on mutual funds, but not about 401(k) or mutual funds held under a 401(k) retirement plan. A 401(k) is a retirement account to which workers can contribute earnings without paying taxes on the earnings. People aren't taxed on their 401(k) accounts un...

- role_fit=1.00 nli=entailment pid=6317::11
  > We should point out that the government currently taxes investment income in various ways and could have simply raised current rates.

- role_fit=1.00 nli=entailment pid=4129::12
  > On the issue of stock market growth, they noted that pension funds and foreign investors don't pay capital gains taxes the same way that individual investors do. "Thus, capital gains tax rates can increase significantly, as they did following the 1986 Tax Reform Act, and have little apparent effect on the stock market," the report said. "Likewise, the stock market can fluctuate even when rates rem...

- role_fit=1.00 nli=entailment pid=2317::15
  > The other question is, did the original tax cut spark "exponential growth," as Loughlin contended.

- role_fit=1.00 nli=entailment pid=2059::13
  > • She voted against Bill 1840, the cigarette surcharge tax .

- role_fit=1.00 nli=entailment pid=7795::2
  > "Buono voted 154 times to raise our taxes -- like the sales tax, the income tax, health care taxes, even small business taxes," the narrator states as text in the commercial states she voted to raise taxes and fees.

- role_fit=1.00 nli=entailment pid=10219::4
  > That claim about income tax cuts drew our attention.

- role_fit=1.00 nli=entailment pid=2251::8
  > Now to the second question -- the ad's claim that the tax "(lets) the IRS take half of your savings when you die."

- role_fit=1.00 nli=entailment pid=7484::11
  > The Legislature, however, was concerned whether the state could afford it and decided to delay any cut to see if Christie’s revenue projections would hit his target. The target wasn’t met and the tax cut wasn’t funded.

- role_fit=1.00 nli=entailment pid=2251::5
  > Toomey's camp points to votes Sestak took in Congress that supported continuation of the estate tax. In one of them, on Dec. 3, 2009, Sestak voted with 225 other Democrats (and no Republicans) to pass the Permanent Estate Tax Relief for Families, Farmers, and Small Businesses Act of 2009. This legislation -- which passed the House but stalled in the Senate -- would have established the top estate ...

- role_fit=1.00 nli=entailment pid=1900::3
  > Hayworth is correct that McCain voted against both the Economic Growth Tax Relief Reconciliation Act of 2001 and the Jobs and Growth Tax Relief Reconciliation Act of 2003. In fact, he was one of just two Republicans to oppose the 2001 bill (along with the late John Chafee of Rhode Island) and one of three Republicans opposing the 2003 bill (along with Chafee and Olympia Snowe of Maine).

- role_fit=1.00 nli=entailment pid=12027::4
  > Yes, Rubio skipped the votes. But this ad misleads by failing to tell the full picture. It doesn’t tell viewers that all of Rubio’s skipped votes pertain to one bill, and that Rubio voted for the overall bill, while Cruz actually voted against it.

- role_fit=1.00 nli=entailment pid=2584::16
  > Ausley voted against the transportation bill in the House, but says she did not know about the amendment that was added to build the courthouse.

- role_fit=1.00 nli=entailment pid=1636::4
  > Rubio contends that the tax swap would have been a huge, net tax cut. And that the plan was supported by former Gov. Jeb Bush.

- role_fit=1.00 nli=entailment pid=7795::14
  > Overall, the lists provided by Republicans showed that there were dozens of increases in taxes or fees or other tax policy changes that could result in individuals or businesses paying higher taxes. We calculated the votes and confirmed that Buono did vote 154 times in favor of higher taxes and fees.

- role_fit=1.00 nli=entailment pid=2251::3
  > We see two questions to ask in evaluating in Toomey's ad. The first is whether Sestak "wants to bring back the death tax." The second is whether it's accurate to say that the tax "(lets) the IRS take half of your savings when you die."

- role_fit=1.00 nli=entailment pid=1636::18
  > Rubio's proposal got the seal of approval from Grover Norquist, president of Americans for Tax Reform and a Rubio supporter. In 2007, he wrote legislators saying Rubio's tax swap proposal amounted to a net tax cut.

- role_fit=1.00 nli=entailment pid=4133::12
  > • "Your tax dollars are not being used to sue you the people who voted the 63 percent" in favor of Amendment 6. In this item, we'll check Hays' assertion that he did not "vote to spend money to fight that lawsuit."

- role_fit=1.00 nli=entailment pid=8607::16
  > Rubio wrote that the plan failed to immediately downsize government and ignored "the biggest driver of our debt, health care spending." Rubio also wrote that he feared the vote would lead to consideration of big tax hikes.

### attack (25 passages)

- role_fit=1.00 nli=contradiction pid=1475::14
  > The new law now awaiting the president's signature would implement additional exemptions from PAYGO, some permanent, some temporary. According to the newsletter CongressDaily, the measure includes "an unlimited exemption for extending the 2001 and 2003 tax cuts for the middle class," plus two-year exemptions for updates to the Alternative Minimum Tax (AMT) and reductions to estate taxes, as well a...

- role_fit=1.00 nli=contradiction pid=1900::15
  > While the bills' benefits were concentrated among those with the highest incomes, taxpayers in all income levels did get some benefit. The Tax Policy Center, a joint project of the centrist-to-liberal Urban Institute and Brookings Institution, looked at all of the Bush-backed tax cuts enacted between 2001 and 2008 (which included, but was not limited to, the 2001 and 2003 bills) and found that the...

- role_fit=0.95 nli=contradiction pid=12471::17
  > Bennet was among a majority of Democrats who voted three times over 10 days in September to successfully block a Republican resolution to kill the Iran deal. According to the New York Times , Republican Senate Majority Leader Mitch McConnell called multiple votes on the measure to reject the Iran accord. In part, he wanted to see if he could win a few votes needed to break the deadlock, the Times ...

- role_fit=0.69 nli=entailment pid=9070::19
  > No Tax For Tracks actually gets the talking point correct elsewhere on its website, saying, "Now PSTA wants to 'replace' the property tax by increasing our sales tax from 7 percent to 8 percent. That’s a 14 percent increase! To convince us to vote 'Yes', they are calling it a 'Tax Swap'."

- role_fit=0.54 nli=neutral pid=10105::9
  > On March 20, 2014, according to an American-Statesman news story , the council by 5-2 voted to raise the property tax exemption for homeowners older than 65 or disabled, from $51,000 to $70,000 -- saving the typical elderly homeowner about $100 a year starting with the 2014 tax year.

- role_fit=1.00 nli=contradiction pid=2584::4
  > "I'm Loranne Ausley, and as chief financial officer I'll eliminate pay-to-play contracts and hold politicians like Jeff Atwater accountable for how they spend our tax dollars," Ausley says. "It's time to clean up the mess in Tallahassee."

- role_fit=1.00 nli=contradiction pid=225::12
  > Giuliani has previously said the rate of adoptions went up 65 to 70 percent. His campaign calculated that number by taking adoption rates for the six years before ACS was created and comparing them to the six years after.

- role_fit=0.87 nli=contradiction pid=6261::17
  > Ghannam used the 2004 report to show that it took six procedures, six days, and a cost of about 0.7 percent of gross national income (GNI) per capita to start a business in the U.S. In 2012, the report shows it still takes six procedures and six days to start a business, with the cost slightly increased to 1.4 percent GNI.

- role_fit=0.53 nli=entailment pid=2190::3
  > "There are currently delays of up to six months in the processing of DNA evidence at the state run crime lab," DeWine states on his campaign website.

- role_fit=0.08 nli=entailment pid=6833::1
  > The candidates repeatedly disagreed about that number. Four times the president spoke of Romney’s $5 trillion tax cut, and four times the governor rejected it.

- role_fit=1.00 nli=contradiction pid=12960::8
  > The claim in the 2014 piece was that McConnell voted "three times for corporate tax breaks that send Kentucky jobs overseas."

- role_fit=1.00 nli=contradiction pid=10219::22
  > Barca cites accurate figures in making the point that Walker and Republicans could have designed tax reforms to even up the raw dollar savings for different groups, but his claim needs more discussion, they said.

- role_fit=1.00 nli=contradiction pid=8607::9
  > Rubio gave props to a plan by Rep. Dave Camp, R-Mich., to lower and simplify tax rates, close loopholes, and make permanent low rates on capital gains and dividends. He also gave a shout out to House Republicans for their budget plan, which he said would lower discretionary spending by $862 billion over 10 years.

- role_fit=1.00 nli=contradiction pid=2251::0
  > In his Senate race against Rep. Joe Sestak, D-Pa., former Republican Rep. Pat Toomey is using a favorite GOP issue: taxes. In an ad , Toomey charges that "Joe Sestak ... even wants to bring back the death tax, letting the IRS take half of your savings when you die."

- role_fit=1.00 nli=contradiction pid=12261::18
  > On Sept. 30, 2013, Ingoglia gave $1,000 to the Rubio Victory Committee, a Senate account. At that point, Rubio was in his first full year in the Senate and wasn’t running for president yet.

- role_fit=1.00 nli=contradiction pid=2584::1
  > This time the accused is state Sen. Jeff Atwater, the Republican candidate for chief financial officer. The accuser is his Democratic opponent, former state Rep. Loranne Ausley.

- role_fit=0.00 nli=entailment pid=4503::25
  > But the claim that the money has been "saved" misconstrues a projected savings as an actual savings. In reality, the total savings wouldn’t be realized for decades.

- role_fit=0.00 nli=entailment pid=7043::5
  > PolitiFact has heard similar claims about Ryan’s budget resolutions many times before. But we hadn’t examined whether those savings would go to bankroll tax cuts for millionaires.

- role_fit=0.00 nli=entailment pid=3433::24
  > Those aspects relate directly to the immediate savings. The next is the central part of the claim of saving $184 million over 25 years.

- role_fit=0.00 nli=entailment pid=1311::40
  > "I would say Save Our Homes is the largest tax cut in the history of Florida," Wilkinson said. "There is a savings, you can look it up, and it's real."

- role_fit=1.00 nli=contradiction pid=11894::10
  > These tax hikes were intended to offset the key element in Kasich’s plan: a sweeping income tax cut. And tax policy analysts from the left and the right both defined it as such.

- role_fit=0.48 nli=neutral pid=614::3
  > Problem is, neither of these votes actually raised taxes, nor were they expected to.

- role_fit=0.49 nli=neutral pid=7064::20
  > In 2001 and again in 2003, Nelson voted against tax cuts. But when Floridians wrote him for help on tax issues, Nelson didn’t tell those constituents to take a hike because he opposed those bills, Maloney said.

- role_fit=0.00 nli=entailment pid=4408::21
  > But four votes don’t go far in refuting the claim and the issue wasn’t whether Baldwin supported the middle class.

- role_fit=0.02 nli=entailment pid=5399::14
  > "And by the way, tax hikes are off the table.

