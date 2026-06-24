# Worked example

**Claim** ('"The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."')

- Gold label: **False**
- Predicted label: **Pants-fire**
- Rationale: The claim attributes specific financial figures to the Clinton Foundation that are not supported by evidence and appear fabricated. The provided evidence does not relate to the foundation's finances but instead discusses unrelated topics, confirming the assertion is baseless.

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
- **pattack** (kept 3/20): premise = 'Only a small amount of the donations collected by the Clinton Foundation are awarded as grants to other nonprofit groups'
  - query: Evidence partially refuting or qualifying that: Only a small amount of the donations collected by the Clinton Foundation are awarded as grants to other nonprofit groups. Context claim: "The fact is" the Clinton Foundation has "got about 80 percent in overhead and 20 percent of the money is actually getting into the places it should."

## Evidence by role

### attack (25 passages)

- role_fit=1.00 nli=contradiction pid=wiki::909::5
  > Anglican Communion: The Church of England has always thought of itself not as a new foundation but rather as a reformed continuation of the ancient "English Church" (Ecclesia Anglicana) and a reassertion of that church's rights. As such it was a distinctly national phenomenon. The Church of Scotland was formed as a separate church from the Roman Catholic Church as a result of the Scottish Reformat...

- role_fit=0.00 nli=entailment pid=wiki::706::1
  > Economy of Angola: Corruption is rife throughout the economy and the country remains heavily dependent on the oil sector, which in 2017 accounted for over 90 percent of exports by value and 64 percent of government revenue. With the end of the oil boom, from 2015 Angola entered into a period of economic contraction.

- role_fit=0.00 nli=entailment pid=wiki::1336::7
  > The Apache Software Foundation: Apache divides its software development activities into separate semi-autonomous areas called "top-level projects" (formally known as a "Project Management Committee" in the bylaws), some of which have a number of sub-projects. Unlike some other organizations that host FOSS projects, before a project is hosted at Apache it has to be licensed to the ASF with a grant ...

- role_fit=0.00 nli=entailment pid=wiki::1336::8
  > The Apache Software Foundation: Board of directors
The Board of Directors of The Apache Software Foundation (ASF) is responsible for management and oversight of the business and affairs of the corporation in accordance with the Bylaws. This includes management of the corporate assets (funds, intellectual property, trademarks, and support equipment), appointment of a President and corporate officer...

- role_fit=0.00 nli=entailment pid=wiki::706::7
  > Economy of Angola: Yet by 1976, these encouraging developments had been reversed. The economy was in complete disarray in the aftermath of the war of independence and the subsequent internal fighting of the liberation movements. According to the ruling MPLA-PT, in August 1976 more than 80 percent of the agricultural plantations had been abandoned by their Portuguese owners; only 284 out of 692 fac...

- role_fit=1.00 nli=contradiction pid=wiki::1336::1
  > The Apache Software Foundation: The Apache Software Foundation is a decentralized open source community of developers. The software they produce is distributed under the terms of the Apache License, a permissive open-source license for free and open-source software (FOSS). The Apache projects are characterized by a collaborative, consensus-based development process and an open and pragmatic softwa...

- role_fit=1.00 nli=contradiction pid=wiki::1111::5
  > Politics of American Samoa: The legislative power is vested in the American Samoa Fono, which has two chambers. The House of Representatives has 21 members serving two-year terms, being 20 representatives popularly elected from various districts and one non-voting delegate from Swains Island elected in a public meeting. The Senate has 18 members, elected for four-year terms by and from the chiefs ...

- role_fit=1.00 nli=contradiction pid=wiki::1316::4
  > Annales school: In 1962, Braudel and Gaston Berger used Ford Foundation money and government funds to create a new independent foundation, the  (FMSH), which Braudel directed from 1970 until his death. In 1970, the 6th Section and the Annales relocated to the FMSH building.  FMSH set up elaborate international networks to spread the Annales gospel across Europe and the world. In 2013, it began pub...

- role_fit=1.00 nli=contradiction pid=wiki::1081::4
  > Economy of Azerbaijan: Republic era
Oil remains the most prominent product of Azerbaijan's economy with cotton, natural gas and agriculture products contributing to its economic growth over the last five years. More than $60 billion was invested into Azerbaijan's oil by major international oil companies in AIOC consortium operated by BP. Oil production under the first of these PSAs, with the Azerb...

- role_fit=1.00 nli=contradiction pid=wiki::1286::8
  > List of governors of Alabama: The office of lieutenant governor was created in 1868, abolished in 1875, and recreated in 1901. According to the current constitution, should the governor be out of the state for more than 20 days, the lieutenant governor becomes acting governor, and if the office of governor becomes vacant the lieutenant governor ascends to the governorship.

- role_fit=1.00 nli=contradiction pid=wiki::705::0
  > Politics of Angola: The current political regime in Angola is presidentialism, in which the President of the Republic is also head of state and government; it is advised by a Council of Ministers, which together with the President form the national executive power. Legislative power rests with the 220 parliamentarians elected to the National Assembly. The President of the Republic, together with t...

- role_fit=0.00 nli=entailment pid=wiki::706::6
  > Economy of Angola: But in the wake of World War II, the rapid growth of industrialization worldwide and the parallel requirements for raw materials led Portugal to develop closer ties with its colonies and to begin actively developing the Angolan economy. In the 1930s, Portugal started to develop closer trade ties with its colonies, and by 1940 it absorbed 63 percent of Angolan exports and account...

- role_fit=0.00 nli=entailment pid=wiki::1495::4
  > Australian Labor Party: Although the ALP officially adopted the spelling without a u, it took decades for the official spelling to achieve widespread acceptance. According to McMullin, "the way the spelling of 'Labor Party' was consolidated had more to do with the chap who ended up being in charge of printing the federal conference report than any other reason". Some sources have attributed the of...

- role_fit=0.00 nli=entailment pid=wiki::1316::0
  > Annales school: The Annales school () is a group of historians associated with a style of historiography developed by French historians in the 20th century to stress long-term social history. It is named after its scholarly journal Annales d'histoire économique et sociale, which remains the main source of scholarship, along with many books and monographs. The school has been highly influential in ...

- role_fit=0.00 nli=entailment pid=wiki::737::3
  > Afghanistan: Afghanistan is rich in natural resources, including lithium, iron, zinc, and copper. It is also the world's largest producer of opium, second largest producer of cannabis resin, and third largest of both saffron and cashmere. The country is a member of the South Asian Association for Regional Cooperation and a founding member of the Organization of Islamic Cooperation. Due to the effe...

- role_fit=1.00 nli=contradiction pid=wiki::771::7
  > American Revolutionary War: Closure of American ports undermined the 1778 strategy devised by Howe's replacement Henry Clinton, which intended to take the war against the Americans into the south. Despite some initial success, Cornwallis was besieged by a Franco-American force in Yorktown in September and October 1781. Cornwallis attempted to resupply the garrison, but failed and was forced to sur...

- role_fit=0.00 nli=entailment pid=wiki::1336::0
  > The Apache Software Foundation: The Apache Software Foundation ( ; ASF) is an American nonprofit corporation (classified as a 501(c)(3) organization in the United States) to support a number of open-source software projects. The ASF was formed from a group of developers of the Apache HTTP Server, and incorporated on March 25, 1999.  it includes approximately 1000 members.

- role_fit=0.01 nli=entailment pid=wiki::1094::3
  > Economy of Armenia: Overview
Under the old Soviet central planning system, Armenia had developed a modern industrial sector, supplying machine tools, textiles, and other manufactured goods to sister republics in exchange for raw materials and energy. Since the implosion of the USSR in December 1991, Armenia has switched to small-scale agriculture away from the large agroindustrial complexes of the...

- role_fit=0.02 nli=entailment pid=wiki::1435::0
  > Abbotsford, Scottish Borders: Abbotsford is a historic country house in the Scottish Borders, near Galashiels, on the south bank of the River Tweed. Now open to the public, it was built as the residence of historical novelist and poet Sir Walter Scott between 1817 and 1825. It is a Category A Listed Building and the estate is listed in the Inventory of Gardens and Designed Landscapes in Scotland.

- role_fit=0.01 nli=entailment pid=wiki::1336::4
  > The Apache Software Foundation: History
The history of the Apache Software Foundation is linked to the Apache HTTP Server, development beginning in February 1993. A group of eight developers started working on enhancing the NCSA HTTPd daemon. They came to be known as the Apache Group. On March 25, 1999, the Apache Software Foundation was formed. The first official meeting of the Apache Software Fo...

- role_fit=0.00 nli=entailment pid=wiki::765::4
  > Abortion: Globally, there has been a widespread trend towards greater legal access to abortion since 1973, but there remains debate with regard to moral, religious, ethical, and legal issues. Those who oppose abortion often argue that an embryo or fetus is a person with a right to life, and thus equate it with murder. Those who support its legality often argue that it is a woman's reproductive rig...

- role_fit=0.00 nli=entailment pid=wiki::1030::7
  > Austrian school of economics: Despite such claim, John Stuart Mill had used value in use in this sense in 1848 in Principles of Political Economy, where he wrote: "Value in use, or as Mr. De Quincey calls it, teleologic value, is the extreme limit of value in exchange. The exchange value of a thing may fall short, to any amount, of its value in use; but that it can ever exceed the value in use, im...

- role_fit=0.00 nli=entailment pid=wiki::863::8
  > American Civil War: Disagreements among states about the future of slavery were the main cause of disunion and the war that followed. Slavery had been controversial during the framing of the Constitution, which, because of compromises, ended up with proslavery and antislavery features. The issue of slavery had confounded the nation since its inception and increasingly separated the United States i...

- role_fit=0.00 nli=entailment pid=wiki::1070::10
  > Politics of Antigua and Barbuda: Antigua and Barbuda elects on national level a legislature. Parliament has two chambers. The House of Representatives has 19 members: 17 members elected for a five-year term in single-seat constituencies, and 2 ex officio members (president and speaker). The Senate has 17 appointed members. The prime minister is the leader of the majority party in the House and con...

- role_fit=0.00 nli=entailment pid=wiki::909::0
  > Anglican Communion: The Anglican Communion is the third largest Christian communion after the Roman Catholic and Eastern Orthodox churches. Founded in 1867 in London, the communion has more than 85 million members within the Church of England and other autocephalous national and regional churches in full communion. The traditional origins of Anglican doctrine are summarised in the Thirty-nine Arti...

### pattack (3 passages)

- role_fit=0.00 nli=entailment pid=wiki::1111::1
  > Politics of American Samoa: There is also the traditional village politics of the Samoan Islands, the  and the , which continues in American Samoa and in independent Samoa, and which interacts across these current boundaries. The  is the language and customs, and the  the protocols of the  (council) and the chiefly system. The  and the  take place at all levels of the Samoan body politic, from the...

- role_fit=0.00 nli=entailment pid=wiki::706::3
  > Economy of Angola: The Angolan economy has been dominated by the production of raw materials and the use of cheap labor since European rule began in the sixteenth century. The Portuguese used Angola principally as a source for the thriving slave trade across the Atlantic; Luanda became the greatest slaving port in Africa. After the Portuguese Empire abolished the slave trade in Angola in 1858, it ...

- role_fit=0.00 nli=entailment pid=wiki::1081::8
  > Economy of Azerbaijan: In 2010, Azerbaijan entered into the top eight biggest oil suppliers to EU countries with €9.46 billion. In 2011, the amount of foreign investments in Azerbaijan was $20 billion, a 61% increase from 2010. According to Minister of Economic Development of Azerbaijan, Shahin Mustafayev, in 2011, "$15.7 billion was invested in the non-oil sector, while the restin the oil sector"...

