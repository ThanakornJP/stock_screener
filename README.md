# stock_screener

# Resource
1. listed company: https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.csv

# Governance and Administration 
[Git Workflow and Project](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

### Branch
- main = contain abridged version -- commit when having new release
- develop = contain complete history of the project -- **keep origin/develop updated** by committing development progress
- feature/xxx = contain feature development -- commit when development finish 
- release = contain snapshot of develop branch

### Procedure
1. create feature branch
   1. without git-flow: 

Note: always start from develop branch

> git checkout develop` 
> 
> git checkout -b feature_xx

   2. with git-flow: 

> git flow `feature start` feature_xx

2. -- develop, add, and commit on feature branch -- 
3. finish feature branch 
   1. without git-flow: 

Note: always start from develop branch

> git checkout develop
>
> git merge feature_xx

   2. with git-flow:
> git flow `feature finish` feature_xx

4. release branch
   1. without git-flow 

> git checkout develop
> git checkout -b release/0.1.0
> git checkout main
> git merge release/0.1.0
   
   2. with git-flow
 
> git flow `release start` 0.1.0
> git flow `release finish` '0.1.0'

.
---

Step
1. get tickers - NASDAQ, NYSE `ticker.py`
2. attribute information `info.py`
   1. exchange, industry, sector, market cap, volume
   2. PE, PS, PFCF, EPS, Yield
   3. Day's Range
   4. 52's Range

> Note: Market Capital Segmentation
> Mega - market cap > 200B
> Large - market cap = 10B - 200B
> Medium - market cap = 2B - 10B
> Small - market cap = 300M - 2B 
> Micro - market cap = 50M - 300M
> Nano - market cap = < 50M

1. attribute dividend `dividend.py`
   1. streak
   2. recently first year that streak begins 
   3. no. year recession that it still paid out

   
   
  

# Strategy


Grade AAA: consecutive payout 25Y+, DPR 50-70%, growth (leap probability) lowest
Grade AA: consecutive payout 10-20Y+, DPR 30-50%
Grade A: consecutive payout 5-10Y+, DPR 10-30%, growth (leap probability) highest


DPR (dividend payout raio) = dividend per share (DPS) / Earning per share (EPS)
- max. DPR = 70%

dividend yield = dividend paid / stock 

div filter (5 Y)
- green: 5Y low - 10%
- yellow:  10% - 20%
- red: 20% - 5Y high

price filter (52 wk)
- green: 5Y low - 40%
- yellow: 40% - 60%
- red: 60% - 5Y high

price zone = [current price - 52w low] / 52w range
highest dividend yield = 5y low dividend / 5y lowest price 
target price = current dividend / highest dividend yield

1st zone = current dividend / (highest dividend yield * 90%)
2nd zone = current dividend / (highest dividend yield * 80%)

money trail 
- good: last <= 1st zone
- ok: 1st zone < last <= 2nd zone
- bad: last > 2nd zone


price trail 
- good: price zone <= 40%
- ok: 40% < price zone <= 60%
- bad: price zone > 60%

