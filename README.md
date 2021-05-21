# SignalProduction
Collection of scripts to produce signal events

# For Ultra Legacy Production

```
git clone git@github.com:StealthStop/SignalProduction.git

cd SignalProduction

git checkout -b forUL --track origin/forUL
```

To run a test submission to condor, an example would be:

```
python submitJob.py --tag 2016_RPV_500  --year 2016 --model RPV --mass 350 --nEvents 10 --eventsPerJob 10
```

This will submit a single 10 event job that will eventually result in a 10 event MINIAOD file.
