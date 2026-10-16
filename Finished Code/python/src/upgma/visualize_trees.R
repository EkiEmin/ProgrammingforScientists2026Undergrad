#!/usr/bin/env Rscript
#
# visualize_trees.R
#
# Reads .nwk files from Output/ and produces a PNG for each dataset in Images/.
# One function per dataset; each tells a different evolutionary story.


if (!requireNamespace("ape", quietly = TRUE)) install.packages("ape")
library(ape)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# ── Colorblind-friendly palette ───────────────────────────────────────────────

PAL <- c(
  africa       = "#E63946",   # vivid red
  m_clade      = "#1D77BF",   # strong blue
  eurasia      = "#9467BD",   # medium purple
  americas     = "#2CA02C",   # strong green
  cetacea      = "#56B4E9",   # sky blue
  artiodactyla = "#E69F00",   # warm orange
  outgroup     = "#999999",   # grey
  bear         = "#0072B2",   # deep blue
  panda_giant  = "#D55E00",   # vermillion
  panda_red    = "#009E73",   # teal green
  primate      = "#0072B2",   # deep blue
  mammal       = "#E69F00",   # warm orange
  bird         = "#56B4E9",   # sky blue
  fish         = "#009E73",   # teal green
  reptile      = "#D55E00",   # vermillion
  amphibian    = "#CC79A7",   # pink/mauve
  hiv1         = "#E63946",   # vivid red
  hiv2         = "#1D77BF",   # strong blue
  siv          = "#2CA02C"    # strong green
)

# ── Helper: replace underscores with spaces in tip labels ─────────────────────

clean_labels <- function(labels) gsub("_", " ", labels)

# ── 1. Human Migration Out of Africa (mitochondrial haplogroups) ──────────────

MitochondrialHaplogroups <- function(
    nwk_file = "Output/mitochondrial_haplogroups.nwk",
    out_file = "Images/mitochondrial_haplogroups.png",
    width = 3200, height = 4500
) {
  tree <- read.tree(nwk_file)

  africa   <- c("L0_San_SouthAfrica", "L0d_KhoeSan_SouthAfrica",
                "L1_Yoruba_WestAfrica", "L1c_Biaka_CentralAfrica",
                "L2a_Mande_WestAfrica", "L2b_Mande_WestAfrica",
                "L3_EastAfrica", "L3b_Mande_WestAfrica")
  m_clade  <- c("M_India_SouthAsia", "D_Japan_EastAsia",
                "C_Evenki_Siberia", "G_Nivkh_Siberia",
                "F_Vietnamese_SoutheastAsia", "E_PapuaNewGuinea_Oceania")
  americas <- c("A_NativeAmerican", "X_NativeAmerican")
  eurasia  <- c("N_ArabianPeninsula", "R_Armenia_Eurasia",
                "B_Polynesian_Pacific", "H_European",
                "J_German_NorthEurope", "K_Druze_NearEast",
                "T_Armenian_NearEast", "U_Belarusian_Europe",
                "V_Iberian_WestEurope")

  node_colors <- ifelse(tree$tip.label %in% africa,   PAL["africa"],
                 ifelse(tree$tip.label %in% m_clade,  PAL["m_clade"],
                 ifelse(tree$tip.label %in% americas, PAL["americas"],
                                                      PAL["eurasia"])))

  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.2)
  legend("bottomright",
         legend = c("Africa (L haplogroups)", "Macrohaplogroup M (east)",
                    "Americas (A, X)", "Eurasia / N / R"),
         col    = c(PAL["africa"], PAL["m_clade"],
                    PAL["americas"], PAL["eurasia"]),
         pch = 19, cex = 2.2, title = "Region")
  dev.off()
}

# ── 2. Whales Are Even-Toed Ungulates (cetaceans) ─────────────────────────────

cetacean_colors <- function(tip_labels) {
  cetacea      <- c("Tursiops_truncatus_Bottlenose_dolphin",
                    "Orcinus_orca_Killer_whale",
                    "Balaenoptera_musculus_Blue_whale",
                    "Physeter_macrocephalus_Sperm_whale")
  artiodactyla <- c("Hippopotamus_amphibius_Hippopotamus",
                    "Sus_scrofa_Pig", "Bos_taurus_Cow",
                    "Giraffa_camelopardalis_Giraffe",
                    "Camelus_dromedarius_Dromedary")

  ifelse(tip_labels %in% cetacea,      PAL["cetacea"],
  ifelse(tip_labels %in% artiodactyla, PAL["artiodactyla"],
                                        PAL["outgroup"]))
}

Cetaceans <- function(
    nwk_file = "Output/cetaceans.nwk",
    out_file = "Images/cetaceans.png",
    width = 2000, height = 1600
) {
  tree <- read.tree(nwk_file)
  node_colors <- cetacean_colors(tree$tip.label)
  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.0)
  legend("bottomleft",
         legend = c("Cetacea (whales & dolphins)",
                    "Artiodactyla (even-toed ungulates)",
                    "Outgroup (horse, rhino, elephant)"),
         col    = c(PAL["cetacea"], PAL["artiodactyla"], PAL["outgroup"]),
         pch = 19, cex = 1.6, title = "Group")
  dev.off()
}

# ── 2b. Cetaceans: UPGMA vs Neighbor-Joining comparison ──────────────────────

CetaceansComparison <- function(
    nwk_file = "Output/cetaceans.nwk",
    mtx_file = "Data/Cetaceans/cetaceans.mtx",
    out_file = "Images/cetaceans_upgma_vs_nj.png",
    width = 4000, height = 1600
) {
  # UPGMA tree (from file)
  upgma_tree <- read.tree(nwk_file)

  # NJ tree (from distance matrix)
  mtx_data <- read.csv(mtx_file, header = FALSE)
  species  <- mtx_data[, 1]
  d        <- as.matrix(mtx_data[, -1])
  rownames(d) <- species
  colnames(d) <- species
  nj_tree <- nj(as.dist(d))

  # Root NJ tree on elephant (outgroup)
  nj_tree <- root(nj_tree, outgroup = "Loxodonta_africana_African_elephant",
                  resolve.root = TRUE)

  upgma_colors <- cetacean_colors(upgma_tree$tip.label)
  nj_colors    <- cetacean_colors(nj_tree$tip.label)

  upgma_tree$tip.label <- clean_labels(upgma_tree$tip.label)
  nj_tree$tip.label    <- clean_labels(nj_tree$tip.label)

  png(out_file, width = width, height = height)
  par(mfrow = c(1, 2), mar = c(2, 1, 3, 1))

  plot(upgma_tree, edge.color = "black", tip.color = upgma_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 1.8,
       main = "UPGMA")
  title(main = "UPGMA", cex.main = 2.5)

  plot(nj_tree, edge.color = "black", tip.color = nj_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 1.8,
       main = "Neighbor-Joining")
  title(main = "Neighbor-Joining", cex.main = 2.5)

  dev.off()
}

# ── 3. The Molecular Clock: Cytochrome C ──────────────────────────────────────

CytochromeC <- function(
    nwk_file = "Output/cytochrome_c.nwk",
    out_file = "Images/cytochrome_c.png",
    width = 2000, height = 1600
) {
  tree <- read.tree(nwk_file)

  primates <- c("Homo_sapiens_Human", "Pan_troglodytes_Chimpanzee",
                "Gorilla_gorilla_Gorilla", "Pongo_pygmaeus_Orangutan",
                "Macaca_mulatta_Rhesus_monkey")
  mammals  <- c("Equus_caballus_Horse", "Bos_taurus_Cow",
                "Sus_scrofa_Pig", "Canis_familiaris_Dog",
                "Mus_musculus_Mouse")

  node_colors <- ifelse(tree$tip.label %in% primates, PAL["primate"],
                 ifelse(tree$tip.label %in% mammals,  PAL["mammal"],
                                                      PAL["fish"]))

  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.0)
  legend("bottomleft",
         legend = c("Primates", "Non-primate mammals",
                    "Non-mammal eukaryotes"),
         col    = c(PAL["primate"], PAL["mammal"], PAL["fish"]),
         pch = 19, cex = 1.6, title = "Group")
  dev.off()
}

# ── 4. The Giant Panda Is a Bear ──────────────────────────────────────────────

GiantPandaBears <- function(
    nwk_file = "Output/giant_panda_bears.nwk",
    out_file = "Images/giant_panda_bears.png",
    width = 2000, height = 1600
) {
  tree <- read.tree(nwk_file)

  node_colors <- ifelse(tree$tip.label == "Ailuropoda_melanoleuca_Giant_panda",
                          PAL["panda_giant"],
                 ifelse(tree$tip.label == "Ailurus_fulgens_Red_panda",
                          PAL["panda_red"],
                 ifelse(tree$tip.label %in% c("Mustela_putorius_Ferret",
                                               "Procyon_lotor_Raccoon"),
                          PAL["outgroup"],
                          PAL["bear"])))

  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.0)
  legend("bottomleft",
         legend = c("Giant panda", "True bears (Ursidae)",
                    "Red panda (not a bear!)", "Outgroup (raccoon, ferret)"),
         col    = c(PAL["panda_giant"], PAL["bear"],
                    PAL["panda_red"], PAL["outgroup"]),
         pch = 19, cex = 1.6, title = "Group")
  dev.off()
}

# ── 5. Great Ape Phylogeny (mtDNA) ───────────────────────────────────────────

GreatApes <- function(
    nwk_file = "Output/great_apes.nwk",
    out_file = "Images/great_apes.png",
    width = 2000, height = 1600
) {
  tree <- read.tree(nwk_file)

  great_apes <- c("Homo_sapiens_Human", "Pan_troglodytes_Chimpanzee",
                  "Pan_paniscus_Bonobo", "Gorilla_gorilla_Gorilla",
                  "Pongo_abelii_Orangutan", "Nomascus_leucogenys_Gibbon")

  node_colors <- ifelse(tree$tip.label %in% great_apes, PAL["primate"],
                 ifelse(tree$tip.label == "Macaca_mulatta_Rhesus_macaque",
                          PAL["primate"],
                 ifelse(tree$tip.label == "Mus_musculus_Mouse",
                          "#D55E00",
                          "#009E73")))

  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.0)
  legend("bottomleft",
         legend = c("Primates", "Mouse (mammal outgroup)",
                    "Zebra finch (bird outgroup)"),
         col    = c(PAL["primate"], "#D55E00", "#009E73"),
         pch = 19, cex = 1.6, title = "Group")
  dev.off()
}

# ── 6. Hemoglobin Alpha (HBA1) Across 108 Vertebrates ────────────────────────

HemoglobinAlpha <- function(
    nwk_file = "Output/hemoglobin.nwk",
    out_file = "Images/hemoglobin.png",
    width = 4000, height = 12000
) {
  tree <- read.tree(nwk_file)

  tips <- tree$tip.label

  is_bird      <- grepl("duck|goose|swan|ibisbill|stilt|guillemot|skua|falcon|plover|sheathbill|nene|teal|eider|scoter|razorbill|parrot|shelduck",
                         tips, ignore.case = TRUE)
  is_fish      <- grepl("cod|sablefish|rockcod|snailfish|trout|wolffish|puffer|ray",
                         tips, ignore.case = TRUE)
  is_reptile   <- grepl("iguana|cobra|tortoise",
                         tips, ignore.case = TRUE)
  is_amphibian <- grepl("frog|newt",
                         tips, ignore.case = TRUE)

  node_colors <- ifelse(is_bird,      PAL["bird"],
                 ifelse(is_fish,      PAL["fish"],
                 ifelse(is_reptile,   PAL["reptile"],
                 ifelse(is_amphibian, PAL["amphibian"],
                                      PAL["mammal"]))))

  tree$tip.label <- clean_labels(tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 2.0,
       label.offset = 0.00002)
  tiplabels(pch = 19, col = node_colors, cex = 2.5)
  legend("bottomright",
         legend = c("Mammals", "Birds", "Fish", "Reptiles", "Amphibians"),
         col    = c(PAL["mammal"], PAL["bird"], PAL["fish"],
                    PAL["reptile"], PAL["amphibian"]),
         pch = 19, cex = 4.0, title = "Group")
  dev.off()
}

# ── 7. HIV Origins: Independent Transmissions from Primates ──────────────────

HIVSubtypes <- function(
    nwk_file = "Output/hiv_subtypes.nwk",
    out_file = "Images/hiv_subtypes.png",
    width = 2000, height = 1600
) {
  tree <- read.tree(nwk_file)

  hiv1 <- c("HIV-1_GroupM_SubtypeB_HXB2", "HIV-1_GroupM_SubtypeC_ETH2220",
             "HIV-1_GroupM_SubtypeD_NDK", "HIV-1_GroupM_SubtypeG_SE6165",
             "HIV-1_GroupO_ANT70", "HIV-1_GroupM_SubtypeA_Q23",
             "HIV-1_GroupN_YBF30")
  hiv2 <- c("HIV-2_GroupA_ROD", "HIV-2_GroupB_EHO")
  siv  <- c("SIVcpz_Tanzania", "SIVgor_Cameroon",
            "SIVsm_SootyMangabey", "SIVrcm_RedCapMangabey")

  node_colors <- ifelse(tree$tip.label %in% hiv1, PAL["hiv1"],
                 ifelse(tree$tip.label %in% hiv2, PAL["hiv2"],
                                                  PAL["siv"]))

  tree$tip.label <- gsub("_", " ", tree$tip.label)

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black", tip.color = node_colors,
       show.node.label = FALSE, show.tip.label = TRUE, cex = 1.8)
  legend("bottomleft",
         legend = c("HIV-1", "HIV-2", "Primate SIV (ancestors)"),
         col    = c(PAL["hiv1"], PAL["hiv2"], PAL["siv"]),
         pch = 19, cex = 1.6, title = "Virus")
  dev.off()
}

# ── 8. SARS-CoV-2 Evolution in the UK (2020–2024) ────────────────────────────

SARSCoV2 <- function(
    nwk_file = "Output/SARS_spike.nwk",
    out_file = "Images/SARS_spike.png",
    width = 3000, height = 5000
) {
  tree <- read.tree(nwk_file)

  color_palette <- c("2020" = "#56B4E9",
                     "2021" = "#009E73",
                     "2022" = "#E69F00",
                     "2023" = "#D55E00",
                     "2024" = "#CC79A7")

  years       <- substr(tree$tip.label, 1, 4)
  node_colors <- color_palette[years]

  png(out_file, width = width, height = height)
  plot(tree, edge.color = "black",
       show.node.label = FALSE, show.tip.label = FALSE)
  tiplabels(pch = 19, col = node_colors, cex = 3.0)
  legend("top",
         legend = names(color_palette),
         col    = color_palette,
         pch = 19, cex = 6.0, title = "Year")
  dev.off()
}


# ── Run all ───────────────────────────────────────────────────────────────────

MitochondrialHaplogroups()
Cetaceans()
CetaceansComparison()
# CytochromeC()
GiantPandaBears()
GreatApes()
HemoglobinAlpha()
HIVSubtypes()
SARSCoV2()
