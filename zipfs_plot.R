path <-"~/Desktop/인응/Zipfs_law_revised/zipf.csv"

library(ggplot2)
library(dplyr)

zipfs <- read.csv(path)
zipfs<-zipfs[,2:6]

zipfs %>% 
  mutate(r_freq = rank*freq) %>%
  ggplot(aes(x=rank, y=r_freq, colour=pos )) +
  geom_point(size=.5) +
  labs(title='Zipf\'s Law Plot',
       x = "Rank", y="Rank*Freq")

zipfs %>%
  filter(rank<1000) %>%
  mutate(r_freq = rank*freq) %>%
  ggplot(aes(x=rank, y=r_freq, colour=pos)) +
  geom_point(size=1) +
  labs(title='Zipf\'s Law Plot top 1000',
       x = "Rank", y="Rank*Freq")

zipfs %>%
  mutate(r_freq = rank * freq) %>%
  group_by(pos) %>%
  summarise(pos_count = n())
