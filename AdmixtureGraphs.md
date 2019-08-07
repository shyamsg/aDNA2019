# Admixture graph exercise notes
We will work on constructing some admixture graphs now, of course with the same populations as we used for the other exercises.

## TreeMix
First, we are going to try the tool `treemix`, to construct a maximum likelihood graph, from the correlation of allele frequencies between pairs of populations.

Before we begin to use `treemix`, we need to convert the geno format files to treemix input format files. We will do this using a custom python script.
```
/science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/convertGeno2Treemix.py [YOUR DATA DIRECTORY]/AncientModern.geno [YOUR DATA DIRECTORY]/AncientModern.ind > AncientModern.treemix
grep -v '0,0' AncientModern.treemix | gzip -c > AncientModern.treemix.gz  
```
Let us quickly take a look at what this file looks like. Each line is a single SNP, and there are counts of the reference and non reference allele for each population. Now we are ready to run treemix to estimate the relationship between our populations. We will first run it without any migration events, with each block being 500 SNPs and starting with a random seed.

```
treemix -i AncientModern.treemix.gz -o AM.m0 -k 500 -root Ju_hoan_North,Yoruba,Mbuti -seed $RANDOM
```

Let us plot the tree in R and see what it looks like.
```
R
source("/science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/plotting_funcs.R")
plot_tree(stem="AM.m0")
```

And now, we can check the goodness of fit of this tree using the residuals. But first we need a file with the names of the populations listed in the order we want to see them.
I have already created such a file, which looks like this.
```
Ju_hoan_North
Yoruba
Mbuti
Ami
Han
Papuan
Mayan
Karitiana
Steppe_EMBA
Europe_LNBA
Sardinian
Italian_North
French
Orcadian

```
This file is located at /science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/poporder.txt. Make a link to this file in your directories using `ln -s /science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/poporder.txt .`. Now we are ready to visualize the residuals.
```
R
source("/science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/plotting_funcs.R")
par(mar=c(6,6,2,2)+0.1)
plot_resid("AM.m0", "poporder.txt")
```

Now we can start adding migration edges. Let us try and run it for 1-3 migration edges.
```
treemix -i AncientModern.treemix.gz -o AM.m1 -k 500 -root Ju_hoan_North,Yoruba,Mbuti -m 1 -seed $RANDOM
treemix -i AncientModern.treemix.gz -o AM.m2 -k 500 -root Ju_hoan_North,Yoruba,Mbuti -m 2 -seed $RANDOM
treemix -i AncientModern.treemix.gz -o AM.m3 -k 500 -root Ju_hoan_North,Yoruba,Mbuti -m 3 -seed $RANDOM
```
Now plot the trees and check the residuals for the tree with 1 migration edge. What is the first migration edge you get?

Do the same for 2 and 3 migration edges. Do the migration edges make sense? What is happening to the residuals?
