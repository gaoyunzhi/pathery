# pathery

## The game
[pathery.com](http://pathery.com)

## How to run the code
- create a raw_[xxx].txt file in test floder contain the web source code from the pathery.com
- run: `python run.py [xxx]`

## Generated test file format
- running the code will automatically generate a test file from raw file, it's in the format of 
```
num_blockers
best_score
raw_map
```

## Algorithm
- First, try to find global solution by trying to connect the connected components of the blockers (I also imaging a tier of blocker on the ceiling and on the floor)
- Then, do local look around (add, remove, move) for improvement

## Performance optimization 
- Trim the solution (if some blocker is useless, remove it)
- Memorize the solution
- Do local improvement only for the good solutions
- Compute all the global solution will cost a lot of time, randomly pick some of the solution. (As to how random without losing the good ones, please read the code)
