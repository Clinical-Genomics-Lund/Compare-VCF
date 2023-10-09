library(tidyverse)

# readClipboard()

# Set the path
setwd("/home/jakob/proj/230920_rd_evaluate")
# setwd("\\\\wsl.localhost\\Ubuntu-22.04\\home\\jakob\\proj\\230920_rd_evaluate\\data")

# vcf1_path <- "\\\\wsl.localhost\\Ubuntu-22.04\\home\\jakob\\proj\\230920_rd_evaluate\\data\\23MD08776-testrun.scored.vcf.gz"
# vcf2_path <- "\\\\wsl.localhost\\Ubuntu-22.04\\home\\jakob\\proj\\230920_rd_evaluate\\data\\23MD08256-jakob_test.scored.vcf.gz"

vcf1_path <- "data/23MD08776-testrun.scored.vcf.gz"
vcf2_path <- "data/23MD08256-jakob_test.scored.vcf.gz"

number_rows <- Inf

vcf1 <- read_tsv(vcf1_path, comment = "##", n_max = number_rows) %>%
	rename(CHROM = `#CHROM`) %>%
    mutate(pos = paste(CHROM, POS, sep = ":")) %>%
    mutate(mut = paste(REF, ALT, sep = ",")) %>%
    mutate(rank = INFO %>% gsub(".*RankScore", "", .) %>% gsub(".*:", "", .) %>% gsub(";.*", "", .) %>% as.numeric()) %>%
    select(pos, mut, rank)
vcf2 <- read_tsv(vcf2_path, comment = "##", n_max = number_rows) %>%
    rename(CHROM = `#CHROM`) %>%
    mutate(pos = paste(CHROM, POS, sep = ":")) %>%
    mutate(mut = paste(REF, ALT, sep = ",")) %>%
    mutate(rank = INFO %>% gsub(".*RankScore", "", .) %>% gsub(".*:", "", .) %>% gsub(";.*", "", .) %>% as.numeric()) %>%
    select(pos, mut, rank)

# FIXME: Position might not be enough, the alternative allele?
# FIXME: Many to many matches?
joined_vcf <- vcf1 %>% full_join(vcf2, by = "pos")

joined_vcf_df <- as.data.frame(joined_vcf)

# Scatter chart
# FIXME: Investigate the outliers?
# FIXME: Density?
plt <- ggplot(joined_vcf_df %>% filter(!is.na(rank.x) & !is.na(rank.y)), aes(x = rank.x, y = rank.y)) +
    geom_point(na.rm = TRUE) +
    ggtitle("Compared rank scores")
ggsave(filename = "test.png", plt)

# Histograms of rank distributions
plt <- ggplot(joined_vcf_df %>% filter(!is.na(rank.x)), aes(x = rank.x)) +
    geom_histogram(na.rm = TRUE, bins = 30) +
    ggtitle("Comparison 1 rank scores")
ggsave(filename = "hist1.png", plt)

plt <- ggplot(joined_vcf_df %>% filter(!is.na(rank.y)), aes(x = rank.y)) +
    geom_histogram(na.rm = TRUE, bins = 30) +
    ggtitle("Comparison 2 rank scores")
ggsave(filename = "hist2.png", plt)

# Table
rank_table <- joined_vcf %>%
    filter(rank.x >= 12 | rank.y >= 12) %>%
    arrange(desc(rank.x), desc(rank.y))
rank_table

write_tsv(rank_table, file = "rank_table.tsv")
