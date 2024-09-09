#Completed by: Nassima Bouhenni
#07/23/21



#Set Working  Directory & Read File into Dataframe
setwd("~/Desktop/ImmuneCell_Data")
immune_freq_df <- read.csv("~/ImmuneCell_Data/gated-ImmuneCell-Frequencies.csv", row.names=1, header=TRUE)

#Plot names
plotname <- row.names(immune_freq_df)
filename <- paste(plotname, ".pdf", sep="")

#Barplot Function
for (i in 1:length(filename)){
    pdf(filename[i], pointsize = 14)
    immune_rf_df <- immune_freq_df[i,]/sum(immune_freq_df[i,])
    barplot(unlist(immune_rf_df), main=plotname[i], xlab = "Biomarker", ylab = "Relative Frequency", ylim = c(0,1), legend.text=TRUE, col=colors())
    dev.off
}

#Other Visualizations - Comparison Box & Whisker Plots
filename_bw <- paste(plotname, "bw.pdf", sep="")

for (i in 1:length(filename_bw)){
    pdf(filename_bw[i], pointsize = 14)
    immune_rf_df <- immune_freq_df[i,]/sum(immune_freq_df[i,])
    boxplot(unlist(immune_rf_df), main=plotname[i], xlab = "Biomarker", ylab = "Relative Frequency", ylim = c(0,1), legend.text=TRUE, col=colors())
    dev.off
}
