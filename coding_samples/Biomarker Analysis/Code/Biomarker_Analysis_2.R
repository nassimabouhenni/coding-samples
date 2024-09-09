#Flow Cytometry Data Analysis
#Completed by: Nassima Bouhenni

#Set Working Directory & Pull Uncommon Libraries Needed
setwd("~/Desktop/FLOW/")
library(FlowSOM)
library(flowCore)
library(ggcyto)

#List of Filenames & Variable Names
file_name <- list.files(path="./FCS_Files")
file_list <- sub("G", "FCS_Files/G", file_name)
leuk_var <- sub(".fcs", "", file_name)

#Load Files & Clean Up
leuk_data <- lapply(file_list, read.FCS)
leuk_expr <- lapply(leuk_data, exprs)
names(leuk_data) <- leuk_var
names(leuk_expr) <- leuk_var

for (i in 1:length(leuk_var)){
     colnames(leuk_expr[[i]]) <- as.vector(leuk_data[[i]]@parameters@data$desc)
}
for (i in 1:length(leuk_var)){
     colnames(leuk_data[[i]]) <- as.vector(leuk_data[[i]]@parameters@data$desc)
}

#Drop Unlabled/Non-Protein Channels - Function
dropnames_fxn <- function(x) {
     x <- subset(x,select = -c(Time, Event_length, Y89Di, BC1,
           BC2, BC3, BC4, BC5, BC6, Xe131Di, Ba138Di,
           Os189, DNA1, DNA2, Cisplatin, beadDist))
}

leuk_expr <- lapply(leuk_expr, dropnames_fxn)


#Drop 2 Other Protein Markers - Function

dropnames_extra_fxn <- function(x) {
     x <- subset(x,select = -c(Luciferase, Ki67))
}

leuk_expr <- lapply(leuk_expr, dropnames_extra_fxn)
#see ReadMe for more information


#Inverse Hyperbolic Sine - Function

arcsinh_fxn <- function(x) {
     asinh(x/5)
     }

leuk_expr <- lapply(leuk_expr, arcsinh_fxn)

#Define Exprs() Matrix in FlowFrames & Create FlowSet
for (i in 1:length(leuk_data)){
    exprs(leuk_data[[i]]) <- leuk_expr[[i]]
}
leuk_fs <- as(leuk_data, "flowSet")
remove(leuk_expr)

#Wrapper Function: FlowSOM
set.seed(42)
leuk_fSOM <- FlowSOM(leuk_fs,
                # Input options:
                compensate = FALSE,
                transform = FALSE,
                scale = FALSE,
                # Metaclustering options:
                nClus = 10)

FlowSOMmary(fsom = leuk_fSOM, plotFile = "leuk_fsom_summary.pdf")

write.flowSet(leuk_fs, outdir=".")

#Get Profile of Clusters/Metaclusters by Group
leuk_percentages <- GetFeatures(fsom = leuk_fSOM,
                files = leuk_data,
                filenames = file_name,
                type = "percentages")

leuk_groups <- list("Group 1" = file_name[1:4],
               "Group 2" = file_name[5:7])
stat <- "fold changes"

MC_stats <- GroupStats(features = leuk_percentages[["metacluster_percentages"]], groups = leuk_groups)

Clust_stats <- GroupStats(leuk_percentages[["cluster_percentages"]], leuk_groups)

fold_changes <- Clust_stats["fold changes", ]
fold_changes <- factor(ifelse(fold_changes < -3, "Underrepresented compared to Group 1",
    ifelse(fold_changes > 3, "Overrepresented compared to Group 1",
    "--")), levels = c("--", "Underrepresented compared to Group 1",
                        "Overrepresented compared to Group 1"))
fold_changes[is.na(fold_changes)] <- "--"

# Show in figure
#Cluster Differences by Group
gr_1 <- PlotStars(leuk_fSOM, title = "Group 1",
                  nodeSizes = Clust_stats["medians Group 1", ],
                  refNodeSize = max(Clust_stats[c("medians Group 1", "medians Group 2"),]),
                  backgroundValues = fold_changes,
                  backgroundColors = c("white", "red", "blue"),
                  list_insteadof_ggarrange = TRUE)

gr_2 <- PlotStars(leuk_fSOM, title = "Group 2",
                  nodeSizes = Clust_stats["medians Group 2", ],
                  refNodeSize = max(Clust_stats[c("medians Group 1", "medians Group 2"),]),
                  backgroundValues = fold_changes,
                  backgroundColors = c("white", "red", "blue"),
                  list_insteadof_ggarrange = TRUE)

p1 <- ggpubr::ggarrange(plotlist = list(gr_1$tree, gr_2$tree, gr_2$backgroundLegend),
    ncol = 2, nrow = 2,
    heights = c(4,1))

pdf("Groups_Clust.pdf", pointsize=10)
print(p1)


#Fold Change
p2 <- PlotVariable(leuk_fSOM,
                title = "Fold change group 1 vs. group 2",
                variable = Clust_stats["fold changes", ])
print(p2, newpage=TRUE)
dev.off()

#Question 4
#Volcano Plot
p3 <- ggplot2::ggplot(data.frame("-log10 p values" = c(Clust_stats[4, ],
                                 MC_stats[4, ]),
            "log10 fold changes" = c(Clust_stats[7, ],
                                    MC_stats[7, ]),
            "feature" = c(colnames(Clust_stats), colnames(MC_stats)),
            "metacluster" = c(as.character(leuk_fSOM$metaclustering),
                            levels(leuk_fSOM$metaclustering)),
            "type" = c(rep("C", ncol(Clust_stats)),
                    rep("MC", ncol(MC_stats))),
            check.names = FALSE),
        ggplot2::aes(x = `log10 fold changes`,
                    y = `-log10 p values`,
                    size = type,
                    col = metacluster)) +
ggplot2::xlim(-3, 3) +
ggplot2::ylim(0, 3) +
ggplot2::geom_point() +
ggplot2::theme_minimal() +
ggplot2::geom_vline(xintercept = 0, col = "darkgrey") +
ggplot2::geom_hline(yintercept = -log10(0.05), col = "darkgrey") +
ggplot2::scale_size_manual(values =c("C" = 1, "MC" = 2))

pdf("Volcano_Plot.pdf")
print(p3)
dev.off()
