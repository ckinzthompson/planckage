# planckage
`planckage` is a git-inspired program for tracking scientific analyses. It is meant to be flexible. In general, any analysis should be contained within a folder containing data, the analysis scripts, and any results/figures. Planckage formalizes that by making it into a repository of sorts.

Each planckage repo is a folder that has at least three items:
* `./data`: a directory where your data files should be stored
* `./results`: a directory where your scripts should save any output information/files
* `./figures`: a directory where your scripts should save any output figures/plots

This approach standardizes an analysis, but also makes it easier to apply your scripts to new bits of data. The reason to keep all of your output in the folders is because you can create recipes of everything else. Feel free to make other folders, they're be included in the recipe.

Recipes are a little like templates that you make. You might have a general approach to analyzing data from one technique. In that case, you would apply those functions to different datasets for a new analysis. "Cooking" a recipe just copies those scripts into a new planckage repo.

## Tutorial
Set up the planckage repo
``` sh
planckage init fancyanalysis7
cd fancyanalysis7
```

Now you are ready to do a bunch of analysis. Keep the analysis scripts in the planckage repo, and save any outputs in to the `./figures/` or `./results` folders. 

## Locks
Once done, you can lock the planckage repo. This will help you detect any changes.
``` sh
planckage lock
```

Once locked, you can check that it's untouched, or whether any file has been modified
``` sh
planckage check
```

## Recipes
Recipes are a way to boot up an analysis. If you have several scripts for a general idea of a workflow, you can turn all the files that aren't in the `./data`, `./figures`, or `./results` directories into a recipe. Recipes can be "cooked", which copies all of those files into *any* other planckage repo.

For instance, if you have a recipe for doing an isothermal calorimetry titration (ITC) analysis called 'itc_analysis`, you can start up a new analysis with

``` sh
planckage init newitcanalysis
cd newitcanalysis
planckage recipe cook itc_analysis
```

If you have worked hard on an analysis, you can make it into a recipe with the create command:
``` sh
planckage recipe create fancy_analysis
```
This will prompt you for a description of the recipe. Once entered, hit enter.

If you want to find which recipes you have, you can run 
``` sh 
planckage recipe list
```

To remove a recipe that you don't like, try
``` sh
planckage recipe remove my_bad_recipe
```
