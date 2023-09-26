library(tidyverse)

vcf1 <- read_tsv("data/23MD08256-jakob_test.scored.vcf.gz", comment="##", n_max=1000) %>%
	rename(CHROM=`#CHROM`) %>%
	mutate(pos=paste(CHROM, POS, sep=":")) %>%
	mutate(mut=paste(REF, ALT, sep=",")) %>% 
	mutate(rank=INFO %>% gsub(".*RankScore", "", .) %>% gsub(".*:", "", .) %>% gsub(";.*", "", .)) %>%
	select(pos, mut, rank)
vcf2 <- read_tsv("data/23MD08776-testrun.scored.vcf.gz", comment="##", n_max=1000) %>%
	rename(CHROM=`#CHROM`) %>%
	mutate(pos=paste(CHROM, POS, sep=":")) %>%
	mutate(mut=paste(REF, ALT, sep=",")) %>% 
	mutate(rank=INFO %>% gsub(".*RankScore", "", .) %>% gsub(".*:", "", .) %>% gsub(";.*", "", .)) %>%
	select(pos, mut, rank)

# OK I have some first data!
# Now join
# And make a scatter chart

