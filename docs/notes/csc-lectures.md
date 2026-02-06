Computational Social Choice by Felix Brandt

1. Introduction

- social choice theory = how to aggregate possibly conflicting preferences into collective choices in a fair and satisfactory way

- ingredients
    - autonomous agents
    - alternatives
    - preferences over alternatives
        - e.g. preferred set
        - e.g. ordinal rank
        - e.g. utility function
    - aggregation functions
    - output types
        - e.g. best alternative
        - e.g. set of good alternatives
        - e.g. ranking of alternatives
        - e.g. probability distribution (lottery)

- examples
    - voting
    - resource allocation
    - coalition formation
    - webpage ranking
    - collaborative filtering

- questions
    - what does it mean to make rational choices
    - which formal properties should be aggregation function satisfy
    - which of these properties can be satisfied simultaneously
    - how difficult is it to compute collective choice
    - can voters benefit by lying about their preferences

- math tools
    - sets, relations
    - directed graphs
    - functions

- recommended literature
    - [intro] Choice Theory - A very short introduction
    - [intro] Computational Social Choice
    - [intro] A Primer in Social Choice Theory
    - [intro] Collective Choice and Preference
    - [adv] Handbook of Computational Social Choice
    - [adv] Axioms of Cooperative Decision Making
    - [adv] Positive Political Theory I.
    - [adv] Tournament Solutions and Majority Voting
    - [adv] Social Choice and the Mathematics of Manipulation

- why study?
    - winner can be the worst choice according to majority of voters
    - preference inversion paradox can occur
    - winner can lose all pairwise majority comparisons
    - "wasting" your vote on an unpopular candidate

- voting rules
    - 1. plurality
        - alternatives that are ranked first by most voters
    - 2. Borda's rule
        - complete ranking preference
        - more preferred alternative of each voter gets m-1 points, second most-preferred m-2 points, etc
        - alternatives with highest accumulated score win
        - "preference intensity"
    - 3. sequential majority comparisons
        - alternatives that win a fixed sequence of pairwise comparisons
    - 4. plurality with runoff
        - two alternatives ranked first by most voters face off in a majority runoff
    - 5. instant runoff
        - complete ranking preference
        - alternatives that are ranked first by lowest number of voters are deleted
        - repeat until no more alternatives can be deleted

(directed graph) preferred candidate --> less preferred candidate

- axioms
    - monotonicity = a chosen alternative will still be chosen when it rises in individual preference rankings (while leaving everything else unchanged)
    - pareto optimality = an alternative should not be chosen if there exists another alternative such that all voters prefer the latter to the former

| Rule | Monotonicity | Pareto |
|------|--------------|--------|
| Plurality | Y | Y |
| Borda | Y | Y |
| SMC | Y | N |
| Plurality w/ runoff | N | Y |
| Instant runoff | N | Y |

- strategic manipulation
    - a voting rule can be manipulated if there is a preference profile which yields a single winner and a voter can misrepresent their preferences such that another alternative, which is preferred to the original one, becomes the unique winner
    - every reasonable single-winner voting rule is prone to manipulation
    - tie-breaking: how to compare sets or probability distributions?
    - computational hardness: how difficult is it to compute beneficial manipulations?
    - restricted domains: which restricted domains of preferences allow for voting rules that are resistant to manipulation?

- strategic abstention
    - a voting rule can be manipulated by strategic abstention if there is a preference profile which yields a single winner and a voter can obtain a more preferred, uniquely selected, alternative by abstaining

- [code] create minimal example using integer programming
    - optimization objective: minimize number of voter types then minimize number of voters
- [code] create pareto-optimality check
- [code] minimal examples of monotonicity / pareto optimality violations

2. Choice Theory

