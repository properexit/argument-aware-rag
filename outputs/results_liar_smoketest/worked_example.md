# Worked example

**Claim** ('"The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."')

- Gold label: **False**
- Predicted label: **Pants-fire**
- Rationale: The claim is fabricated; evidence shows the Clinton Foundation spends far less on overhead and more on programs than claimed.

## Role-targeted queries

- **attack** (kept 5/20): premise = 'Conversely, only between 10-20 percent is spent on management of the foundation and fundraising activities, which is tagged as "overhead."'
  - query: Evidence contradicting or refuting that: Conversely, only between 10-20 percent is spent on management of the foundation and fundraising activities, which is tagged as "overhead.". Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- **attack** (kept 5/20): premise = 'Priebus is incorrectly reading IRS documents'
  - query: Evidence contradicting or refuting that: Priebus is incorrectly reading IRS documents. Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- **attack** (kept 5/20): premise = 'It spends the majority of its money directly on projects rather than through third-party grants'
  - query: Evidence contradicting or refuting that: It spends the majority of its money directly on projects rather than through third-party grants. Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- **attack** (kept 5/20): premise = 'The Clinton Foundation spends between 80-90 percent on program services, which experts say is the standard in the industry to define charitable works'
  - query: Evidence contradicting or refuting that: The Clinton Foundation spends between 80-90 percent on program services, which experts say is the standard in the industry to define charitable works. Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- **attack** (kept 5/20): premise = 'But that doesn’t mean that every other dollar is "overhead."'
  - query: Evidence contradicting or refuting that: But that doesn’t mean that every other dollar is "overhead.". Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."
- **pattack** (kept 5/20): premise = 'Only a small amount of the donations collected by the Clinton Foundation are awarded as grants to other nonprofit groups'
  - query: Evidence partially refuting or qualifying that: Only a small amount of the donations collected by the Clinton Foundation are awarded as grants to other nonprofit groups. Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."

## Evidence by role

### attack (25 passages)

- role_fit=0.00 nli=entailment pid=13188::13
  > The American Institute of Philanthropy’s Charity Watch, reached the same conclusion. It has given the Clinton Foundation an A rating and says it spends only 12 percent of the money it raises on "overhead ."

- role_fit=0.02 nli=entailment pid=10775::19
  > The foundation says its own employees are doing its charitable work. The annual report -- which, remember, includes both the Clinton Foundation and the Clinton Health Access Initiative -- says that 7 percent of expenditures were spent on "management and expenses" and 4.5 percent for "fundraising." (The numbers on the 990s for the two entities are in the same ballpark.)

- role_fit=0.40 nli=entailment pid=10775::12
  > "When anyone contributes to the Clinton Foundation, it actually goes toward fat salaries, administrative bloat, and lavish travel. Between 2009 and 2012, the Clinton Foundation raised over $500 million dollars according to a review of IRS documents by The Federalist ( 2012 , 2011 , 2010 , 2009 , 2008 ). A measly 15 percent of that, or $75 million, went towards programmatic grants. More than $25 mi...

- role_fit=0.07 nli=entailment pid=10775::2
  > "The Marine Corps-Law Enforcement Foundation -- 99 percent pass-through. The Clinton Family Foundation pass-through is 15 percent. The Federalist reports only 15 percent of the money donated to the Clinton Family Foundation went to actual charitable causes. The bulk of the money donated to the Clinton Family Foundation went to travel, salaries, and benefits. Sixty percent of all the money raised w...

- role_fit=0.02 nli=entailment pid=10775::30
  > To offer some context, spending 88 percent of expenses on charitable programs, as the Clinton foundation says it does, would actually be pretty good by industry standards. Parsons said the average reported across all organizations in the National Center for Charitable Statistics is 81 percent -- equal to the Clinton Foundation’s rate on its own -- and the Better Business Bureau’s Wise Giving Allia...

- role_fit=1.00 nli=contradiction pid=7808::2
  > Forbes responded, "Well, Gretchen, first of all, it is the power that the IRS has that's different than any other agency, any other department. … The IRS doesn't have to prove something against you. They can walk in and you've got the burden of proof."

- role_fit=1.00 nli=contradiction pid=10285::19
  > On the other end of the scale, the best reading proficiency score at an 80/80 school was 21 percent at Hartford Avenue University School in MPS. Second (20 percent) was Franklin School, also in MPS. St. Marcus Lutheran was third (19 percent).

- role_fit=1.00 nli=contradiction pid=12992::37
  > "The Bush foundations did not raise comparable amounts of money and from as many foreign sources as the Clinton Foundation," said Holman of Public Citizen.

- role_fit=1.00 nli=contradiction pid=10775::17
  > The correct number for the Clinton Foundation alone -- which owned the account the tweet was sent from -- was just over 80 percent in 2013, not 88 percent.

- role_fit=0.91 nli=contradiction pid=7808::18
  > This ratio of cases suggests that Forbes’ claim is largely accurate. "Nothing the congressman said on the burden of proof would strike me as outside of the norm or the general rule if I or any other tax litigator heard it in everyday conversation," Jacobs said.

- role_fit=1.00 nli=contradiction pid=10775::6
  > When most people in the charitable world think of foundations, they think of organizations that give away a lot of money in the form of grants to others who go out and do good works. The Clinton foundation works differently -- it keeps its money in house and hires staff to carry out its own humanitarian programs.

- role_fit=0.57 nli=neutral pid=10775::18
  > As we noted earlier, many foundations carry out charitable works by giving money to other organizations that, in turn, do the ground-level charity work, whereas the Clinton foundation’s charitable works are mostly done by people on the foundation’s payroll. "We are an implementing organization rather than a grantmaking organization," said the foundation’s Minassian. That’s why the Clinton Foundati...

- role_fit=0.38 nli=neutral pid=13188::2
  > This is based on a misunderstanding of how the foundation operates. In brief, it raises money to deliver services and projects itself. The amount of money it gives away as grants is a small sliver of its activities.

- role_fit=0.49 nli=neutral pid=13188::5
  > "Although it has ‘foundation’ in its name, the Clinton Foundation is actually a public charity," Brian Mittendorf, a professor of accounting at Ohio State University’s Fisher College of Business, wrote in the Chronicle of Philanthropy . "In practical terms, this means both that it relies heavily on donations from the public and that it achieves its mission primarily by using those donations to con...

- role_fit=0.32 nli=neutral pid=13188::3
  > We’ll use the Clinton Foundation’s most recent IRS tax form, for 2014, as an example. (It starts on Page 28 of this document .) The foundation reported total expenses in 2014 of a little over $91 million but grants of just $5.1 million. That’s close to 6 percent of the foundation’s money being spent on grants.

- role_fit=1.00 nli=contradiction pid=13018::2
  > "Because that idea that somehow the Clinton Foundation is this wonderful thing that helps people, most charities give 75 percent of their money in direct aid. The Clinton Foundation gives less than 10 (percent). In 2013, they raised 140 million bucks, gave 9 million to people in direct aid," Castellanos said .

- role_fit=1.00 nli=contradiction pid=13188::1
  > "10 cents on the dollar from the Clinton Foundation goes to charitable causes," Pence said.

- role_fit=0.01 nli=entailment pid=13018::9
  > All together, these programs cost $68 million in 2013 ( page 10 of the foundation’s tax documents for that year), or about 80 percent of all of the foundation's expenses that year. In 2014, programs were 87 percent of the Clinton Foundation’s expenses, according to Charity Navigator , giving it a score of 10 out of 10 on that metric.

- role_fit=0.01 nli=entailment pid=13188::11
  > He said that in 2014, 87.2 percent of the Clinton Foundation’s expenses were on program services.

- role_fit=0.00 nli=entailment pid=10775::0
  > Much of the discussion about the Clinton family foundation has focused on who donated to it and what they may have expected in return from then-Secretary of State Hillary Clinton. But critics of the Clintons have opened up another line of attack on what is formally known as the Bill, Hillary & Chelsea Clinton Foundation, charging that it doesn’t actually spend very much on charitable works.

- role_fit=0.50 nli=neutral pid=13188::4
  > But that doesn’t mean everything else is overhead, people who monitor charities and their practices say, or that only 10 cents of every dollar went to a charitable cause.

- role_fit=0.01 nli=entailment pid=1412::3
  > "What about the administrative costs of donating through WhiteHouse.gov, for crying out loud?" Limbaugh asked. "Do you know that one of the reasons the welfare budget is as high as it is -- and these numbers are I guess 10 years old, but in 1999, maybe earlier than that, for every dollar that was budgeted for welfare or food stamps, AFDC, whatever it is, 28 cents of it was spent on administering i...

- role_fit=0.00 nli=entailment pid=4037::6
  > In an interview with us, the representative conceded the Republican-guided Legislature did not earmark the money expected to pile up in the fund, which has a current balance of $5 billion. But, he said, that doesn’t mean it couldn’t have covered existing needs.

- role_fit=0.00 nli=entailment pid=10775::29
  > That’s more than we had expected to see in domestic spending -- we’re checking with the foundation on why that was so high, and will report their explanation if we receive one -- but even if the foundation devoted as little as one-third of its expenses to programs outside the U.S., then Limbaugh’s 15 percent estimate would be too low.

- role_fit=0.01 nli=entailment pid=10285::17
  > Of course, this is the reading average based on the collective reading proficiency at each school. It doesn’t mean every school came in at the overall school average of 7.3 percent.

### pattack (5 passages)

- role_fit=0.00 nli=entailment pid=13168::13
  > But the donations did not go to Clinton personally; they went to the foundation. While Clinton has been intimately involved in the foundation when not serving in the government or running for office, neither Clinton nor her political campaigns have ever received a direct monetary benefit , such as a salary, from the foundation.

- role_fit=0.00 nli=entailment pid=13168::5
  > On this particular claim, though, Giuliani stretches the truth. The donations from the countries in question do not come close to "hundreds of millions" of dollars. And the money goes to the foundation, not to Clinton.

- role_fit=0.00 nli=entailment pid=13444::7
  > In terms of gifts, the Clinton Foundation did accept millions of dollars in donations from foreign governments while Clinton was secretary of state. The money was to be used for charitable work. But there is no proven evidence that she, as a person holding office, personally solicited or received such gifts.

- role_fit=0.02 nli=entailment pid=13018::11
  > In sum, Castellanos’ claim is "totally wrong," Callahan of Inside Philanthropy told PolitiFact. "The vast majority of the money raised goes to support program work in the field, as anyone can tell from looking at the Clinton Foundation’s annual finances."

- role_fit=0.00 nli=entailment pid=12616::29
  > We created a breakdown of the nine "investors" and their donations to the Clinton Foundation, based on the most complete information we could find through the Clinton Foundation, media reports and public filings as well as what Clinton Cash reported.

