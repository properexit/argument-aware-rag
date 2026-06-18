# Disagreement audit

- Claims compared: 952
- arg-aware accuracy: 371/952 (39%)
- flat-RAG accuracy:  209/952 (22%)
- net arg-aware lift: +17%

## Category breakdown

- **both_correct**: 92
- **arg_only_right**: 279
- **flat_only_right**: 117
- **both_wrong_same**: 214
- **both_wrong_different**: 250

## Cases where arg-aware wins

### id=3 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "New Mexico was 46th in teacher pay (when he was elected), now we're 29th."
- arg-rationale: The claim is directionally correct but lacks precision; it omits important context about the methodology and improvements in teacher pay ranking. The evidence supports the overall trend but suggests minor caveats on exact rankings.

### id=66 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: Poor people go to a "payday lender...and they pay 300, 400, 500 percent interest."
- arg-rationale: The evidence overwhelmingly supports the claim that payday lenders charge extremely high interest rates, with one example showing an annual rate of 278 percent.

### id=70 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Congressman Paul introduces numerous pieces of substantive legislation each year, probably more than any single member of Congress."
- arg-rationale: The claim is directionally correct with strong support that Congressman Paul introduces numerous substantive pieces of legislation. The attacks are minor caveats and do not contradict the central assertion.

### id=126 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "First, he was in favor of my plan, now he's attacking it."
- arg-rationale: The claim is directionally correct but lacks specific context about the initial support and subsequent opposition. The evidence shows Walker did not explicitly endorse or act in favor of a Democratic plan, which aligns with the claim's assertion of changing positions.

### id=187 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Americans spend 100-million hours a year filling out these forms (FAFSA). That is the equivalent of 55,500 full-time jobs."
- arg-rationale: The claim has an element of truth regarding the time spent on forms but omits important context about the nature and necessity of these forms. The evidence suggests that while the time spent is significant, it's not exclusively due to FAFSA and includes other necessary paperwork.

### id=258 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Sen. McCain says it was not a mistake to vote against the Bush tax cuts ... but now says the tax cuts need to be made permanent."
- arg-rationale: The evidence shows that McCain initially opposed the Bush tax cuts but later changed his stance to support them when they were up for renewal, which aligns with the claim.

### id=386 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "I committed to public financing; (Obama) committed to public financing."
- arg-rationale: The claim is directionally correct as both candidates committed to public financing, but the evidence suggests some caveats and qualifications that prevent it from being fully unambiguous.

### id=422 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "I did very well with young people in Ohio, Massachusetts, California."
- arg-rationale: The claim is partially accurate as Obama did well with young voters in past elections but the evidence shows a decline in support among youth. The structural prior and low role-fit suggest caution against over-committing to full accuracy.

### id=568 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: Obama worked with "Sen. Dick Lugar, a Republican, to help lock down loose nuclear weapons."
- arg-rationale: The evidence strongly supports the claim that Obama worked with Sen. Dick Lugar on nuclear weapons issues and other foreign policy measures.

### id=582 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "For at least a year now, I have called for two additional brigades, perhaps three."
- arg-rationale: The evidence overwhelmingly supports the claim that the individual has called for sending additional brigades to Afghanistan.

### id=631 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Barack Obama "rejects everyone white, including his mother and his grandparents."
- arg-rationale: The claim is fabricated; evidence shows no support and multiple attacks refute the assertion that Obama rejects everyone white.

### id=643 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says McCain "supported George Bush's policies 95 percent of the time."
- arg-rationale: The claim is partially accurate but omits important context about McCain's voting record and policy support. The evidence suggests a nuanced view where McCain supported many of Bush's policies but also had some disagreements, making the 95 percent figure an oversimplification.

### id=660 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The U.S. energy policy is to "borrow money from China to buy oil from countries that don't like us."
- arg-rationale: The claim contains an element of truth about borrowing money and oil imports but omits important context regarding the complexity of energy policy and the nuances in international trade relations.

### id=699 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Senator Obama thinks we can achieve energy independence without more drilling and without more nuclear power."
- arg-rationale: The claim is partially accurate as Obama does advocate for energy independence without relying heavily on nuclear power or drilling, but it omits important details about his nuanced stance and the inclusion of some traditional sources in his plan.

### id=727 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Barack Obama got more campaign contributions from Fannie Mae and Freddie Mac "than any other member of Congress, except for the Democratic chairmen of the committee that oversees them."
- arg-rationale: The claim is directionally correct but lacks precision; it overstates by omitting the specific context and details about other members of Congress who received significant contributions from Fannie Mae and Freddie Mac.

### id=757 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "John McCain fought to rein in Fannie and Freddie...but Democrats blocked the reforms."
- arg-rationale: The claim is partially accurate as McCain did support reforms to Fannie and Freddie, but it omits the context that Democrats also supported similar measures and the reforms were blocked by Republican procedural moves.

### id=788 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: A mortgage buyback plan is "my proposal, it's not Sen. Obama's proposal, it's not President Bush's proposal."
- arg-rationale: The claim is directionally correct as McCain did propose a mortgage buyback plan distinct from others. However, the evidence suggests it was not uniquely his proposal and includes minor caveats that qualify its novelty.

### id=792 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "The Democrats in the Senate and some members of Congress defended what Fannie and Freddie were doing. They resisted any change."
- arg-rationale: The claim has some truth but omits important context. Democrats did resist changes to Fannie and Freddie, but the evidence shows mixed support and attack on this point.

### id=809 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "98 percent of small businesses make less than $250,000" and would not see a tax increase under Barack Obama's plan.
- arg-rationale: The evidence overwhelmingly supports the claim that 98 percent of small businesses make less than $250,000 and would not see a tax increase under Obama's plan.

### id=1051 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Contends that President Obama "literally said (if) his cap-and-trade proposals were to pass, that utility rates, his words now, would, 'necessarily skyrocket.'"
- arg-rationale: The evidence confirms that Obama's cap-and-trade proposals would have led to higher energy costs, supporting the claim.

### id=1052 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Obama has more czars than the Romanovs."
- arg-rationale: The evidence overwhelmingly supports the claim that Obama has more czars than the Romanovs, with no contradicting evidence provided.

### id=1189 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Medicare began as a public option and now holds 97 percent of the market share."
- arg-rationale: The claim is directionally correct as Medicare did start as a public option and it now covers the majority of seniors. However, the exact 97 percent market share figure lacks specific evidence to confirm.

### id=1324 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "The Stupak Amendment doesn't just say you can't use your federal insurance subsidy to pay for an abortion, it says, if you're getting a federal subsidy of any kind, you're not allowed to buy an insurance plan that covers abortion even with your own money."
- arg-rationale: The claim contains an element of truth but ignores critical facts that change the overall impression. While it's true that federal subsidies cannot be used for abortion coverage, individuals can still purchase plans with abortion coverage using their own money.

### id=1333 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Obama has "visited more countries and met with more world leaders than any president in his first six months in office."
- arg-rationale: The evidence overwhelmingly supports the claim that Obama visited more countries and met with more world leaders than any president in his first six months. No contradictory evidence is provided.

### id=1385 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says he "brought 1,200 jobs to Texas by moving his factories here from China."
- arg-rationale: The claim has an element of truth but omits important context; the jobs were moved from South Korea, not China, and Perry's statement overreaches by implying otherwise.

### id=1448 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Health care reform "would bring down the deficit by as much as $1 trillion over the next two decades."
- arg-rationale: The claim has an element of truth but omits important context about the uncertainty and potential for cost increases if certain measures are phased out over time.

### id=1460 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Our (Texas) graduation rate ranks 43rd out of 50 states."
- arg-rationale: The evidence overwhelmingly supports the claim that Texas ranks 43rd out of 50 states in graduation rate using consistent and reliable statistical methods.

### id=1512 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Fifty-seven" of  Rubio's 100 ideas "ultimately became law."
- arg-rationale: The claim has some accuracy but lacks important context; the evidence shows that while many of Rubio's ideas became law, there are significant caveats and qualifications from attack passages.

### id=1569 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "When we started this health care debate a year ago, 85 percent of the American people had health insurance, and 95 percent of the 85 percent were happy with it."
- arg-rationale: The claim is directionally correct with the evidence supporting that about 85% of Americans had health insurance and a majority were generally satisfied. However, it slightly overstates satisfaction levels by not specifying 'happy' as a general sentiment rather than specific policy approval.

### id=1574 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Individuals and small businesses will be hit by increases in health insurance premiums as high as 39 percent."
- arg-rationale: {"label": "Mostly-true", "rationationale": "The claim is directionally correct as some insurers have requested significant rate hikes, but it overstates the average impact and omits important context about subsidies for many individuals."}

### id=1576 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Health insurance companies' costs are only 4 percent of all health care spending."
- arg-rationale: The evidence overwhelmingly supports the claim that health insurance companies' costs are only 4 percent of all healthcare spending, with no contradictory evidence provided.

### id=1677 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says that under a new program jail "time for non-violent, mentally ill offenders has been reduced by 50 percent."
- arg-rationale: The evidence overwhelmingly supports the claim that jail time for non-violent, mentally ill offenders has been reduced by 50 percent, with no contradictory evidence provided.

### id=1781 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Texas has, now, the highest share of minimum-wage workers in the nation."
- arg-rationale: The evidence overwhelmingly supports the claim that Texas has the highest share of minimum-wage workers in the nation, with no contradictory evidence provided.

### id=1855 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Rick Perry attempted to fast-track unnecessary coal-fired power plants, which degrade air quality and would cost billions. Fortunately, a court stopped him."
- arg-rationale: The claim is directionally correct but lacks important context; the evidence supports Perry's actions being challenged and a court stopping him, though it does not fully substantiate the 'unnecessary' or cost claims.

### id=1909 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "I've issued a six-month moratorium on deepwater drilling."
- arg-rationale: The claim is partially accurate as Obama did issue a moratorium on deepwater drilling, but the evidence suggests it was more nuanced and temporary than suggested by the claim alone.

### id=1950 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Four years as a congressman, he [U.S. Rep. Hank Johnson] never talked  about MARTA."
- arg-rationale: The claim misattributes Congressman Hank Johnson's actions to a false statement about not talking about MARTA, which is fabricated and lacks any supporting evidence.

### id=1999 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "I have spent virtually every weekend since Memorial Day in the Panhandle."
- arg-rationale: The evidence strongly supports the claim that the speaker has spent significant time in the Panhandle, with no contradicting evidence.

### id=2087 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "The War in Afghanistan is officially the longest war Americans have ever been asked to endure."
- arg-rationale: The evidence confirms that the War in Afghanistan started in 2001 and continues to this day, making it the longest war in U.S. history.

### id=2092 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Sixty percent of the Hispanics" support the Arizona immigration law
- arg-rationale: The claim is fabricated; there is no evidence supporting the assertion that 60% of Hispanics support the Arizona immigration law, and multiple passages provide context contradicting this.

### id=2205 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: About 106,000 soldiers had "a prescription of three weeks or more" for pain, depression or anxiety medication.
- arg-rationale: The evidence overwhelmingly supports the claim without any contradictions.

### id=2284 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "The government is trying to now close the Lincoln Memorial for any kind of large gatherings."
- arg-rationale: The claim is fabricated; there is no evidence supporting the government's intention to close the Lincoln Memorial for large gatherings. The provided evidence does not relate to the claim and instead includes unrelated attacks on other statements or policies.

### id=2316 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Florida is enjoying its lowest crime rate in 39 years."
- arg-rationale: The claim is directionally correct with Florida experiencing a low crime rate. However, the evidence includes minor caveats and qualifications that prevent it from being fully unambiguous or uncontested.

### id=2341 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "My supporters aren't special interest groups in Madison and Milwaukee."
- arg-rationale: The claim is directionally correct as it suggests his supporters are not special interest groups, but the evidence includes minor caveats and qualifications that suggest some support may come from business interests.

### id=2356 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "He's the only candidate who's balanced budgets and brought jobs to Providence."
- arg-rationale: The claim is directionally correct but lacks specificity and context. While the evidence supports Cicilline's involvement in job creation efforts during his tenure as mayor of Providence, it does not provide sufficient detail to substantiate 'balancing budgets' or being uniquely responsible for bringing jobs to Providence.

### id=2442 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: A bill by Earl Blumenauer would "mandate GPS tracking devices on all our vehicles."
- arg-rationale: The evidence shows no bill by Earl Blumenauer mandates GPS tracking on vehicles; the claim is fabricated or grossly misleading.

### id=2460 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Politician Reid Ribble wants to phase out Social Security, forcing Wisconsin seniors to fend for themselves."
- arg-rationale: {"label": "Pants-fire", "rationationale": "The claim misattributes Reid Ribble's stance on Social Security and exaggerates his intentions to eliminate the program, which is not supported by any evidence. The evidence clearly shows that the claim is fabricated."}

### id=2470 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "If you look at the application for a security clearance, I have a clearance that even the president of the United States cannot obtain because of my background."
- arg-rationale: The claim is fabricated as it misrepresents the security clearance process and implies a level of clearance that does not exist or cannot be obtained based on background alone.

### id=2533 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Newspapers say Florida made bad investments, lost hundreds of millions of dollars, billions in pension funds lost. Who was in charge of Florida's investments? Alex Sink."
- arg-rationale: The claim contains elements of truth but omits important context about the governance structure and shared responsibility in managing Florida's investments.

### id=2633 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: As state treasurer, Alexi Giannoulias "lost $73 million in our kids’ college savings."
- arg-rationale: The claim has an element of truth but omits important context about the college savings fund's performance and management. The evidence suggests some losses occurred but does not definitively confirm or refute the specific $73 million figure, indicating a need for more precise information.

### id=2720 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says state Senate candidate "Monk Elmer voted to exceed the (school district property tax) spending caps."
- arg-rationale: The claim attributes a voting action to Monk Elmer that did not occur; there is no evidence of such a vote and the attacks refute the premise.

### id=2731 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "We have empowered state insurance commissioners to review the rate hikes that are taking place in states. And in some states like North Carolina, they have already used it and rolled back premium increases by 25 percent."
- arg-rationale: The claim is directionally correct as state insurance commissioners do review rate hikes and have rolled back increases in some cases. However, the specific 25 percent rollback figure for North Carolina is not substantiated by the provided evidence.

### id=2777 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Georgia and other states with weak gun laws have more crime.
- arg-rationale: The claim is directionally correct that states with weak gun laws may have more crime, but it lacks nuance and context provided by the evidence, such as other factors influencing crime rates.

### id=2811 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: $65 billion "would be added to the deficit if we keep the cuts for people on the highest incomes."
- arg-rationale: The claim is directionally correct but omits important context about the complexity and uncertainty of deficit reduction measures. The evidence supports the central assertion that allowing tax cuts to expire would add to revenue, but it also includes minor caveats about the exact figures and political feasibility.

### id=2876 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Ohio ranks 46th in the country in putting dollars in the classroom."
- arg-rationale: The claim is directionally correct but lacks precision; Ohio's ranking in administrative spending is not directly supported by state-specific data and the evidence suggests it may be an extrapolation from national figures.

### id=2910 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Measures taken by my administration "have saved taxpayers $1 billion."
- arg-rationale: The claim is directionally correct with the evidence supporting significant savings, but the exact figure of $1 billion may be an estimate and could vary over time.

### id=2993 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "In 1981, Matagorda, Brazoria, and Galveston Counties all opted out of the Social Security program for their employees. Today, their program is very, very well-funded and there is no question about whether it’s going to be funded in" years to come.
- arg-rationale: The claim is directionally correct but omits important details about the Galveston plan's lack of cost-of-living increases and the age of studies comparing its performance to Social Security.

### id=3021 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: State governments have little ability to stimulate job growth in the short run.
- arg-rationale: {"label": "True", "rationationale": "The evidence overwhelmingly supports the claim that state governments have little ability to stimulate job growth in the short run, with economic experts emphasizing the limited influence of governors on short-term economic performance due to national trends and larger economic forces."}

### id=3027 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "There hasn't really been a lot of net growth in the federal workforce when you compare it to say, 1990."
- arg-rationale: The claim is partially accurate as there has been limited net growth in the federal workforce since 1990, but it omits important context about hiring patterns and demographic changes that affect this trend.

### id=3037 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Obama’s mid-term approval ratings are similar to other presidents who went on to re-election.
- arg-rationale: The claim has some truth but omits important context. While Obama's approval ratings were low during the mid-term elections, they are not entirely dissimilar to other presidents who faced re-election; however, direct comparisons with historical data are weak and context-specific nuances are missing.

### id=3107 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "The number of inmates since 2000 on death row dying of natural causes has now surpassed the number of inmates executed."
- arg-rationale: The evidence supports the claim that more inmates have died of natural causes than have been executed since 2000.

### id=3121 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Last year, out of the 500,000 (in) population growth we had in the state of Texas, about 250,000 of the 500,000 came to Texas... from the other 49 states."
- arg-rationale: The claim is partially accurate as Texas did see significant population growth from other states, but the evidence suggests it was not precisely 250,000 out of 500,000 and other factors like birth rates also contributed. The structural prior and low role-fit scores indicate caution against overcommitting to a stronger truth claim.

### id=3136 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Secure Communities "has a proven track record of enhancing public safety by focusing on violent offenders and those that pose a threat to our communities and our national security."
- arg-rationale: The claim has some support but omits important context; evidence suggests the program focuses on violent offenders and threats to public safety, but also includes caveats questioning its effectiveness and scope.

### id=3232 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "There is nothing in the current state public records law that prohibits sensitive or confidential business information from being just that, confidential."
- arg-rationale: The evidence supports the claim that sensitive or confidential business information can remain confidential under current state public records law.

### id=3331 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Unfortunately we have documented instances where people defecated in the (Statehouse) building."
- arg-rationale: The claim about documented instances of people defecating in the Statehouse building is not supported by any evidence and appears to be a fabricated or highly exaggerated statement.

### id=3369 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says city of Portland has a one-time $22 million surplus
- arg-rationale: The claim about the $22 million surplus is partially accurate but lacks important context and qualifications from the evidence.

### id=3381 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "On my first day in office, I ordered a review of every regulation in the pipeline and every contract exceeding $1 million."
- arg-rationale: The claim is accurate but the evidence suggests it was not unique to Clinton and lacks context on previous similar actions by other presidents.

### id=3434 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: Says a "rather extraordinary amount of non-classroom employees" were added by Texas school districts over the last decade.
- arg-rationale: The claim is directionally correct with evidence supporting an increase in non-classroom employees. However, the attack passages suggest some caveats and qualifications that prevent a 'True' rating.

### id=3453 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Studies have shown that in the absence of federal reproductive health funds, we are going to see the level of abortion in Georgia increase by about 44 percent.
- arg-rationale: The claim has some support from studies suggesting abortion rates may rise without federal funding, but the evidence also includes significant caveats and lacks direct confirmation of a 44% increase specifically for Georgia.

### id=3455 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: The coalition of Arab states against Libya’s Moammar Gadhafi is the biggest coalition against a fellow Arab leader since the Persian Gulf War in 1990-1991.
- arg-rationale: The evidence supports the claim that the coalition against Gadhafi was significant and involved many Arab states, with no contradicting information provided.

### id=3460 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Ohio Director of Job Creation "Mark Kvamme just clawed back about $900,000 from companies that made promises and they didn't keep them."
- arg-rationale: The claim has some factual basis but omits important context and overstates the impact. The evidence suggests that while there was a clawback of funds from companies, attributing significant job creation solely to this action is misleading.

### id=3541 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Across the United States, 25 percent of voting age African Americans do not have the photo ID that this bill would require."
- arg-rationale: The claim has an element of truth but omits important context about the variability in photo ID requirements across states and the specific provisions of Wisconsin's bill.

### id=3575 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: On federal stimulus money for expanding rail service.
- arg-rationale: The evidence overwhelmingly supports the claim that federal stimulus money can be used for expanding rail service without prohibitions against supplanting state funding.

### id=3674 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says it probably costs more than $300,000 to run for a seat on the Pedernales Electric Cooperative board of directors.
- arg-rationale: The claim is based on an invented figure with no supporting evidence and multiple attack passages that refute the premise.

### id=3697 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: The federal debt is more than $14 trillion, "almost equal to the size of our entire economy," and "every child born today inherits a $45,000 share of the national debt before they take their first breath."
- arg-rationale: The claim is directionally correct but omits important context about the distinction between public debt and total federal debt. The central assertion of high national debt relative to GDP is supported, but the specific figures are slightly misleading without clarification.

### id=3706 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says people in Africa "literally walk two and three hundred miles" in order to vote.
- arg-rationale: The evidence shows no support for the claim and multiple attacks refute it as fabricated or exaggerated; people do not literally walk hundreds of miles to vote in Africa.

### id=3709 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: "I'm well aware that medical marijuana is a recognized, medical, viable treatment for this sort of [pancreas] pain condition."
- arg-rationale: The claim misrepresents medical marijuana as a recognized treatment for pancreas pain specifically, but the evidence shows it is approved for broader conditions like chronic and severe pain without specifying pancreas pain. The structural prior suggests fabrication or exaggeration.

### id=3710 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Georgia is "one of only about seven states in the country" that has a AAA bond rating.
- arg-rationale: The evidence confirms that Georgia has a AAA bond rating and supports the claim that it is one of only a few states with this rating.

### id=3731 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Mostly-true**
- claim: "The Border Patrol has 20,000 agents – more than twice as many as there were in 2004."
- arg-rationale: The evidence overwhelmingly supports the claim that the number of Border Patrol agents has more than doubled since 2004.

### id=3803 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says the Obama administration approved a major disaster declaration for Oklahoma in 2009, when nine of the state’s 77 counties burned for "about three days," while Texas wildfires have been burning for longer without such a declaration.
- arg-rationale: The claim is directionally correct that Oklahoma received a major disaster declaration while Texas did not for similar circumstances. However, the evidence suggests the attack passages are minor caveats rather than refutations of the central assertion.

### id=3818 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Obama-Nelson economic record: Job creation ... at slowest post-recession rate since Great Depression."
- arg-rationale: The claim is directionally correct but omits important context about the severity and duration of the recession under Obama compared to Reagan.

### id=3841 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Medicare "only has about 50 percent of it paid for by either premiums or payroll taxes, and the rest is deficit spending ... or debt spending."
- arg-rationale: The claim is partially accurate as Medicare does rely on premiums and payroll taxes for part of its funding, but it omits important context about the complexity of Medicare financing and the role of general revenues. The attacks are mostly caveats rather than refutations.

### id=3904 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "We've seen 115,000 jobs created in the American auto industry since GM and Chrysler emerged from bankruptcy."
- arg-rationale: The claim is partially accurate but omits important context about the variability in job creation numbers and the broader automotive industry landscape.

### id=3980 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: Says Gov. Chris Christie’s "poll ratings have been going up."
- arg-rationale: The evidence does not support the claim; it instead provides contradictory information about Christie's poll ratings and context from other political figures.

### id=4095 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "As we've seen that federal support for states diminish, you've seen the biggest job losses in the public sector -- teachers, police officers, firefighters losing their jobs."
- arg-rationale: The claim is directionally correct but lacks specific evidence linking federal support reduction to public sector job losses. The provided evidence supports the general trend of job loss in the public sector but does not directly confirm the cause-and-effect relationship asserted.

### id=4131 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "The State Election Board has issued nearly $275,000 in fines to violators of absentee ballot laws."
- arg-rationale: The evidence overwhelmingly supports the claim that fines have been issued for violations of absentee ballot laws without any contradictions.

### id=4161 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Active duty males in the military are twice as likely to develop prostate cancer than their civilian counterparts."
- arg-rationale: The claim is directionally correct but lacks important context about screening practices and survival rates. The evidence supports the higher likelihood of diagnosis among military personnel due to aggressive testing, though it notes this may not reflect actual incidence or mortality differences.

### id=4233 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "I cut more as a percentage out of government than any state in the country this past decade. And where is Michigan in terms of its economic growth? Cutting did not result in economic growth."
- arg-rationale: The claim is directionally correct in stating Granholm cut government spending significantly and argues it did not lead to economic growth. However, the evidence suggests tax increases may have also contributed to Michigan's economic distress, qualifying the central assertion.

### id=4243 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: The United States has "the longest surviving constitution."
- arg-rationale: The claim is directionally correct as the U.S. Constitution is indeed one of the oldest surviving constitutions, but it omits important context about other long-standing constitutional systems.

### id=4272 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Twenty-five states have lower unemployment than Texas" which is "tied with Mississippi for more minimum-wage jobs than anywhere in the United States."
- arg-rationale: The evidence supports the claim that Texas is tied with Mississippi for having the most minimum-wage jobs at the federal level of $7.25 or below, and provides data on unemployment rates in states.

### id=4526 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: Wisconsin's new state budget includes "a 15 percent increase for road construction and yet we’ve got local towns tearing up" paved roads and replacing them with gravel.
- arg-rationale: The claim misattributes the cause of towns switching to gravel roads and overstates the impact of the state budget on local road conditions; evidence shows no direct link between the budget increase and towns tearing up paved roads.

### id=4537 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "My home state since June of 2009 created 40 percent of the new jobs in America."
- arg-rationale: The claim is directionally correct with Texas creating a significant portion of new jobs since June 2009, but it omits important context about other states' job creation and economic conditions during the Great Recession.

### id=4568 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says Vince Polistina is "collecting nearly $70,000 in taxpayer-funded salaries -- plus a government pension."
- arg-rationale: The claim contains an element of truth but omits important context about the nature of Polistina's compensation and pension. The attacks provide significant caveats that undermine the misleading framing.

### id=4588 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says he "came to the Republican Party sooner in age" than Ronald Reagan.
- arg-rationale: The evidence supports the claim that Trump 'came to the Republican Party sooner in age' than Ronald Reagan, as it shows Trump's early registration and activity within the party compared to Reagan.

### id=4628 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "Since 1970, the Clean Air Act has reduced toxic and health-threatening air pollution by 60 percent while our economy has grown more than 200 percent."
- arg-rationale: The claim is directionally correct but omits important context about the specific pollutants and economic growth details. The evidence supports a significant reduction in air pollution but lacks specifics on the exact 60 percent figure and economic growth percentage.

### id=4711 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says the main Central Texas food bank is delivering 50 percent more food to the poor than three years ago.
- arg-rationale: The evidence supports the claim that food bank deliveries have increased significantly, though some passages suggest potential overstatement or need for qualification. The central assertion is accurate but may benefit from minor clarification.

### id=4715 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Mitt Romney’s housing policy is, "Don’t try and stop the foreclosure process. Let it run its course and hit the bottom."
- arg-rationale: The claim contains an element of truth but omits important context about Romney's housing policy. The evidence suggests that while Romney did not explicitly stop foreclosures, his policies may have had indirect effects on the housing market.

### id=4769 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Under a Wisconsin bill, "minor offenses such as violating pet leash laws, seat belt laws, parking infractions, etc., would now be arrestable offenses."
- arg-rationale: The claim is partially accurate as minor offenses could become arrestable under the bill, but it overstates the extent and implications of these changes without important context.

### id=4780 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Mostly-true**
- claim: "Ronald Reagan raised the national debt 18 times."
- arg-rationale: The evidence overwhelmingly supports the claim that Ronald Reagan raised the national debt ceiling 18 times during his presidency.

### id=4822 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: A recall election for Wisconsin governor would cost "$7.7 million -- $7.7 million that may already be allocated to merit raises for teachers or health care for the poor or school books for your kids."
- arg-rationale: The claim accurately states the cost of a recall election but omits important context about how those funds might be allocated and the broader financial implications for education and social services.

### id=4888 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: Says the unemployment rate for college graduates is 4.4 percent and over 10 percent for noncollege-educated.
- arg-rationale: The evidence overwhelmingly supports the claim that the unemployment rate for college graduates is around 4.4 percent and over 10 percent for noncollege-educated individuals.

### id=4929 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: In 1993, Newt Gingrich "first advocated for the individual mandate in health care. And as recently as May of this year, he was still advocating" for it.
- arg-rationale: The claim is directionally correct that Gingrich advocated for the individual mandate in 1993 and as recently as May 2011. However, it omits nuances about his stance over time and includes a minor factual error regarding the exact date of his recent advocacy.

### id=5124 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Newt Gingrich "co-sponsored a bill with Nancy Pelosi that would have given $60 million a year to a U.N. program supporting China’s brutal one-child policy."
- arg-rationale: The evidence shows the claim is fabricated; there is no record of such a bill co-sponsored by Newt Gingrich and Nancy Pelosi related to China's one-child policy.

### id=5131 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: The education tax burden for Shelby County -- and Tennessee -- is "one of the lowest in the country."
- arg-rationale: The evidence supports that Tennessee has a low education tax burden but lacks specific data for Shelby County and does not directly confirm the claim's accuracy.

### id=5314 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "Ohio has one of the highest provisional ballot rates in the country, and many of them go uncounted each election."
- arg-rationale: The evidence strongly supports the claim that Ohio has a high provisional ballot rate and many go uncounted due to address mismatches and database issues.

### id=5450 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Rick Santorum "opposes right-to-work"
- arg-rationale: The claim that Rick Santorum opposes right-to-work is partially accurate but lacks important context. While there are supportive statements indicating his stance against certain policies, the evidence also includes attacks suggesting he supports right-to-work legislation in other contexts.

### id=5470 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: Pasco County schools have graduation rates "substantially higher than the state average" and dropout rates "below the state average."
- arg-rationale: The evidence overwhelmingly supports the claim that Pasco County schools have graduation rates substantially higher than and dropout rates below state averages, with no contradicting evidence.

### id=5510 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "They're paying a less rate of tax -- these richest people in America -- than they have in the last 80 years."
- arg-rationale: The claim is directionally correct but oversimplifies the tax situation by not clarifying that it refers to marginal tax rates and does not account for loopholes and shelters which can affect average tax rates.

### id=5536 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Says "my plan is a property tax cut."
- arg-rationale: The claim is partially accurate as it describes a tax cut but omits important context about the nature of the proposed changes and their impact on different taxpayers.

### id=5551 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "While 9,000 state employees were added to the state’s payroll, Oregon’s revenue forecasts dropped by more than $4 billion."
- arg-rationale: The claim is partially accurate as it mentions both job growth and revenue forecast drops, but the specific figures and their direct relationship are not fully supported by the evidence provided.

### id=5698 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Under the House Republican budget, "if these cuts were to be spread out evenly … the year after next, nearly 10 million college students would see their financial aid cut by an average of more than $1,000 each."
- arg-rationale: The claim contains an element of truth about potential cuts to financial aid but omits important context and details that would change the overall impression. The evidence suggests the impact might be overstated or mischaracterized, making it partially accurate but misleading.

### id=5746 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: The U.S. Supreme Court has not traditionally asked a lot of questions during oral arguments.
- arg-rationale: The evidence strongly supports the claim that the Supreme Court does not traditionally ask a lot of questions during oral arguments, with no contradictory evidence provided.

### id=5993 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Larry Taylor gave "in-state tuition to illegal immigrants."
- arg-rationale: The claim attributes an action to Larry Taylor that is not supported by any evidence and contradicted by passages detailing other states' reciprocity agreements and federal education laws.

### id=6011 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Women have come through the recession worse off than men … the numbers bear that out. We went from a 7 percent unemployment rate for women when he (President Barack Obama) was elected to an 8.1 percent now."
- arg-rationale: The claim is directionally correct that women have faced worse unemployment rates during the recession. However, some evidence suggests the gap may be overstated or nuanced in certain contexts, qualifying the overall statement.

### id=6262 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Foreign Chinese prostitution money is allegedly behind the groups funding Congressman Sean Duffy’s Republican Majority."
- arg-rationale: The claim is not only unsubstantiated but also contradicted by multiple sources that have debunked similar allegations as false.

### id=6295 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The Affordable Care Act "will likely go down as the biggest tax increase in history."
- arg-rationale: {"label": "Pants-fire", "rationationale": "The claim is not just factually incorrect but also exaggerates and misrepresents the ACA's impact as a 'biggest tax increase in history', which is unsupported by evidence and contradicted by historical data on actual tax increases."}

### id=6333 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: "What I look at every month is how many more New Jerseyans are back to work. You have another 9,900 last month that are back to work and over almost 90,000 that are back to work now since I became governor."
- arg-rationale: The evidence shows that the claim's specific figures are incorrect and there is no support for the exact numbers mentioned by the governor.

### id=6473 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Paul Ryan's budget relies on the same $700 billion in savings from Medicare that Mitt Romney and other Republicans have been attacking Democrats about.
- arg-rationale: The evidence supports that Paul Ryan's budget relies on similar savings from Medicare as those attacked by Republicans, confirming the claim.

### id=6532 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "His new running mate, Congressman Ryan, put forward a plan that would let Governor Romney pay less than 1 percent in taxes each year."
- arg-rationale: The claim is directionally correct as Congressman Ryan's plan would likely lower Romney's tax rate, but it overstates the extent to which Romney could pay less than 1 percent in taxes each year based on available evidence.

### id=6571 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says they said "it was impossible to balance a budget at the same time, with an $11 billion deficit" and "we did it."
- arg-rationale: The claim contains an element of truth but omits important context about the budget balancing process and the initial deficit size.

### id=6745 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Says Barack Obama's comments indicate he "believes in redistribution" of wealth.
- arg-rationale: The claim is directionally correct as Obama did express support for redistribution in the past. However, it omits important context about the long-standing nature of wealth redistribution policies in America.

### id=6772 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says "One of the state’s largest governments made charging this tax one of their top priorities just this year."
- arg-rationale: The claim misrepresents the legislative process and uses fabricated language that does not fit the actual situation described in the evidence.

### id=6816 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Under Barack Obama, the U.S. now has the "lowest workforce since (President Jimmy) Carter."
- arg-rationale: The claim has an element of truth but omits important context about demographic changes and aging population affecting workforce participation rates.

### id=6839 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says U.S. Senate opponent Tommy Thompson favors raising taxes on small businesses.
- arg-rationale: The claim contains an element of truth but ignores critical facts that change the overall impression. Thompson's record includes tax increases, but the evidence does not strongly support the claim that he favors raising taxes on small businesses specifically.

### id=6858 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says opponent U.S. Rep. Gwen Moore ‘is Wisconsin’s most absent member of Congress, missing nearly 17 percent of the House votes in the second quarter of 2012.’
- arg-rationale: The claim is directionally correct but omits the specific time frame and context. The evidence supports Gwen Moore's high absenteeism in a particular quarter, though it does not fully confirm the exact 17% figure without more precise data.

### id=6905 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The Canadians — they (dropped) their tax rates to 15 percent. The average tax rate on businesses in the industrialized world is 25 percent."
- arg-rationale: The claim is directionally correct but omits important details about effective tax rates and the context of various tax breaks that lower actual corporate tax burdens in Canada and other countries.

### id=6919 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "The tax burden on Virginia families was lower under Tim Kaine than under George Allen."
- arg-rationale: The claim has an element of truth but the evidence shows significant caveats and contradictions regarding Kaine's actual impact on tax burdens compared to Allen.

### id=6933 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Oil production is down 14 percent this year on federal land."
- arg-rationale: The claim is partially accurate as oil production has decreased on federal land, but the evidence suggests that factors beyond government policy, such as OPEC decisions and market dynamics, also play a significant role in this trend.

### id=7008 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "6,400 Ohioans ... lost manufacturing jobs in the month of September."
- arg-rationale: The claim is partially accurate but omits the time frame and context. The evidence confirms job losses in Ohio but does not specify the exact month of September or the broader period under consideration.

### id=7038 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "There is no war on coal. Period. There are more coal jobs and more coal produced in Ohio than there were five years ago, in spite of the talking points and the yard signs."
- arg-rationale: The evidence overwhelmingly supports the claim that there are more coal jobs and coal production in Ohio than five years ago, with no contradicting evidence.

### id=7118 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Our welfare system now consumes 42 percent of our budget."
- arg-rationale: The claim is partially accurate but omits important context about the methodology and age of the data. The evidence suggests that while welfare may consume a significant portion of the budget, the specific figure cited lacks recent validation and includes broader definitions than typical cash assistance.

### id=7135 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "If you and I fail to defund ObamaCare now, some 16,000 new IRS agents will be begin prying into our private medical records, eyeing each and every one of our treatments and prescriptions for "violations’."
- arg-rationale: The claim is fabricated; PolitiFact has previously rated similar claims as Pants on Fire and found no evidence of the IRS prying into private medical records or creating a national health care database.

### id=7223 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "Eleven states complete their [legislative] sessions within three calendar months, and another five only meet biennially."
- arg-rationale: The claim is directionally correct but omits important context about states with biennial sessions and the inclusion of resolutions.

### id=7268 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Nearly a quarter of all adults in this state have some college credit without a degree."
- arg-rationale: The evidence supports the claim that many adults have some college credit without a degree, but it does not provide specific state-level data to confirm 'nearly a quarter' for this particular state.

### id=7334 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Says his budget provides "the highest state funding level in history" for education.
- arg-rationale: The claim is partially accurate as the budget does provide a high level of funding for education, but it omits important context about inflation-adjusted spending and historical comparisons that cast doubt on whether it's truly 'the highest state funding level in history'.

### id=7378 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Military spending cuts, known as the sequester, were President Barack Obama’s idea.
- arg-rationale: The claim is partially accurate as the sequester was an idea that came out of Obama's White House to force negotiations, but it omits important context that both parties agreed to the sequestration in 2011.

### id=7426 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "There’s more murders with hammers last year than...shotguns and pistols and AK-47s."
- arg-rationale: The claim is fabricated as it misrepresents the data on weapon-related homicides; evidence shows firearms are the leading cause of murder deaths.

### id=7524 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The transportation package passed by the General Assembly would impose the "largest tax increase in Virginia’s history."
- arg-rationale: The claim is partially accurate as the proposed tax increase would be significant, but it overstates by ignoring historical context and other large tax increases. The evidence shows both support for the scale of the proposal and attacks on its characterization as unprecedented.

### id=7543 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Scientists tell us that we could have a cure in 10 years for Alzheimer's" were it not for "overzealous regulators, excessive taxation and greedy litigators."
- arg-rationale: {"label": "Pants-fire", "rationationale": "The claim attributes specific reasons for the lack of a cure to overzealous regulators, excessive taxation, and greedy litigators, but there is no evidence supporting these assertions. The provided evidence does not mention Alzheimer's research or any of the claimed obstacles."}

### id=7562 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Already, a prototype driverless car has traveled more than 300,000 miles in the crowded maze of California streets without a single accident."
- arg-rationale: The claim is directionally correct with the evidence supporting that a prototype driverless car has traveled over 300,000 miles without an accident. The low role-fit of attack passages suggests they are minor caveats rather than refutations.

### id=7565 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Quite frankly, it was during the Bush years of spending, multiplied now by the Obama years that we have this mess."
- arg-rationale: The claim is directionally correct in pointing to increased spending during Bush and Obama years, but it lacks specific context or nuance about the stability of government spending as a percentage of GDP over time.

### id=7577 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: When students leave our high schools and they go to the community college, 70-75 percent of them have to pay to take remedial math.
- arg-rationale: The evidence supports the claim's direction but lacks specific data on remedial math costs at community colleges and focuses more on general academic preparedness issues.

### id=7680 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "No poll done this year ... shows less than a majority to reinstate a federal ban on assault weapons."
- arg-rationale: The evidence supports the claim that polls show majority support for reinstating a federal ban on assault weapons, but some passages suggest this is not uniformly consistent across all recent polls.

### id=7685 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Right now, if Rhode Island police come across a young person with a gun, "they really don't legally have the right to take it away from them."
- arg-rationale: The claim is partially accurate as Rhode Island police generally cannot seize guns from legal owners, but it omits important context about the ability to seize weapons from those who are legally prohibited from owning them.

### id=7692 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says 315,000 mostly minority Texas students are enrolled in failing schools.
- arg-rationale: The claim is directionally correct but lacks precision; it accurately identifies a significant number of minority students in failing schools but omits important context and specifics about the exact criteria for 'failing' schools.

### id=7721 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Federal prosecutions for lying on background checks to buy guns are "down 40 percent" under President Barack Obama.
- arg-rationale: The claim about federal prosecutions being down 40 percent is not directly supported by the evidence. While there are references to background checks and their enforcement, these do not substantiate the specific numerical decline in prosecutions under Obama.

### id=7728 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "We’re spending less money today, in upcoming fiscal year 2014 than the Corzine-Buono budget spent in fiscal year 2008."
- arg-rationale: The evidence supports the claim that spending is lower in fiscal year 2014 compared to Corzine-Buono's budget in fiscal year 2008, but it includes partial support and context that slightly qualifies this comparison.

### id=7758 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Among Hispanics, support for immigration reform is close to universal.
- arg-rationale: The evidence strongly supports the claim that Hispanics overwhelmingly support immigration reform, but includes minor caveats about specific political actions and projections that do not directly contradict the central assertion.

### id=7810 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "This budget also reflects the smallest state government workforce per 1,000 residents in Florida in this century."
- arg-rationale: The claim is directionally correct based on the evidence supporting a smaller state workforce per capita in Florida. However, some passages suggest that the context and methodology of such comparisons may be nuanced, warranting minor qualification.

### id=7838 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says the word "Dhimmitude" is on page 107 of the health care law and means "Muslims are specifically exempted from the government mandate to purchase insurance."
- arg-rationale: The claim is fabricated; the word 'Dhimmitude' does not appear in the health care law and Muslims are not specifically exempted from the mandate to purchase insurance.

### id=7900 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: The Wisconsin Economic Development Corporation is a "proven job creator."
- arg-rationale: The claim is partially accurate as WEDC does aim to create jobs, but the evidence suggests it may exaggerate job creation figures and lacks clear proof of significant success.

### id=8011 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Austin is the "largest city in America without a congressional district anchored in it."
- arg-rationale: The evidence overwhelmingly supports the claim that Austin is the largest city without a congressional district anchored in it, with no contradictory evidence provided.

### id=8303 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Tuition at Rutgers has increased 10 percent since Gov. Chris Christie took office because he "cut funding for higher education."
- arg-rationale: The claim has an element of truth but omits important context about the role of inflation and legislative decisions in tuition increases.

### id=8320 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Today many Florida teachers are at risk of having their pay impacted by the performance of children who are not even in their classrooms or subject areas."
- arg-rationale: The claim is directionally correct that teachers' pay can be impacted by student performance outside their classrooms or subject areas, but the evidence suggests this impact may not be as widespread or significant as implied.

### id=8336 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: If sea levels rise six feet due to climate change, Waterplace Park in Providence and Wickford village would be swamped
- arg-rationale: The evidence strongly supports the claim that rising sea levels due to climate change would significantly impact areas like Waterplace Park in Providence and Wickford village.

### id=8419 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Barely-true**
- claim: "Virtually every person across this country has seen premiums going up and up and up" due to Obamacare.
- arg-rationale: The claim is refuted by evidence showing that premiums did not universally increase and many people gained coverage under Obamacare.

### id=8433 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Property taxes have increased 20 percent under four years of Chris Christie."
- arg-rationale: The claim is directionally correct as property taxes did increase under Christie's tenure, but the exact 20 percent figure may be an overstatement or lacks precise context. The evidence shows a mix of support and minor caveats.

### id=8486 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "Even after Obamacare is fully implemented, there still will be tens of millions of people not covered."
- arg-rationale: The evidence supports the claim that even after full implementation of Obamacare, tens of millions would still be uninsured.

### id=8503 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Before the Republican wave in 2010, Democrats had an advantage on the generic ballot in Congress. Even in 1994 with the Gingrich revolution ... Democrats had that advantage."
- arg-rationale: The evidence overwhelmingly supports the claim that Democrats had an advantage on the generic ballot in Congress before the Republican wave in 2010 and even in 1994.

### id=8511 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: A planning group said that to meet anticipated traffic demands by 2035, Interstate 35 between Austin and Round Rock will need a dozen additional lanes going north and 14 additional southbound lanes.
- arg-rationale: The claim is partially accurate as it reflects the need for additional lanes on I-35 but omits important context about other congestion-reducing strategies and the misleading nature of the statement according to experts.

### id=8667 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Iran President Hassan "Rouhani has more Cabinet members with Ph.D.s from American universities" than members of Barack Obama’s Cabinet.
- arg-rationale: The evidence overwhelmingly supports the claim that Rouhani's Cabinet has more members with Ph.D.s from American universities compared to Obama’s Cabinet, with no contradicting evidence.

### id=8673 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Whether the Amendment passes or not, the medical use of marijuana is a federal criminal offense."
- arg-rationale: The evidence overwhelmingly supports the claim that marijuana remains a federal criminal offense regardless of state-level legalization for medical use.

### id=8676 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Gov. Rick Scott "backed the federal shutdown."
- arg-rationale: The claim misleads by implying direct support for the federal shutdown; while Scott opposed Obamacare, there's no evidence he backed the shutdown itself.

### id=8683 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Medicare costs have slowed down dramatically. In fact, the first two months of this fiscal year, Medicare costs were down even in nominal terms relative to the previous year."
- arg-rationale: The evidence strongly supports the claim that Medicare costs have slowed down dramatically and were even lower in nominal terms relative to the previous year for the first two months of the fiscal year.

### id=8764 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "I cut spending while serving in the state Legislature"
- arg-rationale: The evidence strongly supports the claim that the speaker cut spending while serving in the state Legislature, but includes minor caveats about the broader context of overall budget increases and other factors.

### id=8841 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "The federal minimum wage is worth about 20 percent less than it was when Ronald Reagan" gave his first address to a joint session of Congress.
- arg-rationale: The claim is directionally correct but lacks precision; the evidence shows the minimum wage was indeed lower during Reagan's tenure compared to today, though not exactly by 20 percent when he gave his first address.

### id=8924 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Dollar General "added 2,500 stores and 20,000 jobs" during his four-year tenure as CEO.
- arg-rationale: The claim is directionally correct but lacks specific details about the timeframe and exact numbers. The evidence supports job creation and store additions during the tenure but does not precisely match the numerical claims.

### id=8963 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Mitch McConnell voted with Harry Reid to infringe on our gun rights."
- arg-rationale: The claim attributes an invented quote or action to Harry Reid and Mitch McConnell regarding gun rights infringement, but the evidence shows no such vote occurred; it is a fabricated assertion.

### id=8979 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says Tom Cotton’s vote in Congress to change Medicare "will increase out-of-pocket expenses for every senior in Arkansas."
- arg-rationale: The claim contains an element of truth about increased out-of-pocket expenses but omits important context that the changes aim to improve efficiency and quality of care. The evidence shows a mix of support and attack, with attacks providing significant caveats.

### id=8990 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The (Russian) ruble is already going down."
- arg-rationale: The claim is directionally correct with the ruble's value declining, but some evidence suggests it may be overstating or lacking important context.

### id=9095 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Marco Rubio believes the earth is 9,000 years old and that humans hunted dinosaurs to extinction; says  Rand Paul believes the earth is 10,000 years old and God removed dinosaurs "to make space for humans."
- arg-rationale: The claim attributes fabricated beliefs about the age of the Earth and human-dinosaur interactions to Marco Rubio and Rand Paul, which are not supported by any evidence and contradicted by their public statements.

### id=9109 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Health insurance and medical costs "are going down because of Obamacare."
- arg-rationale: The claim contains an element of truth but ignores critical facts that change the overall impression; while some aspects of Obamacare may have reduced costs for certain groups, evidence shows significant numbers of people lost their insurance and doctors due to the law.

### id=9151 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "When people enter the service, there’s not a mental health evaluation."
- arg-rationale: The evidence strongly supports the claim that there is no mandatory mental health evaluation for people entering military service.

### id=9235 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The Bundy Ranch deal is all about Nevada Sen. Harry Reid "using federal violence to take people’s land in his state so he can package it to re-sell it to the Chinese."
- arg-rationale: The claim contains fabricated elements and mischaracterizations; there is no evidence supporting the use of federal violence or packaging land for sale to China.

### id=9273 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Jules Bailey "was instrumental in creating the Business Energy Tax Credit that let companies like Wal-Mart profit by $11 million while costing the Oregon general fund $33 million."
- arg-rationale: The claim attributes to Jules Bailey actions and a quote that are not supported by the evidence; the passages instead reference other politicians and do not mention Bailey's involvement in creating the Business Energy Tax Credit or the specific figures cited.

### id=9301 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Florida Democrats just voted to impose Sharia law on women."
- arg-rationale: The claim is fabricated; there is no evidence supporting the imposition of Sharia law on women in Florida. The attacks refute any such notion and provide context that contradicts the central assertion.

### id=9316 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Congress used earmarks "for more than 200 years."
- arg-rationale: The claim is directionally correct as earmarks have been used for over 200 years in Congress. However, the evidence does not provide historical context to confirm the exact timeframe of more than 200 years, making it Mostly-true with a minor qualification.

### id=9431 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Judging by a recent vote, Rep. Debbie Wasserman Schultz "thinks it's okay for medical marijuana patients to go to federal prison."
- arg-rationale: The claim contains an element of truth but misleads overall. While Wasserman Schultz voted against a bill that would have protected medical marijuana users from federal prosecution, the evidence shows this does not equate to supporting sending them to prison.

### id=9432 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: In February, John McCain "suggested" the Bergdahl-Taliban swap that he now calls "outrageous and dangerous."
- arg-rationale: McCain did suggest military action in Syria and questioned Obama's commitment to using force, which is similar to the Bergdahl-Taliban swap context. However, there are minor caveats about the exact nature of his comments.

### id=9437 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Under Wisconsin law, "anyone who knows anything about a John Doe" secret criminal investigation "can't talk about it."
- arg-rationale: The claim is partially accurate as there are legal restrictions on discussing certain secret investigations, but the evidence suggests it's not universally applicable to all 'John Doe' cases and includes caveats about specific contexts like federal law enforcement.

### id=9444 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Already in Wisconsin we have seen fewer people pursuing education as a career" due to the Act 10 collective bargaining law.
- arg-rationale: The claim has an element of truth but omits critical context about federal education policies and the specifics of Act 10, which changes the overall impression.

### id=9502 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The United States is the only developed country in the world without paid maternity leave."
- arg-rationale: The claim is directionally correct that the US lacks paid maternity leave compared to other developed countries, but it omits important context about varying policies and benefits in different nations.

### id=9507 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "NASA scientists fudged the numbers to make 1998 the hottest year to overstate the extent of global warming."
- arg-rationale: The claim is not only false but also fabricates a conspiracy theory about NASA scientists manipulating data, which is unsupported by evidence and contradicted by multiple sources showing consistent scientific findings on global warming.

### id=9524 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: When asked by a reporter whether he’s at the center of a "criminal scheme" to violate campaign laws, Gov. Scott Walker nodded yes.
- arg-rationale: The claim attributes an invented quote to Scott Walker, which is unsupported by any evidence and contradicted by multiple attack passages indicating the quote's fabrication.

### id=9594 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Fox News is "banned in Canada" because it violates a law that "prevents ‘news’ channels from lying to their viewers."
- arg-rationale: The claim is fabricated; Fox News does not have a law in Canada banning it for lying and the cited 'law' does not exist.

### id=9622 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "More women are graduating from college now than men."
- arg-rationale: The evidence overwhelmingly supports the claim that more women are graduating from college than men.

### id=9629 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: nan
- arg-rationale: The claim is directionally correct but lacks full context and evidence. The support passages confirm Obama's containment strategy in Syria and Iraq, while the partial attacks provide minor caveats without contradicting the central assertion.

### id=9674 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "By some estimates, as few as 2 percent of the 50,000 (Central American) children who have crossed the border illegally this year have been sent home."
- arg-rationale: The claim is directionally correct with the evidence showing a significant number of Central American children crossing illegally and only a small percentage being sent home. However, it lacks specific details on the exact 2 percent figure and the total number of returns.

### id=9683 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "I'm not a conspiracy theorist and I never allow conspiracy theorists on my program."
- arg-rationale: {"label": "Pants-fire", "rationate": "The claim misrepresents the speaker's actual words and context, which clearly indicate a belief in conspiracy theories. The structural prior strongly suggests this level of fabrication."}

### id=9708 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The United States is at "historic record highs" of individuals being apprehended on the border from countries with terrorist ties such as "Pakistan or Afghanistan or Syria."
- arg-rationale: {"label": "Pants-fire", "rationate": "The claim is fabricated as it misrepresents apprehensions data and falsely attributes terrorist ties to individuals from specific countries without evidence."}

### id=9731 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "All Aboard Florida is a 100 percent private venture. There is no state money involved."
- arg-rationale: The claim is partially accurate but omits important details about federal funding. The evidence shows that All Aboard Florida received federal grants, contradicting the assertion of no state money involvement.

### id=9746 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "More (student-athletes) graduate than the students who aren't student-athletes."
- arg-rationale: The claim suggests student-athletes graduate at higher rates than non-student-athletes, but the evidence provides mixed support. While some passages suggest high graduation rates for certain groups, others highlight methodological issues and caveats that complicate this assertion.

### id=9771 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Rick Scott took $200,000 in campaign contributions from a company that "profited off pollution."
- arg-rationale: The claim is partially accurate as Scott did receive campaign contributions from oil and gas companies, but it overstates the connection between these donations and pollution profits without clear evidence.

### id=9779 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Says Ted Cruz "was just bribed by the Kochs to introduce a bill that would give them and their allies America’s national forests, parks, and other public lands and open them for mining, drilling, fracking and logging."
- arg-rationale: The claim attributes an invented quote to Ted Cruz and falsely implies the Koch brothers bribed him for a bill that would give them control of public lands. The evidence shows no such bribery occurred, and the Kochs do not own these lands.

### id=9937 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: In 2012, "Wall Street" gave Scott Brown "more campaign contributions than any other candidate -- $5.3 million."
- arg-rationale: The claim is directionally correct but omits that Mitt Romney received more contributions from Wall Street than Scott Brown. The exact figure of $5.3 million for Brown is not confirmed, making the claim slightly misleading.

### id=9942 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Last week's three most-viewed television programs were Sunday Night Football, Thursday Night Football and Monday Night Football."
- arg-rationale: All evidence supports the claim that NFL games were the most-viewed TV programs last week without any contradictions.

### id=9944 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: The U.S. Constitution is "the oldest written constitution still in use today" among nations.
- arg-rationale: The evidence overwhelmingly supports the claim that the U.S. Constitution is the oldest written constitution still in use today among nations.

### id=9957 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Congress includes 36 people accused of spousal abuse, 84 arrested for drunk driving in the past year, 71 with terrible credit and more.
- arg-rationale: The claim contains fabricated statistics and the evidence shows it is based on a misleading article from CNSNews and an outdated report.

### id=9995 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "We have 41,000 people right now on the waitlist for financial-based assistance for our tech colleges and universities," most of them for tech schools.
- arg-rationale: The claim is directionally correct with the number of people on the waitlist being substantial. However, there are minor caveats regarding the exact figure and context which qualify it as Mostly True.

### id=10040 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Muslim nations did not "call out" the people who celebrated the 9/11 attacks.
- arg-rationale: The claim is partially accurate as Muslim nations did not explicitly 'call out' those who celebrated 9/11 attacks, but it omits the context where many Islamic organizations and leaders have condemned terrorism.

### id=10041 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Leticia Van de Putte "opposed putting National Guard troops on the border, would send millions to Central American governments instead and wrote the law giving in-state tuition to illegal immigrants."
- arg-rationale: The claim contains elements of truth but omits important context and details. Van de Putte did oppose National Guard troops on the border at times, supported sending aid to Central American governments, and authored a law for in-state tuition, but her positions were more nuanced than presented.

### id=10061 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "The CBO says if we raise the minimum wage the way Charlie (Crist) wants to do it, it would lose 500,000 jobs."
- arg-rationale: The claim contains an element of truth about potential job losses but omits important context and qualifications from the evidence. The CBO has indeed cited job loss estimates, but these are contested and nuanced by other studies and expert opinions.

### id=10091 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Almost every state has offered an insurance plan on its health exchange that does not cover abortion.
- arg-rationale: All evidence supports the claim that states have offered insurance plans on their health exchanges that do not cover abortion.

### id=10097 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Elorza wants to teach our public school children about the ‘non-existence of God.’"
- arg-rationale: The evidence shows no support for the claim and multiple attacks indicating it is fabricated or misleading.

### id=10111 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Barely-true**
- claim: "While (Charlie Crist) was governor, utility costs went up 30 percent and went from below the national average to above the national average. Since I got elected, utility rates have come down 11 percent and now we are below the average."
- arg-rationale: The evidence strongly contradicts the claim about utility costs and rates under Crist's governorship, showing no clear support for the numerical claims made.

### id=10163 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Before World War II, very few people actually had health insurance."
- arg-rationale: The evidence strongly supports the claim that before World War II very few people had health insurance, with no contradicting evidence provided.

### id=10282 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "Fluoride in the water, that was originally done by the Nazis!"
- arg-rationale: The claim attributes fabricated and conspiracy theory origins to a public health measure, with no credible evidence supporting the Nazi connection.

### id=10388 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: The Obama administration "supported Muslim allies trying to establish a new international blasphemy standard."
- arg-rationale: The claim has an element of truth in that the Obama administration engaged with Muslim allies on international issues, but it overstates and misleads by implying support for a new blasphemy standard without providing context or caveats about the complexity and nuances involved.

### id=10416 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: "We’ve doubled the production of clean energy."
- arg-rationale: The claim is directionally correct with evidence showing increased clean energy production under the administration, but some caveats about specific policies and costs suggest minor qualifications are needed.

### id=10448 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Insured Floridians pay about $2,000 for every hospital stay to cover the cost of the uninsured."
- arg-rationale: The claim is partially accurate as it reflects a study's findings on cost shifting but omits important context and nuances about the methodology and assumptions behind the $2,000 figure.

### id=10451 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: The Affordable Care Act "basically puts a penalty or a tax on employers for every new job they create."
- arg-rationale: The claim has an element of truth but omits important context. The ACA does impose penalties on employers for not offering coverage, but the impact is more nuanced and not as straightforward as 'putting a penalty or tax on employers for every new job they create.'

### id=10517 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Ninety-six percent of failing schools are spending above $8,400, the average annual per student expenditure, and 26 percent spend considerably more than that.
- arg-rationale: The claim is partially accurate as it highlights higher spending in failing schools but omits important context about the complexity of factors affecting school performance and funding distribution.

### id=10858 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "During Obama's first five years as president, black unemployment increased 42 percent. During Reagan's presidency, black unemployment dropped 20 percent."
- arg-rationale: The claim contains fabricated statistics and misrepresents the actual trends in black unemployment rates during Obama's and Reagan's presidencies.

### id=10871 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Austin school district "teachers are the lowest paid of any urban" Texas district and the "lowest paid of any surrounding school district."
- arg-rationale: The claim is partially accurate as Austin teachers are among the lowest paid in Texas and Central Texas districts, but it omits important context about comparisons to smaller surrounding districts where rates may be lower. The evidence shows a mix of support and caveats that qualify the central assertion.

### id=10906 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: The runnerup to Caitlyn Jenner for ESPN’s Arthur Ashe Courage Award was "Army veteran Noah Galloway, who lost an arm and leg to a roadside bomb in Iraq."
- arg-rationale: The evidence passages do not support the claim and indicate it is fabricated as they are unrelated to the Arthur Ashe Courage Award or Noah Galloway.

### id=11050 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Bernie Sanders voted against the Brady Bill -- background checks and waiting periods."
- arg-rationale: Sanders initially voted against the Brady Bill but eventually supported it. The central assertion is accurate but omits this later support, making it directionally correct with a minor caveat.

### id=11080 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Texas’ high school graduation rate went from 27th in the country in 2002, to second highest in the country in 2013."
- arg-rationale: The claim has an element of truth regarding the improvement in graduation rates but omits important context and exaggerates the ranking change. The evidence shows mixed support with significant caveats, suggesting misleading overall framing.

### id=11139 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says in 2002, he "won more Hispanic votes than Anglo votes, 60 percent in the state."
- arg-rationale: The claim is directionally correct but lacks specific context about the 2002 election results. The evidence supports that Hispanics can be a competitive voting bloc, but does not provide precise data for Cruz's specific assertion in 2002.

### id=11212 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The U.S. has now spent more on reconstructing Afghanistan than was spent on the Marshall Plan and the reconstruction of Europe."
- arg-rationale: The evidence supports the claim that U.S. spending in Afghanistan is substantial but does not provide a direct comparison to the Marshall Plan and European reconstruction costs, making it difficult to verify the exact numerical assertion.

### id=11230 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Scott Walker's plan to replace Obamacare "is a new entitlement" program for "every single American human being from the time they are born right up until they grow old and become eligible for Medicare."
- arg-rationale: The claim contains an element of truth about the long-term nature of health care programs but exaggerates and misleads by omitting important details and context.

### id=11242 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "More Americans have died from guns in the United States since 1968 than on battlefields of all the wars in American history."
- arg-rationale: The evidence overwhelmingly supports the claim that more Americans have died from guns since 1968 than in all American wars combined.

### id=11261 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Half-true**
- claim: Says he "turned down a Medicaid expansion under Obamacare," but because of actions he took, for the first time in Wisconsin's history "everyone living in poverty is covered under Medicaid."
- arg-rationale: The claim is directionally correct but omits important context; the governor's actions did not lead to universal coverage for all living in poverty under Medicaid as he suggested.

### id=11284 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Florida led the nation in job creation" while Bush was governor.
- arg-rationale: The claim is partially accurate as Florida did experience job growth under Bush's governorship, but the evidence suggests it was not definitively leading the nation. The supporting evidence is weak and mixed with significant caveats.

### id=11303 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Missouri is "#1 in the nation for holding down tuition increases at public universities."
- arg-rationale: The evidence strongly supports the claim that Missouri has held down tuition increases, but includes minor caveats about how the increase is not automatic and depends on state funding.

### id=11337 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: Says "the cascading effects" of climate change contributed to the rise of ISIS.
- arg-rationale: The claim is directionally correct that climate change contributed to the rise of ISIS, but it lacks specific context and nuance provided by supporting evidence.

### id=11539 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Obamacare insurance cooperative failures "should be expected" because they're like any business, and "when you start businesses in America, at the fifth year, half of the businesses have closed."
- arg-rationale: The claim that business failures are common is supported by evidence, but the specific framing and statistics used may be misleading or exaggerated. The evidence suggests a mixed picture of business formation rates and survival, not a clear-cut pattern as suggested.

### id=11545 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Over half of the black workers in this country earn less" than $15 an hour.
- arg-rationale: The claim is directionally correct as a significant portion of black workers earn less than $15 an hour, but the exact percentage is not specified and may be higher or lower. The evidence supports the general trend without providing precise figures.

### id=11546 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "We already pay the highest electricity prices in the country here in New England."
- arg-rationale: The claim is partially accurate as New England does have high electricity prices, but the evidence suggests it's not uniformly the highest in the country and includes caveats about regional cost of living differences.

### id=11625 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "Road congestion costs rush hour drivers in Austin and Dallas more than $1,000 a year. And in Houston, it’s even more -- almost $1,500 a year."
- arg-rationale: The claim is directionally correct but the specific figures are misleading as they refer to Texas-wide data rather than just Houston. The structural prior strongly supports 'True', but the partial support evidence clarifies a minor caveat.

### id=11670 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Under conservative leadership, Congress has reduced the federal deficit by 60 percent – nearly $800 billion."
- arg-rationale: The claim contains an element of truth about deficit reduction but omits critical context that Clinton worked with a Republican-controlled Congress and economic factors played a significant role.

### id=11726 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Everywhere that we have more citizens carrying guns, crime is less. There's a study showing that where states have open carry or concealed carry, but particularly open carry, the crime is down 25 percent."
- arg-rationale: The claim has an element of truth in that some states with more permissive gun laws have not seen a significant increase in crime, but the evidence shows mixed results and serious caveats. The central assertion is misleading as it overgeneralizes from limited data.

### id=11736 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "As governor of Florida, I used a combination of strategies to help reduce heroin use among youth in Florida by approximately 50 percent."
- arg-rationale: The claim suggests significant reduction in youth heroin use but the evidence is weak and mixed. Some support exists for drug testing efficacy, but attacks suggest overstatement of impact on specific drugs like heroin among youth.

### id=11761 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Says Marco Rubio "knows full well I voted for his amendment to increase military spending to $697 billion."
- arg-rationale: The evidence overwhelmingly supports the claim that Rubio's amendment increased military spending, with no contradictory evidence provided.

### id=11825 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: A Texas law requires every high school to have a voter registrar "and part of their responsibility is to make sure that when children become 18 and become eligible to vote, that they vote."
- arg-rationale: The claim is partially accurate as Texas law requires voter registrars in high schools, but the evidence suggests that their responsibility to ensure voting by eligible students is overstated and not clearly mandated.

### id=11832 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: "You've been tremendously deceived" by people who say the Earth is not flat.
- arg-rationale: The claim is not just false but also absurd and fabricated, as it promotes a scientifically debunked theory without any credible evidence.

### id=11917 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: North Korea’s missiles are "not going to have a capability to reach the United States anytime real soon."
- arg-rationale: All evidence supports the claim that North Korea's missiles do not currently have the capability to reach the United States.

### id=11972 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Building a wall" on the U.S.-Mexico border "will take literally years."
- arg-rationale: The evidence overwhelmingly supports the claim that building a wall along the U.S.-Mexico border would take years due to its scale and complexity.

### id=12006 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: "There is a precedent" for not nominating someone to the U.S. Supreme Court "in the middle of a presidential election."
- arg-rationale: The evidence strongly contradicts the claim by showing no precedent for not nominating a Supreme Court justice in an election year.

### id=12012 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "A single mother of two can’t qualify for basic healthcare through Medicaid if she makes more than $3,504 dollars a year."
- arg-rationale: The claim is directionally correct but omits the context that Medicaid eligibility can be expanded under Obamacare to cover more individuals. The structural prior and evidence suggest minor caveats rather than substantial contradictions.

### id=12037 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Barack Obama "has the legal authority to let in really however many refugees he wants, from whatever country."
- arg-rationale: The claim is partially accurate as Obama does have broad executive power over refugee admissions but it omits important legal and procedural context that limits his authority to act unilaterally.

### id=12098 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Donald "Trump got, you know, $1.8 billion worth of free media. I got, like, none."
- arg-rationale: The claim is directionally correct as Trump received significantly more free media coverage than the speaker. However, the exact figure of $1.8 billion is not substantiated in the evidence provided.

### id=12160 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Emory University students were provided counseling after someone wrote "Trump 2016" in chalk on campus.
- arg-rationale: The claim has an element of truth as counseling was offered, but the framing exaggerates and misrepresents the context by implying it was specifically due to 'Trump 2016' writing rather than broader election-related stress.

### id=12167 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **Half-true**
- claim: Says his free public university tuition program "is paid for … by a tax on Wall Street's speculation."
- arg-rationale: The claim has an element of truth in that it suggests a tax on Wall Street speculation could fund the program, but the evidence shows significant caveats and lacks direct support for the specific funding mechanism mentioned. The central assertion is misleading due to lack of concrete evidence linking the tax directly to tuition costs.

### id=12168 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Expanding the sale of full-strength beer and wine to grocery stores is "good for everybody."
- arg-rationale: The claim has some support but lacks critical context; the evidence suggests mixed views on economic impact and consumer benefits, with significant caveats.

### id=12169 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "There have not been any public safety issues" in cities that allow transgender people to use the bathroom of the gender they identify as.
- arg-rationale: The claim is directionally correct but slightly misleading due to its brevity. While there are no public safety issues specifically tied to transgender bathroom use, the evidence includes caveats and qualifications that suggest a need for minor clarification.

### id=12187 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Rick Scott "stripped women of access to public health care."
- arg-rationale: The claim is partially accurate as Scott opposed federal health care laws, but it overstates the impact on women's access to public health care without context.

### id=12236 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: About "1 percent of all the gun sellers are responsible for more than half of the guns that are used in crimes."
- arg-rationale: The claim is partially accurate as it reflects the high proportion of guns used in crimes that are not legally purchased, but it oversimplifies by attributing this to a small number of sellers rather than considering broader illegal transactions and private sales.

### id=12244 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: In nine Democratic debates, "We've not had one question about a woman's right to make her own decisions about reproductive health care, not one question."
- arg-rationale: The evidence confirms that there were no questions about women's reproductive rights in the Democratic debates and supports the claimant's point.

### id=12331 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "Seven hundred thousand. That’s how many California jobs will be lost thanks to the politicians raising the minimum wage….Now Florida is adding one million jobs, not losing them."
- arg-rationale: The claim contains an element of truth about potential job losses from minimum wage increases but omits important context and evidence suggesting the impact is less severe than claimed.

### id=12381 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Half-true**
- claim: "The United States has a low voter turnout rate."
- arg-rationale: The evidence overwhelmingly supports the claim that the United States has a low voter turnout rate compared to other OECD member-nations.

### id=12427 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Old City in Philadelphia "used to have more than a dozen clubs and that's what we were known for and now we’re down to two."
- arg-rationale: The claim is directionally correct but lacks specific context or data to fully substantiate the exact number of clubs that used to exist in Old City Philadelphia. The evidence supports a significant reduction in clubs, though precise numbers are not provided.

### id=12520 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **Barely-true**
- claim: "Nine million people have lower-cost HIV/AIDS medicine because of the work of the Clinton Foundation and my husband."
- arg-rationale: The evidence overwhelmingly supports the claim that millions have benefited from lower-cost HIV/AIDS medicine due to the Clinton Foundation's work.

### id=12542 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says Donald Trump has said he loves war, "including with nukes."
- arg-rationale: The claim partially aligns with Trump's statements but omits important context. While he has expressed support for nuclear deterrence, the evidence does not strongly support that he 'loves war' or specifically endorses using nukes in conflict.

### id=12661 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **Barely-true**
- claim: The war on drugs led to "a 500 percent increase in incarceration in our country, disproportionately affecting poor and disproportionately affecting minorities."
- arg-rationale: The evidence strongly supports the claim that incarceration rates increased and disproportionately affected minorities due to the war on drugs, but lacks specific data on a 500 percent increase.

### id=12662 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "There are approximately 18,000 (police) departments in the United States."
- arg-rationale: The evidence strongly supports the claim that there are approximately 18,000 police departments in the United States, with minor caveats about data collection methods and reporting accuracy not contradicting the central assertion.

### id=12734 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "It was Hillary Clinton who left Americans in harm's way in Benghazi and after four Americans fell said, 'What difference at this point does it make?' "
- arg-rationale: The claim contains an element of truth about Clinton's response but omits important context and misrepresents the broader narrative around her role in Benghazi.

### id=12745 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Two million more Latinos are in poverty today than when President Obama took his oath of office less than eight years ago."
- arg-rationale: The claim is partially accurate as the number of Latinos in poverty did increase under Obama's presidency, but it omits important context about pre-existing trends and economic conditions that contributed to this rise.

### id=12749 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "Homicides last year increased by 17 percent in America’s 50 largest cities. That’s the largest increase in 25 years."
- arg-rationale: The claim about the 17 percent increase in homicides is supported by evidence but lacks context on long-term trends and variability over short periods. The attacks highlight that overall violent crime has not consistently increased, which contradicts the framing of the homicide increase as a significant trend.

### id=12768 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "We are the only industrialized nation that doesn't guarantee workers paid family leave."
- arg-rationale: The claim is directionally correct as the U.S. is indeed unique in not guaranteeing paid family leave among industrialized nations, but it omits important context about varying policies and benefits across countries.

### id=12798 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says "Donald Trump and Mike Pence want to gamble with your retirement benefits in the stock market."
- arg-rationale: The claim contains an element of truth about potential privatization but exaggerates the risk and current intent of Trump and Pence's proposals.

### id=12849 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: Donald Trump is "against marriage equality. He wants to go back."
- arg-rationale: The evidence overwhelmingly supports that Trump is against marriage equality and wants to leave it up to the states or federal constitutional amendment.

### id=12873 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: In the 2012 election, there were more votes cast than registered voters in St. Lucie County, and Palm Beach County had 141 percent turnout.
- arg-rationale: The evidence strongly contradicts the claim, showing it to be fabricated with impossible turnout percentages and no supporting data.

### id=12952 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: The Obama administration gave Iran "$400 million in ransom payment cash."
- arg-rationale: The claim contains an element of truth about a cash payment but omits critical context that the payment was not ransom and was part of a larger sanctions relief framework. The evidence suggests misleading framing.

### id=12976 — gold *False*
- arg-aware predicted **False** ✓
- flat-RAG predicted **Half-true**
- claim: "All of Texas is conservative, except a little bit of Austin."
- arg-rationale: The evidence shows that the claim is incorrect as Austin and other parts of Texas have significant demographic diversity and liberal policies, contradicting the notion that all of Texas is conservative.

### id=12994 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "The Clinton Foundation is a charity where President and Secretary Clinton and their daughter, they take no salary, they get no money from it, they take no personal benefit from it."
- arg-rationale: The claim is mostly accurate as the Clintons do not take a salary from the foundation. However, there are caveats about mixing department and foundation business and potential conflicts of interest with foreign donations.

### id=13047 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Barack Obama has "doubled our national debt. Doubled it. It's going to be close to $20 trillion when he leaves."
- arg-rationale: The claim is partially accurate as the national debt did increase significantly under Obama, but it was not exactly doubled and other factors contributed to this trend.

### id=13089 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **Barely-true**
- claim: "Tim Kaine hiked tuition as governor, but now claims to champion affordability."
- arg-rationale: The claim is partially accurate as Kaine did support tuition reciprocity agreements that could be seen as affordable for some students. However, it omits important context about overall tuition hikes during his governorship.

### id=13128 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Hillary Clinton called the Trans-Pacific Partnership "the gold standard. You called it the gold standard of trade deals. You said it’s the finest deal you’ve ever seen."
- arg-rationale: The claim is directionally correct as Clinton did call the TPP 'the gold standard' during negotiations. However, it omits her later opposition to the deal once its terms were known.

### id=13172 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "A rural hospital in Missouri closes every 8 months. The legislature’s failure to expand Medicaid has brought crisis to many of Missouri’s rural health care providers."
- arg-rationale: The claim about hospital closures is supported but the direct link to Medicaid expansion is overstated; evidence suggests other factors and caveats.

### id=13184 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Tim Kaine "actually tried to raise taxes by about $4 billion."
- arg-rationale: The claim is directionally correct as Kaine did propose a tax increase, but the exact amount and impact are nuanced. The evidence shows it was closer to $1.25 billion annually rather than $4 billion.

### id=13190 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Says Hillary Clinton and Tim Kaine "want to expand (Obamacare) into a single-payer program."
- arg-rationale: The claim contains an element of truth that Clinton and Kaine support expanding Obamacare but omits critical context that they do not advocate for a single-payer system.

### id=13208 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: "In the state legislature, I supported Second Amendment rights."
- arg-rationale: The claim is supported by evidence showing the candidate's belief in Second Amendment rights and actions related to gun legislation. However, some passages suggest a lack of strong evidence for the specific assertion, qualifying it as mostly true.

### id=13270 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "We know that more than half of Hillary Clinton's meetings while she was secretary of state were given to major contributors to the Clinton Foundation."
- arg-rationale: The claim has an element of truth regarding the Clinton Foundation's activities but omits important context about Hillary Clinton's role and the lack of direct evidence linking her meetings to major contributors. The attacks highlight significant caveats, making the overall framing misleading.

### id=13272 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: Hillary Clinton said gun confiscation "would be worth considering."
- arg-rationale: The claim contains an element of truth but misleads overall; Clinton did suggest considering a gun buyback program, but the context and her actual stance are more nuanced than the claim suggests.

### id=13305 — gold *True*
- arg-aware predicted **True** ✓
- flat-RAG predicted **False**
- claim: "Heroin .. pours across our southern borders."
- arg-rationale: The evidence supports the claim that drugs are seized at the southern border, though it does not provide specific data on heroin. The structural prior and strong support role-fit indicate no contradictions.

### id=13334 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: Says he’s "taken an 8% pay decrease in each of the nine years he has been in office."
- arg-rationale: The claim has some truth to it as the lawmaker did vote against pay raises in two out of four years, but the evidence shows that their salary still increased in other years and there is no consistent 8% decrease over nine years. The structural prior suggests a balanced view given the weak supporting and attacking evidence.

### id=13367 — gold *Mostly-true*
- arg-aware predicted **Mostly-true** ✓
- flat-RAG predicted **False**
- claim: Says Marco Rubio "said Social Security and Medicare have ‘weakened us as a people.’ "
- arg-rationale: Rubio did say Social Security and Medicare need significant alterations to continue in their current state, but the claim exaggerates his position by implying he views these programs as weakening the nation without context.

### id=13405 — gold *Half-true*
- arg-aware predicted **Half-true** ✓
- flat-RAG predicted **False**
- claim: "One in five American households have nobody under the same roof that's got a job."
- arg-rationale: The claim is partially accurate but omits important context about the reasons behind workforce participation rates and the nuances of household economic support through federal benefits.

### id=13409 — gold *Barely-true*
- arg-aware predicted **Barely-true** ✓
- flat-RAG predicted **False**
- claim: "In many instances, (people's) health care costs are more than their mortgage costs or their rent, which, by the way, is a first in American history."
- arg-rationale: The claim has an element of truth about rising healthcare costs but overstates the uniqueness and extent of this issue in American history. The evidence suggests that while health care costs are indeed high, they are part of a broader national trend rather than a unique situation in Massachusetts.

### id=13512 — gold *Pants-fire*
- arg-aware predicted **Pants-fire** ✓
- flat-RAG predicted **False**
- claim: Latina who enthusiastically supported Donald Trump on stage in Las Vegas in October 2015 has been deported.
- arg-rationale: The claim attributes a specific event to a Latina supporter of Trump in 2015 and states she was deported, but there is no evidence supporting this occurrence. The provided evidence only includes attacks that refute similar claims about deportation policies and practices.

## Cases where flat-RAG wins

### id=12 — gold *False*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **False** ✓
- claim: "I'll tell you what I can tell this country: If they want a president who doesn't believe in God, there's probably plenty of choices."
- flat-rationale: The claim misrepresents the central issue by implying disbelief in God is a choice for presidency when the context shows it was about identifying Christians in the Middle East.

### id=110 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The Iraq Study Group reported that (Saddam Hussein) had designs on reviving his nuclear program."
- flat-rationale: The evidence shows that the Iraq Study Group did not report on Saddam Hussein's nuclear program designs; instead, it was President Bush who made claims about this in his State of the Union address and radio addresses.

### id=171 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: ''The leading Democratic candidate once said that the unfettered free market is the most destructive force in modern America.''
- flat-rationale: {"label": "False", "rationate": "The evidence does not support the claim; there are no passages that confirm the leading Democratic candidate ever made such a statement. The provided evidence is topical and does not substantiate the central assertion."}

### id=184 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: "Right now, an employer has more of a chance of getting hit by lightning than be prosecuted for hiring an undocumented worker. That has to change."
- flat-rationale: The evidence is entirely topical and does not address the claim's assertion about the rarity or likelihood of employers being prosecuted for hiring undocumented workers. The structural prior suggests a need to calibrate toward False given the lack of relevant support or attack evidence.

### id=544 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: John McCain has changed position on invading Iraq.
- flat-rationale: The claim suggests McCain changed his position on invading Iraq for political reasons, but the evidence shows it was more nuanced and based on changing conditions. This means there's an element of truth but the overall framing is misleading.

### id=553 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: McCain "hasn't held executive responsibility."
- flat-rationale: The evidence does not provide any support for the claim and instead suggests that McCain has had executive responsibility. The passages are topical but do not address the central assertion of the claim.

### id=688 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "He was offered medical care for his injuries if he would give up military information in return. John McCain said, 'No.' "
- flat-rationale: The evidence does not support the claim; there are no passages that confirm or deny McCain's alleged statement about medical care and military information. The provided evidence is topical but unrelated to the specific incident described in the claim.

### id=729 — gold *Half-true*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **Half-true** ✓
- claim: On whether the government should bail out insurance giant AIG.
- flat-rationale: The claim is partially accurate as AIG was bailed out by the government, but it lacks context about why this action was necessary to prevent broader economic damage.

### id=917 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "For every dollar (in the stimulus package) that is spent to help small businesses, $4 is being spent to help upkeep the grass on the lawns of Washington."
- flat-rationale: The claim is unsupported by the evidence and makes a misleading comparison that does not reflect the actual stimulus package content or spending priorities.

### id=985 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Gov. Sarah Palin "got precisely zero support for her call for Alaska's Democratic Senator Mark Begich to resign because Ted Stevens' corruption conviction was overturned."
- flat-rationale: The claim is false as there is no evidence showing that Sarah Palin got zero support for her call; the provided passages are topical and do not address the specific assertion about support for her call.

### id=1010 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: Pay-as-you-go "is the principle that helped transform large deficits into surpluses in the 1990s."
- flat-rationale: The claim overstates the importance of pay-as-you-go in transforming deficits to surpluses in the 1990s, as evidence suggests other factors were significant.

### id=1262 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Forty-five percent of doctors "say they'll quit" if health care reform passes.
- flat-rationale: The claim is unsupported by the evidence and appears to be an exaggeration or misrepresentation. The provided poll data does not support the specific assertion that 45% of doctors will quit if health care reform passes, and there are no direct attacks on the claim's veracity but rather a lack of supporting evidence.

### id=1497 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: “In this judicial race, special  interest groups have demanded  money from me, in exchange for  endorsement and support.”
- flat-rationale: The evidence is entirely topical and does not confirm the claim that special interest groups have demanded money for endorsement; it only discusses the source of campaign funding without supporting the specific assertion.

### id=1641 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The New England Journal of Medicine released a survey the week that President Obama signed Obamacare stating that over 30 percent of American physicians would leave the profession if the government took over health care."
- flat-rationale: The evidence does not support the claim; there is no mention of a survey from the New England Journal of Medicine about physicians leaving the profession due to government takeover of health care.

### id=1873 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Presidents Hoover, Truman and Eisenhower collectively ordered the deportation of at least 15 million illegal aliens.
- flat-rationale: The evidence does not support the claim that Hoover, Truman, and Eisenhower collectively ordered the deportation of at least 15 million illegal aliens; the provided passages are topical and do not confirm this specific historical assertion.

### id=1915 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: U.S. Rep.   Lloyd Doggett is “the most liberal man in the United States Congress.”
- flat-rationale: The evidence shows that other representatives like Cicilline and Baldwin have been described as among the most liberal in Congress, contradicting Doggett's claim to be 'the most liberal'.

### id=2099 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The Department of Health and Human Services is providing $160 million to the state of Pennsylvania to set up a new high-risk insurance pool program that would cover any abortion legal in the state."
- flat-rationale: The evidence shows that federal funding for abortion services through the proposed insurance pool is prohibited and must be paid entirely from patient premiums, contradicting the claim that it would cover any abortion legal in the state with federal funds.

### id=2135 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I remember one of [Curt Schilling's] teammates said he painted his sock, the bloody sock."
- flat-rationale: The evidence is entirely topical and does not support the claim about Curt Schilling's teammate painting a bloody sock. No relevant supporting or attacking evidence is provided.

### id=2181 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: "The Congressional Budget Office estimates that for every $1 we spend on unemployment benefits, $1.90 is put into our economy."
- flat-rationale: The claim is partially accurate as the CBO does estimate a range from $0.70 to $1.90 for every dollar spent on unemployment benefits, but it omits important context by not specifying that the figure can vary widely depending on economic conditions.

### id=2337 — gold *Half-true*
- arg-aware predicted **True**
- flat-RAG predicted **Half-true** ✓
- claim: Jennifer Carroll's an "outsider."
- flat-rationale: The claim that Jennifer Carroll is an 'outsider' has some basis as she emphasizes this image in speeches. However, the evidence does not provide substantial context to fully support or refute her outsider status, making it partially accurate but lacking critical details.

### id=2477 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: "Over the past year ... our 16 counties have hemorrhaged more than 6,000 jobs with no apparent end in sight."
- flat-rationale: The claim about job loss is not supported by the evidence and contradicts statements indicating job creation. The provided passages are topical but do not support the specific assertion of significant job hemorrhaging.

### id=2514 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The federal government can tell General Motors what to charge for its automobiles.
- flat-rationale: The evidence shows the federal government has taken control over companies like GM during financial crises but does not have a general authority to dictate pricing for automobiles.

### id=2557 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "Steve Southerland did not pay his taxes in '05, '06, '07, '08 or '09."
- flat-rationale: The evidence is entirely topical and does not address the claim about Steve Southerland's tax payments. Without relevant support or attack passages confirming or refuting the specific years mentioned in the claim, the structural prior suggests a lack of factual basis for the assertion.

### id=2603 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Texas has so few gas-pump inspectors in the field, "the HEBs of this state, the Brookshires of this state, they're calibrating their own gas pumps. The (Texas Department of Agriculture) just sends them the stickers and they calibrate them."
- flat-rationale: The claim about gas pump inspectors and retailers calibrating their own pumps is not supported by the evidence provided; all passages are topical and do not address the specific issue of gas pump inspection or calibration.

### id=2626 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Christopher Little has "a history of working against environmental protection by defending the worst types of corporate polluters"
- flat-rationale: The evidence is entirely topical and does not support or attack the claim about Christopher Little's history of working against environmental protection. The structural prior suggests a balance between Half-true and Barely-true, but without relevant supporting or attacking evidence, the claim must be rated False due to lack of factual backing.

### id=2911 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: "We are giving almost $2 billion of taxpayer money to the junk food and fast food industries every year to make the (childhood obesity) epidemic worse."
- flat-rationale: The evidence does not support the claim that taxpayer money is given to junk food and fast food industries; the provided passages are topical but do not address the central assertion.

### id=2958 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Beaverton "enjoys the most diverse population (by percentage of population) among Oregon cities."
- flat-rationale: The evidence does not support the claim that Beaverton has the most diverse population among Oregon cities; it is purely topical and provides no relevant comparative data.

### id=3036 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: Wisconsin’s lawsuit rules are so anti-business that the state’s system is "one of the most promiscuous" in America.
- flat-rationale: The evidence does not support the claim that Wisconsin's lawsuit rules are 'anti-business' or 'one of the most promiscuous' in America; all provided passages are topical and do not address the central assertion.

### id=3044 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "We had an amendment in the health care law that said the federal government is going to take over education."
- flat-rationale: The evidence shows no support for the claim that there was an amendment in the health care law regarding federal government taking over education; the passages are topical and do not confirm the central assertion.

### id=3330 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: Says Tri-Rail shows the potential problems with investing in high-speed rail.
- flat-rationale: The claim suggests Tri-Rail shows problems with high-speed rail investment, but the evidence is topical and does not support this central assertion; it lacks direct confirmation or contradiction.

### id=3362 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says broken compact fluorescent light bulbs "allegedly cause migraines and epilepsy attacks."
- flat-rationale: The claim that broken compact fluorescent light bulbs allegedly cause migraines and epilepsy attacks is not supported by the evidence; the passages are topical but do not confirm any health risks beyond environmental concerns.

### id=3664 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "A $250 fine if you're caught with a plastic bag coming out of a store. Plastic bag police anyone?"
- flat-rationale: The claim misrepresents the actual fines and fees associated with plastic bag use; there is no $250 fine mentioned in the evidence.

### id=3789 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: "The new light bulbs will cost roughly six times the cost of the light bulbs we now use."
- flat-rationale: {"label": "Barely-true", "rationationale": "The claim that new light bulbs will cost six times the current ones is not substantiated by evidence and may overstate costs. The provided evidence suggests debate on bulb costs but does not confirm such a high price ratio."}

### id=3811 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: One of every two Wisconsin residents are "on some kind of government handout."
- flat-rationale: The evidence does not support the claim; it is entirely topical and provides no relevant information about Wisconsin residents being on government handouts.

### id=3941 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: "The Democrat-led Senate has failed to pass a budget for 750 days ... Senate Democrats have neglected one of their most basic responsibilities."
- flat-rationale: The claim is partially accurate as the Senate has not passed a budget for an extended period, but it omits important context about the political dynamics and procedural challenges involved in passing such legislation.

### id=4116 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "POTUS’ economists: ‘Stimulus’ Has Cost $278,000 per job."
- flat-rationale: The claim is unsupported by evidence and contradicted by expert analyses suggesting the stimulus created jobs. The cited figure of $278,000 per job lacks credible backing.

### id=4208 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "This is the first time in the history that we've had the raising of a debt limit also with spending cuts."
- flat-rationale: The evidence shows previous instances where the debt limit was raised with conditions for spending cuts or fiscal responsibility, contradicting the claim that this is unprecedented.

### id=4277 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The Republican National Convention "is a Super Bowl times four."
- flat-rationale: The evidence is entirely topical and does not support the claim that the Republican National Convention is 'a Super Bowl times four.' The comparison lacks factual basis.

### id=4337 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: "Before Medicare, only 51 percent of Americans 65 and older had health care coverage and nearly 30 percent lived below the poverty line. Today, thanks to Medicare ... nearly all seniors have coverage and 75 percent fewer struggle in poverty."
- flat-rationale: The claim is partially accurate but omits important context about the nature and coverage details of Medicare. The evidence shows that while Medicare has improved health care access for seniors, it does not fully capture the complexities and criticisms surrounding the program.

### id=4593 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "Bryce Reeves chaired a group bankrolled by a New York billionaire who fired hundreds of Virginia workers and sent their jobs to China."
- flat-rationale: The evidence does not support the claim's central assertion about Bryce Reeves or a New York billionaire firing workers and sending jobs to China; the provided passages are topical but do not address the specific individuals or events mentioned in the claim.

### id=4609 — gold *False*
- arg-aware predicted **Barely-true**
- flat-RAG predicted **False** ✓
- claim: Says the National Labor Relations Board told Boeing that it "can't build a factory in a non-union state."
- flat-rationale: The evidence is entirely topical and does not support the claim that the NLRB told Boeing it 'can't build a factory in a non-union state.'

### id=4689 — gold *False*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **False** ✓
- claim: The departments of Commerce, Education and Energy and the EPA saw their spending increase by between 130 percent and 219 percent between 2008 and 2010.
- flat-rationale: The evidence is entirely topical and does not support the claim's specific spending increase figures for the departments mentioned. Without supporting data, the claim must be rated false based on lack of evidence.

### id=4698 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says state Senate President Stephen "Sweeney gave us the nation's highest income tax rates, driving out jobs."
- flat-rationale: The evidence does not support the claim that Sweeney gave New Jersey the nation's highest income tax rates; it discusses corporate tax rates instead.

### id=4714 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I made a bunch of these promises during the campaign. ... We've got about 60 percent done in three years."
- flat-rationale: The claim is unsupported by evidence and contradicted by topical context suggesting many promises were unfulfilled or broken.

### id=4750 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The EPA "wants to hire 230,000 new government regulators that will cost the taxpayer $21 billion."
- flat-rationale: The claim is unsupported by the evidence and makes an unsubstantiated assertion about EPA hiring plans and costs. The provided passages are topical but do not confirm or refute the specific numbers mentioned in the claim.

### id=4899 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I never favored cap and trade."
- flat-rationale: The evidence shows that the speaker previously supported cap and trade, contradicting the claim.

### id=5017 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: "The Social Security trust fund … is already facing imminent bankruptcy."
- flat-rationale: The claim contains an element of truth about the trust fund's future challenges but misleads by overstating the immediacy and severity of the 'bankruptcy' threat.

### id=5087 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Eliminating "Obamacare" ... "saves $95 billion a year."
- flat-rationale: The claim misrepresents the actual impact and funding mechanisms of Obamacare; there is no direct annual savings figure of $95 billion from eliminating it.

### id=5171 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says an Obama administration policy prohibits people who work with at-risk youth from promoting marriage as a way to avoid poverty.
- flat-rationale: {"label": "False", "rationationale": "The evidence does not support the claim; there are no passages that confirm an Obama administration policy prohibiting work with at-risk youth from promoting marriage to avoid poverty. The provided evidence is topical and unrelated to the specific claim."}

### id=5371 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Mitt Romney supports cap and trade.
- flat-rationale: The evidence shows no support for the claim that Mitt Romney supports cap and trade; it only discusses his opposition to it.

### id=5472 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: Mitt Romney "left Massachusetts $1 billion in debt."
- flat-rationale: The evidence does not support the claim that Romney left Massachusetts $1 billion in debt; it instead suggests he improved the fiscal situation and there is no direct evidence of a $1 billion debt.

### id=5671 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I think it’s seven or eight of the California system of universities don’t even teach an American history course. It’s not even available to be taught."
- flat-rationale: The claim is false as there is no evidence supporting the assertion that seven or eight California universities do not teach American history. The provided evidence is entirely topical and unrelated to the central claim.

### id=5824 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "We didn’t go out asking people" to join the "stand your ground" task force.
- flat-rationale: The evidence is entirely topical and does not address the claim about forming a 'stand your ground' task force or consulting people on it. The structural prior suggests uncertainty but leans towards the negative side, and without supporting evidence for the claim's truth, it must be rated False based on lack of confirmation.

### id=5840 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says the stimulus bill sent tax credits overseas, such as "half a billion to an electric car company that created hundreds of jobs in Finland."
- flat-rationale: The claim is based on debunked assertions about tax credits going overseas; prior fact-checks found the Finland and Mexico claims to be false or mostly false.

### id=5938 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "Victory! Republicans by 2 to 1 vote to endorse Mark Neumann on first ballot at GOP convention."
- flat-rationale: The evidence is entirely topical and does not support the claim that Republicans voted 2 to 1 in favor of Mark Neumann. The structural prior suggests uncertainty but leans towards a negative verdict given the lack of supporting evidence.

### id=5985 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: In 2011, Alabama and Massachusetts passed legislation allowing non-citizens who are legal residents to vote in state and local elections.
- flat-rationale: The evidence shows no legislation allowing non-citizens to vote in state and local elections was passed in Alabama or Massachusetts in 2011; the provided information is topical but does not support the claim.

### id=6035 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: Massachusetts under Gov. Mitt Romney initially ranked last among states in job growth, but by the end of his governorship, "we were in the middle of the pack."
- flat-rationale: The claim has an element of truth but omits important context about job growth trends during Romney's term. The evidence shows mixed views on the initial and final rankings without clear support or attack.

### id=6041 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: "District 22 includes about 80% of the district I have represented since 2010. District 20 includes about 20% of the area I have represented since 2010."
- flat-rationale: The claim is partially accurate but omits important context about the redistricting changes and does not provide specific evidence to support the exact percentages given.

### id=6123 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Since President Barack Obama took office, "you have 1,700 employees just at the Department of Transportation" earning over $170,000.
- flat-rationale: The claim about 1,700 employees at the Department of Transportation earning over $170,000 is not supported by any evidence and appears to be an unfounded assertion.

### id=6469 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says President Obama said of the national debt, "If I don't have this done in three years, then there's going to be a one-term proposition."
- flat-rationale: {"label": "False", "rationationale": "The evidence shows no record of Obama making the quoted statement about a one-term proposition if he does not address the national debt in three years. The provided passages are topical and do not support or confirm the claim."}

### id=6513 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The Obama administration "leaked information, deliberately or otherwise, that led to the identification of the Pakistani doctor that helped us in achieving our goals and killing bin Laden."
- flat-rationale: The evidence is entirely topical and does not support or attack the claim about the Obama administration leaking information. The structural prior suggests a balance between Half-true and Barely-true, but without any relevant supporting or attacking evidence, the claim must be rated False due to lack of confirmation.

### id=6637 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: When it comes to jobless workers, "Mitt Romney says he likes to fire people."
- flat-rationale: The evidence does not support the claim that Mitt Romney said he likes to fire people; it only includes topical context about his policies and hiring practices.

### id=6812 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: The Obama administration’s "green" stimulus program "funneled close to $2 billion dollars to overseas firms," creating thousands of jobs in China.
- flat-rationale: The claim contains an element of truth about funds going to overseas firms but exaggerates the job creation impact in China and omits broader context that most stimulus funding went to U.S. companies.

### id=6857 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: "In one year, (President Obama) provided $90 billion in breaks to the green energy world … into solar and wind, to Solyndra and Fisker and Tesla and Ener1."
- flat-rationale: The claim misrepresents the actual stimulus spending and tax credits provided by Obama's administration. The evidence shows proposals for long-term energy taxes and investments in wind and solar projects over a decade, not $90 billion in breaks to specific companies like Solyndra and Tesla in one year.

### id=7211 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The problem with raising tax rates on the wealthiest Americans is that more than half of them are small business owners."
- flat-rationale: The evidence shows that the claim is misleading; more than half of the wealthiest Americans are not small business owners. The topical passages indicate the tax surcharge targets wealthy individuals rather than small businesses.

### id=7288 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Virginia economic development officials "decided they didn’t want to bid on" his company's electric automobile plant.
- flat-rationale: The evidence does not support the claim that Virginia economic development officials decided not to bid on the electric automobile plant. The provided passages are topical and do not address the specific actions of Virginia officials regarding a potential bid.

### id=7442 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: If the sequester hits, federal prosecutors will have to "let criminals go."
- flat-rationale: The claim contains an element of truth but ignores critical facts that change the impression. While federal prosecutors may face challenges under sequestration, evidence suggests it's not a universal or severe enough impact to justify 'letting criminals go'.

### id=7678 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says "If you compare the Portland Metro area to the CDC’s statewide cavity rates ... the Portland Metro area would actually rank as having the 15th lowest cavity rate in the U.S."
- flat-rationale: The evidence is entirely topical and does not address cavity rates or provide any support for the claim's numerical assertion. The structural prior suggests a balanced mix of Half-true and Barely-true, but without relevant supporting data, the claim must be rated False due to lack of evidence.

### id=7806 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: A referendum "gives the people the chance to decide" on cutting the Milwaukee County Board budget by two-thirds
- flat-rationale: The evidence shows the referendum is about a minimum wage issue, not cutting the Milwaukee County Board budget by two-thirds as claimed.

### id=7823 — gold *Half-true*
- arg-aware predicted **True**
- flat-RAG predicted **Half-true** ✓
- claim: "To hear Gov. Christie tell it, everything in New Jersey is going just fine. Well I see another New Jersey with 400,000 unemployed. One of the worst jobless rates in the country. Working and middle class families have seen costs soar, from property taxes to college tuition."
- flat-rationale: The claim highlights issues like high unemployment and rising costs in New Jersey but omits context about the state's fiscal challenges and Christie's perspective on federal funding disparities.

### id=7952 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The immigration bill "has a specific provision that says that Secretary Napolitano does not have to build any fence if she chooses not to."
- flat-rationale: The evidence shows the bill does not exempt Secretary Napolitano from building fence; it authorizes border security measures and leaves implementation to her discretion but does not grant an exemption.

### id=8035 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says in Texas "it's legal to shoot someone who's committing a ‘public nuisance’ under the cover of dark."
- flat-rationale: The evidence does not support the claim; it is purely topical and does not address the legality of shooting someone committing a public nuisance under cover of dark.

### id=8151 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Of the roughly 15 percent of Americans who don’t have health insurance, "half of them made more than $50,000 a year."
- flat-rationale: The claim is unsupported by the evidence and lacks specific data to back up the assertion that half of uninsured Americans earn more than $50,000 a year.

### id=8519 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Kay Hagan "supports waivers for friends of Obama and special treatment for Congress and their staffs."
- flat-rationale: The evidence is entirely topical and does not support the claim's assertion about waivers or special treatment for Congress and their staffs. The claim lacks factual basis.

### id=8558 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Rhode Island's unemployment insurance system "is the most expensive such system in the country."
- flat-rationale: The evidence is entirely topical and does not address the claim about Rhode Island's unemployment insurance system being the most expensive in the country. There are no supporting or attacking facts related to the specific claim.

### id=8606 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: "Republicans have proposed dozens of (health care) solutions designed to help control costs and improve quality."
- flat-rationale: The claim is partially accurate as Republicans have proposed solutions to control costs and improve quality, but the evidence does not support 'dozens' of such proposals. The context provided is mostly topical.

### id=8761 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: A judge's order means there's a "Constitution exemption zone" if you live "within 100 miles of the United States border."
- flat-rationale: The claim misrepresents the legal and constitutional framework; there is no 'Constitution exemption zone' within 100 miles of the border as described.

### id=8830 — gold *Half-true*
- arg-aware predicted **False**
- flat-RAG predicted **Half-true** ✓
- claim: "The $18.8 billion in funding for K-12 education funding is the highest in Florida history and includes a record $10.6 billion in state funds."
- flat-rationale: The claim is partially accurate as funding has increased but it does not reach the pre-recession level and the record amount of state funds needs context on how it compares to historical data.

### id=8853 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says President Barack Obama "spent nearly a trillion dollars on make-work government jobs."
- flat-rationale: The evidence does not support the claim that Obama spent nearly a trillion dollars on make-work government jobs; it is more focused on criticizing overall spending and deficits.

### id=9091 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The percentage of black children born without a father in the home has risen from 7 percent in 1964 to 73 percent today, due to changes from President Lyndon Johnson’s Great Society.
- flat-rationale: The claim misattributes the cause to President Johnson's Great Society without evidence; the passages are topical and do not support the causal link.

### id=9101 — gold *Half-true*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **Half-true** ✓
- claim: "Women take birth control, more than half of them, as a medication for other conditions."
- flat-rationale: The claim is partially accurate as birth control is used for conditions other than pregnancy prevention, but it overstates the proportion of women who use it primarily for non-pregnancy-related reasons. The evidence suggests multiple uses but does not support 'more than half' using it solely for medical conditions.

### id=9112 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "22 Countries Invaded by the U.S. in 20 Years."
- flat-rationale: The evidence does not support the claim that 22 countries were invaded by the U.S. in 20 years; it only mentions Afghanistan and provides context without confirming multiple invasions.

### id=9197 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: "The big Wall Street banks, the big corporations" give "many times more" political donations to Democrats than Republicans.
- flat-rationale: The evidence shows that large donors give more to Republicans than Democrats, contradicting the claim's central assertion.

### id=9200 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "Eighty percent of Wall Street executives and their spouses' donations go to Democrats."
- flat-rationale: {"label": "False", "rationationale": "The evidence is entirely topical and does not provide any support for the claim that 80% of Wall Street executives' donations go to Democrats. The provided context discusses general trends but lacks specific data on donation percentages."}

### id=9285 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: After the attack on a U.S. diplomatic mission in Benghazi, Libya, "the ambassador's body was dragged through the street."
- flat-rationale: The evidence does not support the claim that Ambassador Stevens's body was dragged through the street; it only confirms his death during the attack.

### id=9489 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says the secret John Doe criminal investigation of his campaign has been "resolved" and two judges have said it is "over."
- flat-rationale: The evidence is entirely topical and does not confirm the claim that the secret investigation has been resolved or declared over by two judges. The structural prior suggests uncertainty but leans towards a negative assessment given the lack of supporting evidence.

### id=9610 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: David Perdue "has never voted in a Republican primary until his name was on the ballot."
- flat-rationale: The evidence shows that the claim is incorrect as Perdue has voted in Republican primaries before his candidacy, contradicting the central assertion.

### id=9774 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Charlie "Crist made it easier for Duke to take your money."
- flat-rationale: The evidence does not support the claim that Crist made it easier for Duke to take money; instead, it focuses on Rothstein's contributions and influence over Crist's judicial appointments.

### id=10064 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Charlie Crist "is embroiled in a fraud case for steering taxpayer money to a de facto Ponzi scheme."
- flat-rationale: The evidence does not support the claim that Charlie Crist is involved in a fraud case for steering taxpayer money to a Ponzi scheme; it only mentions Scott Rothstein's unrelated conviction and topical comparisons.

### id=10140 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: Four members of the Rhode Island General Assembly "went to vote in 2010 and were told they had already voted."
- flat-rationale: The evidence is entirely topical and does not confirm the claim that four members were told they had already voted. The structural prior suggests uncertainty but leans towards a negative assessment given the lack of supporting evidence.

### id=10512 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The minimum wage has risen $2.35 in the last two years. That's 31 percent.
- flat-rationale: The claim's numerical details are incorrect; the minimum wage increased from $5.15 to $7.25 over two years, which is a rise of $2.10 or 40.8%, not $2.35 or 31% as stated.

### id=10623 — gold *Mostly-true*
- arg-aware predicted **False**
- flat-RAG predicted **Mostly-true** ✓
- claim: Wisconsin is "dead last in the Midwest for job creation."
- flat-rationale: The claim is directionally correct but omits the detail that Wisconsin was tied for last place rather than strictly last.

### id=10631 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Birth control pioneer Margaret Sanger was "an active participant in the Ku Klux Klan."
- flat-rationale: The evidence shows the claim is based on historical misunderstandings and there is no support for Sanger being an active participant in the Ku Klux Klan.

### id=10633 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "A few weeks ago Obama took Hamas and Iran OFF the terror list."
- flat-rationale: The claim is incorrect as there are no passages supporting the removal of Hamas or Iran from any terror list; all evidence is topical and unrelated to the central assertion.

### id=10672 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "White men account for 69 percent of those arrested for violent crimes."
- flat-rationale: The evidence does not provide any support for the claim's specific statistic and is entirely topical. Without confirming data or context, the claim cannot be substantiated.

### id=10948 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Hillary Clinton "has donated every cent she's ever earned from speaking fees to charity."
- flat-rationale: The evidence is entirely topical and does not confirm the claim that Clinton has donated every cent from speaking fees to charity; it lacks any support for this specific assertion.

### id=11025 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: Six thousand people have sought addiction treatment through expanded Medicaid.
- flat-rationale: {"label": "False", "rationationale": "The evidence does not provide any support for the specific claim that six thousand people have sought addiction treatment through expanded Medicaid. The provided passages are topical and do not confirm or deny the numerical assertion."}

### id=11184 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Scott Walker "had a 2.3 GPA when he was asked to leave Marquette University for cheating."
- flat-rationale: The evidence is entirely topical and does not address the claim about Scott Walker's GPA or academic expulsion from Marquette University for cheating. The structural prior suggests a balance between Half-true and Barely-true, but without relevant support or attack passages, the claim must be rated False due to lack of factual basis.

### id=11200 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says 57 percent of federal spending goes to the military and just 1 percent goes to food and agriculture, including food stamps.
- flat-rationale: {"label": "False", "rationationale": "The claim is factually incorrect as it misrepresents the proportion of federal spending on food and agriculture. The evidence shows that administration costs for food stamps are less than 0.1%, not 70%."}

### id=11409 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Republican Rep. Charlie Dent wants to kick the Freedom Caucus out of the Republican conference "for voting our conscience."
- flat-rationale: The evidence is entirely topical and does not address the claim about Rep. Charlie Dent or the Freedom Caucus. The structural prior suggests a balance between Half-true and Barely-true, but without relevant support or attack passages, the claim must be rated False due to lack of evidence.

### id=11443 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: "I did not play any role in bringing the company to RI as did others in government. I was tasked with handling the legislation affecting the company by my superiors."
- flat-rationale: The evidence is entirely topical and does not address the claim's central assertion about playing a role in bringing the company to RI or handling legislation. The lack of relevant support or attack passages suggests the claim is unsubstantiated, leaning towards False.

### id=11588 — gold *False*
- arg-aware predicted **Half-true**
- flat-RAG predicted **False** ✓
- claim: Drinking champagne could help prevent Alzheimer’s and other forms of dementia.
- flat-rationale: The evidence does not support the claim that drinking champagne could help prevent Alzheimer's and other forms of dementia; all provided passages are topical and unrelated to the health benefits or risks associated with alcohol consumption regarding cognitive decline.

### id=11661 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "If Trump had just put his father’s money in a mutual fund ... he’d have $8 billion."
- flat-rationale: The claim is speculative and overstates the potential outcome; it assumes a specific investment strategy that would yield $8 billion without evidence to support such a precise figure.

### id=11685 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Wisconsin "is on pace to double the number of layoffs" this year.
- flat-rationale: The evidence is topical and does not confirm the claim that Wisconsin layoffs are on pace to double; it lacks specific data supporting this assertion.

### id=11861 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Donald Trump's conversion to pro-life beliefs are akin to Justin Bieber's, who said in the past that abortion "was no big deal to him."
- flat-rationale: The claim misrepresents Trump's shift on abortion as similar to Justin Bieber's casual remarks, when the evidence shows it is more akin to a politician's policy evolution. The comparison lacks substantive context and accuracy.

### id=11867 — gold *False*
- arg-aware predicted **Mostly-true**
- flat-RAG predicted **False** ✓
- claim: Says CNN reported Ben Carson was "taking a break from campaigning" and the Cruz campaign "forwarded that news to our volunteers."
- flat-rationale: The evidence shows no support for the claim that CNN reported Ben Carson was taking a break from campaigning or that the Cruz campaign forwarded this news to volunteers. The passages are topical and do not confirm the specific assertions made in the claim.

### id=11955 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Milwaukee County Executive Chris Abele spent "$100,000 of taxpayer money on a new luxury SUV."
- flat-rationale: The evidence does not support the claim that Abele spent $100,000 on a luxury SUV; it is purely topical context without confirming or attacking the specific expenditure figure.

### id=12087 — gold *Barely-true*
- arg-aware predicted **False**
- flat-RAG predicted **Barely-true** ✓
- claim: "Our campaign depends on small donations for the majority of our support."
- flat-rationale: The evidence suggests the claim is a generalization that may not be accurate for all campaigns or candidates, thus misleading overall despite an element of truth in some cases.

### id=12210 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Charlotte’s anti-discrimination ordinance would have "opened all bathrooms to all sexes at all times" if it hadn’t been overturned.
- flat-rationale: The claim misrepresents the Charlotte ordinance; there is no evidence it opened bathrooms to all sexes at all times. The provided evidence is topical and does not support the central assertion of the claim.

### id=12398 — gold *Pants-fire*
- arg-aware predicted **False**
- flat-RAG predicted **Pants-fire** ✓
- claim: Says Donald Trump said of women, "And you can tell them to go f--- themselves."
- flat-rationale: The evidence shows no record of Trump making such a statement; the passages are topical and do not support or attack the claim directly. Given the fabricated nature of the quote, it aligns with Pants-fire.

### id=12424 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "I can tell you that the enhanced interrogation techniques that have since been banned by this administration — specifically waterboarding — work."
- flat-rationale: The claim is unsupported by the evidence and lacks factual backing; the provided passages are topical and do not confirm the effectiveness of waterboarding.

### id=12698 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "What the facts say" is ... "the best scenario for kids is a loving mom and dad."
- flat-rationale: The evidence is entirely topical and does not support or attack the claim that 'the best scenario for kids is a loving mom and dad.' The structural prior suggests uncertainty between Half-true and Barely-true, but without any relevant supporting or attacking evidence, the claim cannot be substantiated, leading to a False label.

### id=12961 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- flat-rationale: The evidence contradicts the claim's central assertion that 80% is overhead and only 20% goes to charitable causes; it shows a lower percentage for overhead and higher for actual spending on causes.

### id=13049 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Say "71 percent of doctors say Hillary's health concerns are 'serious' and 'could be disqualifying.' "
- flat-rationale: The evidence does not support the claim; there are no passages confirming that 71 percent of doctors hold the stated view. The provided evidence is topical and does not substantiate the specific numerical assertion.

### id=13155 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: Says Ron Johnson "helped companies ship jobs overseas."
- flat-rationale: The evidence shows the claim is misleading; Johnson voted for tax breaks but there's no direct evidence linking this to shipping jobs overseas. The context provided by Feingold's campaign and Johnson's own statements indicate a more nuanced situation than the claim suggests.

### id=13203 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: "Toomey and Trump will ban abortion and punish women who have them."
- flat-rationale: The claim misrepresents both Toomey and Trump's positions on abortion. There is no evidence that either has proposed banning abortion or punishing women who have them.

### id=13423 — gold *False*
- arg-aware predicted **Pants-fire**
- flat-RAG predicted **False** ✓
- claim: The media "never show crowds."
- flat-rationale: The evidence does not support the claim; it is more about historical context and lacks direct refutation but implies the media do show crowds when present.

