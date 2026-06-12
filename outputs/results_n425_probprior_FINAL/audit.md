# Disagreement audit

- Claims compared: 425
- arg-aware accuracy: 182/425 (43%)
- flat-RAG accuracy:  83/425 (20%)
- net arg-aware lift: +23%

## Category breakdown

- **both_correct**: 37
- **arg_only_right**: 145
- **flat_only_right**: 46
- **both_wrong_same**: 77
- **both_wrong_different**: 120

## Cases where arg-aware wins

### id=14 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Senator McCain voted against the Bush tax cuts. Now he's for them."
- arg-rationale: The evidence clearly shows McCain voted against the Bush tax cuts in 2001 and 2003 but now supports them, confirming the claim's central assertion.

### id=66 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: Poor people go to a "payday lender...and they pay 300, 400, 500 percent interest."
- arg-rationale: The evidence overwhelmingly supports the claim that payday lenders charge extremely high interest rates, with one example showing an annual rate of 278 percent.

### id=386 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "I committed to public financing; (Obama) committed to public financing."
- arg-rationale: The claim is directionally correct as both candidates initially committed to public financing. However, the evidence suggests that Obama later opted out of it, which qualifies the original commitment.

### id=422 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "I did very well with young people in Ohio, Massachusetts, California."
- arg-rationale: The claim has some support but lacks strong evidence; the partial support and attack passages suggest a mixed picture regarding Trump's performance with young people in Ohio, Massachusetts, and California.

### id=570 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Obama "voted for and even sponsored amendments that were intended to kill the (immigration overhaul) legislation."
- arg-rationale: The claim is partially accurate as Obama did sponsor amendments, but the context and intent are misleading. The evidence shows that while he sponsored amendments, his remarks suggest a nuanced stance rather than an intention to kill the legislation.

### id=916 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The stimulus bill includes "$300,000 for a sculpture garden in Miami."
- arg-rationale: The claim misattributes the stimulus bill funding to a specific sculpture garden in Miami, which is not accurate. The evidence shows it refers to Washington's National Mall improvements and not Miami.

### id=975 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Obama's budget plan would "take national debt up to about 80 percent of gross national product. ... Historically, it's been about 40 percent."
- arg-rationale: The evidence overwhelmingly supports the claim that Obama's budget plan would increase national debt to about 80 percent of gross domestic product, with no contradicting evidence.

### id=1044 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "If you actually took the number of Muslims [sic] Americans, we'd be one of the largest Muslim countries in the world."
- arg-rationale: The claim is based on fabricated data and misrepresents the actual number of Muslims in America, which does not make the U.S. one of the largest Muslim countries in the world.

### id=1052 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Obama has more czars than the Romanovs."
- arg-rationale: The evidence overwhelmingly supports the claim that Obama has more czars than the Romanovs, with no contradicting evidence provided.

### id=1112 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "As many as 22,000 Americans die each year because they don’t have health insurance."
- arg-rationale: The claim has an element of truth but omits important context; the cited number is debated and lacks strong supporting evidence while including caveats.

### id=1246 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Forty percent of gross domestic product "is state, local, or federal money."
- arg-rationale: The claim is directionally correct as a significant portion of GDP is government spending, but it overstates the exact figure of 40%. The evidence supports federal spending being around 23% to 25%, with state and local contributions adding up to less than the claimed total.

### id=1324 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "The Stupak Amendment doesn't just say you can't use your federal insurance subsidy to pay for an abortion, it says, if you're getting a federal subsidy of any kind, you're not allowed to buy an insurance plan that covers abortion even with your own money."
- arg-rationale: The claim contains an element of truth but ignores critical facts that change the overall impression. While it's true federal subsidies cannot be used for abortion coverage, individuals can still purchase plans with abortion coverage using their own money.

### id=1412 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: There are "high administrative costs" when you donate to Haiti relief through the White House Web site.
- arg-rationale: The evidence does not support the claim about high administrative costs for Haiti relief donations through the White House website; instead, it focuses on unrelated criticisms of the Clinton Foundation and Trump Foundation.

### id=1439 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: “Under (Rick Perry’s) watch as governor, over six million Texans have no health care coverage, including one million children, homeowners suffer from the highest insurance rates in the country, and college tuition has skyrocketed 136 percent.”
- arg-rationale: The claim includes accurate statistics but omits important context about the legislative changes that allowed for tuition increases and does not provide a balanced view of the situation.

### id=1569 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "When we started this health care debate a year ago, 85 percent of the American people had health insurance, and 95 percent of the 85 percent were happy with it."
- arg-rationale: The claim is directionally correct with the evidence supporting that about 85 percent of Americans had health insurance and a majority were generally satisfied. However, it omits important context regarding specific groups' satisfaction levels.

### id=1591 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: People "can't go fishing anymore because of Obama."
- arg-rationale: The claim is fabricated; there is no evidence supporting the idea that people cannot go fishing due to Obama's policies.

### id=1597 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: St. Pete Beach's experiences are a "fair example" of what could happen if Amendment 4 passes.
- arg-rationale: The claim has some basis in St. Pete Beach's experiences but omits important context and qualifications from the evidence.

### id=1616 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Last week the Texas State Board of Education (SBOE), led by Rick Perry's appointee, voted to remove Thomas Jefferson from social studies textbook standards. That's right. Thomas Jefferson... was deleted from a list of historical figures who inspired political change."
- arg-rationale: The claim is partially accurate as Jefferson was removed from the list, but it omits important context about the specific wording change and overstates the significance of Perry's involvement.

### id=1844 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "The Democratic Congress has already taken significant steps to create jobs and jump-start the economy, resulting in the lowest tax rates in over 50 years and the creation of over 500,000 new jobs so far this year."
- arg-rationale: The claim contains partially accurate information but omits important context and qualifications about job creation rates and tax policies.

### id=1900 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: John McCain "voted against the tax cuts of 2001 and 2003, wrongly claiming they helped only the rich."
- arg-rationale: McCain did vote against the tax cuts but supported less generous alternatives and had valid reasons for his opposition, making the claim directionally correct but requiring clarification on context and nuances.

### id=2046 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Under President George W. Bush, the U.S. had "52 months of ... uninterrupted job creation" and "revenues were at an all-time high in 2007."
- arg-rationale: The claim is directionally correct with minor caveats; the evidence confirms job creation and revenue highs under Bush but notes some selective comparisons.

### id=2060 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "We went from losing 3 million jobs in the last six months of the Bush Administration," adding almost 600,000 private sector jobs in the first six months of the year.
- arg-rationale: The claim is directionally correct but omits important context about the timing and scale of job losses under Bush versus gains under Obama.

### id=2094 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: House Republicans who complained they didn't have enough time to consider a constitutional ban against oil drilling "shoved through a proposal in just a few days to open state waters to oil drilling."
- arg-rationale: The evidence shows that Republicans pushed through a proposal to open state waters to oil drilling quickly, supporting the claim's central assertion without contradiction.

### id=2238 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "The unemployment rate for folks who've never gone to college is almost double what it is for those who have."
- arg-rationale: The evidence overwhelmingly supports the claim that unemployment rates are significantly higher for those without college education compared to those with it.

### id=2284 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "The government is trying to now close the Lincoln Memorial for any kind of large gatherings."
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is fabricated or false.

### id=2340 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Georgia's U.S. senators voted for legislation that would "gut clean air protections and increase oil dependence."
- arg-rationale: The claim is partially accurate as the senators voted against clean air protections and for legislation that would increase oil dependence. However, it omits important context about the nuances of their votes and the broader economic impacts.

### id=2384 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Clayton County has employed 1,300 people over the past seven months through the Neighborhood Stabilization Program.
- arg-rationale: The claim is partially accurate as Clayton County has employed a significant number of people through the program, but it lacks context about job losses in the broader area and may overstate its impact.

### id=2424 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Ganley said that if elected, he wants to ‘cut the dickens’ out of Social Security, Medicare and Veterans’ benefits."
- arg-rationale: The quote is fabricated; evidence shows Ganley made a statement supporting Social Security without cuts, contradicting the claim.

### id=2442 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: A bill by Earl Blumenauer would "mandate GPS tracking devices on all our vehicles."
- arg-rationale: The evidence shows no bill by Earl Blumenauer mandates GPS tracking devices on vehicles; the claim is fabricated.

### id=2728 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Republican gubernatorial candidate Scott Walker "increased his own pay by $50,000."
- arg-rationale: The claim attributes an invented salary increase to Scott Walker; evidence shows no factual basis for the assertion.

### id=2731 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "We have empowered state insurance commissioners to review the rate hikes that are taking place in states. And in some states like North Carolina, they have already used it and rolled back premium increases by 25 percent."
- arg-rationale: The claim is directionally correct as state insurance commissioners have reviewed rate hikes and rolled back some increases. However, the specific 25 percent rollback in North Carolina needs minor clarification or verification.

### id=2769 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Georgia has the second-highest rate of childhood obesity in the United States."
- arg-rationale: The evidence supports the claim that Georgia has a high rate of childhood obesity, though specific rankings are not provided in the passages.

### id=2876 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Ohio ranks 46th in the country in putting dollars in the classroom."
- arg-rationale: The claim is directionally correct but lacks precision; Ohio's ranking in administrative spending is not directly supported by state-specific data and the national figures are used for comparison.

### id=2908 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "There’s talk in Congress now about basically confiscating your private 401(k) or IRA plan and rolling it into Social Security to strengthen Social Security."
- arg-rationale: {"label": "Pants-fire", "rationationale": "The claim misrepresents the actual proposals and uses fabricated or highly exaggerated claims about confiscating private retirement plans to strengthen Social Security, which is not supported by any evidence."}

### id=2918 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Joe Straus "was co-author of a bill that would have allowed Planned Parenthood to control public school sex education."
- arg-rationale: The claim attributes to Joe Straus an action he did not take and misrepresents the involvement of Planned Parenthood in sex education policy.

### id=2993 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "In 1981, Matagorda, Brazoria, and Galveston Counties all opted out of the Social Security program for their employees. Today, their program is very, very well-funded and there is no question about whether it’s going to be funded in" years to come.
- arg-rationale: The claim is directionally correct but omits important details about the Galveston plan's lack of cost-of-living increases and the complexity in comparing its performance to Social Security.

### id=3027 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "There hasn't really been a lot of net growth in the federal workforce when you compare it to say, 1990."
- arg-rationale: The claim is partially accurate as there has been limited net growth in the federal workforce since 1990, but it omits important context about demographic changes and hiring practices that affect this figure.

### id=3161 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "From 1980 to 1990, the top 1 percent saw their income go up by roughly 80 percent" while "the median wage in the country over (the same) 10 years went up 3 percent."
- arg-rationale: The claim is directionally correct with the top 1% experiencing significant income growth while median wages increased modestly. However, it lacks precision in specifying the exact percentage changes and omits some fluctuations in median wage data.

### id=3478 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: The hour of sleep you lose during the change to daylight saving time might initially pose some health risks.
- arg-rationale: The evidence overwhelmingly supports the claim that losing an hour of sleep during daylight saving time might pose initial health risks.

### id=3625 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: Says Texas routinely gets "a lot more federal spending" than it pays in taxes.
- arg-rationale: {"label": "Mostly-true", "rationationale": "The claim is directionally correct that Texas receives more federal spending than it pays in taxes, but the evidence suggests this is a general trend for all states due to high deficit spending rather than a unique situation for Texas alone."}

### id=3706 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says people in Africa "literally walk two and three hundred miles" in order to vote.
- arg-rationale: The claim is fabricated; there is no evidence supporting people walking hundreds of miles to vote in Africa, and the provided passages do not relate to this specific assertion.

### id=3864 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Michigan and Massachusetts raised their bottle deposit and "could no longer afford the program because the redemptions were so high there was no profit in there."
- arg-rationale: The claim contains fabricated information about bottle deposit programs in Michigan and Massachusetts; there is no evidence supporting the assertion that these states could not afford their programs due to high redemptions.

### id=3994 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Phil Puckett "voted no on sending the EPA a message that they’ve gone too far not once, but twice."
- arg-rationale: The claim attributes fabricated quotes and actions to Phil Puckett that never occurred, as multiple sources confirm the votes did not have the described impact or were not cast in the manner suggested.

### id=4103 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says for the first time in the history of the United States, the government cut taxes during wartime
- arg-rationale: The claim is directionally correct but oversimplifies the context; while there were tax increases during wartime, it was not unprecedented and the scale of these changes does not match historical precedents.

### id=4352 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "The estimated savings of this (debt ceiling) deal only pay for half of the cost of extending all of the Bush-era tax cuts for another decade."
- arg-rationale: The evidence supports the claim that the savings from the debt ceiling deal only cover half the cost of extending all Bush-era tax cuts for another decade.

### id=4408 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Democratic U.S. Senate candidate Tammy Baldwin ranks "as the most liberal member of the House."
- arg-rationale: The evidence supports Baldwin being among the most liberal members but does not definitively confirm her as the single most liberal member of the House.

### id=4537 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "My home state since June of 2009 created 40 percent of the new jobs in America."
- arg-rationale: The claim is directionally correct with Texas creating a significant portion of new jobs since June 2009, but it omits important context about the economic factors and limitations in attributing job creation solely to state leadership.

### id=4588 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says he "came to the Republican Party sooner in age" than Ronald Reagan.
- arg-rationale: The evidence supports the claim that the speaker came to the Republican Party at a younger age than Ronald Reagan, with no contradictory evidence provided.

### id=4995 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "I've done more impeachments than anybody else in the history of the country."
- arg-rationale: The evidence supports that the speaker has initiated more impeachments than any other individual in U.S. history.

### id=5023 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "We have one of the highest percentages per capita of nonprofits in this state of any state in the union."
- arg-rationale: The claim is directionally correct but lacks specific evidence to support the exact 'highest per capita' assertion for nonprofits. The provided evidence supports related negative economic conditions in Illinois but does not directly confirm the nonprofit statistic.

### id=5131 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: The education tax burden for Shelby County -- and Tennessee -- is "one of the lowest in the country."
- arg-rationale: The evidence supports the claim that Tennessee's education tax burden is low compared to other states, but it does not provide specific data for Shelby County or a direct comparison of all counties in the country.

### id=5385 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Scott Walker enacted "the biggest cuts to education in our state’s history."
- arg-rationale: The evidence overwhelmingly supports the claim that Scott Walker enacted significant cuts to education in Wisconsin's history, with no contradicting evidence.

### id=5398 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "Florida ranks 45th" in the nation for tuition.
- arg-rationale: The evidence passages confirm that Florida ranked 45th in tuition costs, with no contradictory information provided.

### id=5423 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Florida is "the largest dog-racing state in the country."
- arg-rationale: The evidence overwhelmingly supports Florida being the largest dog-racing state in the country without any contradictions.

### id=5521 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Ohio is not meeting its obligation to update voter registrations when voters change their address with the BMV."
- arg-rationale: All evidence supports the claim that Ohio is not meeting its obligation to update voter registrations when voters change their address with the BMV.

### id=5613 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "The poorest in this country are women."
- arg-rationale: The evidence overwhelmingly supports the claim that women are disproportionately affected by poverty due to underpaid jobs and other factors.

### id=5664 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Ohio Treasurer Josh "Mandel first claimed bank fraud in June 2010 but did nothing for more than a year while raising money for his (Republican) Senate campaign."
- arg-rationale: The claim attributes an invented quote or action to Mandel; evidence shows no support and multiple attacks refute the timeline and context of the claim.

### id=5849 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "The United States already has the highest corporate tax rate in the world."
- arg-rationale: The claim is directionally correct as the U.S. statutory corporate tax rate is indeed high, but it omits important context about effective rates which are lower due to deductions and exclusions.

### id=5928 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: There are "49 different federal job training programs that report to eight agencies."
- arg-rationale: The claim is directionally correct but lacks precision; the evidence confirms there are multiple federal job training programs across various agencies, though it does not specify exactly 49 or eight reporting agencies.

### id=5940 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: President Obama "promised" families making less than $250,000 a year would not see taxes go up, but "Obamacare raises 18 different taxes."
- arg-rationale: The claim contains an element of truth about new taxes but misleads by ignoring that these are targeted at higher-income individuals, not those making less than $250,000 as the promise implied.

### id=6057 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Barack Obama has played nearly 100 rounds of golf as president.
- arg-rationale: The evidence overwhelmingly supports the claim that Obama played nearly 100 rounds of golf as president, with no contradicting information.

### id=6310 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Nearly 100,000 people get shot every year. That's 270 people a day and 87 dead."
- arg-rationale: The claim is directionally correct but omits important context about the definition and source of the statistic. The number of people shot annually is high, but the specific framing and context are crucial for accuracy.

### id=6450 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says the federal government "mandates transexuals (sic) and homosexuals grabbing children in their stranger-danger zones in the name of airport security."
- arg-rationale: The claim contains fabricated elements and makes an absurd assertion about government mandates for sexual minorities interacting with children in the name of airport security; there is no evidence supporting this.

### id=6473 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Paul Ryan's budget relies on the same $700 billion in savings from Medicare that Mitt Romney and other Republicans have been attacking Democrats about.
- arg-rationale: The evidence supports that Paul Ryan's budget relies on similar savings from Medicare as those attacked by Republicans, confirming the claim.

### id=6782 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Barack Hussein Obama will ... force local authorities to allow Occupy protesters to live in parks."
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is fabricated.

### id=7008 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "6,400 Ohioans ... lost manufacturing jobs in the month of September."
- arg-rationale: The claim is partially accurate but omits the time frame and context. The evidence confirms job losses in Ohio but does not specify the exact month of September or the broader period under consideration.

### id=7078 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "Texas’ population is projected to double in the next 50 years or so, but our basic amount of water will remain about where it is now."
- arg-rationale: The claim is directionally correct but lacks specific context about Texas's water management and projections. The evidence supports the population growth projection but does not provide a direct comparison of current and future water availability for Texas, making it mostly true with minor caveats.

### id=7244 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Barely-true**
- claim: "The amount of money that we put into running our own state legislature is nearly as much as we put into the University of Rhode Island."
- arg-rationale: The evidence shows the claim is speculative and lacks factual support; it overstates the comparison between state legislature funding and university spending.

### id=7262 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: In 2010, 2,694 young people were killed by gunfire. 1,773 were victims of homicide; 67 were elementary school-age children.
- arg-rationale: The claim is directionally correct with the provided numbers for gun deaths and homicides in 2010. The caveats about data sources and methods do not significantly undermine the central assertion, qualifying it as mostly true.

### id=7268 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Nearly a quarter of all adults in this state have some college credit without a degree."
- arg-rationale: The evidence supports the claim that many adults have some college credit without a degree, but lacks specific data to confirm 'nearly a quarter' of all adults in the state.

### id=7492 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "In 32 other states and Washington D.C., they [voters] can avoid the wait by voting before Election Day."
- arg-rationale: The evidence overwhelmingly supports the claim that voters in 32 other states and Washington D.C. can vote before Election Day to avoid waiting.

### id=7577 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: When students leave our high schools and they go to the community college, 70-75 percent of them have to pay to take remedial math.
- arg-rationale: The claim is directionally correct but lacks precision; the evidence supports high remediation rates in community colleges but does not provide exact figures of 70-75 percent.

### id=7609 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "A report by the US General Accountability Office (GAO) in 2008 found that the disposal of Katrina wastes by AshBritt in the south resulted in the creation of contaminated sites along the Gulf Coast and two new Superfund sites in New Orleans."
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is fabricated; there are no credible sources confirming the creation of contaminated sites or Superfund sites due to AshBritt's disposal activities as stated.

### id=7635 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: When the NECAP proficiency test is re-given to the kids the second and third time, harder questions are taken out.
- arg-rationale: The claim suggests that easier questions are removed in subsequent tests, but the evidence is mixed and weak. While there's some support for retesting conditions being different, attacks suggest this isn't a standard practice and critics argue against it.

### id=8011 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Austin is the "largest city in America without a congressional district anchored in it."
- arg-rationale: The evidence overwhelmingly supports the claim that Austin is the largest city without a congressional district anchored in it, with no contradicting evidence.

### id=8303 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Tuition at Rutgers has increased 10 percent since Gov. Chris Christie took office because he "cut funding for higher education."
- arg-rationale: The claim has an element of truth regarding funding cuts but omits important context about tuition increases being influenced by factors beyond just state funding decisions.

### id=8408 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Congressional lawmakers earn their salaries "FOR LIFE," which for House Minority Leader Nancy Pelosi would add up to "$803,700 Dollars a year for LIFE including FREE medical."
- arg-rationale: The claim contains fabricated information about congressional salaries and medical benefits. Pelosi's salary does not continue indefinitely after leaving office, and there is no 'free' medical coverage for life.

### id=8433 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Property taxes have increased 20 percent under four years of Chris Christie."
- arg-rationale: The claim is directionally correct as property taxes did increase under Christie's tenure, but the exact 20 percent figure may be an overstatement and lacks precise context. The evidence suggests a significant reduction in tax increases compared to previous years.

### id=8511 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: A planning group said that to meet anticipated traffic demands by 2035, Interstate 35 between Austin and Round Rock will need a dozen additional lanes going north and 14 additional southbound lanes.
- arg-rationale: The claim is partially accurate as it reflects the need for additional lanes on I-35 but omits important context about other congestion-reducing strategies and the misleading nature of the statement according to experts.

### id=8607 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "I did not support the sequester."
- arg-rationale: The evidence clearly shows that the sequester was established with bipartisan support and votes from both Republicans and Democrats, including the claimant's party members.

### id=8727 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The federal health care law tells "the American people precisely what type of coverage they have to have."
- arg-rationale: The claim is partially accurate as the Affordable Care Act does specify certain requirements for health insurance coverage. However, it omits important context about the specifics and exceptions to these requirements, such as subsidies and exemptions for those who choose to pay a fine instead of purchasing insurance.

### id=8838 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: There is "more oil produced at home than we buy from the rest of the world – the first time that’s happened in nearly 20 years."
- arg-rationale: The evidence overwhelmingly supports the claim that domestic oil production exceeds imports for the first time in nearly 20 years.

### id=9251 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Up "to 45 percent" of illegal immigrants "are not people that physically crossed the southern border or northern border. They are visa overstayers."
- arg-rationale: The evidence supports the claim that a significant portion of illegal immigrants are visa overstayers, but does not provide precise figures to confirm 'up to 45 percent'.

### id=9305 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Wendy Davis raised money for a U.S. House Democrat who is a member of a Democratic socialists group.
- arg-rationale: The claim is unsupported and the evidence provided refutes it; no credible backing for Wendy Davis raising money for a U.S. House Democrat who is a member of a Democratic socialists group exists.

### id=9387 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Florida has "the most errors and exonerations from death row."
- arg-rationale: The claim is partially accurate as Florida has a high number of death row exonerations and natural deaths compared to executions, but it omits important context about other states' data and the complexity of comparing across jurisdictions.

### id=9437 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Under Wisconsin law, "anyone who knows anything about a John Doe" secret criminal investigation "can't talk about it."
- arg-rationale: The claim is partially accurate as John Doe investigations are typically conducted in secrecy and involve special powers. However, the evidence shows that there are exceptions and qualifications to this rule, such as the ability of a judge to order secret proceedings and specific legal contexts where disclosure may be restricted but not universally prohibited.

### id=9502 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "The United States is the only developed country in the world without paid maternity leave."
- arg-rationale: The claim is directionally correct as the U.S. lacks mandated paid maternity leave compared to other developed countries, but it overstates by excluding New Guinea and not specifying 'developed' nations.

### id=9577 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "There are more than 46 million Americans living in poverty today -- the largest number in 54 years."
- arg-rationale: The claim is directionally correct with the number of Americans in poverty increasing to a high level recently. However, it lacks precision by not specifying the exact timeframe and population context.

### id=9683 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "I'm not a conspiracy theorist and I never allow conspiracy theorists on my program."
- arg-rationale: {"label": "Pants-fire", "rationate": "The claim misrepresents the speaker's actual words and context, which clearly indicate a belief in conspiracy theories. The structural prior strongly suggests this level of fabrication."}

### id=9731 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "All Aboard Florida is a 100 percent private venture. There is no state money involved."
- arg-rationale: The claim is partially accurate but omits important details about potential state involvement and funding. The evidence suggests some caveats and partial support, indicating the central assertion is misleading without context.

### id=9992 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The non-profit group Feeding America is lying when it claims "that one in five kids is fighting starvation daily" in the United States.
- arg-rationale: The claim misrepresents Feeding America's statement and the evidence shows no support for the specific numerical assertion made in the claim.

### id=10027 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: More women were killed by their husbands or boyfriends since Sept. 11 than "all the Americans who were killed by 9/11 or in Afghanistan and Iraq."
- arg-rationale: The evidence supports the claim that more women were killed by their partners since Sept. 11 than Americans killed in the wars mentioned.

### id=10040 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Muslim nations did not "call out" the people who celebrated the 9/11 attacks.
- arg-rationale: The claim is partially accurate as Muslim nations did not widely 'call out' those who celebrated 9/11 attacks, but the evidence shows some context and caveats that complicate this straightforward interpretation.

### id=10092 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "In 2013," Dan Patrick voted "against funding to test the backlog of rape kits, allowing rapists to walk free."
- arg-rationale: The claim attributes to Dan Patrick an action and quote that he did not take or make. Evidence shows no support for the claim's central assertion, with multiple passages refuting it.

### id=10097 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Elorza wants to teach our public school children about the ‘non-existence of God.’"
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is fabricated or misleading.

### id=10111 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Barely-true**
- claim: "While (Charlie Crist) was governor, utility costs went up 30 percent and went from below the national average to above the national average. Since I got elected, utility rates have come down 11 percent and now we are below the average."
- arg-rationale: The evidence shows no support for the claim's central assertion about utility costs and rates under Crist's governorship. The attacks refute the numerical claims and context provided is contradictory.

### id=10165 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "If Cory Gardner gets his way, you'd better stock up on condoms."
- arg-rationale: The claim attributes an invented quote to Cory Gardner and misrepresents his stance on healthcare policy.

### id=10171 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Nathan Deal saved the HOPE scholarship program.
- arg-rationale: The evidence strongly supports that Nathan Deal saved the HOPE scholarship program, but it also notes that context is needed to fully understand its current status and funding.

### id=10229 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: Repeal of Obamacare would "take away health care for 10.3 million Americans" who have received coverage since Oct. 1, 2013.
- arg-rationale: The claim is directionally correct as it highlights the potential loss of coverage for millions under Obamacare repeal. However, it lacks specific qualifiers and context about the nuanced impact on different groups, making it Mostly-true with minor caveats.

### id=10344 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "We've caught Iran cheating on the interim (nuclear) deal."
- arg-rationale: The claim suggests Iran is cheating on the deal, but evidence shows it's more about concerns and potential for future violations rather than confirmed cheating. The attacks highlight that Iran has not yet violated the agreement.

### id=10451 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The Affordable Care Act "basically puts a penalty or a tax on employers for every new job they create."
- arg-rationale: The claim contains an element of truth about the ACA imposing penalties on employers for not providing health insurance but omits important context that these penalties are minimal and do not necessarily cause job loss, making it misleading overall.

### id=10667 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "Inflation-adjusted defense spending has declined 21 percent since 2010, and even if we discount the drawdowns in Iraq and Afghanistan, it has still declined by a dangerous 12 percent."
- arg-rationale: The claim is directionally correct but omits important context about the baseline and growth rates of defense spending. The evidence shows a decline in real terms since 2010, but with caveats on the rate of decline and comparison to historical trends.

### id=10694 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says President Ronald Reagan "had a month of job creation of 1 million."
- arg-rationale: The claim attributes an unrealistically high job creation figure to Reagan with no supporting evidence and multiple attacks refuting the plausibility of such a number.

### id=10868 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Democrat "Russ Feingold announced his Wisconsin Senate run today from…California."
- arg-rationale: The claim is fabricated; evidence shows Feingold announced his campaign from Wisconsin, not California.

### id=10964 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Currently, almost 40 percent of people with HIV are not diagnosed until they already have developed AIDS. And that can be up to 10 years after they first are infected with HIV.
- arg-rationale: The claim is directionally correct but lacks specific evidence to support the exact 40 percent figure and the up-to-10-year timeframe. The provided evidence supports high infection rates among certain demographics but does not directly confirm or refute the precise percentages mentioned in the claim.

### id=11027 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Hundreds of thousands of (illegal immigrants are) going to state and federal penitentiaries."
- arg-rationale: The claim has an element of truth regarding the presence of illegal immigrants in prisons but lacks specificity and overstates the scale. The evidence suggests a small percentage (4%) of prisoners are non-U.S. citizens, without breaking down legal vs. illegal status.

### id=11032 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: A photograph of 21-year-old Hillary Clinton featured a Confederate battle flag in the background.
- arg-rationale: The evidence clearly shows the claim is fabricated; there are no confirmed images of Hillary Clinton with a Confederate battle flag in the background.

### id=11079 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Christian Pastor in Vermont Sentenced to One Year in Prison After Refusing to Marry Gay Couple"
- arg-rationale: The claim is fabricated; the evidence shows no record of a Christian pastor being sentenced to prison for refusing to marry a gay couple.

### id=11393 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Pope Francis uses a modest compact car to get around, while Creflo Dollar drives an expensive sports car.
- arg-rationale: The evidence shows the claim is fabricated; there are no supporting details for Pope Francis using a modest car or Creflo Dollar driving an expensive sports car.

### id=11480 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Because of Obamacare "people’s premiums ... are going up 35, 45, 55 percent."
- arg-rationale: The claim has an element of truth as some individuals may see significant premium increases, but it omits important context about subsidies and the overall impact on most people's premiums.

### id=11510 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Electric car sales in Georgia have dropped dramatically since a $5,000 tax credit was eliminated and a $200 annual registration fee was imposed July 1.
- arg-rationale: The evidence overwhelmingly supports the claim that electric car sales in Georgia dropped dramatically after tax incentives were removed and fees imposed.

### id=11539 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Obamacare insurance cooperative failures "should be expected" because they're like any business, and "when you start businesses in America, at the fifth year, half of the businesses have closed."
- arg-rationale: The claim that Obamacare insurance cooperatives should be expected to fail like any business is partially accurate but omits important context about the unique challenges faced by these entities. While it's true many businesses close within five years, the evidence suggests that factors specific to healthcare and regulation influenced the performance of these cooperatives.

### id=11566 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The Consumer Financial Protection Bureau has "no congressional oversight."
- arg-rationale: The claim is partially accurate as the CFPB does face limited congressional oversight compared to other agencies, but it still undergoes some form of oversight and accountability mechanisms.

### id=11625 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Road congestion costs rush hour drivers in Austin and Dallas more than $1,000 a year. And in Houston, it’s even more -- almost $1,500 a year."
- arg-rationale: The claim is directionally correct but the specific figures are not clearly sourced or verified for accuracy. The evidence suggests the statistic may apply to all of Texas rather than just Houston and Austin/Dallas, making it a minor qualification.

### id=11642 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: President Barack Obama "wants to take in 250,000 (people) from Syria."
- arg-rationale: The claim misattributes troop deployment numbers to refugee intake and inflates the actual number of Syrian refugees Obama sought to admit by a factor of 25.

### id=11813 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Barack Obama, right now, No. 1, over seven years has dramatically degraded our military."
- arg-rationale: {"label": "Barely-true", "rationationale": "The claim contains an element of truth about military spending cuts but ignores critical facts that would give a different impression. The evidence suggests the claim misleads overall by omitting context and qualifications."}

### id=11917 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: North Korea’s missiles are "not going to have a capability to reach the United States anytime real soon."
- arg-rationale: All support passages confirm that North Korea's missile capability is not currently a threat to the United States and lacks the immediate capacity to reach U.S. territory.

### id=12012 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "A single mother of two can’t qualify for basic healthcare through Medicaid if she makes more than $3,504 dollars a year."
- arg-rationale: The claim is directionally correct but omits the context that Medicaid eligibility varies by state and can be expanded beyond $3,504 a year for single mothers.

### id=12091 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Given the results of the primary, the vote of one New Hampshire superdelegate is equal to the votes of about 10,000 grassroots activists."
- arg-rationale: {"label": "Mostly-true", "rationationale": "The claim is directionally correct but overstates the equivalence by not specifying it applies only to Democratic primary voters and lacks important context about broader voter participation."}

### id=12160 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Emory University students were provided counseling after someone wrote "Trump 2016" in chalk on campus.
- arg-rationale: The claim has an element of truth as counseling was offered, but the framing implies it was specifically due to 'Trump 2016' and not broader election-related stress, which is misleading.

### id=12162 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Twenty-seven out-of-state pharmaceutical companies have raised more campaign dollars (against a drug price control measure) than all other state ballot measures have raised to date, combined."
- arg-rationale: The claim is partially accurate but omits important context about the nature and source of the funds raised against the drug price control measure. The evidence shows significant support for the numerical aspect but includes caveats that suggest misleading framing.

### id=12186 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "The economy always does better when there’s a Democrat in the White House."
- arg-rationale: The claim is partially accurate as the economy has shown periods of growth under Democratic presidents, but it ignores important context and nuances such as varying time frames and economic conditions at the start of each presidency.

### id=12244 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: In nine Democratic debates, "We've not had one question about a woman's right to make her own decisions about reproductive health care, not one question."
- arg-rationale: The evidence confirms that there were no questions about reproductive health care in the Democratic debates.

### id=12381 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "The United States has a low voter turnout rate."
- arg-rationale: The evidence overwhelmingly supports the claim that the United States has a low voter turnout rate compared to other OECD member-nations.

### id=12428 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **Barely-true**
- claim: "Look, we are at war with these people and they don't wear uniforms. … This is a war against people that are vicious, violent people, that we have no idea who they are, where they come from. We are allowing tens of thousands of them into our country now."
- arg-rationale: The claim misrepresents the context and scale of immigration issues by exaggerating the threat and conflating different immigrant groups. The evidence shows it is an overstatement and misleading characterization.

### id=12446 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Hypocrisy at the Clinton Foundation: Top male staff made on average $218,029 while top female staff made $153,014 from 2010-2014."
- arg-rationale: The claim presents a factual wage gap but lacks context about the reasons for the disparity and does not address whether this gap is typical or indicative of systemic issues within the organization.

### id=12535 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "ISIS is running through a border made porous by Barack Obama’s policies."
- arg-rationale: The claim attributes fabricated causation to Obama's policies and exaggerates the impact on border security; evidence shows no support for this assertion.

### id=12552 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Kelly Ayotte "voted again yesterday against a proposal to expand background checks -- (buyers) can continue to simply go online or to gun shows to purchase guns without background checks."
- arg-rationale: The evidence overwhelmingly supports the claim that Kelly Ayotte voted against expanding background checks for gun sales.

### id=12684 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Today, there are more Hoosiers going to work than ever before in the 200-year history of the great state of Indiana."
- arg-rationale: The claim is partially accurate as it reflects a high number of employed Hoosiers but omits important context about the limitations of unemployment rate metrics and population growth factors.

### id=12994 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The Clinton Foundation is a charity where President and Secretary Clinton and their daughter, they take no salary, they get no money from it, they take no personal benefit from it."
- arg-rationale: The claim is directionally correct that the Clintons do not take salary or personal benefit from the Clinton Foundation. However, there are minor caveats suggesting some potential conflicts of interest with speaking fees and donations.

### id=12999 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "And while (Ted) Strickland proposed cuts for services for children, he wasted over $250,000 remodeling his bathrooms at the governor’s mansion."
- arg-rationale: The claim attributes fabricated remodeling expenses to Strickland and misrepresents his budget proposals; evidence shows no record of such expenditures.

### id=13082 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "I finished" the controversy about where President Barack Obama was born.
- arg-rationale: The claim is fabricated as there is no evidence suggesting the controversy about Obama's birthplace was 'finished'; polls and media reports indicate it persisted.

### id=13118 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Most private sector jobs in the history of Buffalo exist in Buffalo today"
- arg-rationale: The evidence strongly supports the claim that Buffalo has a majority of private sector jobs existing today compared to historical data.

### id=13136 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: According to "independent experts," Donald Trump's tax plan "would blow up the debt by over $5 trillion and would in some instances disadvantage middle-class families compared to the wealthy."
- arg-rationale: The evidence overwhelmingly supports the claim that Trump's tax plan would increase debt and potentially disadvantage middle-class families compared to the wealthy.

### id=13163 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "If you look at any real analysis," the Trans-Pacific Partnership is "going to generate better-paying jobs that are more stable."
- arg-rationale: The claim suggests the TPP will generate better-paying and more stable jobs, but evidence is mixed with weak support and caveats about potential benefits to workers. The central assertion lacks strong confirmation.

### id=13184 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Tim Kaine "actually tried to raise taxes by about $4 billion."
- arg-rationale: The claim is directionally correct as Kaine did propose a tax increase, but the exact amount and impact are nuanced; it was not uniformly $4 billion and had offsets.

### id=13262 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says Libya "Ambassador (Christopher) Stevens sent 600 requests for help" in Benghazi.
- arg-rationale: The claim contains an element of truth about requests for help but misleads by exaggerating the number and implying direct involvement from Ambassador Stevens, who was not based in Benghazi.

### id=13263 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Donald Trump’s plan to repeal the estate tax would mean the Walmart Walton family would "get a $53 billion tax break."
- arg-rationale: The claim is partially accurate as the estate tax repeal would benefit wealthy families like the Waltons, but it omits important context about who actually pays the estate tax and exaggerates its impact on middle-class families.

### id=13277 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Marco Rubio made it clear: Not only does he think Donald Trump is a con man, he went on to say he doesn't trust Donald Trump with the nuclear codes."
- arg-rationale: The evidence supports that Rubio criticized Trump and questioned his trustworthiness without any contradicting information.

### id=13298 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "What the District of Columbia was trying to do (with its handgun ban) was to protect toddlers from guns."
- arg-rationale: The claim has an element of truth but omits important context. The District of Columbia's handgun ban was related to public safety concerns including protecting children from gun accidents, but the evidence suggests it was not solely or primarily aimed at toddlers and includes broader legal implications.

### id=13309 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: When Hillary Clinton "ran the State Department, $6 billion was missing. How do you miss $6 billion? You ran the State Department, $6 billion was either stolen — they don't know."
- arg-rationale: The claim is fabricated; there is no evidence of $6 billion missing from the State Department during Clinton's tenure.

### id=13387 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "One of George Soros' companies has provided some of the (voting) machines" for some states.
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is baseless and potentially fabricated.

### id=13405 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "One in five American households have nobody under the same roof that's got a job."
- arg-rationale: The claim is partially accurate as it reflects a portion of households dependent on government income, but it oversimplifies the complex reasons behind labor participation rates and underemployment.

### id=13484 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Harambe received 15,000 votes in the presidential election.
- arg-rationale: The claim is fabricated as there are no records or credible sources indicating Harambe received votes in a presidential election.

### id=13495 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "In 2015 roughly 10,000 political arrests occurred in Cuba. That is five times as many as occurred in 2010, when there were only about 2,000."
- arg-rationale: The claim is directionally correct with the number of political arrests in Cuba increasing significantly from 2010 to 2015. However, the exact figures provided need verification and context, making it a minor qualification.

## Cases where flat-RAG wins

### id=664 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: McCain "still thinks it's okay when women don't earn equal pay for equal work."
- flat-rationale: The evidence shows no support for McCain's stance on equal pay and the claim is based on a misattribution or fabrication; Trump's campaign supports equal pay.

### id=1414 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The Democrats' health care bills would provide "free health care for illegal immigrants."
- flat-rationale: The evidence shows the claim is fabricated; the bills do not provide free health care for illegal immigrants.

### id=2626 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Christopher Little has "a history of working against environmental protection by defending the worst types of corporate polluters"
- flat-rationale: The evidence is entirely topical and does not support or attack the claim about Christopher Little's history with environmental protection. Without relevant supporting or attacking evidence, the claim cannot be verified.

### id=2699 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "When President, then candidate, Obama was asked to disclose some of his donors because there was suspicion of their being the foreign source of money into his campaign, they refused to do it."
- flat-rationale: The claim misrepresents the situation; there is no evidence that Obama or his campaign refused to disclose donors due to suspicion of foreign funding. The provided evidence is topical and does not support the central assertion.

### id=2958 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Beaverton "enjoys the most diverse population (by percentage of population) among Oregon cities."
- flat-rationale: The evidence does not provide any information about population diversity in Oregon cities to support or refute the claim. The provided passages are topical and do not address the central assertion.

### id=3330 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: Says Tri-Rail shows the potential problems with investing in high-speed rail.
- flat-rationale: The claim suggests Tri-Rail shows problems with high-speed rail investment, but the evidence is topical and does not support this central assertion; it lacks direct confirmation or contradiction.

### id=4342 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Texas gained 21,000 doctors due to tort reform.
- flat-rationale: The evidence does not support the claim that Texas gained 21,000 doctors due to tort reform; it only discusses theoretical impacts and lacks specific data on doctor gains in Texas.

### id=4455 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says CNN's Wolf Blitzer was wrong to say that "the wealthiest Americans, they pay the most in taxes already -- 50 percent of Americans don't even pay any federal income tax."
- flat-rationale: The evidence shows that the claim misrepresents the tax situation; while some Americans do not pay federal income taxes, the wealthiest do not necessarily pay 50% of their income in taxes.

### id=4837 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Mahmoud Ahmadinejad said that "if he has a nuclear weapon he will use it to wipe Israel off the face of the earth. He will use it against the United States of America."
- flat-rationale: The evidence does not support the claim that Ahmadinejad said he would use a nuclear weapon against Israel or the United States; it only mentions his rhetoric and Iran's potential for developing nuclear weapons.

### id=5087 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Eliminating "Obamacare" ... "saves $95 billion a year."
- flat-rationale: The claim misrepresents the actual impact and funding mechanisms of Obamacare; there is no direct annual savings figure of $95 billion from eliminating it.

### id=5348 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "You're supposed to throw away your shoes" if mercury from a broken CFL light bulb gets on them.
- flat-rationale: The evidence does not support the claim that shoes should be thrown away if mercury from a broken CFL light bulb gets on them; instead, it suggests proper cleanup and ventilation methods without mentioning disposal of footwear.

### id=5371 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Mitt Romney supports cap and trade.
- flat-rationale: The evidence shows Mitt Romney does not support cap and trade; the claim is contradicted by topical context indicating strong Republican opposition to it.

### id=5671 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I think it’s seven or eight of the California system of universities don’t even teach an American history course. It’s not even available to be taught."
- flat-rationale: The claim is unsupported by the evidence and contradicts known facts about university curricula. The provided passages are topical but do not address the central assertion about American history courses.

### id=5959 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Jon Runyan voted to "end programs to aid homeless veterans."
- flat-rationale: The evidence is entirely topical and does not support the claim that Jon Runyan voted to end programs aiding homeless veterans; there are no supporting or attacking facts related to this specific assertion.

### id=5973 — gold *Barely-true*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **Barely-true** ✓
- claim: "Obama’s flush with cash, returning to Wall Street for even more money. … Wall Street sure supports President Obama."
- flat-rationale: The claim has an element of truth about Obama's fundraising from Wall Street but misleads by ignoring his regulatory actions against it.

### id=7567 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "This (parent trigger) legislation was drafted by President Obama's top advisers. It was drafted by President Clinton’s top advisers."
- flat-rationale: The evidence shows no support for the claim that the legislation was drafted by Obama or Clinton's top advisers; it is purely topical and does not confirm the central assertion.

### id=7672 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Proposed immigration legislation would give new immigrants "a taxpayer-funded cellular phone."
- flat-rationale: {"label": "False", "rationationale": "The evidence shows no support for the claim that proposed immigration legislation would give new immigrants taxpayer-funded cellular phones. The passages are topical and do not confirm or refute the specific claim about cellphones being provided to immigrants under any proposed legislation."}

### id=8151 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Of the roughly 15 percent of Americans who don’t have health insurance, "half of them made more than $50,000 a year."
- flat-rationale: The claim is unsupported by the evidence provided; there are no passages that confirm or deny the income level of uninsured Americans relative to $50,000.

### id=8489 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Terry McAuliffe "wants to raise your taxes $1,700 to pay for his infinite promises."
- flat-rationale: The evidence is topical and does not support the specific claim about McAuliffe raising taxes by $1,700; it lacks direct confirmation or refutation of this central assertion.

### id=8558 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Rhode Island's unemployment insurance system "is the most expensive such system in the country."
- flat-rationale: The evidence is entirely topical and does not address the claim about Rhode Island's unemployment insurance system being the most expensive in the country. There are no supporting or attacking facts related to the specific claim.

### id=8830 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: "The $18.8 billion in funding for K-12 education funding is the highest in Florida history and includes a record $10.6 billion in state funds."
- flat-rationale: The claim is partially accurate as it correctly states the funding levels but omits important context about pre-recession funding levels being higher.

### id=8853 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says President Barack Obama "spent nearly a trillion dollars on make-work government jobs."
- flat-rationale: The evidence does not support the claim that Obama spent nearly a trillion dollars on make-work government jobs; it is more focused on criticizing overall spending and deficits.

### id=8994 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: "We are seeing dramatic rate cuts" to Medicare that will affect seniors’ ability to keep their doctor, hospital and prevention services.
- flat-rationale: The claim contains an element of truth about Medicare rate cuts but omits important context that these cuts are part of a broader effort to control costs and do not necessarily mean reduced services for seniors.

### id=9546 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: A statewide poll showing 76 percent support and other surveys are a "strong indicator" of  broad public support in Milwaukee County for a $10.10 minimum wage
- flat-rationale: The claim is partially accurate as it highlights strong support in Milwaukee County but omits broader context showing varying levels of support across different polls.

### id=10062 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "We were told there would never be a case of Ebola in the United States."
- flat-rationale: The claim is false because there have been cases of Ebola in the United States, contradicting the assertion that it would never happen.

### id=10296 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The pass rate for a high school level test to join the military" is 35 to 40 percent.
- flat-rationale: The evidence does not support the claim's assertion about a 35 to 40 percent pass rate for high school level tests to join the military; it is topical information without confirming or attacking the specific numerical range given.

### id=10363 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "When Disney was looking to build Disney World, they came to Miami and we told Disney to take a hike."
- flat-rationale: {"label": "False", "rationationale": "The evidence does not support the claim; it is entirely topical and unrelated to Disney World's development in Florida. No passages confirm or refute the specific interaction with Disney mentioned."}

### id=10425 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: Since Rick Perry became governor, "poverty rates in Texas increased from 15.1% to 17.5% — which is higher than the national average."
- flat-rationale: The claim is partially accurate as poverty rates in Texas did increase from 15.1% to 17.5%, but it omits important context about long-standing demographic and economic factors that contribute to higher poverty rates in Texas compared to the national average.

### id=10584 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "A lot of people who go into prison straight, and when they come out they’re gay."
- flat-rationale: The claim is unsupported by the evidence and makes an unfounded assertion about people's sexual orientation upon release from prison.

### id=10623 — gold *Mostly-true*
- arg-aware predicted **False**
- flat-RAG predicted **Mostly-true** ✓
- claim: Wisconsin is "dead last in the Midwest for job creation."
- flat-rationale: The claim is directionally correct but omits the detail that Wisconsin was tied for last place rather than strictly last.

### id=10640 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: Says Israel Prime Minister Benjamin Netanyahu "didn't change his position" on a two-state solution.
- flat-rationale: The claim contains an element of truth but ignores critical facts that change the impression. Netanyahu had previously supported a two-state solution but his position became ambiguous during the election period.

### id=10680 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: By allowing brewpubs to sell beer, Georgia could become like Mexico with only a couple of manufacturers controlling all aspects of market.
- flat-rationale: The evidence does not support the claim that allowing brewpubs to sell beer would lead to a monopolized market like Mexico's. The provided passages are topical and do not address the central assertion about Georgia's potential market outcome.

### id=10712 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The founders of New Hampshire came up with the motto Live Free or Die."
- flat-rationale: The evidence passages are topical and do not provide any support or attack on the claim about New Hampshire's motto. The structural prior suggests a balanced view but without relevant supporting evidence for the central assertion, the claim is false.

### id=10725 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "U.S. police killed more people in just one month than the U.K.’s did in over a century."
- flat-rationale: The claim is not supported by the evidence and makes a misleading comparison. The provided passages are topical but do not address the specific numerical claims about police killings in the U.S. and U.K.

### id=10743 — gold *Half-true*
- arg-aware predicted **True**
- flat-RAG predicted **Half-true** ✓
- claim: "Medicaid expansion isn’t necessarily a very popular issue on the street."
- flat-rationale: The claim is partially accurate as it acknowledges the complexity and mixed views on Medicaid expansion, but lacks specific evidence to fully support or refute its popularity.

### id=11105 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The Iran deal says that "if any other country tries to undermine (Iran's) nuclear program, we have to help them defend themselves against Israel, Egypt, Saudis, our own allies."
- flat-rationale: {"label": "False", "rationationale": "The claim misrepresents the Iran deal by inventing a clause that does not exist. The JCPOA document explicitly states that Iran will not seek nuclear weapons and lacks any provision related to defending other countries against Israel, Egypt, or Saudi Arabia."}

### id=11184 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Scott Walker "had a 2.3 GPA when he was asked to leave Marquette University for cheating."
- flat-rationale: The evidence does not support the claim about Scott Walker's GPA or his expulsion from Marquette University for cheating; it is entirely topical and unrelated.

### id=11201 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Between 2008 and 2014, "criminal aliens accounted for 38 percent of all murder convictions in the five states of California, Texas, Arizona, Florida and New York."
- flat-rationale: The evidence does not support the specific claim about 38 percent of murder convictions; it provides general statistics on criminal aliens but no data matching the exact assertion.

### id=11661 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "If Trump had just put his father’s money in a mutual fund ... he’d have $8 billion."
- flat-rationale: The claim is speculative and overstates the potential outcome; it assumes a specific investment strategy that would yield $8 billion without evidence to support this precise figure.

### id=11685 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Wisconsin "is on pace to double the number of layoffs" this year.
- flat-rationale: The evidence is topical and does not confirm the claim that Wisconsin layoffs are on pace to double; it lacks specific data supporting this assertion.

### id=12130 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says her representation of an ex-boyfriend "who was then my friend" in a family law case is "something that lawyers do on a regular basis."
- flat-rationale: The evidence is entirely topical and does not address the claim about legal representation. The structural prior suggests a balance between Half-true and Barely-true, but without relevant support or attack passages, the claim must be evaluated as false due to lack of evidence supporting it.

### id=12252 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: "We’re the worst state in the country at moving people from welfare to work."
- flat-rationale: The evidence is entirely topical and does not support or attack the claim about Rhode Island's performance in moving people from welfare to work. The structural prior suggests a balanced view but lacks concrete evidence either way, leading to an overall negative assessment of the claim.

### id=12456 — gold *Barely-true*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **Barely-true** ✓
- claim: It's entirely possible that the Democratic nominee, [Hillary Clinton], earned more money giving a single speech on Wall Street than I made the six years that I was there back in the 1980s… In fact, it’s quite likely.
- flat-rationale: {"label": "Barely-true", "rationationale": "The claim suggests Hillary Clinton earned significantly more from a single speech than the speaker made in six years on Wall Street, which is likely an exaggeration. The evidence provides context but does not confirm or refute specific earnings figures, making it difficult to verify the exact comparison."}

### id=12568 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Hillary Clinton’s immigration platform would "create totally open borders."
- flat-rationale: The evidence shows that Clinton's statement was not a call for open borders and was taken out of context; thus the claim is misleading.

### id=13155 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Ron Johnson "helped companies ship jobs overseas."
- flat-rationale: The evidence shows the claim is misleading; Johnson voted for tax breaks but there's no direct evidence linking this to shipping jobs overseas. The context provided by Feingold's campaign and Johnson's own statements indicate a more nuanced situation than the claim suggests.

### id=13188 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: "10 cents on the dollar from the Clinton Foundation goes to charitable causes."
- flat-rationale: The evidence shows that the claim is misleading; while some sources suggest 15% goes to charitable causes, the overall context indicates a higher percentage of funds are used for charitable purposes compared to administrative costs.

