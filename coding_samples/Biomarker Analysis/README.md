#Biomarker_Analysis_1.r

Biomarker_Analysis_1.r is a script that outputs the following pdfs to the working directory:
(a) boxplots describing relative biomarker frequencies of each flow cytometry experiment run
(b) box and whisker plots describing relative biomarker frequencies of each flow cytometry experiment run

#Usage
To run Biomarker_Analysis_1.r, 
(1) edit working directory to your preference
(1) enter in terminal: Rscript Biomarker_Analysis_1.r

#Biomarker_Analysis_2.r

Biomarker_Analysis_2.r is a script that outputs to the working directory:
(a) edited FCS files, annotation.txt file.
(b) leuk_fsom_summary.pdf - summary file of flowSOM object, contains many graphics visualizing the leukocyte data, including clustering.
(c) Groups_Clust.pdf - two cluster maps highlighting the fold changes between the two groups of fcs data.
(d) Volcano_Plot.pdf - volcano plot of fold changes between the two groups of fcs data.

#Usage
To run Biomarker_Analysis_2.r, 
(1) edit working directory to your preference
(1) enter in terminal: Rscript Biomarker_Analysis_2.r

#Question 2 Notes
The 2 variables were irrelevant for understanding this data at this stage:

(1) Luciferase - This is a bioluminescent gene reporter not expressed by human cells but genetically engineered to report gene expression. Because the specific gene which the luciferase was gene was inserted into was not recorded in the dataset, this information alone does not tell us anything about immune cell responses or whether or not the cell was cancerous.
source: https://doi.org/10.1016/B978-0-12-374984-0.00565-9

(2) Ki67 - This is a biomarker strongly associated with cancer cell proliferation and thus is vital as a cancer cell marker. However, it is the only protein not directly related to immune cells (since we aim to see how immune cell gene expression is impacted when cancerous), and our cancerous cells are already designated (Group 1[control] vs Group 2[tumor]), so this control is not necessary at this stage.
source:https://doi.org/10.3892/mmr.2014.2914

#Question 4 Notes
Output (d) describes a volcano plot of the fold changes between the two groups of data. The volcano plot gives the most statistically significant metacluster differences (denoted by p value) and the degree (denoted by log(fold_changes)), and thus this plot, when analyzed in conjuction with the data from ouput (b), is sufficient for understanding which biomolecules are associated with cancer and to what degree. The most significant metacluster differences were in metaclusters 1, 10, and 2, respectively, as also referenced in the Question 6 README.md, and the associated biomolecule differences are illustrated on page 11 of output (b).

#Contributing
Nassima Bouhenni
07/23/21
