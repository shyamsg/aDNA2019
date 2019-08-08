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
This file is located at /science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/scripts/poporder.txt. Make a link to this file in your directories using `ln -s /science/groupdirs-nfs/SCIENCE-SNM-Archaeo/2019/Day4/treemix/poporder.txt .`. Now we are ready to visualize the residuals.
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

## Admixture graphs using f-statistics : qpGraph
Now that we have made admixture graphs using correlations of allele frequencies between populations, we can also explore the construction of admixture graphs using F statistics. A package that allows us to do this is called qpGraph. To run qpGraph, we need a par file, and a input graph file. Let us first construct the par file. We have met most of these parameters already.
```
DIR:   [YOUR DATA DIRECTORY]
indivname:       DIR/AncientModern.ind  
snpname:         DIR/AncientModern.snp       
genotypename:    DIR/AncientModern.geno  
blgsize:        0.005
lsqmode:       YES
diag:          .0001
hires:         YES
```

Now let us build a graph from the treemix tree.

```
root     R
label    Ju_hoan_North JhN  
## label lables populations (leaf nodes) here population is "Out"  vertex is "O"
label    Mbuti   M      
label    Yoruba  Y    
label    Karitiana K   
label    Mayan My
label    Han H
label    Ami A
label    Papuan P
label    French F
label    Italian_North IN
label    Sardinian S
label    Orcadian O
label    Europe_LNBA Elb
label    Steppe_EMBA Sem
## edge name q  R -> O
edge aaa R Afr
edge aab Afr Y
edge aac Afr Afr2
edge aad Afr2 M
edge aae Afr2 JhN
edge aaf R notA
edge aag notA SA
edge aah SA P
edge aai SA Asian
edge aaj Asian HA
edge aak HA H
edge aal HA A
edge aam Asian SAm
edge aan SAm K
edge aao SAm My
edge aap notA allEur    
edge aaq allEur oldEur
edge aar oldEur Elb
edge aas oldEur Sem
edge aat allEur modEur
edge aau modEur O
edge aav modEur FI
edge aaw FI F
edge aax FI I
edge aay I S
edge aaz I IN
```

Now we are ready to run `qpGraph` to generate our multiple population graph, assuming that the par file is called qpg.par and the graph file is called initGraph.txt
```
qpGraph -p qpg.par -g initGraph.txt -d multPopulation_noAdmixture.dot
```
Let us now plot the output graph and see what it looks like. Also, let us see where the poor fitting F statistics are.

```
dot -Tpdf < multPopulation_noAdmixture.dot > multPopulation_noAdmixture.pdf
```
What does that poor F-stat fit tell us? What component is missing? If we add an admixture edge, where would we add it?
